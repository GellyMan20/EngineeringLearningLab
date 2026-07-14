import numpy as np
import matplotlib.pyplot as plt

def main():
    t=np.arange(0,10,0.001)
    streams=[t[::10],t[::200],t[::50],t[::25]]
    plt.figure(); plt.eventplot(streams,lineoffsets=[4,3,2,1],linelengths=.8)
    plt.yticks([1,2,3,4],['Altimeter','Magnetometer','GPS','IMU']); plt.title('Multi-Rate Sensor Timing'); plt.xlabel('Time [s]'); plt.grid(True,axis='x'); plt.show()
if __name__=='__main__': main()
