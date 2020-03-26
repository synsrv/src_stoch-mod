
from pypet import cartesian_product

name = 'pypet_data'

Nprocess_prm = 100
Npool_factor = [1.]

input_dict = {'bn_mu': [0.],
              'bn_sig': [0.1],
              'Nprocess': [Nprocess_prm],
              'Npool': [int(Nprocess_prm*f) for f in Npool_factor],
              'Nsteps': [100],
              'X_0': [0.1],
              'up_cap': [0.],
              'p_prune': [1.],
              'c' : [0.],
              'process_type': ['Brownian'],
              'rnd_seed': [20200326, 20200326, 1]}


mode = 'cartesian'
# mode = 'nlist'

if mode == 'cartesian':
    explore_dict = cartesian_product(input_dict)

elif mode == 'nlist':

    explore_dict = {}

    n = max([len(item) for key,item in input_dict.items()])

    for key,item in input_dict.items():
        if len(item) == n:
            explore_dict[key] = item
        elif len(item) == 1:
            explore_dict[key] = item*n
        else:
            raise ValueError("items must be either n or 1" +\
                             "received n=%d and value %d" %(n, len(item)))



if __name__ == "__main__":
    print(name)

