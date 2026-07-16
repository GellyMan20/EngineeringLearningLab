import numpy as np
import matplotlib.pyplot as plt
def wrap(a): return (a+np.pi)%(2*np.pi)-np.pi
def h(x):
 px,py=x[0,0],x[1,0]; return np.array([[np.hypot(px,py)],[np.arctan2(py,px)]])
def Hj(x):
 px,py=x[0,0],x[1,0]; r2=max(px*px+py*py,1e-9); r=np.sqrt(r2); return np.array([[px/r,py/r,0,0],[-py/r2,px/r2,0,0]])
rng=np.random.default_rng(6); dt=.1; t=np.arange(0,50,dt); tx=20+1.1*t; ty=10+.6*t; zr=np.hypot(tx,ty)+rng.normal(0,1,len(t)); zb=np.arctan2(ty,tx)+rng.normal(0,np.deg2rad(1),len(t)); x=np.array([[18.],[8.],[0.],[0.]]); P=np.diag([100.,100.,10.,10.]); F=np.array([[1,0,dt,0],[0,1,0,dt],[0,0,1,0],[0,0,0,1.]]); Q=np.diag([.05,.05,.2,.2]); R=np.diag([1.,np.deg2rad(1)**2]); I=np.eye(4); est=[]
for r,b in zip(zr,zb):
 x=F@x; P=F@P@F.T+Q; y=np.array([[r],[b]])-h(x); y[1,0]=wrap(y[1,0]); H=Hj(x); S=H@P@H.T+R; K=P@H.T@np.linalg.inv(S); x=x+K@y; P=(I-K@H)@P; est.append(x.ravel())
est=np.array(est); plt.plot(tx,ty,label='Truth'); plt.plot(est[:,0],est[:,1],label='EKF'); plt.axis('equal'); plt.grid(); plt.legend(); plt.show()
