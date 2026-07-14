import numpy as np
import matplotlib.pyplot as plt

def main():
    rng=np.random.default_rng(21); dt=.1; t=np.arange(0,50,dt); truth=.5*t; s=truth+rng.normal(0,.8,len(t)); s[(t>=18)&(t<=28)]+=5; s[np.argmin(abs(t-38))]+=18
    est=np.zeros_like(t); alpha=.15
    for k in range(1,len(t)): est[k]=est[k-1]+.5*dt; est[k]+=alpha*(s[k]-est[k])
    r=s-est; th=3.; flags=np.abs(r)>th; print(f'Detected fault samples: {flags.sum()}')
    plt.figure(); plt.plot(t,r,label='Residual'); plt.axhline(th,linestyle='--'); plt.axhline(-th,linestyle='--'); plt.scatter(t[flags],r[flags],marker='x',label='Anomalies'); plt.grid(True); plt.legend(); plt.show()
if __name__=='__main__': main()
