import numpy as np
import matplotlib.pyplot as plt
def run(qs,rs,z,dt):
 x=np.zeros((2,1)); P=np.diag([25.,9.]); F=np.array([[1,dt],[0,1.]]); H=np.array([[1.,0.]]); Q=np.diag([.02,.2])*qs; R=np.array([[4.*rs]]); I=np.eye(2); o=[]
 for m in z:
  x=F@x; P=F@P@F.T+Q; y=np.array([[m]])-H@x; S=H@P@H.T+R; K=P@H.T@np.linalg.inv(S); x=x+K@y; P=(I-K@H)@P; o.append(x[0,0])
 return o
rng=np.random.default_rng(5); dt=.1; t=np.arange(0,40,dt); truth=1.2*t+3*np.sin(.2*t); z=truth+rng.normal(0,2,len(t)); plt.plot(t,truth,label='Truth')
for q,r in [(.1,1),(1,1),(10,1),(1,10)]: plt.plot(t,run(q,r,z,dt),label=f'Qx{q}, Rx{r}')
plt.title('Process vs Measurement Noise'); plt.grid(); plt.legend(); plt.show()
