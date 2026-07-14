from collections import deque
import numpy as np
import matplotlib.pyplot as plt

def main():
    rng=np.random.default_rng(5); dt=0.01; t=np.arange(0,30,dt); truth=np.sin(0.6*t)
    next_sample=0.0; q=deque(); td=[]; yd=[]
    for time,val in zip(t,truth):
        if time>=next_sample:
            q.append((time+0.35,val+rng.normal(0,0.05))); next_sample+=max(0.01,0.1+rng.normal(0,0.01))
        while q and q[0][0]<=time:
            a,b=q.popleft(); td.append(a); yd.append(b)
    plt.figure(); plt.plot(t,truth,label='Truth'); plt.scatter(td,yd,s=12,label='Delivered'); plt.title('Timing Jitter and Latency'); plt.grid(True); plt.legend(); plt.show()
if __name__=='__main__': main()
