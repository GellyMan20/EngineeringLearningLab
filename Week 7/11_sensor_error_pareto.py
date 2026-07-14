from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

def main():
    rng=np.random.default_rng(11); cats=rng.choice(['Accel bias','GPS dropout','Latency','GPS outlier','Timing jitter','Gyro drift'],500,p=[.28,.22,.18,.12,.10,.10])
    ordered=Counter(cats).most_common(); names=[x[0] for x in ordered]; vals=[x[1] for x in ordered]; cum=100*np.cumsum(vals)/np.sum(vals)
    plt.figure(); plt.bar(names,vals); plt.xticks(rotation=35); plt.title('Sensor Error Pareto'); plt.tight_layout(); plt.show()
    plt.figure(); plt.plot(names,cum,marker='o'); plt.axhline(80,linestyle='--'); plt.xticks(rotation=35); plt.tight_layout(); plt.show()
if __name__=='__main__': main()
