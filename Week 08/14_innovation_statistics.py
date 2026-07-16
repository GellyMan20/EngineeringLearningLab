import numpy as np
import matplotlib.pyplot as plt
rng=np.random.default_rng(14); n=2000; innovations=rng.normal(0,1,n); innovations[800:1000]+=2
window=100; means=np.array([innovations[max(0,i-window):i+1].mean() for i in range(n)]); stds=np.array([innovations[max(0,i-window):i+1].std() for i in range(n)])
plt.plot(means,label='Rolling mean'); plt.plot(stds,label='Rolling std'); plt.title('Innovation Statistics'); plt.grid(); plt.legend(); plt.show()
