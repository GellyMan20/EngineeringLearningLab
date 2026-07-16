import numpy as np
import matplotlib.pyplot as plt
rng=np.random.default_rng(17); t=np.arange(0,60,.1); truth=np.sin(.15*t); s1=truth+rng.normal(0,.1,len(t)); s2=truth+rng.normal(0,.1,len(t)); s3=truth+rng.normal(0,.1,len(t)); s2[(t>25)&(t<40)]+=.8; med=np.median(np.vstack([s1,s2,s3]),axis=0); residuals=np.vstack([s1-med,s2-med,s3-med]); rms=np.sqrt(np.mean(residuals**2,axis=1)); print('Sensor residual RMS:',rms); plt.plot(t,residuals.T); plt.title('Sensor Fault Isolation Residuals'); plt.grid(); plt.show()
