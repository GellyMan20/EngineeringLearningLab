import numpy as np
def O(F,H):
 blocks=[H]; cur=H.copy()
 for _ in range(1,F.shape[0]): cur=cur@F; blocks.append(cur)
 return np.vstack(blocks)
dt=.1; F=np.array([[1,dt],[0,1.]]);
for name,H in [('Position only',np.array([[1.,0.]])),('Velocity only',np.array([[0.,1.]]))]:
 M=O(F,H); print(name); print(M); print('rank=',np.linalg.matrix_rank(M),'of',F.shape[0])
