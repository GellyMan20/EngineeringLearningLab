import numpy as np
import matplotlib.pyplot as plt

def main():
    rng=np.random.default_rng(3); dt=0.01; t=np.arange(0,40,dt)
    ta=0.8*np.sin(0.4*t); tg=0.15*np.cos(0.25*t)
    a=ta+0.08+np.cumsum(rng.normal(0,0.0004,len(t)))+rng.normal(0,0.06,len(t))
    g=tg+np.deg2rad(0.4)+np.cumsum(rng.normal(0,np.deg2rad(0.002),len(t)))+rng.normal(0,np.deg2rad(0.08),len(t))
    plt.figure(); plt.plot(t,ta,label='True accel'); plt.plot(t,a,alpha=.7,label='Measured accel'); plt.grid(True); plt.legend(); plt.show()
    plt.figure(); plt.plot(t,np.rad2deg(tg),label='True gyro'); plt.plot(t,np.rad2deg(g),alpha=.7,label='Measured gyro'); plt.grid(True); plt.legend(); plt.show()
if __name__=='__main__': main()
