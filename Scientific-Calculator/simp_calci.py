import tkinter as tk
from math import *
class SimCalci:
    def __init__(self,master):
        self.master = master
        master.title("Simple Calculator")

        self.entry = tk.Entry(master, width=30, borderwidth=5, font=("Monospace",16))
        self.entry.grid(row=0, column=0,columnspan=5,padx=10,pady=10)

        self.create_buttons()
    
    def create_buttons(self):
        buttons =[
            '7','8','9','/','C',
            '4','5','6','*','sqrt',
            '1','2','3','-','^',
            '0','.','=','+','log',
            'sin','cos','tan','(',')',
            'pi','e','DEL',','
        ]
        row=1
        col=0
        for button in buttons:
            if button != '':
                tk.Button(self.master, text=button, width=5,height=2,font=("Monospace",14),command=lambda b=button:self.on_button_click(b)).grid(row=row,column=col)
            col+=1
            if col>4:
                col=0
                row+=1
    
    def on_button_click(self,button):
        current = self.entry.get()
        if button == "C":
            self.entry.delete(0,tk.END)
        elif button == "DEL":
            self.entry.delete(len(current)-1,tk.END)
        elif button == "=":
            try:
                result = eval(current.replace("^","**").replace("sqrt","sqrt"))
                self.entry.delete(0,tk.END)
                self.entry.insert(0,result)
            except Exception as e:
                self.entry.delete(0,tk.END)
                self.entry.insert(0,"Error")
        elif button in ['sin','cos','tan','log','sqrt']:
            self.entry.insert(tk.END, f"{button}(")
        elif button in ['pi','e']:
            self.entry.insert(tk.END,str(eval(button)))
        else:
            self.entry.insert(tk.END,button)

if __name__ == "__main__":
    root = tk.Tk()
    calci = SimCalci(root)
    root.mainloop()