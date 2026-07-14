import numpy as np
import matplotlib.pyplot as plt

def trial(rng):
    dt=.05; t=np.arange(0,40,dt); a=.15*np.sin(.25*t); v=np.cumsum(a)*dt; truth=np.cumsum(v)*dt; bias=rng.normal(0,.03); imu_std=rng.uniform(.02,.08); gps_std=rng.uniform(.7,2.5); imu=a+bias+rng.normal(0,imu_std,len(t)); gps=np.full(len(t),np.nan); gps[::20]=truth[::20]+rng.normal(0,gps_std,len(gps[::20]))
    x=np.zeros((2,1)); P=np.diag([20.,8.]); H=np.array([[1.,0.]]); I=np.eye(2); est=[]
    for k in range(len(t)):
        F=np.array([[1,dt],[0,1.]]); B=np.array([[.5*dt**2],[dt]]); Q=np.diag([.001,.03]); x=F@x+B*imu[k]; P=F@P@F.T+Q
        if not np.isnan(gps[k]):
            R=np.array([[gps_std**2]]); y=np.array([[gps[k]]])-H@x; S=H@P@H.T+R; K=P@H.T@np.linalg.inv(S); x=x+K@y; P=(I-K@H)@P
        est.append(x[0,0])
    e=np.array(est)-truth; return np.sqrt(np.mean(e**2)),np.max(np.abs(e))

def main():
    rng=np.random.default_rng(23); r=np.array([trial(rng) for _ in range(300)]); print(f'Mean RMSE: {np.mean(r[:,0]):.2f} m'); print(f'95th percentile max error: {np.percentile(r[:,1],95):.2f} m'); plt.figure(); plt.hist(r[:,0],bins=30); plt.title('Monte Carlo RMSE'); plt.grid(True); plt.show()
if __name__=='__main__': main()
