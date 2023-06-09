import cv2
import  numpy as np
from PIL import Image
import os
from tkinter import filedialog
import tkinter
from natsort import natsorted

for ii in range(99):
    root = tkinter.Tk()
    root.withdraw()  # 隐藏
    TEST_IMAGE_PATH = filedialog.askdirectory()
    root.destroy()  # 销毁

    for root, dirs, files in os.walk(TEST_IMAGE_PATH):
        files = natsorted(files)
        folder = (root + '//new//')
        if not os.path.exists(folder):
            os.makedirs(folder)
        for name in files:
            if name.endswith('png'):


                img=cv2.imread(root + '\\' + name,cv2.IMREAD_GRAYSCALE) #灰度图像
                img = np.array(img)
                print(type(img))
                x,y= img.shape
                print(x,y)
                SCLUP= []   #巩膜镜上表面
                TRFUP=[]    #泪液层上表面
                CORUP=[]    #角膜上表面
                CORDOWN=[]  #角膜下表面
                midver=[]
                L=[]
                R=[]
                #遍历二值图，
                for i in range(y-1):
                         for j in range(x-1):
                             #
                             if (img[j,i] == 51 and img[j+1,i]==153) or (img[j,i] == 102 and img[j+1,i]==153) :
                                img[j, i] =255
                                CORUP.append([j,i])
                             elif img[j-1,i]==0 and  img[j,i] ==51 :
                                 # img[j, i] = 255
                                 SCLUP.append([i,j])
                             elif img[j-1,i]==51 and img[j,i] ==102 :
                                 # img[j, i] = 255
                                 TRFUP.append([j,i])
                             elif img[j,i] == 153 and img[j+1,i]==204:
                                 #img[j, i] = 255
                                 CORDOWN.append([j,i])
                lx,ly=CORDOWN[0]
                lx+=1
                rx,ry=CORDOWN[-1]
                rx+=1
                # img[lx,ly]=255
                # img[rx,ry]=255
                print(lx,ly)
                print(rx,ry)
                print(ly)
                print(ry)
                midy=(ly+ry)//2
                midx= (lx+rx)//2
                print(midx,midy)
                img[midx,midy]=0
                K = (lx-rx)/(ly-ry)
                b=477-131*K
                print(b)
                #midy = -1/K *midx+b1
                b1=midy+ K*midx
                print(b1)
                y= -K *x+b1

                for y in range(ly,ry):
                    x = K * y + b    #左右两点之间方程
                    x = round(x)
                    #print(x)
                    #y=y.astype('uint8')
                    img[x,y]=255
                for x in range(796):
                    y =  -K * x + b1  # 左右两点之间垂线方程
                    y = round(y)
                    # print(x)
                    # y=y.astype('uint8')
                    midver.append([x,y])
                    #print(midver)
                    img[x, y] = 255
                print(type(CORUP))
                res=[v for v in CORUP if v in midver]
                a= (res[0])     #角膜上表面的中点
                print(a)


                img[a[0],a[1]]=0
                # print(CORUP)
                # CORUP=[item-[a[0],a[1]] for item in CORUP]
                # print(CORUP)
                # img.save(root  + '\\' + name)
                cv2.imwrite(root + '\\' + 'new' + '\\' + name + '.png',img )

                print('ok')
