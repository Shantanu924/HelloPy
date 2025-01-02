import tkinter as tk
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from math import *
import cmath

class SciCalci:
    def __init__(self,master):
        self.master = master
        master.title("Scientific Calculator")

        self.entry = tk.Entry(master,  width=40, borderwidth=5, font=("Monospace",16))
        self.entry.grid(row=0, column=0, columnspan=5,padx=10,pady=10)

        self.create_buttons()
    
    def create_buttons(self):
        buttons = [
            '7','8','9','/','C',
            '4','5','6','*','DEL',
            '1','2','3','-','(',
            '0','.','=','+',')',
            'sin','cos','tan','log','^',
            '√','∑','∫','diff','solve',
            'matrix','complex','|z|','arg(z)','pi',
            'e','DET','INV','CLEAR',''
        ]

        row=1
        col=0
        for button in buttons:
            if button !='':
                tk.Button(self.master, text=button,width=8,height=2,font=("Monospace",12), command=lambda b=button:self.on_button_click(b)).grid(row=row,column=col)
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
            self.calculate(current)
        elif button in ['sin','cos','tan','log','diff','∫','∑','solve','matrix','complex','|z|','arg(z)','DET','INV']:
            self.entry.insert(tk.END,f"{button}(")
        elif button in ['pi','e']:
            self.entry.insert(tk.END,str(eval(button)))
        else:
            self.entry.insert(tk.END,button)
    
    def calculate(self, expression):
        try:
            if 'sin' in expression or 'cos' in expression or 'tan' in expression:
                expression = expression.replace('sin','cmath.sin').replace('cos','cmath.cos').replace('tan','cmath.tan')
            if 'log' in expression:
                expression = expression.replace('log','cmath.log')

            if 'diff' in expression:
                result = self.differentiate(expression)
            elif '∫' in expression:
                result = self.integrate(expression)
            elif '∑' in expression:
                result = self.summation(expression)
            elif 'solve' in expression:
                result = self.solve_equation(expression)
            elif 'matrix' in expression:
                result = self.matrix_operations(expression)
            elif 'complex' in expression:
                result = self.complex_operations(expression)
            elif '|z|' in expression or 'arg(z)' in expression:
                result = self.angular_operations(expression)
            elif 'DET' in expression or 'INV' in expression:
                result = self.matrix_operations(expression)
            else:
                result = eval(expression)
            self.entry.delete(0,tk.END)
            self.entry.insert(0,result)
        
        except Exception as e:
            self.entry.delete(0,tk.END)
            self.entry.insert(0,'Error')
    
    def differentiate(self, expression):
        var = symbols("x")
        func = parse_expr(expression.split("diff(")[1].strip(")"))
        return diff(func, var)
    
    def integrate(self, expression):
        var = symbols("x")
        func = parse_expr(expression.split("∫(")[1].strip(")"))
        return integrate(func, var)
    
    def summation(self, expression):
        var,n = symbols("x n")
        func = parse_expr(expression.split("∑(")[1].strip(")"))
        return summation(func,(var,1,n))
    
    def solve_equation(self, expression):
        var = symbols("x")
        eq = parse_expr(expression.split("solve(")[1].strip(")"))
        return solve(eq, var)
    
    def matrix_operations(self, expression):
        try:
            matrices = eval(expression.split("matrix(")[1].strip(")"))
            mat = Matrix(matrices)
            determinant = mat.det()
            inverse = mat.inv() if mat.det() != 0 else "Not Invertible"
            return f"Det: {determinant} , Inv: {inverse}"
        except Exception as e:
            return "Error"
        
    def complex_operations(self, expression):
        try:
            z = complex(expression.split("complex(")[1].strip(")"))
            return z
        except Exception as e:
            return "Error"
    
    def angular_operations(self, expression):
        try:
            z = complex(expression.split("z(")[1].strip(")"))
            if "|z|" in expression:
                return abs(z)
            elif "arg(z)" in expression:
                return cmath.phase(z)
        except Exception as e:
            return "Error "

if __name__ == "__main__":
    root = tk.Tk()
    calci = SciCalci(root)
    root.mainloop()