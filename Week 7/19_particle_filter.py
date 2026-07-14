import numpy as np
import matplotlib.pyplot as plt

def resample(w,rng):
    n=len(w); pos=(rng.random()+np.arange(n))/n; idx=np.zeros(n,dtype=int); c=np.cumsum(w); i=j=0
    while i<n:
        if pos[i]<c[j]: idx[i]=j; i+=1
        else: j+=1
    return idx

def main():
    rng=np.random.default_rng(19); landmarks=np.array([20.,50.,75.]); true_x=0.; vel=.35; n=1000; p=rng.normal(0,5,n); w=np.full(n,1/n); truth=[]; est=[]
    for _ in range(250):
        true_x+=vel+rng.normal(0,.03); p+=vel+rng.normal(0,.12,n); obs=np.abs(landmarks-true_x)+rng.normal(0,.8,len(landmarks)); w.fill(1.)
        for lm,z in zip(landmarks,obs): w*=np.exp(-.5*((z-np.abs(lm-p))/.8)**2)+1e-12
        w/=np.sum(w); truth.append(true_x); est.append(np.sum(w*p))
        if 1/np.sum(w**2)<n/2: p=p[resample(w,rng)]; w.fill(1/n)
    plt.figure(); plt.plot(truth,label='Truth'); plt.plot(est,label='Particle filter'); plt.grid(True); plt.legend(); plt.show()
if __name__=='__main__': main()
