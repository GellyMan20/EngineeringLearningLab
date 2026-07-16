import numpy as np
import matplotlib.pyplot as plt
def run(inflate,z,truth,dt):
 x=np.zeros((2,1)); P=np.diag([5.,2.]); F=np.array([[1,dt],[0,1.]]); H=np.array([[1.,0.]]); Q=np.diag([.005,.05]); R=np.array([[1.]]); I=np.eye(2); est=[]
 for k,m in enumerate(z):
  x=F@x; P=inflate*(F@P@F.T)+Q; y=np.array([[m]])-H@x; S=H@P@H.T+R; K=P@H.T@np.linalg.inv(S); x=x+K@y; P=(I-K@H)@P; est.append(x[0,0])
 return est
rng=np.random.default_rng(18); dt=.1; t=np.arange(0,50,dt); truth=.03*t**2; z=truth+rng.normal(0,1,len(t)); plt.plot(t,truth,label='Truth'); plt.plot(t,run(1,z,truth,dt),label='No inflation'); plt.plot(t,run(1.05,z,truth,dt),label='Inflation'); plt.grid(); plt.legend(); plt.show()
