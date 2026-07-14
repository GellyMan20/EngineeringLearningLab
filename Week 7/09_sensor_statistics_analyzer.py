import numpy as np
import pandas as pd

def main():
    rng=np.random.default_rng(9); n=5000; truth=np.linspace(0,100,n); m=truth+0.7+rng.normal(0,1.4,n); e=m-truth
    df=pd.DataFrame({'truth':truth,'measurement':m,'error':e})
    metrics={'bias':df.error.mean(),'std':df.error.std(ddof=1),'rmse':np.sqrt(np.mean(e**2)),'mae':np.mean(np.abs(e)),'p95_abs_error':np.percentile(np.abs(e),95),'max_abs_error':np.max(np.abs(e))}
    for k,v in metrics.items(): print(f'{k:>15}: {v:.3f}')
if __name__=='__main__': main()
