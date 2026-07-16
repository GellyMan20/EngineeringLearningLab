import numpy as np
import matplotlib.pyplot as plt
def score(q,r,z,truth,dt):
 x=np.zeros((2,1)); P=np.diag([20.,8.]); F=np.array([[1,dt],[0,1.]]); H=np.array([[1.,0.]]); Q=np.diag([.01,.1])*q; R=np.array([[4.*r]]); I=np.eye(2); est=[]
 for m in z:
  x=F@x; P=F@P@F.T+Q; y=np.array([[m]])-H@x; S=H@P@H.T+R; K=P@H.T@np.linalg.inv(S); x=x+K@y; P=(I-K@H)@P; est.append(x[0,0])
 return np.sqrt(np.mean((np.array(est)-truth)**2))
rng=np.random.default_rng(15); dt=.1; t=np.arange(0,40,dt); truth=1.3*t+2*np.sin(.3*t); z=truth+rng.normal(0,2,len(t)); best=None
for q in [.1,.3,1,3,10]:
 for r in [.1,.3,1,3,10]:
  s=score(q,r,z,truth,dt); best=(s,q,r) if best is None or s<best[0] else best
print('Best RMSE, Q scale, R scale =',best)
