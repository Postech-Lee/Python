from tkinter import *
import math
import os

class MainWindow:

    def __init__(self, main):
        # canvas for image
        self.canvas = Canvas(main, width=550, height=390)
        self.canvas.grid(row=0, column=0)
        main.title("Monitoring")
        main.resizable(0, 0)

        # images
        self.my_images = []
        files = ['a0','a1', #0~1
                 'b0','b1', #2~3
                 'c0','cn','cnnw','cnw','cnww','cw','csww','csw','cssw','cs','csse','cse','csee','ce','cnee','cne','cnne', #4~20
                 'd0','da','db','dx','dy', #21~25
                 'e0','eu','ed','el','er', #26~30
                 'f0','fn','fnnw','fnw','fnww','fw','fsww','fsw','fssw','fs','fsse','fse','fsee','fe','fnee','fne','fnne'] #31~47
        # each represent part of picture, it will be added and printed

        image_path = os.getcwd() # paste photo directory
        
        for i in files:
            try:
                self.my_images.append(PhotoImage(file=os.path.join(image_path, i + ".png")))
            except TclError as e:
                print(f"Error loading image {i}.png: {e}")

        self.autoChange([0, 2, 4, 21, 26, 31])

    def apply(self, A, B, X, Y, Z, digital_L, digital_R, main_x, main_y, c_stick_x, c_stick_y, L, R):
        convertedList = []

        
        if digital_L == 0:
            convertedList.append(0)  #a0
        else:
            convertedList.append(1) # a1, analog값 출력 코드 필요
        
        if digital_R == 0:
            convertedList.append(2)  #b0
        else:
            convertedList.append(3) # b1, analog값 출력 코드 필요

        #Z키 누락됨 ==> 이미지 추가 후 코드 추가필요

        # Handling main stick (x, y)
        if main_x != 0 or main_y != 0:
            convertedList.append(self.findAngle(main_x, main_y) + 4)
        else:
            if main_x == 0:
                convertedList.append(5 if main_y > 0 else 13)
            elif main_y == 0:
                convertedList.append(17 if main_x > 0 else 9)
            else:
                convertedList.append(4)
        if A :
            convertedList.append(22)
        elif B :
            convertedList.append(23)
        elif X :
            convertedList.append(24)
        elif Y :
            convertedList.append(25)
        else:
            convertedList.append(21)
        
        
        convertedList.append(26) # dpad signal is none => set default

        # Handling C stick (x, y)
        if c_stick_x != 0 or c_stick_y != 0:
            convertedList.append(self.findAngle(c_stick_x, c_stick_y) + 31)
        else:
            if c_stick_x == 0:
                convertedList.append(32 if c_stick_y > 0 else 40)
            elif c_stick_y == 0:
                convertedList.append(44 if c_stick_x > 0 else 36)
            else:
                convertedList.append(31)

        self.autoChange(convertedList)

    def autoChange(self, imgList):
        self.setImage(imgList)

    def setImage(self, buttonList):  
        self.canvas.delete("all") 
        self.canvas.create_image(0, 0, anchor='nw', image=self.my_images[buttonList[0]])  # left upside pic
        self.canvas.create_image(275, 0, anchor='nw', image=self.my_images[buttonList[1]])  # right upside pic
        self.canvas.create_image(0, 60, anchor='nw', image=self.my_images[buttonList[2]])  # left middle pic
        self.canvas.create_image(275, 60, anchor='nw', image=self.my_images[buttonList[3]])  # right middle pic
        self.canvas.create_image(0, 195, anchor='nw', image=self.my_images[buttonList[4]])  # left bottom pic
        self.canvas.create_image(275, 195, anchor='nw', image=self.my_images[buttonList[5]])  # right bottom pic

    def findAngle(self, x, y):
        angle = math.degrees(math.atan2(y, x))
        if angle < 0:
            angle += 360
        ccw = 360 - angle
        region = int(ccw // 22.5)
        return region

def start_gui():
    global root
    root = Tk()
    app = MainWindow(root)
    return app

def update_states(app, states, index=0): 
    if index < len(states):
        state = states[index]
        app.apply(*state)
        root.after(16, update_states, app, states, index + 1)
    else:
        print("All states processed")

# input order: [A, B, X, Y, Z, digital L, digital R, main x, main y, c stick x, c stick y, L, R]
# range of state: idx 0~6: bool, 7~10: -1~1 float, 11~12: 0~1 float