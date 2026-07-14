import numpy as np
import matplotlib.pyplot as plt

def main():
    rng=np.random.default_rng(24); dt=.1; t=np.arange(0,40,dt); tp=1.2*t; tv=np.full_like(t,1.2); z=tp+rng.normal(0,2,len(t))
    x=np.zeros((2,1)); P=np.diag([30.,10.]); F=np.array([[1,dt],[0,1.]]); H=np.array([[1.,0.]]); Q=np.diag([.01,.05]); R=np.array([[4.]]); I=np.eye(2); nees=[]; nis=[]
    for k,m in enumerate(z):
        x=F@x; P=F@P@F.T+Q; y=np.array([[m]])-H@x; S=H@P@H.T+R; nis.append(float(y.T@np.linalg.inv(S)@y)); K=P@H.T@np.linalg.inv(S); x=x+K@y; P=(I-K@H)@P; truth=np.array([[tp[k]],[tv[k]]]); e=truth-x; nees.append(float(e.T@np.linalg.inv(P)@e))
    print(f'Mean NIS: {np.mean(nis):.2f} (expected near 1)'); print(f'Mean NEES: {np.mean(nees):.2f} (expected near 2)')
    plt.figure(); plt.plot(t,nis,label='NIS'); plt.axhline(1,linestyle='--'); plt.grid(True); plt.legend(); plt.show(); plt.figure(); plt.plot(t,nees,label='NEES'); plt.axhline(2,linestyle='--'); plt.grid(True); plt.legend(); plt.show()
if __name__=='__main__': main()
