import numpy as np
import matplotlib.pyplot as plt
def wrap(a): return (a+np.pi)%(2*np.pi)-np.pi
rng=np.random.default_rng(8); dt=.01; t=np.arange(0,60,dt); th=.4*np.sin(.15*t); rate=np.gradient(th,dt); gyro=rate+np.deg2rad(.3)+rng.normal(0,np.deg2rad(.08),len(t)); mag=th+rng.normal(0,np.deg2rad(3),len(t)); x=0.; P=np.deg2rad(10)**2; q=np.deg2rad(.15)**2; r=np.deg2rad(3)**2; est=[]
for k in range(len(t)):
 x=wrap(x+gyro[k]*dt); P+=q; y=wrap(mag[k]-x); K=P/(P+r); x=wrap(x+K*y); P=(1-K)*P; est.append(x)
plt.plot(t,np.rad2deg(th),label='Truth'); plt.plot(t,np.rad2deg(mag),alpha=.35,label='Mag'); plt.plot(t,np.rad2deg(est),label='Fused'); plt.grid(); plt.legend(); plt.show()
