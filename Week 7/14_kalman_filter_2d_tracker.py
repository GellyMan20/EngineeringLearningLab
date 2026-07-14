import numpy as np
import matplotlib.pyplot as plt

def main():
    rng=np.random.default_rng(14); dt=.2; t=np.arange(0,60,dt); tx=2*t; ty=.8*t+10*np.sin(t/10); z=np.column_stack((tx+rng.normal(0,2,len(t)),ty+rng.normal(0,2,len(t))))
    x=np.zeros((4,1)); P=np.diag([100,100,25,25]).astype(float); F=np.array([[1,0,dt,0],[0,1,0,dt],[0,0,1,0],[0,0,0,1.]],float); H=np.array([[1,0,0,0],[0,1,0,0.]],float); Q=np.diag([.1,.1,.8,.8]); R=np.diag([4.,4.]); I=np.eye(4); est=[]
    for m in z:
        x=F@x; P=F@P@F.T+Q; y=m.reshape(2,1)-H@x; S=H@P@H.T+R; K=P@H.T@np.linalg.inv(S); x=x+K@y; P=(I-K@H)@P; est.append(x.ravel())
    est=np.array(est); plt.figure(); plt.plot(tx,ty,label='Truth'); plt.scatter(z[:,0],z[:,1],s=10,alpha=.4,label='Measurements'); plt.plot(est[:,0],est[:,1],label='Estimate'); plt.axis('equal'); plt.grid(True); plt.legend(); plt.show()
if __name__=='__main__': main()
