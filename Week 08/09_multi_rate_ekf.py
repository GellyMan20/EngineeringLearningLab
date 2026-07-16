import numpy as np
import matplotlib.pyplot as plt
rng=np.random.default_rng(9); dt=.01; t=np.arange(0,50,dt); a=.2*np.sin(.25*t); v=np.cumsum(a)*dt; truth=np.cumsum(v)*dt; imu=a+.015+rng.normal(0,.04,len(t)); gps=np.full(len(t),np.nan); gps[::100]=truth[::100]+rng.normal(0,1.2,len(gps[::100])); x=np.zeros((2,1)); P=np.diag([20.,8.]); H=np.array([[1.,0.]]); I=np.eye(2); est=[]
for k in range(len(t)):
 F=np.array([[1,dt],[0,1.]]); B=np.array([[.5*dt**2],[dt]]); Q=np.diag([.0005,.02]); x=F@x+B*imu[k]; P=F@P@F.T+Q
 if not np.isnan(gps[k]):
  R=np.array([[1.44]]); y=np.array([[gps[k]]])-H@x; S=H@P@H.T+R; K=P@H.T@np.linalg.inv(S); x=x+K@y; P=(I-K@H)@P
 est.append(x[0,0])
plt.plot(t,truth,label='Truth'); plt.scatter(t[::100],gps[::100],s=15,label='GPS'); plt.plot(t,est,label='EKF'); plt.grid(); plt.legend(); plt.show()
