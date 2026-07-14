import numpy as np
import matplotlib.pyplot as plt

def main():
    rng=np.random.default_rng(2); dt=0.2; t=np.arange(0,100,dt)
    tx=0.8*t; ty=12*np.sin(t/15)
    gx=tx+1.5+rng.normal(0,1.8,len(t)); gy=ty-0.8+rng.normal(0,1.8,len(t))
    out=rng.choice(len(t),8,replace=False); gx[out]+=rng.normal(0,20,len(out)); gy[out]+=rng.normal(0,20,len(out))
    drop=rng.random(len(t))<0.06; gx[drop]=np.nan; gy[drop]=np.nan
    err=np.hypot(gx-tx,gy-ty)
    print(f'Mean error: {np.nanmean(err):.2f} m'); print(f'95th percentile: {np.nanpercentile(err,95):.2f} m'); print(f'Dropout rate: {100*np.mean(drop):.1f}%')
    plt.figure(); plt.plot(tx,ty,label='Truth'); plt.scatter(gx,gy,s=10,label='GPS'); plt.title('GPS Noise, Outliers, Dropouts'); plt.axis('equal'); plt.grid(True); plt.legend(); plt.show()
if __name__=='__main__': main()
