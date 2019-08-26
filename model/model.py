
import os, pickle

from . import standard_parameters as prm

import numpy as np
import scipy.stats as scts


def add_params(tr):
    tr.f_add_parameter('prm.bn_mu', prm.bn_mu)
    tr.f_add_parameter('prm.bn_sig', prm.bn_sig)
    tr.f_add_parameter('prm.X_0', prm.X_0)
    tr.f_add_parameter('prm.up_cap', prm.up_cap)
    tr.f_add_parameter('prm.Nprocess', prm.Nprocess)
    tr.f_add_parameter('prm.Nsteps', prm.Nsteps)
    tr.f_add_parameter('prm.p_prune', prm.p_prune)
    tr.f_add_parameter('prm.c', prm.c)
    
    
class Kesten_process(object):

    def __init__(self, N, X_0, b, up_cap):
        self.N = N
        self.X = np.ones(N)*X_0
        self.b = b
        self.up_cap = up_cap

    def step(self):
        self.X += self.b.rvs(size=self.N)
        self.X[self.X<0.] = 0.
        self.X[self.X>self.up_cap] = self.up_cap


        
def run_model(tr):

    np.random.seed(int(tr.v_idx))
    
    print("Started process with id ", str(tr.v_idx))

    namespace = tr.prm.f_to_dict(short_names=True, fast_access=True)
    namespace['idx'] = tr.v_idx

    b_n = scts.norm(loc=tr.bn_mu, scale=tr.bn_sig)

    kx = []
    lts = []

    for i in range(1):
    
        K = Kesten_process(tr.Nprocess, tr.X_0, b_n, tr.up_cap)
        counter,ts = np.zeros(tr.Nprocess), np.zeros(tr.Nprocess)

        for j in range(0,tr.Nsteps):


            ids = np.logical_and(K.X<=tr.c,
                                 np.random.uniform(size=tr.Nprocess)<tr.p_prune)


            for c,t in zip(counter[ids],ts[ids]):

                lts.append([i, c, j, t, 1,-10])

            counter[ids] += 1
            K.X[ids] = tr.X_0
            ts[ids] = j

            K.step()

        # -1 for end of simulation "synapse didn't die"
        for c,t,kx_v in zip(counter, ts, K.X):
            lts.append([i,c,j,t,-1,kx_v])
            kx.append([kx_v,tr.Nsteps-t])

    raw_dir = './data/%.4d' %(tr.v_idx)
    
    if not os.path.exists(raw_dir):
        os.makedirs(raw_dir)

    with open(raw_dir+'/namespace.p','wb') as pfile:
        pickle.dump(namespace,pfile)   

    with open(raw_dir+'/kx.p','wb') as pfile:
        pickle.dump(kx,pfile)   
    with open(raw_dir+'/lts.p','wb') as pfile:
        pickle.dump(lts,pfile)


    from code.analysis.kx_trace import kx_trace_figure
    kx_trace_figure(raw_dir)
    
    from code.analysis.synsrv_trace import synsrv_trace_figure
    synsrv_trace_figure(raw_dir)


    

    
