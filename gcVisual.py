from tkinter import *
import math
import os

class MainWindow:

    def __init__(self, main):
        # canvas for image
        self.canvas = Canvas(main, width=1100, height=390)
        self.canvas.grid(row=0, column=0)
        main.title("Monitoring")
        main.resizable(0, 0)

        # images
        self.my_images = []
        files = ['a0','a1', #0~1
                 'b0','b1','b2', #2~4
                 'c0','cn','cnnw','cnw','cnww','cw','csww','csw','cssw','cs','csse','cse','csee','ce','cnee','cne','cnne', #5~21
                 'd0','da','db','dx','dy', #22~26
                 'e0','eu','ed','el','er', #27~31
                 'f0','fn','fnnw','fnw','fnww','fw','fsww','fsw','fssw','fs','fsse','fse','fsee','fe','fnee','fne','fnne'] #32~48
        # each represent part of picture, it will be added and printed

        image_path = os.getcwd() # paste photo directory
        
        for i in files:
            try:
                self.my_images.append(PhotoImage(file=os.path.join(image_path, i + ".png")))
            except TclError as e:
                print(f"Error loading image {i}.png: {e}")

        self.autoChange([0, 2, 5, 22, 27, 32], [0, 2, 5, 22, 27, 32])

    def apply(self, A, B, X, Y, Z, digital_L, digital_R, main_x, main_y, c_stick_x, c_stick_y, L, R):
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
            convertedList.append(self.findAngle(main_x, main_y) + 5)
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
            convertedList.append(self.findAngle(c_stick_x, c_stick_y) + 32)
        else:
            if c_stick_x == 0 and c_stick_y == 0:
                convertedList.append(32)
            elif c_stick_x == 0:
                convertedList.append(33 if c_stick_y > 0 else 41)
            elif c_stick_y == 0:
                convertedList.append(45 if c_stick_x > 0 else 37)

        return convertedList

    def autoChange(self, buttonList1,buttonList2):  
        self.canvas.delete("all") 
        self.canvas.create_image(0, 0, anchor='nw', image=self.my_images[buttonList1[0]])  # left upside pic
        self.canvas.create_image(275, 0, anchor='nw', image=self.my_images[buttonList1[1]])  # right upside pic
        self.canvas.create_image(0, 60, anchor='nw', image=self.my_images[buttonList1[2]])  # left middle pic
        self.canvas.create_image(275, 60, anchor='nw', image=self.my_images[buttonList1[3]])  # right middle pic
        self.canvas.create_image(0, 195, anchor='nw', image=self.my_images[buttonList1[4]])  # left bottom pic
        self.canvas.create_image(275, 195, anchor='nw', image=self.my_images[buttonList1[5]])  # right bottom pic

        self.canvas.create_image(550, 0, anchor='nw', image=self.my_images[buttonList2[0]])  # left upside pic
        self.canvas.create_image(825, 0, anchor='nw', image=self.my_images[buttonList2[1]])  # right upside pic
        self.canvas.create_image(550, 60, anchor='nw', image=self.my_images[buttonList2[2]])  # left middle pic
        self.canvas.create_image(825, 60, anchor='nw', image=self.my_images[buttonList2[3]])  # right middle pic
        self.canvas.create_image(550, 195, anchor='nw', image=self.my_images[buttonList2[4]])  # left bottom pic
        self.canvas.create_image(825, 195, anchor='nw', image=self.my_images[buttonList2[5]])  # right bottom pic

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

def update_states(app, states1,states2, index=0): 
    if index < len(states1) and index < len(states2):
        state1 = states1[index]
        state2 = states2[index]
        temp1= app.apply(*state1)
        temp2= app.apply(*state2)
        app.autoChange(temp1,temp2)
        root.after(41, update_states, app, states1,states2, index + 1) #1000/24 ~= 41
    else:
        print("All states processed")


#stateList1 = action_history[0]
#stateList2 = action_history[1]
import pickle
file_path = "C:/Users/LEE/Downloads/action_history_09_13_102319.pkl"

with open(file_path, 'rb') as f:
    data = pickle.load(f)
stateList1,stateList2=data.get(0),data.get(1)

app = start_gui()
update_states(app, stateList1, stateList2)
root.mainloop()


# input order: [A, B, X, Y, Z, digital L, digital R, main x, main y, c stick x, c stick y, L, R]
# range of state: idx 0~6: bool, 7~10: -1~1 float, 11~12: 0~1 float