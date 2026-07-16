import numpy as np
import matplotlib.pyplot as plt
rng=np.random.default_rng(1); dt=.1; t=np.arange(0,40,dt); truth=2*t; z=truth+rng.normal(0,4,len(t))
x=np.array([[0.],[0.]]); P=np.diag([100.,25.]); F=np.array([[1,dt],[0,1.]]); H=np.array([[1.,0.]]); Q=np.diag([.05,.2]); R=np.array([[16.]]); I=np.eye(2); est=[]
for m in z:
 x=F@x; P=F@P@F.T+Q; y=np.array([[m]])-H@x; S=H@P@H.T+R; K=P@H.T@np.linalg.inv(S); x=x+K@y; P=(I-K@H)@P; est.append(x[0,0])
plt.plot(t,truth,label='Truth'); plt.scatter(t,z,s=10,alpha=.4,label='Measurements'); plt.plot(t,est,label='Estimate'); plt.title('Kalman Filter Review'); plt.grid(); plt.legend(); plt.show()
