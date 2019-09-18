import numpy as np
import scipy.stats


class Browian_motion(object):

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



class Kesten_process(object):

    def __init__(self, N, X_0, a, b, up_cap, Npool):
        self.N = N
        self.X = np.ones(N)*X_0
        self.a, self.b = a, b
        self.up_cap = up_cap
        self.pid = np.random.choice(range(Npool), replace=False,
                                    size=N)

        print("Up-cap disabled!")

    def step(self):

        asv = self.a.rvs(size=self.N)
        while len(asv[asv<=0])>0:
            asv[asv<=0] = self.a.rvs(size=len(asv[asv<=0]))

        self.X = asv*self.X + self.b.rvs(size=self.N)
        self.X[self.X<0.] = 0.
        # self.X[self.X>self.up_cap] = self.up_cap



class LWOU_process(object):

    def __init__(self, N, X_0, mu1, theta1, sigma1, mu2, theta2,
                 sigma2, mu_global, up_cap, Npool, dt=0.01):

        self.N = N
        self.pid = np.random.choice(range(Npool), replace=False,
                                    size=N)

        self.X1 = np.ones(N)*X_0
        self.X2 = np.ones(N)*X_0

        self.X = np.ones(N)*X_0
        
        self.dt = dt

        self.mu1, self.mu2 = mu1, mu2
        self.theta1, self.theta2 = theta1, theta2
        self.sigma1, self.sigma2 = sigma1, sigma2

        self.mu_global = mu_global

        print("Up-cap disabled!")
        self.up_cap = up_cap

        self.setup_1()
        self.setup_2()
        

    def setup_1(self):
        self.emdt1 = np.exp(-self.theta1*self.dt)
        self.a1 = np.sqrt(self.sigma1**2/(2*self.theta1) *
                         (1 - np.exp(-2*self.theta1*self.dt)))

    def setup_2(self):
        self.emdt2 = np.exp(-self.theta2*self.dt)
        self.a2 = np.sqrt(self.sigma2**2/(2*self.theta2) *
                         (1 - np.exp(-2*self.theta2*self.dt)))
        

    def step(self):
        self.X1 = self.X1*self.emdt1+self.mu1*(1 - self.emdt1) + \
                 self.a1*np.random.normal(size=self.N)
        # self.X1[self.X1<0.] = 0.
        self.X2 = self.X2*self.emdt2+self.mu2*(1 - self.emdt2) + \
                 self.a2*np.random.normal(size=self.N)


        self.X = 10.**(self.X1 + self.X2 + self.mu_global)

        self.X[self.X<0.] = 0.

        # if self.up_cap > 0:
        #     self.X[self.X>self.up_cap] = self.up_cap


        
class LWOU_process_euler(object):

    def __init__(self, N, X_0, mu1, theta1, sigma1, mu2, theta2,
                 sigma2, mu_global, up_cap, Npool, dt=1/60.*1/24.):

        self.N = N
        self.pid = np.random.choice(range(Npool), replace=False,
                                    size=N)

        self.X1 = np.ones(N)*0.
        self.X2 = np.ones(N)*0.

        self.X = np.ones(N)*X_0
        
        self.dt = dt

        self.mu1, self.mu2 = mu1, mu2
        self.theta1, self.theta2 = theta1, theta2
        self.sigma1sq, self.sigma2sq = sigma1, sigma2

        self.mu_global = mu_global

        zeta1_sd = np.sqrt(2*self.theta1*self.sigma1sq)
        self.zeta1 = scipy.stats.norm(loc=0, scale=zeta1_sd)
        zeta2_sd = np.sqrt(2*self.theta2*self.sigma2sq)
        self.zeta2 = scipy.stats.norm(loc=0, scale=zeta2_sd)

        print("Up-cap disabled!")
        self.up_cap = up_cap

        

    def _step_x1(self):
        self.X1 += self.dt*1/self.theta1*(-1*self.X1 + \
                     self.zeta1.rvs(size=self.N))

    def _step_x2(self):
        self.X2 += self.dt*2/self.theta2*(-1*self.X2 + \
                     self.zeta2.rvs(size=self.N))
        
    def step(self):

        self._step_x1()
        self._step_x2()

        self.X = 10.**(self.X1 + self.X2 + self.mu_global)
        self.X[self.X<0.] = 0.

        # if self.up_cap > 0:
        #     self.X[self.X>self.up_cap] = self.up_cap


        
