import numpy as np
import matplotlib.pyplot as plt
rng=np.random.default_rng(24); dt=.01; t=np.arange(0,60,dt); true_a=np.zeros_like(t); true_a[(t>5)&(t<15)]=.4; true_a[(t>30)&(t<40)]=-.4; true_v=np.cumsum(true_a)*dt; imu=true_a+.02+rng.normal(0,.03,len(t)); v=0.; nozupt=[]; zupt=[]; vz=0.
for k,time in enumerate(t):
 v+=imu[k]*dt; nozupt.append(v); vz+=imu[k]*dt
 stationary=(time<5) or (15<time<30) or (time>40)
 if stationary: vz=0.
 zupt.append(vz)
plt.plot(t,true_v,label='Truth'); plt.plot(t,nozupt,label='No ZUPT'); plt.plot(t,zupt,label='With ZUPT'); plt.grid(); plt.legend(); plt.show()
