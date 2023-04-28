import cv2
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageChops
import pandas as pd


class oil():

    def __init__(self):
        self.realh=13/796#像素与实际尺寸间的关系
        self.realw=16/1160#像素与实际尺寸间的关系
        self.sum=32#图片数量，即一份巩膜分成多少个角度
        self.name="3D"#存储结果的文件名
        self.path=r'D:\Deep-Learing\NetModel\3D\img_msk'#目标文件的地址
        self.save_csv=r'D:\Deep-Learing\NetModel\3D\csv'#存储csv的地址
        self.list_name=[' ', 'x1', 'y1', 'z1', 'x2', 'y2', 'z2', 'x3', 'y3', 'z3', 'x4', 'y4', 'z4']#列名
    def XYZ(self):
        filelist = os.listdir(self.path)
        SCLUP_ = [[],[],[]]  # 巩膜镜上表面
        TRFUP_ = [[],[],[]]  # 泪液层上表面
        CORUP_ = [[],[],[]]  # 角膜上表面
        CORDOWN_ = [[],[],[]]  # 角膜下表面
        ALL=[[],[],[],[],[],[],[],[],[],[],[],[]]
        flag=0
        self.name="test"
        self.sum=self.sum/2
        print("==================图像处理中=====================")
        for item in filelist:
            #self.name=item.split(".")[0]
            img_name = os.path.join(self.path, item)
            img = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)  # 灰度图像
            img = np.array(img)
            x, y = img.shape
            t=x
            SCLUP = []  # 巩膜镜上表面
            SCLUP_x = []
            SCLUP_y = []
            TRFUP = []  # 泪液层上表面
            TRFUP_x = []
            TRFUP_y = []
            CORUP = []  # 角膜上表面
            CORUP_x = []
            CORUP_y = []
            CORDOWN = []  # 角膜下表面
            CORDOWN_x = []
            CORDOWN_y = []
            midver = []
            L = []
            R = []
            # 遍历二值图，
            for i in range(y - 1):
                for j in range(x - 1):
                    #
                    if (img[j, i] == 51 and ((img[j + 1, i] == 153)or img[j,i+1]==153 or img[j,i-1]==153))  or (img[j, i] == 102 and ((img[j + 1, i] == 153)or img[j,i+1]==153 or img[j,i-1]==153)):
                        img[j, i] = 255
                        CORUP.append([j, i])
                    elif (img[j - 1, i] == 0 or img[j,i-1] == 0 or img[j,i+1] == 0) and img[j, i] == 51:
                        # img[j, i] = 255
                        SCLUP.append([j, i])
                    elif (img[j - 1, i] == 51 or img[j,i-1] == 51 or img[j,i+1] == 51) and img[j, i] == 102:
                        # img[j, i] = 255
                        TRFUP.append([j, i])
                    elif img[j, i] == 153 and (img[j + 1, i] == 204 or img[j+1,i+1] == 204 or img[j+1,i-1] == 204):
                        # img[j, i] = 255
                        CORDOWN.append([j, i])
            lx, ly = CORDOWN[0]
            lx += 1
            rx, ry = CORDOWN[-1]
            rx += 1
            # img[lx,ly]=255
            # img[rx,ry]=255
            # print(lx, ly)
            # print(rx, ry)
            # print(ly)
            # print(ry)
            midy = (ly + ry) // 2
            midx = (lx + rx) // 2
            # print(midx, midy)
            img[midx, midy] = 0
            K = (lx - rx) / (ly - ry)
            b = 477 - 131 * K
            # print(b)
            # midy = -1/K *midx+b1
            b1 = midy + K * midx
            # print(b1)
            y = -K * x + b1

            for y in range(ly, ry):
                x = K * y + b  # 左右两点之间方程
                x = round(x)
                # print(x)
                # y=y.astype('uint8')
                img[x, y] = 255
            for x in range(t):
                y = -K * x + b1  # 左右两点之间垂线方程
                y = round(y)
                # print(x)
                # y=y.astype('uint8')
                midver.append([x, y])
                # print(midver)
                img[x, y] = 255
            #print(type(CORUP))
            res = [v for v in CORUP if v in midver]
            for i in range(len(res)):
                if res[0][0]<res[i][0]:
                    res[0]=res[i]
            a = (res[0])  # 角膜上表面的中点
            print("坐标轴中心:"+str(a))
            print("已完成" + str((flag + 1) / 32 * 100) + "%" + "当前角度" + str(180 / self.sum * (flag) % 360) + "°")
            ansx=(a[1])
            ansy=(a[0])
            for item in SCLUP:
                SCLUP_x.append((item[1]-a[1])*self.realw)
                SCLUP_y.append(-(item[0]-a[0])*self.realh)
            for item in TRFUP:
                TRFUP_x.append((item[1]-a[1])*self.realw)
                TRFUP_y.append(-(item[0]-a[0])*self.realh)
            for item in CORUP:
                CORUP_x.append((item[1]-a[1])*self.realw)
                CORUP_y.append(-(item[0]-a[0])*self.realh)
            for item in CORDOWN:
                CORDOWN_x.append((item[1]-a[1])*self.realw)
                CORDOWN_y.append(-(item[0]-a[0])*self.realh)
            SCLUP_z=SCLUP_y
            SCLUP_y=[item*(math.sin(math.pi/self.sum*flag)) for item in SCLUP_x]
            SCLUP_x=[item*(math.cos(math.pi/self.sum*flag)) for item in SCLUP_x]
            TRFUP_z=TRFUP_y
            TRFUP_y=[item*(math.sin(math.pi/self.sum*flag)) for item in TRFUP_x]
            TRFUP_x=[item*(math.cos(math.pi/self.sum*flag)) for item in TRFUP_x]
            CORUP_z=CORUP_y
            CORUP_y=[item*(math.sin(math.pi/self.sum*flag)) for item in CORUP_x]
            CORUP_x=[item*(math.cos(math.pi/self.sum*flag)) for item in CORUP_x]
            CORDOWN_z=CORDOWN_y
            CORDOWN_y=[item*(math.sin(math.pi/self.sum*flag)) for item in CORDOWN_x]
            CORDOWN_x=[item*(math.cos(math.pi/self.sum*flag)) for item in CORDOWN_x]
            ALL[0].extend(SCLUP_x)
            ALL[1].extend(SCLUP_y)
            ALL[2].extend(SCLUP_z)
            ALL[3].extend(TRFUP_x)
            ALL[4].extend(TRFUP_y)
            ALL[5].extend(TRFUP_z)
            ALL[6].extend(CORUP_x)
            ALL[7].extend(CORUP_y)
            ALL[8].extend(CORUP_z)
            ALL[9].extend(CORDOWN_x)
            ALL[10].extend(CORDOWN_y)
            ALL[11].extend(CORDOWN_z)
            # ALL[0].extend(SCLUP_)
            # ALL[1].extend(TRFUP_)
            # ALL[2].extend(CORUP_)
            # ALL[3].extend(CORDOWN_)
            flag=flag+1
        print("转置中")
        dataframe = pd.DataFrame(ALL).T
        save = os.path.join(self.save_csv,self.name+'result'+".csv")
        dataframe.to_csv(save,header=True,index_label=self.list_name)
        return()
    def all(self):
        T.XYZ()
T = oil()
# print(T.XYZ(r"D:\Deep-Learing\NetModel\3D\img_msk\LYR_1H_00012.png"))
#T.Canny()
#T.erzhi()
#T.get_line_position()
T.all()

