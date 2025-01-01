import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import Image,ImageDraw, ImageTk
 
class PaintApp:
    def __init__(self,root):
        self.root = root
        self.root.title("Paint App")
        self.root.geometry("1000x800")

        self.canvas = tk.Canvas(root, bg='white', width=800, height=600)
        self.canvas.pack(pady=20)

        self.pen_color ='black'
        self.fill_color =None
        self.pen_width = 5
        self.active_tool = "brush"

        self.last_x =None
        self.last_y = None

        self.image = Image.new("RGB",(800,500),"white")
        self.draw = ImageDraw.Draw(self.image)

        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack()

        self.color_button = tk.Button(self.controls_frame,text='choose color',command=self.choose_color)
        self.color_button.pack(side='left',padx=5)

        self.fill_color_button = tk.Button(self.controls_frame,text='fill color',command=self.choose_fill_color)
        self.fill_color_button.pack(side='left',padx=5)

        self.clear_button = tk.Button(self.controls_frame,text='clear',command=self.clear_canvas)
        self.clear_button.pack(side='left',padx=5)

        self.save_button = tk.Button(self.controls_frame,text='save',command=self.save_image)
        self.save_button.pack(side='left',padx=5)

        self.pen_size_slider = tk.Scale(self.controls_frame, from_=1,to=20,orient='horizontal',label='pen size')
        self.pen_size_slider.set(self.pen_width)
        self.pen_size_slider.pack(side='left',padx=10)

        self.tool_menu = tk.OptionMenu(self.controls_frame, tk.StringVar(value=self.active_tool), "brush","line","rectangle","oval","eraser", command=self.set_tool,)
        self.tool_menu.pack(side='left',padx=5)

        self.canvas.bind("<ButtonPress-1>",self.on_button_press)
        self.canvas.bind("<B1-Motion>",self.on_drag)
        self.canvas.bind("<ButtonRelease-1>",self.on_button_release)

        self.current_shape = None

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.pen_color = color

    def choose_fill_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.fill_color = color
    
    def set_tool(self, tool):
        self.active_tool = tool
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB",(800,500),"white")
        self.draw = ImageDraw.Draw(self.image)
    
    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG Files","*.png"),("All Files","*.*")],)
        if file_path:
            self.image.save(file_path)

    def on_button_press(self, event):
        self.last_x, self.last_y = event.x, event.y
        if self.active_tool in {"rectangle","oval"}:
            self.current_shape = self.canvas.create_rectangle(
                event.x, 
                event.y,
                event.x, 
                event.y, 
                outline=self.pen_color, 
                fill=self.fill_color if self.fill_color else "",
                width=self.pen_size_slider.get(),) if self.active_tool == "rectangle" else self.canvas.create_oval(
                    event.x,
                    event.y,
                    event.x,
                    event.y,
                    outline=self.pen_color, 
                    fill=self.fill_color if self.fill_color else "",
                    width=self.pen_size_slider.get(),
                )

    def on_drag(self, event):
        if self.active_tool == "brush":
            self.canvas.create_line(
                self.last_x,
                self.last_y,
                event.x,
                event.y,
                fill = self.pen_color,
                width = self.pen_size_slider.get(),
                capstyle = tk.ROUND,
                smooth = True
            )
            self.draw.line(
                [self.last__x,self.last__y,event.x,event.y],
                fill = self.pen_color,
                width = self.pen_size_slider.get(),
            )
            self.last_x,self.last_y = event.x,event.y

        elif self.active_tool == "eraser":
            self.canvas.create_line(
                self.last_x,
                self.last_y,
                event.x,
                event.y,
                fill = "white",
                width = self.pen_size_slider.get(),
                capstyle = tk.ROUND,
                smooth = True,
            )
            self.draw.line(
                [self.last_x, self.last_y, event.x, event.y],
                fill = "white",
                width = self.pen_size_slider.get(),
            )
            self.last_x, self.last_y = event.x, event.y
        
        elif self.active_tool in {"rectangle","oval"} and self.current_shape:
            x0, y0 = self.last_x, self.last_y
            x1, y1 = event.x, event.y
            if self.active_tool == "rectangle":
                self.canvas.coords(self.current_shape,x0,y0,x1,y1)
            elif self.active_tool == "oval":
                self.canvas.coords(self.current_shape,x0,y0,x1,y1)

    
    def on_button_release(self, event):
        if self.active_tool in {"rectangle","oval"}:
            x0,y0 = self.last_x,self.last_y
            x1,y1 = event.x,event.y
            if self.active_tool == "rectangle":
                self.draw.rectangle(
                    [x0,y0,x1,y1],
                    outline=self.pen_color,
                    fill=self.fill_color if self.fill_color else None,
                    width=self.pen_size_slider.get(),
                )
            elif self.active_tool == "oval":
                self.draw.ellipse(
                    [x0,y0,x1,y1],
                    outline=self.pen_color,
                    fill=self.fill_color if self.fill_color else None,
                    width=self.pen_size_slider.get(),
                )
            self.current_shape = None
        self.last_x, self.last_y = None, None

if __name__ == '__main__':
    root =tk.Tk()
    app = PaintApp(root)
    root.mainloop()