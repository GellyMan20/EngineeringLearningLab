import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
def ell(mean,P,n=2):
 w,v=np.linalg.eigh(P); idx=w.argsort()[::-1]; w=w[idx]; v=v[:,idx]; a=np.degrees(np.arctan2(v[1,0],v[0,0])); return Ellipse(mean,2*n*np.sqrt(w[0]),2*n*np.sqrt(w[1]),angle=a,fill=False)
fig,ax=plt.subplots(); means=[(0,0),(5,2),(10,5),(15,9)]; Ps=[np.array([[1,.2],[.2,.5]]),np.array([[2,.8],[.8,1]]),np.array([[4,1.5],[1.5,2]]),np.array([[1.5,-.4],[-.4,.8]])]
for m,P in zip(means,Ps): ax.add_patch(ell(m,P)); ax.scatter(*m)
ax.set_xlim(-4,20); ax.set_ylim(-4,14); ax.set_aspect('equal'); ax.grid(); ax.set_title('Covariance Ellipse Evolution'); plt.show()
