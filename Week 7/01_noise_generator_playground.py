import numpy as np
import matplotlib.pyplot as plt

def main():
    rng=np.random.default_rng(1); dt=0.01; t=np.arange(0,30,dt); truth=np.sin(0.7*t)
    series={
        'White noise': truth+rng.normal(0,0.08,len(t)),
        'Bias': truth+0.25,
        'Random walk': truth+np.cumsum(rng.normal(0,0.0015,len(t))),
        'Drift': truth+0.01*t,
        'Quantized': np.round(truth/0.1)*0.1,
    }
    plt.figure(); plt.plot(t,truth,label='Truth')
    for name,y in series.items(): plt.plot(t,y,alpha=0.75,label=name)
    plt.title('Common Sensor Error Types'); plt.xlabel('Time [s]'); plt.ylabel('Measurement'); plt.grid(True); plt.legend(); plt.show()
if __name__=='__main__': main()
