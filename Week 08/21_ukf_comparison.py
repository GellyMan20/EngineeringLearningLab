import numpy as np
import matplotlib.pyplot as plt
rng=np.random.default_rng(21); dt=.1; t=np.arange(0,30,dt); truth=np.zeros_like(t)
for k in range(1,len(t)): truth[k]=truth[k-1]+dt*np.sin(truth[k-1])+.05
z=truth**2/20+rng.normal(0,.25,len(t)); x=.2; P=1.; Q=.03; R=.25**2; a=.4; b=2.; lam=a*a-1; wm=np.array([lam/(1+lam),1/(2*(1+lam)),1/(2*(1+lam))]); wc=wm.copy(); wc[0]+=1-a*a+b; est=[]
for m in z:
 s=np.sqrt((1+lam)*P); sig=np.array([x,x+s,x-s]); sp=sig+dt*np.sin(sig)+.05; xp=np.sum(wm*sp); Pp=np.sum(wc*(sp-xp)**2)+Q; zs=sp**2/20; zp=np.sum(wm*zs); S=np.sum(wc*(zs-zp)**2)+R; C=np.sum(wc*(sp-xp)*(zs-zp)); K=C/S; x=xp+K*(m-zp); P=Pp-K*S*K; est.append(x)
plt.plot(t,truth,label='Truth'); plt.scatter(t,z,s=10,alpha=.4,label='Measurements'); plt.plot(t,est,label='UKF'); plt.grid(); plt.legend(); plt.show()
