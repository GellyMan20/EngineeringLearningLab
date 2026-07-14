import numpy as np
import matplotlib.pyplot as plt

def main():
    rng=np.random.default_rng(18); dt=.1; t=np.arange(0,30,dt); truth=np.zeros_like(t)
    for k in range(1,len(t)): truth[k]=truth[k-1]+dt*np.sin(truth[k-1])+.05
    z=truth**2/20+rng.normal(0,.25,len(t)); x=.2; P=1.; Q=.03; R=.25**2; alpha=.4; beta=2.; kappa=0.; n=1; lam=alpha**2*(n+kappa)-n; wm=np.array([lam/(n+lam),1/(2*(n+lam)),1/(2*(n+lam))]); wc=wm.copy(); wc[0]+=1-alpha**2+beta; est=[]
    for m in z:
        spread=np.sqrt((n+lam)*P); sigma=np.array([x,x+spread,x-spread]); sp=sigma+dt*np.sin(sigma)+.05; xp=np.sum(wm*sp); Pp=np.sum(wc*(sp-xp)**2)+Q; zs=sp**2/20; zp=np.sum(wm*zs); S=np.sum(wc*(zs-zp)**2)+R; C=np.sum(wc*(sp-xp)*(zs-zp)); K=C/S; x=xp+K*(m-zp); P=Pp-K*S*K; est.append(x)
    plt.figure(); plt.plot(t,truth,label='Truth'); plt.scatter(t,z,s=10,alpha=.4,label='Measurements'); plt.plot(t,est,label='UKF'); plt.grid(True); plt.legend(); plt.show()
if __name__=='__main__': main()
