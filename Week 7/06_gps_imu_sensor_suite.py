from dataclasses import dataclass
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

@dataclass
class Config:
    imu_rate_hz: float=100.0
    gps_rate_hz: float=5.0
    gps_latency_s: float=0.4
    gps_dropout_probability: float=0.05

def main():
    rng=np.random.default_rng(6); c=Config(); dt=1/c.imu_rate_hz; t=np.arange(0,60,dt)
    ax=0.3*np.sin(0.3*t); ay=0.2*np.cos(0.2*t); vx=np.cumsum(ax)*dt; vy=np.cumsum(ay)*dt; x=np.cumsum(vx)*dt; y=np.cumsum(vy)*dt
    iax=ax+0.03+rng.normal(0,0.05,len(t)); iay=ay-0.02+rng.normal(0,0.05,len(t))
    stride=int(c.imu_rate_hz/c.gps_rate_hz); gx=np.full(len(t),np.nan); gy=np.full(len(t),np.nan)
    gx[::stride]=x[::stride]+rng.normal(0,1.5,len(x[::stride])); gy[::stride]=y[::stride]+rng.normal(0,1.5,len(y[::stride]))
    idx=np.where(~np.isnan(gx))[0]; drop=rng.random(len(idx))<c.gps_dropout_probability; gx[idx[drop]]=np.nan; gy[idx[drop]]=np.nan
    d=int(c.gps_latency_s/dt); gx=np.roll(gx,d); gy=np.roll(gy,d); gx[:d]=np.nan; gy[:d]=np.nan
    df=pd.DataFrame({'time_s':t,'true_x_m':x,'true_y_m':y,'imu_ax_mps2':iax,'imu_ay_mps2':iay,'gps_x_m':gx,'gps_y_m':gy})
    print(df.head()); print(df.describe())
    plt.figure(); plt.plot(x,y,label='Truth'); plt.scatter(gx,gy,s=12,label='GPS'); plt.axis('equal'); plt.grid(True); plt.legend(); plt.show()
if __name__=='__main__': main()
