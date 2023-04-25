import numpy as np
import matplotlib.pyplot as plt
from PIL import  Image

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

"""
December 16, 2022，LuoNicus
获取曲线分割后的图像点坐标类
用不同的方法获取坐标
只可提取像素 0 or 255，提取其它自行修改
正常提取，上边缘提取，中值提取，各有优缺，根据实际情况使用
"""

"""   图像像素示意
    [[255,255, 255, 0,   0]
     [0,   0,  255, 0,   0]
     [0,   0,  255, 0,   0]
     [0,   0,  255, 255,255]]     
"""

class Get_Line_Positon:
    def __init__(self, image):
        self.image = image
        self.list_x = []
        self.list_y = []
        print("已获取图像信息,准备提取二值图像位置坐标")

    def by_allline_point(self):  # 提取坐标，存在bug，会重复提取x的值
        # 细化算法存在bug，第一行和第一列为0黑色，不合理，因此首先去掉
        print("warn:常规算法提取，容易出现多个x为相同值")
        self.image = np.delete(self.image, 0, axis=0)  # 删除第一行
        self.image = np.delete(self.image, 0, axis=1)  # 删除第一列

        for i in range(len(self.image)):
            for j in range(len(self.image[i])):
                if self.image[i][j] == 0:
                    # print(mask[i][j],j,i)
                    self.list_x.append(j)
                    self.list_y.append(len(self.image) - i)
        return self.list_x, self.list_y

    def by_upline_point(self):  # 提取直线坐标，提取曲线的边缘坐标，避免出现x的重复值
        print("提取曲线上边缘的值")
        self.image = np.delete(self.image, 0, axis=0)  # 删除第一行
        self.image = np.delete(self.image, 0, axis=1)  # 删除第一列
        # y_len = len(self.image)
        # print(y_len)

        for i in range(len(self.image[0])):  # 遍历列数
            for j in range(len(self.image)):  # 遍历行数
                if self.image[j][i] == 0:
                    self.list_x.append(i)
                    self.list_y.append(len(self.image) - j)
                    break
        return self.list_x, self.list_y

    def by_lineMedium_point(self):  # 提取像素上下值的中位数坐标，该方法不用对函数进行细化
        print("提取曲线的中值")
        self.image = np.delete(self.image, 0, axis=0)  # 删除第一行
        self.image = np.delete(self.image, 0, axis=1)  # 删除第一列
        start_index = 0
        end_index = 0

        for i in range(len(self.image[0])):  # 遍历列数
            for j in range(len(self.image) - 1):  # 遍历行数
                print(self.image[j][i])
                if self.image[j][i] == 255 and self.image[j + 1][i] == 0:
                    start_index = j
                    continue
                if self.image[j][i] == 0 and self.image[j + 1][i] == 255:
                    end_index = j
                    y_position = (start_index + end_index) / 2
                    self.list_x.append(i)
                    self.list_y.append(len(self.image) - y_position)
                    start_index = 0
                    end_index = 0
                    break
        return self.list_x, self.list_y

img = Image.open(r"D:\Deep-Learing\NetModel\3D\img_msk\CKY_OD_1H_img003_outcome.png")
Img = img.convert('L')
threshold = 200
table = []
for i in range(512):
    if i<threshold:
        table.append(0)
    else:
        table.append(1)
photo = Img.p
G = Get_Line_Positon(img)
G.by_lineMedium_point()