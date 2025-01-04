import torch
import torchvision.transforms as trans
from tkinter import Tk,Button,Label,Canvas,filedialog,Scale,HORIZONTAL
from PIL import Image, ImageTk

app = Tk()
app.title("Image Blender")
app.geometry("800x600")

img1 = None
img2 = None
blended_img = None
canvas = None

transform = trans.Compose([trans.ToTensor(),trans.Resize((500,500)),])
to_pil = trans.ToPILImage()

def load_img1():
    global img1
    file_path = filedialog.askopenfilename(filetypes = [("Image files","*.jpg;*.png;*.jpeg")])
    if file_path:
        img1 = Image.open(file_path)
        update_canvas()

def load_img2():
    global img2
    file_path = filedialog.askopenfilename(filetypes = [("Image files","*.jpg;*.png;*.jpeg")])
    if file_path:
        img2 = Image.open(file_path)
        update_canvas()

def blend_images(alpha_value):
    global blended_img
    if img1 and img2:
        img1_tensor = transform(img1)
        img2_tensor = transform(img2)
        alpha = float(alpha_value)
        blended_tensor = alpha * img1_tensor + (1 - alpha) * img2_tensor
        blended_img = to_pil(blended_tensor)
        update_canvas()

def update_canvas():
    global canvas
    if canvas:
        canvas.delete("all")
    if img1:
        img1_resized = img1.resize((250,250))
        img1_tk = ImageTk.PhotoImage(img1_resized)
        canvas.create_image(150,150,image=img1_tk,anchor="center")
        canvas.img1 = img1_tk
    if img2:
        img2_resized = img2.resize((250,250))
        img2_tk = ImageTk.PhotoImage(img2_resized)
        canvas.create_image(450,150,image=img2_tk,anchor="center")
        canvas.img2 = img2_tk
    if blended_img:
        blended_tk = ImageTk.PhotoImage(blended_img.resize((500,500)))
        canvas.create_image(300,450,image = blended_tk, anchor = "center")
        canvas.blend_image = blended_tk

Label(app, text="Image Blender", font=("Monospace", 16)).pack(pady=10)

Button(app,text = "Load Image", command = load_img1).pack(pady=5)
Button(app,text = "Load Image 2", command = load_img2).pack(pady=5)

Label(app, text = "Blend alpha").pack(pady=5)
blend_slider = Scale(app,from_=0.0, to=1.0, resolution = 0.01, orient=HORIZONTAL, command=blend_images)
blend_slider.set(0.5)
blend_slider.pack(pady=5)

canvas = Canvas(app, width=600, height=600, bg="white")
canvas.pack(pady=10)

app.mainloop()