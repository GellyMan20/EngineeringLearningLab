import numpy as np
import matplotlib.pyplot as plt

def main():
    rng=np.random.default_rng(10); dt=.1; t=np.arange(0,60,dt); truth=.4*t; s=truth+rng.normal(0,.5,len(t)); labels=np.array(['nominal']*len(t),dtype=object)
    w=(t>=10)&(t<20); s[w]+=4; labels[w]='bias'
    w=(t>=20)&(t<35); s[w]+=.4*(t[w]-20); labels[w]='drift'
    w=(t>=35)&(t<43); s[w]=s[np.where(t>=35)[0][0]]; labels[w]='stuck'
    w=(t>=43)&(t<50); s[w]=np.nan; labels[w]='dropout'
    i=np.argmin(abs(t-54)); s[i]+=15; labels[i]='outlier'
    for label in np.unique(labels): print(label,np.sum(labels==label))
    plt.figure(); plt.plot(t,truth,label='Truth'); plt.plot(t,s,label='Sensor'); plt.title('Sensor Anomalies'); plt.grid(True); plt.legend(); plt.show()
if __name__=='__main__': main()
