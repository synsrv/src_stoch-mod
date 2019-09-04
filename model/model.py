
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
    tr.f_add_parameter('prm.Npool', prm.Npool)
    tr.f_add_parameter('prm.Nsteps', prm.Nsteps)
    tr.f_add_parameter('prm.p_prune', prm.p_prune)
    tr.f_add_parameter('prm.c', prm.c)

    
    
class Kesten_process(object):

    def __init__(self, N, X_0, b, up_cap, Npool):
        self.N = N
        self.X = np.ones(N)*X_0
        self.b = b
        self.up_cap = up_cap
        self.pid = np.random.choice(range(Npool), replace=False,
                                    size=N)

        print("Up-cap disabled!")

    def step(self):
        self.X += self.b.rvs(size=self.N)
        self.X[self.X<0.] = 0.
        # self.X[self.X>self.up_cap] = self.up_cap


        
def run_model(tr):
    """generates

    lts data structure
      [0] : empty for now
      [1] : counts how often synapse was renewed
      [2] : step at which synapse was eliminated
      [3] : step at which was inserted
      [4] : | =  1   if eliminated during sim time
            | = -1   else
      [5] : | =-10   if eliminated during sim time
            | = x    synapse weight x if survived
      [6] : id for the process chosen from Npool
    """

    np.random.seed(int(tr.v_idx))
    
    print("Started process with id ", str(tr.v_idx))

    namespace = tr.prm.f_to_dict(short_names=True, fast_access=True)
    namespace['idx'] = tr.v_idx

    b_n = scts.norm(loc=tr.bn_mu, scale=tr.bn_sig)

    kx = []
    lts = []

    K = Kesten_process(tr.Nprocess, tr.X_0, b_n, tr.up_cap, tr.Npool)

    pid_pool = np.array(range(tr.Npool))
    counter,ts = np.zeros(tr.Nprocess), np.zeros(tr.Nprocess)

    for j in range(0,tr.Nsteps):


        ids = np.logical_and(K.X<=tr.c,
                             np.random.uniform(size=tr.Nprocess)<tr.p_prune)


        for c,t,pid in zip(counter[ids],ts[ids],K.pid[ids]):

            lts.append([1, c, j, t, 1,-10, pid])

        counter[ids] += 1
        K.X[ids] = tr.X_0
        ts[ids] = j

        K.pid[ids] = -10
        K.pid[ids] = np.random.choice(np.setdiff1d(pid_pool, K.pid),
                                      replace=False,
                                      size=np.sum(ids))

        K.step()

    # -1 for end of simulation "synapse didn't die"
    for c,t,kx_v,pid in zip(counter, ts, K.X, K.pid):
        lts.append([1,c,j,t,-1,kx_v,pid])
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

        

    from code.analysis.post_process.equal_dt import (
        subsamp_equal_dt )
    subsamp_equal_dt(raw_dir)

    from code.analysis.post_process.fixed_start_dt import (
        subsamp_fixed_start_dt )
    subsamp_fixed_start_dt(raw_dir)


    

    

    
