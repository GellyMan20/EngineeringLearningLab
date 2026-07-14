import numpy as np
import matplotlib.pyplot as plt

def main():
    rng=np.random.default_rng(4); dt=0.01; t=np.arange(0,60,dt)
    a=np.zeros_like(t); a[(t>=3)&(t<12)]=0.7; a[(t>=30)&(t<38)]=-0.5
    v=np.cumsum(a)*dt; x=np.cumsum(v)*dt
    am=a+0.025+rng.normal(0,0.04,len(t)); ve=np.cumsum(am)*dt; xe=np.cumsum(ve)*dt
    plt.figure(); plt.plot(t,x,label='Truth'); plt.plot(t,xe,label='Dead reckoning'); plt.title('Dead Reckoning Drift'); plt.grid(True); plt.legend(); plt.show()
if __name__=='__main__': main()
