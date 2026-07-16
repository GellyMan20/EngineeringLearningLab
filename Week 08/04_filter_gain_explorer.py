import numpy as np
import matplotlib.pyplot as plt
P=np.logspace(-2,2,200)
for R in [.1,1,10]: plt.semilogx(P,P/(P+R),label=f'R={R}')
plt.title('Scalar Kalman Gain'); plt.grid(which='both'); plt.legend(); plt.show()
