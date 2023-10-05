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
bg_color = "#31345e"
win.configure(bg=bg_color)
seasons_path = "ColorSeasonsHSV.csv"
curr_image = ""
max_image_dim = 500
right_panel_x = 550
right_panel_y_padding = 100
left_panel_x = 20
left_panel_y = 50
button_scale = 10

@dataclass
class ImageInfo:
    name: str
    image: cv2.typing.MatLike
    width: int
    height: int


color_list = {}

class Control():
    def __init__(self):
        self.screen = Label(win)
        self.btn = Button(win,text="Select New Image",command=self.change_image)
        self.btn.place(x=max_image_dim+150, y=max_image_dim+30)
        self.season_label = Label(win, bg=bg_color)
        self.season_label.place(x=right_panel_x, y=right_panel_y_padding,width=150,height=200)
        self.mouse_pos = Label(win,bg=bg_color,fg="white")
        self.mouse_pos.place(x=right_panel_x, y=right_panel_y_padding+220)
        self.hex_label = Label(win, bg=bg_color, fg="white", text="Click on image for hex")
        self.hex_label.place(x=right_panel_x, y=right_panel_y_padding+240)
        self.choose_file()
        self.display()
        self.populate_color_list()

    def display_image(self):
        image = Image.fromarray(curr_image.image)
        print(f"New file: {curr_image.name}")
        pic = ImageTk.PhotoImage(image)
        self.screen.configure(image=pic)
        self.screen.image = pic
        image_x = (max_image_dim - curr_image.width) // 2 + left_panel_x
        image_y = (max_image_dim - curr_image.height) // 2 + left_panel_y
        self.screen.place(x=image_x, y=image_y)
        

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
        height, width = cv2_image.shape[:2]
        aspect_ratio = width / height
        new_width = int(min(max_image_dim, max_image_dim * aspect_ratio))
        new_height = int(min(max_image_dim, max_image_dim / aspect_ratio))
        rgb_image = cv2.resize(rgb_image, (new_width, new_height))
        curr_image = ImageInfo(curr_image_path, rgb_image, new_width, new_height)

    def rgb2hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def find_closest_seasons(self, target_color):
        min_delta = 1000000
        closest_colors = []
        threshold = 50
        for name, colors in color_list.items():
            for color in colors:
                labColor = color_conversions.convert_color(color, LabColor)
                delta_e = delta_e_cmc(target_color, labColor)
                if abs(min_delta - delta_e) <= threshold and name not in closest_colors:
                    closest_colors.append(name)
                    if delta_e < min_delta:
                      min_delta = delta_e
                elif delta_e < min_delta:
                    min_delta = delta_e
                    closest_colors = [name]
        return closest_colors

    def analyze_color(self, x, y):
        img = curr_image.image
        color = img[y, x, :]
        r, g, b = color
        rgbColor = sRGBColor(r, g, b)
        labColor = color_conversions.convert_color(rgbColor, LabColor)
        closest_color = self.find_closest_seasons(labColor)
        print(f"Closest Season(s): {closest_color}")

        rgb = self.rgb2hex((r, g, b))
        self.hex_label.configure(text=rgb)
        self.season_label['bg'] = rgb
        self.season_label['fg'] = self.choose_text_color(r, g, b)
        self.season_label.configure(text='\n'.join(closest_color), wraplength=100)

    def calculate_luminance(self, r, g, b):
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
        return luminance

    def choose_text_color(self, r, g, b):
        background_luminance = self.calculate_luminance(r, g, b)

        if background_luminance < 0.5:
            return "white"
        else:
            return "black"
        
    def change_image(self):
        self.choose_file()
        self.display()

    def display(self):
        self.display_image()
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