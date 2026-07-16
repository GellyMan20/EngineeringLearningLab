import numpy as np
import matplotlib.pyplot as plt
def run(qs,rs,z,dt):
 x=np.zeros((2,1)); P=np.diag([5.,5.]); F=np.array([[1,dt],[0,1.]]); H=np.array([[1.,0.]]); Q=np.diag([.01,.1])*qs; R=np.array([[4.*rs]]); I=np.eye(2); o=[]
 for m in z:
  x=F@x; P=F@P@F.T+Q; y=np.array([[m]])-H@x; S=H@P@H.T+R; K=P@H.T@np.linalg.inv(S); x=x+K@y; P=(I-K@H)@P; o.append(x[0,0])
 return o
rng=np.random.default_rng(12); dt=.1; t=np.arange(0,50,dt); truth=.05*t**2; z=truth+rng.normal(0,2,len(t)); plt.plot(t,truth,label='Truth'); plt.plot(t,run(1,1,z,dt),label='Well tuned'); plt.plot(t,run(.001,.01,z,dt),label='Overconfident'); plt.grid(); plt.legend(); plt.show()
