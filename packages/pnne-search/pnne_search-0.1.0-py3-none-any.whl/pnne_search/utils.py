import numpy as np
import pandas as pd
import scipy.sparse
from scipy.optimize import minimize
from scipy.interpolate import interp1d




def interpolate(query, x, v):
    interp_func = interp1d(x, v, kind='linear', bounds_error=False, fill_value='extrapolate')
    return interp_func(query)

def search_model(par, curve, Xp, Xa, Xc, consumer_idx):
    p = Xp.shape[1]
    a = Xa.shape[1]
    c = Xc.shape[1]
    
    par = np.array(par).flatten()
    consumer_idx = np.array(consumer_idx).flatten()
    
    if len(par) != p + a + c + 2:
        raise ValueError("Incorrect number of parameters.")
    
    n = Xc.shape[0]  # number of consumers
    J = Xp.shape[0] // n  # number of search options
    
    alpha0 = par[0]
    alpha = par[1:a+1]
    eta0 = par[a+1]
    eta = par[a+2:a+c+2]
    beta = par[a+c+2:a+c+p+2]
    delta = 0
    
    o = eta0 + Xc @ eta + np.random.randn(n)
    v = Xp @ beta - o[consumer_idx-1] + np.random.randn(n * J) * np.exp(delta)
    u = v + np.random.randn(n * J)
    
    r = v + interpolate(alpha0 + Xa @ alpha, curve['log_cost'], curve['utility'])
    
    sort_idx = np.lexsort((-r, consumer_idx))
    u = u[sort_idx]
    r = r[sort_idx]
    
    Y_sorted = np.full((n * J, 2), np.nan)
    
    for i in range(n):
        k = slice(i * J, (i + 1) * J)
        r_i = r[k]
        u_i = u[k]
        
        searched = np.maximum.accumulate(np.insert(u_i[:-1], 0, 0)) <= r_i
        searched[0] = True
        
        u_i[~searched] = -np.inf
        
        j = np.argmax(u_i)
        bought = np.zeros(J, dtype=bool)
        bought[j] = np.max(u_i) > 0
        
        Y_sorted[k, 0] = searched
        Y_sorted[k, 1] = bought
    
    Y = np.empty_like(Y_sorted)
    Y[sort_idx] = Y_sorted
    
    return Y


def reg_linear(penalty, X, y):
    """
    Estimate a linear model with ridge penalty.
    """
    n = len(y)
    
    # Add intercept term
    X = np.column_stack((np.ones(n), X))
    
    # Define penalty weights
    w = penalty * np.concatenate(([0], np.ones(X.shape[1] - 1)))
    
    # Compute regularized covariance matrix
    B = (X.T @ X) / n + 2 * np.diag(w)
    
    # Check condition number
    flag = np.linalg.eigvals(B).min() > 1e-9
    
    # Compute coefficients
    coef = np.linalg.solve(B, (X.T @ y) / n)
    
    # Compute sensitivity
    # sens = -2* np.linalg.solve(B, np.concatenate(([0], coef[1:])))

    return coef, flag


def reg_logit(penalty, X, y, consumer_idx=None):

    m = int(1e4)
    
    y = y.astype(bool)
    X = np.column_stack((np.ones(len(y)), X))
    coef = np.zeros(X.shape[1])
    
    if consumer_idx is None:  # Simple logit
        n = len(y)
        if n > m:
            n1 = np.sum(y)
            n0 = n - n1
            m1 = min(n1, max(m - n0, m // 2))
            m0 = m - m1
            
            idx1 = np.random.choice(np.where(y)[0], m1, replace=False)
            idx0 = np.random.choice(np.where(~y)[0], m0, replace=False)
            i = np.concatenate((idx1, idx0))

            res = minimize(fun=lambda c: loss_binary(X[i], y[i], penalty, c)[0],
                           x0=coef,
                           jac=lambda c: loss_binary(X[i], y[i], penalty, c)[1],
                           hess=lambda c: loss_binary(X[i], y[i], penalty, c)[2],
                           method='trust-ncg')
            coef = res.x
            coef[0] -= np.log(n0 / n1 * m1 / m0)
        
        res = minimize(fun=lambda c: loss_binary(X, y, penalty, c)[0],
                        x0=coef,
                        jac=lambda c: loss_binary(X, y, penalty, c)[1],
                        hess=lambda c: loss_binary(X, y, penalty, c)[2],
                        method='trust-ncg')
        coef = res.x
        res.hess = loss_binary(X, y, penalty, coef)[2]
        flag = res.success and np.min(np.linalg.eigvals(res.hess)) > 1e-9
    
    else:  # Multinomial logit
        n = np.max(consumer_idx)
        if n > m:
            t = np.bincount(consumer_idx, weights=y)
            m1 = max(1, int(np.mean(t) * m))
            m0 = m - m1
            
            k1 = np.random.choice(np.where(t > 0)[0], m1, replace=False)
            k0 = np.random.choice(np.where(t == 0)[0], m0, replace=False)
            i = np.isin(consumer_idx, np.concatenate((k1, k0)))
            
            res = minimize(fun=lambda c: loss_multi(X[i], y[i], consumer_idx[i], penalty, c)[0], 
                x0=coef, 
                jac=lambda c: loss_multi(X, y, consumer_idx, penalty, c)[1], 
                hess=lambda c: loss_multi(X, y, consumer_idx, penalty, c)[2],
                method='trust-ncg')

            coef = res.x
        
        res = minimize(fun=lambda c: loss_multi(X, y, consumer_idx, penalty, c)[0], 
                        x0=coef, 
                        jac=lambda c: loss_multi(X, y, consumer_idx, penalty, c)[1], 
                        hess=lambda c: loss_multi(X, y, consumer_idx, penalty, c)[2],
                        method='trust-ncg')
        coef = res.x
        res.hess = loss_multi(X, y, consumer_idx, penalty, coef)[2]
        flag = res.success and np.min(np.linalg.eigvals(res.hess)) > 1e-9
    
    # sens = -2 * np.concatenate(([0], coef[1:])) / res.hess
    return coef, flag

def loss_binary(X, y, penalty, coef):
    n = len(y)
    w = penalty * np.concatenate(([0], np.ones(X.shape[1] - 1)))
    
    v = X @ coef
    e = np.exp(-v)
    s = e + 1
    val = (1/n) * (-np.sum(v[y]) + np.sum(v) + np.sum(np.log(s))) + np.sum(w * coef**2)
    
    Q = X / s[:, None]
    grad = (1/n) * (-np.sum(X[y], axis=0) + np.sum(Q, axis=0)) + 2 * w * coef
    hess = (1/n) * ((X - Q).T @ Q) + 2 * np.diag(w)
    hess = (hess + hess.T) / 2
    
    return val, grad, hess

def loss_multi(X, y, idx, penalty, coef):
    n = np.max(idx)
    w = penalty * np.concatenate(([0], np.ones(X.shape[1] - 1)))
    
    v = X @ coef
    e = np.exp(v)
    s = np.bincount(idx, weights=e) + 1
    val = (1/n) * (-np.sum(v[y]) + np.sum(np.log(s))) + np.sum(w * coef**2)
    
    Q = X * (e / s[idx])[:, None]
    grad = (1/n) * (-np.sum(X[y], axis=0) + np.sum(Q, axis=0)) + 2 * w * coef
    
    Hmat = scipy.sparse.csr_matrix((np.ones(len(idx)), (idx, np.arange(len(idx)))),
                                   shape=(idx.max() + 1, len(idx)))
    H = Hmat.dot(Q)
    hess = (1/n) * (X.T @ Q - H.T @ H) + 2*np.diag(w)

    hess = (hess + hess.T) / 2
    
    return val, grad, hess
