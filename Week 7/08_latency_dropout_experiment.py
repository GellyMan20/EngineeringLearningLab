import numpy as np
import matplotlib.pyplot as plt

def run(latency,dropout,rng):
    dt=.05; t=np.arange(0,40,dt); truth=np.sin(.3*t); m=truth+rng.normal(0,.08,len(t)); s=int(latency/dt); m=np.roll(m,s); m[:s]=np.nan; m[rng.random(len(t))<dropout]=np.nan; return t,truth,m

def main():
    rng=np.random.default_rng(8); plt.figure()
    for l,d in [(0,0),(.2,.05),(.5,.15)]:
        t,truth,m=run(l,d,rng); plt.plot(t,m,label=f'{l}s, {100*d:.0f}%')
    plt.plot(t,truth,linewidth=2,label='Truth'); plt.title('Latency and Dropout'); plt.grid(True); plt.legend(); plt.show()
if __name__=='__main__': main()
