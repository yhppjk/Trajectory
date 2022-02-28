import numpy as np
import matplotlib.pyplot as plt
import utm
import math

import glob

from scipy.spatial.transform import Rotation as R


#matrice a inverser
H = np.array([[ 0.4330127 , -0.77181154,  0.46562532, 15.        ],
			[ 0.75      ,  0.59503485,  0.28884863, 30.        ],
			[-0.5       ,  0.22414387,  0.8365163 , 38.5       ],
			[ 0.        ,  0.        ,  0.        ,  1.        ]])
			   
### TODO :recuperer la translation et les angles dans l'ordre ZYX
### attention en fonction de votre version de scipy, la methode as_dcm est peut etre remplace par as_matrix

r = R.from_matrix(H[0:3,0:3])
print(r.as_euler('zyx', degrees=True))

h = np.linalg.inv(H)
r = R.from_matrix(h[0:3,0:3])
print(r.as_euler('ZYX', degrees=True))





### TODO inverser la matrice H,extraire les translations et angles dans l'ordre ZYX  (regarder np.linalg.inv pour realiser l'inversion)

