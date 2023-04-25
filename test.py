import pandas as pd
import matplotlib as mb
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

csv = pd.read_csv(r'D:\NET-MODEL\3D\csv\testresult2.csv')  # 文件路径
ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
#  将数据点分成三部分画，在颜色上有区分度
ax.scatter(csv.x4, csv.y4, csv.z4, c='b')  # 绘制数据点
plt.xlim((-10, 10))
plt.ylim((-10, 10))
#plt.zlim((-15, 15))

ax.set_zlabel('Z')  # 坐标轴
ax.set_ylabel('Y')
ax.set_xlabel('X')
plt.show()