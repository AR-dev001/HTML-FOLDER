import matplotlib.pyplot as plt
import numpy as np
X=np.array([0,10,20,30,40])
Y1=np.array([0,40,10,60,360])
Y2=np.array([0,240,198,130,300])
plt.plot(X,Y1,marker='+',ms=20,mec='y',linestyle="dotted",color='#800080',linewidth=20)
plt.plot(Y2,'o',color='r',linestyle='dotted',linewidth=20)
plt.title('Cool Graph Thingy')
plt.xlabel('plus')
plt.ylabel('weird square line')
plt.show()