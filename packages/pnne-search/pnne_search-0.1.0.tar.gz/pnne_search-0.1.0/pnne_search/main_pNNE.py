import time 
import pnne_search

data = pnne_search.load_example_data()

pnne_search.pnne_estimate(data['Y'], data['Xp'], data['Xa'], data['Xc'], 
                          data['consumer_idx'], checks = True)

start_time = time.time()
pnne_search.pnne_estimate(data['Y'], data['Xp'], data['Xa'], data['Xc'], 
                          data['consumer_idx'], checks = True, se=True)
time.time() - start_time

