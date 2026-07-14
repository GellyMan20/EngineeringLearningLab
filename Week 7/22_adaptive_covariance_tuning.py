import numpy as np
import matplotlib.pyplot as plt

def main():
    rng=np.random.default_rng(22); dt=.1; t=np.arange(0,60,dt); truth=.8*t; std=np.where((t>=20)&(t<=40),5.,1.); z=truth+rng.normal(0,std)
    x=np.array([[0.],[0.]]); P=np.diag([50.,10.]); F=np.array([[1,dt],[0,1.]]); H=np.array([[1.,0.]]); Q=np.diag([.02,.2]); I=np.eye(2); Rv=1.; est=[]; rh=[]
    for m in z:
        x=F@x; P=F@P@F.T+Q; innov=float(m-(H@x)[0,0]); Rv=.97*Rv+.03*np.clip(innov**2,.5,36.); R=np.array([[Rv]]); S=H@P@H.T+R; K=P@H.T@np.linalg.inv(S); x=x+K*np.array([[innov]]); P=(I-K@H)@P; est.append(x[0,0]); rh.append(Rv)
    plt.figure(); plt.plot(t,truth,label='Truth'); plt.scatter(t,z,s=10,alpha=.35,label='Measurements'); plt.plot(t,est,label='Adaptive'); plt.grid(True); plt.legend(); plt.show(); plt.figure(); plt.plot(t,rh); plt.title('Adaptive R'); plt.grid(True); plt.show()
if __name__=='__main__': main()
