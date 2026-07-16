import numpy as np
import matplotlib.pyplot as plt
dt=.1; F=np.array([[1,dt],[0,1.]]); Q=np.diag([.02,.1]); P=np.diag([1.,1.]); ps=[]; vs=[]
for _ in range(200): P=F@P@F.T+Q; ps.append(np.sqrt(P[0,0])); vs.append(np.sqrt(P[1,1]))
plt.plot(ps,label='Position sigma'); plt.plot(vs,label='Velocity sigma'); plt.title('Covariance Growth'); plt.grid(); plt.legend(); plt.show()
