import numpy as np
import matplotlib.pyplot as plt
rng=np.random.default_rng(20); dt=.02; t=np.arange(0,80,dt); a=.1*np.sin(.2*t); v=np.cumsum(a)*dt; truth=np.cumsum(v)*dt; imu=a+.02+rng.normal(0,.035,len(t)); gps=np.full(len(t),np.nan); gps[::50]=truth[::50]+rng.normal(0,1,len(gps[::50])); gps[(t>25)&(t<55)]=np.nan; x=np.zeros((2,1)); P=np.diag([20.,8.]); H=np.array([[1.,0.]]); I=np.eye(2); est=[]; sig=[]
for k in range(len(t)):
 F=np.array([[1,dt],[0,1.]]); B=np.array([[.5*dt**2],[dt]]); Q=np.diag([.0008,.03]); x=F@x+B*imu[k]; P=F@P@F.T+Q
 if not np.isnan(gps[k]):
  R=np.array([[1.]]); y=np.array([[gps[k]]])-H@x; S=H@P@H.T+R; K=P@H.T@np.linalg.inv(S); x=x+K@y; P=(I-K@H)@P
 est.append(x[0,0]); sig.append(np.sqrt(P[0,0]))
plt.plot(t,truth,label='Truth'); plt.plot(t,est,label='Estimate'); plt.axvspan(25,55,alpha=.2,label='GPS denied'); plt.fill_between(t,np.array(est)-2*np.array(sig),np.array(est)+2*np.array(sig),alpha=.2); plt.grid(); plt.legend(); plt.show()
