import numpy as np
import matplotlib.pyplot as plt
rng=np.random.default_rng(10); dt=.01; t=np.arange(0,40,dt); truth=.5*np.sin(.2*t); rate=np.gradient(truth,dt); btrue=np.deg2rad(.4); gyro=rate+btrue+rng.normal(0,np.deg2rad(.08),len(t)); meas=truth+rng.normal(0,np.deg2rad(2),len(t)); ang=0.; best=0.; P=np.diag([np.deg2rad(10)**2,np.deg2rad(1)**2]); est=[]; bh=[]
for k in range(len(t)):
 ang+=(gyro[k]-best)*dt; F=np.array([[1,-dt],[0,1.]]); Q=np.diag([np.deg2rad(.1)**2,np.deg2rad(.005)**2]); P=F@P@F.T+Q; H=np.array([[1.,0.]]); R=np.array([[np.deg2rad(2)**2]]); y=np.array([[meas[k]-ang]]); S=H@P@H.T+R; K=P@H.T@np.linalg.inv(S); dx=K@y; ang+=dx[0,0]; best+=dx[1,0]; P=(np.eye(2)-K@H)@P; est.append(ang); bh.append(best)
plt.plot(t,np.rad2deg(truth),label='Truth'); plt.plot(t,np.rad2deg(est),label='Estimate'); plt.grid(); plt.legend(); plt.show(); plt.plot(t,np.rad2deg(bh),label='Bias estimate'); plt.axhline(np.rad2deg(btrue),ls='--',label='True bias'); plt.grid(); plt.legend(); plt.show()
