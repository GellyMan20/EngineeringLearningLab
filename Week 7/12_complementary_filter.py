import numpy as np
import matplotlib.pyplot as plt

def main():
    rng=np.random.default_rng(12); dt=.01; t=np.arange(0,40,dt); truth=np.deg2rad(20*np.sin(.35*t)); rate=np.gradient(truth,dt)
    gyro=rate+np.deg2rad(.35)+rng.normal(0,np.deg2rad(.12),len(t)); accel=truth+rng.normal(0,np.deg2rad(2.5),len(t))
    gi=np.zeros_like(t); fused=np.zeros_like(t); a=.98
    for k in range(1,len(t)):
        gi[k]=gi[k-1]+gyro[k]*dt; fused[k]=a*(fused[k-1]+gyro[k]*dt)+(1-a)*accel[k]
    plt.figure(); plt.plot(t,np.rad2deg(truth),label='Truth'); plt.plot(t,np.rad2deg(gi),label='Gyro'); plt.plot(t,np.rad2deg(accel),alpha=.4,label='Accel'); plt.plot(t,np.rad2deg(fused),label='Fused'); plt.grid(True); plt.legend(); plt.show()
if __name__=='__main__': main()
