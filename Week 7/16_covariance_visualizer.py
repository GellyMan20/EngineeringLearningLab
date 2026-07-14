import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

def ell(mean,cov,n):
    vals,vecs=np.linalg.eigh(cov); o=vals.argsort()[::-1]; vals=vals[o]; vecs=vecs[:,o]; ang=np.degrees(np.arctan2(vecs[1,0],vecs[0,0])); w,h=2*n*np.sqrt(vals); return Ellipse(mean,w,h,angle=ang,fill=False,linewidth=2)

def main():
    rng=np.random.default_rng(16); mean=np.array([10.,5.]); cov=np.array([[9.,5.5],[5.5,6.]]); s=rng.multivariate_normal(mean,cov,800)
    fig,ax=plt.subplots(); ax.scatter(s[:,0],s[:,1],s=8,alpha=.3); ax.scatter([mean[0]],[mean[1]],marker='x',label='Mean')
    for n in [1,2,3]: ax.add_patch(ell(mean,cov,n))
    ax.axis('equal'); ax.grid(True); ax.legend(); plt.show()
if __name__=='__main__': main()
