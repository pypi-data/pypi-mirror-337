import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'   
os.environ['XLA_FLAGS'] = '--xla_gpu_autotune_level=0'

import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

import numpy as np
import pandas as pd
import scipy.sparse
from scipy.stats import zscore, skew, mode
import warnings
from joblib import Parallel, delayed
import tensorflow as tf
from tensorflow.keras.models import load_model
import json

from . import masked_mse
from .utils import *
from .moments import moments
from .data_checks import data_checks

base_dir = os.path.dirname(__file__)

model = load_model(os.path.join(base_dir, 'nne.keras'))

with open(os.path.join(base_dir, "nne_info.json"), "r") as f:
    nne = json.load(f)

nne["dim"] = pd.DataFrame(nne["dim"])
nne["stat"] = pd.DataFrame(nne["stat"])

curve = pd.read_csv(os.path.join(base_dir,"curve.csv"))


def pnne_estimate(Y, Xp, Xa, Xc, consumer_idx, checks=True, se=False, se_repeats = 50, use_parallel=True): 

    Zp = zscore(Xp, axis=0)
    Za = zscore(Xa, axis=0)
    Zc = zscore(Xc, axis=0)

    n = consumer_idx[-1].item()
    J = len(consumer_idx) // n

    if Xa.size == 0:
        Xa = np.zeros((n * J, 0))
    if Xc.size == 0:
        Xc = np.zeros((n, 0))
    if Y.shape[1] > 2:
        Y = Y[:, :2]

    # warnings.filterwarnings('ignore', category=UserWarning)

    if checks:        
        _, buy_rate, srh_rate, num_srh, buy_n, srh_n = data_checks(Y, Zp, Za, Zc, consumer_idx)
        if buy_rate == 0:
            raise ValueError("There are no purchases.")
        if Xp.shape[1] < nne['dim'].loc['lower', 'p']:
            raise ValueError(f"Number of attributes in Xp must be at least {nne['dim'].loc['lower', 'p']}")
        if Xp.shape[1] > nne['dim'].loc['upper', 'p']:
            raise ValueError(f"Number of attributes in Xp must be at most {nne['dim'].loc['upper', 'p']}")
        if Xa.shape[1] > nne['dim'].loc['upper', 'a']:
            raise ValueError(f"Number of attributes in Xa must be at most {nne['dim'].loc['upper', 'a']}")
        if Xc.shape[1] > nne['dim'].loc['upper', 'c']:
            raise ValueError(f"Number of attributes in Xc must be at most {nne['dim'].loc['upper', 'c']}")

        if n < nne['dim'].loc['lower', 'n']:
            warnings.warn(f"Sample size n must be at least: {nne['dim'].loc['lower', 'n']}")
        if J < nne['dim'].loc['lower', 'J']:
            warnings.warn(f"Number of options J must be at least: {nne['dim'].loc['lower', 'J']}")
        if J > nne['dim'].loc['upper', 'J']:
            warnings.warn(f"Number of options J must be at most: {nne['dim'].loc['upper', 'J']}")

        if buy_n < nne['stat'].loc["lower", "buy_n"]:
            warnings.warn("Very few consumers made purchases.")
        if srh_n < nne['stat'].loc["lower", "srh_n"]:
            warnings.warn("Very few consumers made non-free searches.")

        if buy_rate < nne['stat'].loc["lower", "buy_rate"]:
            warnings.warn("Buy rate is too small.")
        if buy_rate > nne['stat'].loc["upper", "buy_rate"]:
            warnings.warn("Buy rate is too large.")

        if srh_rate < nne['stat'].loc["lower", "srh_rate"]:
            warnings.warn("Search rate (non-free) is too small.")
        if srh_rate > nne['stat'].loc["upper", "srh_rate"]:
            warnings.warn("Search rate (non-free) is too large.")

        if num_srh < nne['stat'].loc["lower", "num_srh"]:
            warnings.warn("Average number of searches is too small.")
        if num_srh > nne['stat'].loc["upper", "num_srh"]:
            warnings.warn("Average number of searches is too large.")

        Z = np.hstack([Zp, Za, Zc[consumer_idx-1]])

        q = np.percentile(Z, [2.5, 50, 97.5], axis=0)

        if np.any(np.max(Z, axis=0) > 2 * q[2] - q[1]) or np.any(np.min(Z, axis=0) < 2 * q[0] - q[1]):
            warnings.warn("X has extreme values; winsorizing may help.")
        if np.any(np.logical_and(np.abs(skew(Z, axis=0)) > 2, np.abs(mode(np.round(Z, 1), axis=0)[0]) > 0.5)):
            warnings.warn("X has highly skewed attributes.")

        A = scipy.sparse.csr_matrix((np.ones(n * J), (consumer_idx-1, np.arange(n * J))), shape=(n, n * J))
        Zp_t = A.dot(Zp) / J
        Za_t = A.dot(Za) / J

        if np.any(np.std(Zp - Zp_t[consumer_idx-1], axis=0) < 0.01):
            warnings.warn("Xp lacks variation within consumers.")
        if np.any(np.std(Za - Za_t[consumer_idx-1], axis=0) < 0.01):
            warnings.warn("Xa lacks variation within consumers.")
        if np.any(np.std(Za - Zp.dot(np.linalg.pinv(Zp.T.dot(Zp)).dot(Zp.T).dot(Za)), axis=0) < 0.01):
            warnings.warn("Xa lacks variation independent of Xp.")

    # Estimation
    par = Estimator(Y, Xp, Xa, Xc, consumer_idx)

    # Post-estimation checks
    if checks:
        if par['mmt_sens'] > 1:
            warnings.warn("Reduced-form patterns are unstable; estimates are likely inaccurate.")
        elif par['mmt_sens'] > 0.5:
            warnings.warn("Reduced-form patterns are not very stable; estimates may be inaccurate.")
        
        if 'diff' in nne:
            if par['pred_diff'] > nne['diff']['q2']:
                warnings.warn("The data is probably ill-suited for this search model.")
            elif par['pred_diff'] > nne['diff']['q1']:
                warnings.warn("The data might be ill-suited for this search model.")

    warnings.filterwarnings('default', category=UserWarning)

    # Bootstrap SE
    if not se:
        return     pd.DataFrame({'estimate': par['val']})

    vals = []
    locators = [np.arange((i-1)*J, i*J) for i in range(1, n+1)] 
    
    def compute_val(r):
        np.random.seed(r)
        k = np.random.choice(n, size=n, replace=True)
        i = np.concatenate([locators[idx] for idx in k])
        par_bt = Estimator(Y[i], Xp[i], Xa[i], Xc[k], consumer_idx)
        return par_bt['val']
    
    if use_parallel:
        vals = Parallel(n_jobs=-1)(delayed(compute_val)(r) for r in range(se_repeats))
    else:
        for r in range(se_repeats):
            vals.append(compute_val(r))

    par['se'] = np.std(np.array(vals), axis=0)
    
    df = pd.DataFrame({
        'estimate': par['val'],
        'SE': par['se']
    })

    return df

def Estimator(Y, Xp, Xa, Xc, consumer_idx):

    Zp = zscore(Xp, axis=0)
    Za = zscore(Xa, axis=0)
    Zc = zscore(Xc, axis=0)
    mu_p = np.mean(Xp, axis=0); sigma_p = np.std(Xp, axis=0)
    mu_a = np.mean(Xa, axis=0); sigma_a = np.std(Xa, axis=0)
    mu_c = np.mean(Xc, axis=0); sigma_c = np.std(Xc, axis=0)

    p = Xp.shape[1]
    a = Xa.shape[1]
    c = Xc.shape[1]

    # i = [name in nne['name_active'](p, a, c) for name in nne['name']]
    i = []
    for name in nne['name']:
        if name == "alpha_0":
            i.append(True)
        elif name.startswith("alpha_") and int(name.split("_")[1]) <= a:
            i.append(True)
        elif name == "eta_0":
            i.append(True)
        elif name.startswith("eta_") and int(name.split("_")[1]) <= c:
            i.append(True)
        elif name.startswith("beta_") and int(name.split("_")[1]) <= p:
            i.append(True)
        else:
            i.append(False)
    i = np.array(i)
    par = {'mmt_sens': None, 'pred_diff': None}

    mmt, sens = moments(Y, Zp, Za, Zc, consumer_idx, nne)
    par['mmt_sens'] = sens

    pred_net = model.predict(mmt.reshape(1, -1), verbose=0).flatten()[i]
    par['pred_net'] = pred_net

    # if 'tree' in nne:
    #     pred_tree = np.array([nne['tree'][k].predict(mmt) for k in range(len(nne['tree']))])
    #     par['pred_tree'] = pred_tree[i]

    #     diff = np.mean(nne['diff']['w'][i] * np.abs(par['pred_net'] - par['pred_tree']))
    #     par['pred'] = par['pred_net'] + (par['pred_tree'] - par['pred_net']) * np.clip((diff - nne['diff']['q1']) / (nne['diff']['q2'] - nne['diff']['q1']), 0, 1)
    # else:
    #     diff = 0
    #     par['pred'] = par['pred_net']

    # par['pred_diff'] = diff
    par['pred'] = {
        "alpha_0": pred_net[0],  # alpha_0 is always the first element
    }
    for j in range(1, a + 1):
        par['pred'][f"alpha_{j}"] = pred_net[j]
    par['pred']["eta_0"] = pred_net[a + 1]
    for j in range(1, c + 1):
        par['pred'][f"eta_{j}"] = pred_net[a + 1 + j]
    for j in range(1, p + 1):
        par['pred'][f"beta_{j}"] = pred_net[a + 1 + c + j]

    alpha0 = par['pred']["alpha_0"]
    alpha = np.array([par['pred'][f"alpha_{j}"] for j in range(1, a+1)])
    eta0 = par['pred']["eta_0"]
    eta = np.array([par['pred'][f"eta_{j}"] for j in range(1, c+1)])
    beta = np.array([par['pred'][f"beta_{j}"] for j in range(1, p+1)])

    par['val'] = np.concatenate([
        [alpha0 - np.sum(alpha / sigma_a * mu_a)],
        alpha / sigma_a,
        [eta0 - np.sum(eta / sigma_c * mu_c) + np.sum(beta / sigma_p * mu_p)],
        eta / sigma_c,
        beta / sigma_p
    ])

    return par

