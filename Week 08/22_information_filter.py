import numpy as np
import matplotlib.pyplot as plt
rng=np.random.default_rng(22); t=np.arange(0,40,.1); truth=1.5*t; z=truth+rng.normal(0,2,len(t)); x=0.; P=100.; est=[]
for m in z:
 P=P+0.2; Y=1/P; y=Y*x; R=4.; Y+=1/R; y+=m/R; P=1/Y; x=P*y; est.append(x)
plt.plot(t,truth,label='Truth'); plt.scatter(t,z,s=10,alpha=.4,label='Measurements'); plt.plot(t,est,label='Information filter'); plt.grid(); plt.legend(); plt.show()
