import cv2
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageChops
import pandas as pd


class oil():

    def __init__(self):
        #先边界化，再二值化
        self.name=""
        self.path= r'/img_msk'  #目标文件的地址
        self.save_path= r'/img_after'  #存储Canny文件的地址
        self.save_path2=r'D:\Deep-Learing\NetModel\3D\img_erzhi'#存储二值文件的地址
        self.save_csv=r'D:\Deep-Learing\NetModel\3D\csv'#存储csv
    def Canny(self):
        self.path
        filelist = os.listdir(self.path)  # 获取文件路径
        i = 1
        for item in filelist:
            total_num = len(filelist)  # 获取文件长度（个数）
            self.name=item.split(".")[0]
            #转化为灰度图像
            img_name = os.path.join(self.path,item)
            img = cv2.imread(img_name)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            #sobel算子，对效率要求较高，对纹理不太关心的时候。

            # soblex = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=3)
            # sobley = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=3)
            # sobel = cv2.addWeighted(soblex,0.5,sobley,0,5,0)
            # cv2.imshow('Sobel',sobel)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            #Canny算子
            canny = cv2.Canny(gray,100,200)
            save = os.path.join(self.save_path,'00' + format(str(i), '0>3s')+".png")
            cv2.imwrite(save,canny)
            i=i+1
            # cv2.imshow('Canny',canny)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

    def get_line_position(self):
        print("==========================生成图表中===========================")
        flag=0
        filelist = os.listdir(self.save_path2)
        anglex,angley = self.XYZ()
        out=[[],[],[]]
        for item in filelist:
            img_name = os.path.join(self.save_path2,item)
            image = cv2.imread(img_name)
            ans = [[],[],[]]
            list_x = []
            list_y = []
            list_z = []
            max_y=0
            max_x=0
            # y_len = len(image)
            # print(y_len)
            for i in range(len(image[0])):  # 遍历列数
                for j in range(len(image)):  # 遍历行数
                    if (image[j][i] == [0,0,0]).all():
                        y=len(image) - j
                        x=i
                        list_x.append(x)
                        list_y.append(y)
                        if(max_y<y):
                            max_y=y
                            max_x=x
                        # break
            msk_name=os.path.join(r"/img_msk", item)
            #a = self.XYZ(msk_name)
            list_x=[item -anglex[flag] for item in list_x]
            list_y=[item +angley[flag] for item in list_y]
            list_z=list_y
            list_y=[item*(math.sin(math.pi/16*flag)) for item in list_x]
            list_x=[item*(math.cos(math.pi/16*flag)) for item in list_x]
            ans[0]=[item*16/1160 for item in list_x]
            ans[1]=[item*16/1160 for item in list_y]
            ans[2]=[item*13/796 for item in list_z]
            out[0].extend(ans[0])
            out[1].extend(ans[1])
            out[2].extend(ans[2])
            #save = os.path.join(self.save_csv,'00' + format(str(flag), '0>3s')+".csv")
            #print("已完成"+str((flag+1)/32*100)+"%"+"当前角度"+str(180/16*(flag)%360)+"°")
            flag=flag+1
        print("转置中")
        dataframe = pd.DataFrame(out).T
        save = os.path.join(self.save_csv,self.name+'result'+".csv")
        dataframe.to_csv(save)
    def erzhi(self):
        i=1
        filelist = os.listdir(self.save_path)  # 获取文件路径
        for item in filelist:
            img_name = os.path.join(self.save_path,item)
            img = cv2.imread(img_name)
            ret,mask_all = cv2.threshold(src=img,
                                         thresh=127,#阈值
                                         maxval=255,
                                         type=cv2.THRESH_BINARY)
            # plt.imshow(mask_all, cmap='gray')
            # plt.show()
            # plt.title("全局阈值")
            save = os.path.join(self.save_path2,'00' + format(str(i), '0>3s')+".png")
            i=i+1
            cv2.imwrite(save,img)
        filelist = os.listdir(self.save_path2)
        i=1
        for item in filelist:
            fname = os.path.join(self.save_path2, item)
            im = Image.open(fname)
            im_inverted = ImageChops.invert(im)
            save = os.path.join(self.save_path2, '00' + format(str(i), '0>3s') + ".png")
            im_inverted.save(save)
            i=i+1
    def XYZ(self):
        filelist = os.listdir(self.path)
        ansx = []
        ansy = []
        flag=0
        for item in filelist:
            img_name = os.path.join(self.path, item)
            img = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)  # 灰度图像
            img = np.array(img)
            x, y = img.shape
            SCLUP = []  # 巩膜镜上表面
            TRFUP = []  # 泪液层上表面
            CORUP = []  # 角膜上表面
            CORDOWN = []  # 角膜下表面
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
                    elif img[j - 1, i] == 0 and img[j, i] == 51:
                        # img[j, i] = 255
                        SCLUP.append([i, j])
                    elif img[j - 1, i] == 51 and img[j, i] == 102:
                        # img[j, i] = 255
                        TRFUP.append([j, i])
                    elif img[j, i] == 153 and img[j + 1, i] == 204:
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
            for x in range(796):
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
            print("已完成" + str((flag + 1) / 32 * 100) + "%" + "当前角度" + str(180 / 16 * (flag) % 360) + "°")
            ansx.append(a[1])
            ansy.append(a[0])
            flag=flag+1
        return(ansx,ansy)
    def all(self):
        T.Canny()
        T.erzhi()
        T.get_line_position()
T = oil()
# print(T.XYZ(r"D:\Deep-Learing\NetModel\3D\img_msk\LYR_1H_00012.png"))
#T.Canny()
#T.erzhi()
#T.get_line_position()
T.all()

