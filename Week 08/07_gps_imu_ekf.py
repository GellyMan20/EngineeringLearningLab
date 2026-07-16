import numpy as np
import matplotlib.pyplot as plt
rng=np.random.default_rng(7); dt=.02; t=np.arange(0,80,dt); ax=.12*np.sin(.18*t); ay=.08*np.cos(.12*t); vx=np.cumsum(ax)*dt; vy=np.cumsum(ay)*dt; px=np.cumsum(vx)*dt; py=np.cumsum(vy)*dt; iax=ax+.02+rng.normal(0,.04,len(t)); iay=ay-.015+rng.normal(0,.04,len(t)); gx=np.full(len(t),np.nan); gy=np.full(len(t),np.nan); gx[::50]=px[::50]+rng.normal(0,1.2,len(px[::50])); gy[::50]=py[::50]+rng.normal(0,1.2,len(py[::50])); x=np.zeros((4,1)); P=np.diag([25.,25.,9.,9.]); H=np.array([[1,0,0,0],[0,1,0,0]],float); R=np.diag([1.44,1.44]); I=np.eye(4); est=[]
for k in range(len(t)):
 F=np.array([[1,0,dt,0],[0,1,0,dt],[0,0,1,0],[0,0,0,1]],float); B=np.array([[.5*dt**2,0],[0,.5*dt**2],[dt,0],[0,dt]],float); Q=np.diag([.001,.001,.03,.03]); x=F@x+B@np.array([[iax[k]],[iay[k]]]); P=F@P@F.T+Q
 if not np.isnan(gx[k]):
  z=np.array([[gx[k]],[gy[k]]]); y=z-H@x; S=H@P@H.T+R; K=P@H.T@np.linalg.inv(S); x=x+K@y; P=(I-K@H)@P
 est.append(x.ravel())
est=np.array(est); plt.plot(px,py,label='Truth'); plt.plot(est[:,0],est[:,1],label='Estimate'); plt.scatter(gx,gy,s=10,alpha=.4,label='GPS'); plt.axis('equal'); plt.grid(); plt.legend(); plt.show()
