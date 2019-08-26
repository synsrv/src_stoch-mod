
from pypet import cartesian_product

sigv = 4.095946771684454e-09

# FIXED KESTEN PROCESS!
input_dict = {'bn_mu': [0.],
              'bn_sig': [0.1],
              'Nsteps': [10000],
              'Nprocess': [1000],
              'X_0': [0.],
              'up_cap': [1.],
              'p_prune': [0.1],
              'c' : [0.0001]}

name = 'brownian_wUpLim'
explore_dict = cartesian_product(input_dict)

if __name__ == "__main__":
    print(name)
