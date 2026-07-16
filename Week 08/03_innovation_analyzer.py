import numpy as np
import matplotlib.pyplot as plt
rng=np.random.default_rng(3); t=np.arange(0,50,.1); truth=.5*t; pred=truth+.2*np.sin(.3*t); z=truth+rng.normal(0,1,len(t)); y=z-pred
print('mean',y.mean(),'std',y.std(ddof=1)); plt.plot(t,y); plt.axhline(0,ls='--'); plt.title('Innovation Sequence'); plt.grid(); plt.show(); plt.hist(y,bins=30); plt.title('Innovation Distribution'); plt.grid(); plt.show()
