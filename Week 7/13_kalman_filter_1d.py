import numpy as np
import matplotlib.pyplot as plt

def main():
    rng=np.random.default_rng(13); dt=.1; t=np.arange(0,40,dt); truth=.5*t**2; z=truth+rng.normal(0,8,len(t))
    x=np.array([[0.],[0.]]); P=np.diag([100.,100.]); F=np.array([[1,dt],[0,1.]]); H=np.array([[1.,0.]]); Q=np.diag([.05,.5]); R=np.array([[64.]]); I=np.eye(2)
    est=[]; sig=[]
    for meas in z:
        x=F@x; P=F@P@F.T+Q; y=np.array([[meas]])-H@x; S=H@P@H.T+R; K=P@H.T@np.linalg.inv(S); x=x+K@y; P=(I-K@H)@P; est.append(x[0,0]); sig.append(np.sqrt(P[0,0]))
    est=np.array(est); sig=np.array(sig)
    plt.figure(); plt.plot(t,truth,label='Truth'); plt.scatter(t,z,s=10,alpha=.4,label='Measurements'); plt.plot(t,est,label='Estimate'); plt.fill_between(t,est-2*sig,est+2*sig,alpha=.2,label='±2σ'); plt.grid(True); plt.legend(); plt.show()
if __name__=='__main__': main()
