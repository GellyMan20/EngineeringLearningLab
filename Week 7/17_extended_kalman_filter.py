import numpy as np
import matplotlib.pyplot as plt

def wrap(a): return (a+np.pi)%(2*np.pi)-np.pi

def h(x):
    px,py=x[0,0],x[1,0]; return np.array([[np.hypot(px,py)],[np.arctan2(py,px)]])

def H_jac(x):
    px,py=x[0,0],x[1,0]; r2=max(px**2+py**2,1e-9); r=np.sqrt(r2); return np.array([[px/r,py/r,0,0],[-py/r2,px/r2,0,0]])

def main():
    rng=np.random.default_rng(17); dt=.1; t=np.arange(0,50,dt); tx=25+1.2*t; ty=15+.7*t; zr=np.hypot(tx,ty)+rng.normal(0,1,len(t)); zb=np.arctan2(ty,tx)+rng.normal(0,np.deg2rad(1),len(t))
    x=np.array([[20.],[10.],[0.],[0.]]); P=np.diag([100.,100.,10.,10.]); F=np.array([[1,0,dt,0],[0,1,0,dt],[0,0,1,0],[0,0,0,1.]],float); Q=np.diag([.05,.05,.2,.2]); R=np.diag([1.,np.deg2rad(1)**2]); I=np.eye(4); est=[]
    for r,b in zip(zr,zb):
        x=F@x; P=F@P@F.T+Q; z=np.array([[r],[b]]); y=z-h(x); y[1,0]=wrap(y[1,0]); H=H_jac(x); S=H@P@H.T+R; K=P@H.T@np.linalg.inv(S); x=x+K@y; P=(I-K@H)@P; est.append(x.ravel())
    est=np.array(est); plt.figure(); plt.plot(tx,ty,label='Truth'); plt.plot(est[:,0],est[:,1],label='EKF'); plt.axis('equal'); plt.grid(True); plt.legend(); plt.show()
if __name__=='__main__': main()
