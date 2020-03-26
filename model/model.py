
import os, pickle

from . import standard_parameters as prm
from .processes import *

import numpy as np
import scipy.stats as scts


def add_params(tr):
    tr.f_add_parameter('prm.process_type', prm.process_type)

    tr.f_add_parameter('prm.an_mu', prm.an_mu)
    tr.f_add_parameter('prm.an_sig', prm.an_sig)
    tr.f_add_parameter('prm.bn_mu', prm.bn_mu)
    tr.f_add_parameter('prm.bn_sig', prm.bn_sig)

    tr.f_add_parameter('prm.mu1', prm.mu1)
    tr.f_add_parameter('prm.theta1', prm.theta1)
    tr.f_add_parameter('prm.sigma1', prm.sigma1)
    tr.f_add_parameter('prm.mu2', prm.mu2)
    tr.f_add_parameter('prm.theta2', prm.theta2)
    tr.f_add_parameter('prm.sigma2', prm.sigma2)
    tr.f_add_parameter('prm.mu_global', prm.mu_global)
    tr.f_add_parameter('prm.dt', prm.dt)

    tr.f_add_parameter('prm.X_0', prm.X_0)
    tr.f_add_parameter('prm.up_cap', prm.up_cap)
    tr.f_add_parameter('prm.Nprocess', prm.Nprocess)
    tr.f_add_parameter('prm.Npool', prm.Npool)
    tr.f_add_parameter('prm.Nsteps', prm.Nsteps)
    tr.f_add_parameter('prm.p_prune', prm.p_prune)
    tr.f_add_parameter('prm.X_prune', prm.X_prune)
    tr.f_add_parameter('prm.pid_mode', prm.pid_mode)

    tr.f_add_parameter('prm.n_trace_rec', prm.n_trace_rec)

    tr.f_add_parameter('prm.rnd_seed', prm.rnd_seed)
    
        
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

    np.random.seed(tr.rnd_seed)
    
    print("Started process with id ", str(tr.v_idx))

    namespace = tr.prm.f_to_dict(short_names=True, fast_access=True)
    namespace['idx'] = tr.v_idx

    kx, lts, xt = [], [], []

    a_n = scts.norm(loc=tr.an_mu, scale=tr.an_sig)
    b_n = scts.norm(loc=tr.bn_mu, scale=tr.bn_sig)

    if tr.process_type=='Brownian':

        K = Browian_motion(tr.Nprocess, tr.X_0, b_n,
                           tr.up_cap, tr.Npool)

    elif tr.process_type=='Kesten':

        K = Kesten_process(tr.Nprocess, tr.X_0, a_n, b_n,
                           tr.up_cap, tr.Npool)

    elif tr.process_type=='LWOU':

        K = LWOU_process(tr.Nprocess, tr.X_0, tr.mu1, tr.theta1,
                         tr.sigma1, tr.mu2, tr.theta2, tr.sigma2,
                         tr.mu_global, tr.up_cap, tr.Npool)

    elif tr.process_type=='LWOU_euler':

        K = LWOU_process_euler(tr.Nprocess, tr.X_0, tr.mu1, tr.theta1,
                               tr.sigma1, tr.mu2, tr.theta2, tr.sigma2,
                               tr.mu_global, tr.up_cap, tr.Npool, tr.dt)


    pid_pool, pid_c = np.array(range(tr.Npool)),  tr.Npool
    counter,ts = np.zeros(tr.Nprocess), np.zeros(tr.Nprocess)

    for j in range(0,tr.Nsteps):


        ids = np.logical_and(K.X<=tr.X_prune,
                             np.random.uniform(size=tr.Nprocess)<tr.p_prune)


        for c,t,pid in zip(counter[ids],ts[ids],K.pid[ids]):

            lts.append([1, c, j, t, 1,-10, pid])

        counter[ids] += 1
        K.X[ids] = tr.X_0
        if tr.process_type=='LWOU_euler':
            K.X1[ids], K.X2[ids] = 0.,0.
        ts[ids] = j

        if tr.pid_mode == 'pool':
            K.pid[ids] = -10
            K.pid[ids] = np.random.choice(np.setdiff1d(pid_pool, K.pid),
                                          replace=False,
                                          size=np.sum(ids))

        elif tr.pid_mode == 'unique':
            K.pid[ids] = np.arange(pid_c+1, pid_c+np.sum(ids)+1, dtype='int')
            pid_c += np.sum(ids)+5

        xt.append(list(K.X[:tr.n_trace_rec]))

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
    with open(raw_dir+'/xt.p','wb') as pfile:
        pickle.dump(np.array(xt),pfile)

        

    from src.analysis.post_process.equal_dt import (
        subsamp_equal_dt )
    subsamp_equal_dt(namespace, lts, raw_dir)

    # from src.analysis.post_process.fixed_start_dt import (
    #     subsamp_fixed_start_dt )
    # subsamp_fixed_start_dt(namespace, lts, raw_dir)



    

    

    
