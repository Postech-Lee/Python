import os
from PIL import Image
import pickle
import math
def findAngle(x, y):
    angle = math.degrees(math.atan2(y, x))
    if angle < 0:
        angle += 360
    ccw = 360 - angle
    region = int(ccw // 22.5)
    return region
def change2img(A, B, X, Y, Z, digital_L, digital_R, main_x, main_y, c_stick_x, c_stick_y, L, R):
    convertedList = []

    if digital_L == 0:
        convertedList.append(0)  #a0
    else:
        convertedList.append(1) # a1, analog값 출력 코드 필요
    
    if digital_R == 0:
        if Z:
            convertedList.append(4) #b2
        else:
            convertedList.append(2)  #b0
    else:
        convertedList.append(3) # b1, analog값 출력 코드 필요
        # Handling main stick (x, y)
    if main_x != 0 and main_y != 0:
        convertedList.append(findAngle(main_x, main_y) + 5)
    else:
        if main_x == 0 and main_y == 0:
            convertedList.append(5)
        elif main_x == 0 and main_y != 0:
            convertedList.append(6 if main_y > 0 else 14)
        elif main_y == 0 and main_x != 0:
            convertedList.append(18 if main_x > 0 else 10)
    if A :
        convertedList.append(23)
    elif B :
        convertedList.append(24)
    elif X :
        convertedList.append(25)
    elif Y :
        convertedList.append(26)
    else:
        convertedList.append(22)
    
    
    convertedList.append(27) # dpad signal is none => set default
    # Handling C stick (x, y)
    if c_stick_x != 0 and c_stick_y != 0:
        convertedList.append(findAngle(c_stick_x, c_stick_y) + 32)
    else:
        if c_stick_x == 0 and c_stick_y == 0:
            convertedList.append(32)
        elif c_stick_x == 0:
            convertedList.append(33 if c_stick_y > 0 else 41)
        elif c_stick_y == 0:
            convertedList.append(45 if c_stick_x > 0 else 37)

    return convertedList


file_path = "C:/Users/LEE/Downloads/action_history_09_13_102319.pkl"


with open(file_path, 'rb') as f:
    data = pickle.load(f)

sList1,sList2=data.get(0),data.get(1)

files = ['a0','a1', #0~1
'b0','b1','b2', #2~4
'c0','cn','cnnw','cnw','cnww','cw','csww','csw','cssw','cs','csse','cse','csee','ce','cnee','cne','cnne', #5~21
'd0','da','db','dx','dy', #22~26
'e0','eu','ed','el','er', #27~31
'f0','fn','fnnw','fnw','fnww','fw','fsww','fsw','fssw','fs','fsse','fse','fsee','fe','fnee','fne','fnne'] #32~48
pList=[(0, 0),(275, 0),(0, 60),(275, 60),(0, 195),(275, 195),(550, 0),(825, 0),(550, 60),(825, 60),(550, 195),(825, 195)]

image_path = os.getcwd()

for i in range(len(sList1)):
    empty_img = Image.new('RGB', (1100, 390), '#FFFFFF')
    bList=change2img(*sList1[i]) + change2img(*sList2[i])
    for j in range(12):
        image = Image.open(os.path.join(image_path, files[bList[j]] + ".png")) 
        empty_img.paste(image, (pList[j][0],pList[j][1]))
    empty_img.save(os.path.join(image_path,'resultImg','vis'+str(i+1)+'.png'))
    if i % 50 == 0:
        print(f'saved {i} pictures. {len(sList1)-i} left.')

pathIn= image_path
VideoName='gan'
pathOut = os.path.join(image_path,'resultVid',VideoName','.mp4')
path = os.path.join(image_path,'resultImg')
fps = 24
import re
import cv2
frame_array = []
paths = [os.path.join(path , i ) for i in os.listdir(path) if re.search(".png$", i )]
for idx , path in enumerate(paths) : 
    if (idx % 2 == 0) | (idx % 5 == 0) :
        continue
    img = cv2.imread(path)
    height, width, layers = img.shape
    size = (width,height)
    frame_array.append(img)
out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
for i in range(len(frame_array)):
    out.write(frame_array[i])
out.release()