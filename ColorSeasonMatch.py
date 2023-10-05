import os
import cv2
from tkinter import *
from PIL import ImageTk, Image
from colormath import color_conversions
from colormath.color_objects import HSVColor, sRGBColor, LabColor
from colormath.color_diff import delta_e_cmc
from dataclasses import dataclass
import csv
from tkinter import filedialog

win = Tk()
win.geometry("800x600+400+200")
bg_color = "#708f93"
win.configure(bg=bg_color)
seasons_path = "ColorSeasonsHSV.csv"
curr_image = ""

@dataclass
class ImageInfo:
    name: str
    image: cv2.typing.MatLike


color_list = {}

class Control():
    def __init__(self):
        self.screen = Label(win)
        self.mouse_pos = Label(win,bg=bg_color,fg="white")
        self.mouse_pos.place(x=600, y=280)
        self.color_label = Label(win)
        self.color_label.place(x=600, y=50,width=150,height=200)
        self.input = Entry(win)
        self.input.place(x=600, y=350 , width=150)
        # self.input2 = Entry(win)
        # self.input2.place(x=600, y=350, width=150, height=70)
        # self.color_label = Label(win,bg=bg_color,fg="white")
        # self.color_label.place(x=600, y=350)
        self.btn = Button(win,text="Select Image",command=self.change_image)
        self.btn.place(x=600, y=450)
        self.choose_file()
        self.display()
        self.populate_color_list()

    def to_pil(self):
        image = Image.fromarray(curr_image.image)
        print(f"New file: {curr_image.name}")
        pic = ImageTk.PhotoImage(image)
        self.screen.configure(image=pic)
        self.screen.image = pic
        self.screen.place(x=20, y=50)

    def move_mouse(self, event):
        x = event.x
        y = event.y
        self.mouse_pos.configure(text=f"x= {x}  y= {y}")
        self.screen.bind('<Button-1>', lambda e: self.analyze_color(x, y))
    
    def choose_file(self):
        global curr_image
        curr_image_path = filedialog.askopenfilename()
        cv2_image = cv2.imread(f"{curr_image_path}")
        rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        rgb_image = cv2.resize(rgb_image, (500, 500))
        curr_image = ImageInfo(curr_image_path, rgb_image)

    def rgb2hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def find_closest_seasons(self, target_color):
        min_delta = 1000000
        closest_colors = []
        threshold = 25
        for name, colors in color_list.items():
            for color in colors:
                labColor = color_conversions.convert_color(color, LabColor)
                delta_e = delta_e_cmc(target_color, labColor)
                # print(f"Difference for {name} {color}: {delta_e}")
                # print(f"checking thDereshold: {abs(min_delta - delta_e)}")
                if abs(min_delta - delta_e) <= threshold:
                    # print("here")
                    closest_colors.append(name)
                    if delta_e < min_delta:
                      min_delta = delta_e
                elif delta_e < min_delta:
                    min_delta = delta_e
                    closest_colors = [name]
        return closest_colors

    def analyze_color(self, x, y):
        hints = StringVar()
        # hints2 = StringVar()
        img = curr_image.image
        color = img[y, x, :]
        r, g, b = color
        rgbColor = sRGBColor(r, g, b)
        labColor = color_conversions.convert_color(rgbColor, LabColor)
        closest_color = self.find_closest_seasons(labColor)
        print(f"Closest Season(s): {closest_color}")

        rgb = self.rgb2hex((r, g, b))
        hints.set(rgb)
        self.input['textvariable'] = hints
        # hints2.set(f"{b},{g},{r}")
        # self.input2['textvariable'] = hints2
        self.color_label['bg'] = rgb
        self.color_label.configure(text='\n'.join(closest_color), wraplength=100)
        
        # print(r, g, b, 'hex= ', rgb)

    def change_image(self):
        self.choose_file()
        self.display()

    def display(self):
        self.to_pil()
        self.screen.bind('<Motion>', self.move_mouse)
    
    def populate_color_list(self):
        with open(seasons_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 2: # should have name and >= 1 val
                    continue
                color_list[row[0]] = self.convert_to_hsv(row[1:])

    def convert_to_hsv(self, colors):
        hsv_colors = []
        for color_str in colors:
            h, s, v = map(float, color_str.strip('()').split(','))
            hsv_colors.append(HSVColor(h, s, v))
        return hsv_colors
                

if __name__ == '__main__':
    Control()
    win.mainloop()

cv2.destroyAllWindows()