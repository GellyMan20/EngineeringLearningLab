import numpy as np
import matplotlib.pyplot as plt
rng=np.random.default_rng(16); t=np.arange(0,50,.1); truth=.8*t; z=truth+rng.normal(0,1,len(t)); z[150]+=12; z[320]-=10; pred=truth+.1*np.sin(.2*t); S=1.5**2; nis=(z-pred)**2/S; threshold=6.63; flags=nis>threshold
print('Rejected measurements:',flags.sum()); plt.plot(t,nis); plt.axhline(threshold,ls='--'); plt.scatter(t[flags],nis[flags],marker='x'); plt.title('Chi-Square Innovation Gating'); plt.grid(); plt.show()
