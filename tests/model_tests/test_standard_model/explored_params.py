
from pypet import cartesian_product

sigv = 4.095946771684454e-09


Nprocess_prm = 100
# Npool_factor = [1.,1.25, 1.5, 2., 2.5, 5., 10., 100.]
Npool_factor = [1.25, 10.]


# FIXED KESTEN PROCESS!
input_dict = {'bn_mu': [0.],
              'bn_sig': [0.1],
              'Nprocess': [Nprocess_prm],
              'Npool': [int(Nprocess_prm*f) for f in Npool_factor],
              'Nsteps': [100],
              'X_0': [0.1],
              'up_cap': [10.**10],
              'p_prune': [1.],
              'c' : [0.],
              'process_type': ['Brownian']}

name = 'brownian_wUpLim'
explore_dict = cartesian_product(input_dict)

if __name__ == "__main__":
    print(name)
