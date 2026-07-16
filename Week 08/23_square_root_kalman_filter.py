import numpy as np
import matplotlib.pyplot as plt
rng=np.random.default_rng(23); t=np.arange(0,40,.1); truth=1.2*t; z=truth+rng.normal(0,2,len(t)); x=0.; s=np.sqrt(100.); q=np.sqrt(.2); r=np.sqrt(4.); est=[]
for m in z:
 s=np.sqrt(s*s+q*q); K=s*s/(s*s+r*r); x=x+K*(m-x); s=np.sqrt(max((1-K)*s*s,1e-12)); est.append(x)
plt.plot(t,truth,label='Truth'); plt.scatter(t,z,s=10,alpha=.4,label='Measurements'); plt.plot(t,est,label='Square-root form'); plt.grid(); plt.legend(); plt.show()
