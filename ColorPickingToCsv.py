import os
import cv2
from tkinter import *
from PIL import ImageTk, Image
from colormath import color_conversions
from colormath.color_objects import HSVColor, sRGBColor, LabColor
from dataclasses import dataclass
import csv

win = Tk()
win.geometry("800x600+400+200")
bg_color = "#708f93"
win.configure(bg=bg_color)
path = "/Users/Alvina/Documents/SeasonPics"
rgb_csv_path = "/Users/Alvina/Documents/ColorSeasonsRGB.csv"
hsv_csv_path = "/Users/Alvina/Documents/ColorSeasonsHSV.csv"
hex_csv_path = "/Users/Alvina/Documents/ColorSeasonsHex.csv"

@dataclass
class ImageInfo:
    name: str
    image: cv2.typing.MatLike


images = os.listdir(path)
all_images = []
rgb_values = []
hsv_values = []
hex_values = []

rgb_file = open(rgb_csv_path, 'w')
hsv_file = open(hsv_csv_path, 'w')
hex_file = open(hex_csv_path, 'w')
rgb_writer = csv.writer(rgb_file)
hsv_writer = csv.writer(hsv_file)
hex_writer = csv.writer(hex_file)

for image_name in images:
    if image_name == ".DS_Store":
      continue
    # TODO: add check for file type == image
    img_path = cv2.imread(f"{path}/{image_name}")
    rgb_image = cv2.cvtColor(img_path, cv2.COLOR_BGR2RGB)
    rgb_image = cv2.resize(rgb_image, (500, 500))
    all_images.append(ImageInfo(image_name, rgb_image))

curr_image_name = all_images[0].name

class Control():
    def __init__(self):
        self.screen = Label(win)
        self.mouse_pos = Label(win,bg=bg_color,fg="white")
        self.mouse_pos.place(x=600, y=180)
        self.color_label = Label(win)
        self.color_label.place(x=600, y=50,width=150,height=100)
        self.input = Entry(win)
        self.input.place(x=600, y=250 , width=150)
        self.input2 = Entry(win)
        self.input2.place(x=600, y=350, width=150)
        self.btn = Button(win,text="Change image",command=self.change_img_color)
        self.btn.place(x=600, y=450)
        self.counter = 0
        self.display()
        
    def to_pil(self, img_info):
        global curr_image_name
        image = Image.fromarray(img_info.image)
        print(f"New file: {img_info.name}")
        if len(rgb_values) > 0:
            rgb_values.insert(0, curr_image_name)
            hsv_values.insert(0, curr_image_name)
            hex_values.insert(0, curr_image_name)
            rgb_writer.writerow(rgb_values)
            hsv_writer.writerow(hsv_values)
            hex_writer.writerow(hex_values)
        curr_image_name = img_info.name
        rgb_values.clear()
        hsv_values.clear()
        hex_values.clear()
        pic = ImageTk.PhotoImage(image)
        self.screen.configure(image=pic)
        self.screen.image = pic
        self.screen.place(x=20, y=50)

    def move_mouse(self, event):
        x = event.x
        y = event.y
        self.mouse_pos.configure(text=f"x= {x}  y= {y}")
        img = all_images[self.counter]
        self.screen.bind('<Button-1>', lambda e: self.capture_color(img, x, y))

    def rgb2hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def capture_color(self, img_info, x, y):
        hints = StringVar()
        hints2 = StringVar()
        img = img_info.image
        color = img[y, x, :]
        r, g, b = color
        rgbColor = sRGBColor(r, g, b)
        hsvColor = color_conversions.convert_color(rgbColor, HSVColor)
        rgb_values.append(str(rgbColor.get_value_tuple()))
        hsv_values.append(str(hsvColor.get_value_tuple()))


        rgb_hex = self.rgb2hex((r, g, b))
        hex_values.append(rgb_hex)
        hints.set(rgb_hex)
        self.input['textvariable'] = hints
        hints2.set(f"{b},{g},{r}")#for opencv and rgb for the rest of use
        self.input2['textvariable'] = hints2
        self.color_label['bg'] = rgb_hex

    def change_img_color(self):
        self.counter +=1
        if self.counter >= len(all_images):
            self.counter = 0
        self.display()

    def display(self):
        print(self.counter)
        self.to_pil(all_images[self.counter])
        self.screen.bind('<Motion>', self.move_mouse)

if __name__ == '__main__':
    Control()
    win.mainloop()

cv2.destroyAllWindows()
rgb_file.close()
hsv_file.close()
hex_file.close()
