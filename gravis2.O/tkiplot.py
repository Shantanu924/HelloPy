import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, filedialog, Label, Button, StringVar, OptionMenu

def load_data(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    else:
        raise TypeError('Unsupported file type')

def plot(data, x_col, y_col, plot_type):
    try:
        if plot_type == "Line Chart":
            plt.plot(data[x_col], data[y_col], marker='o')
        elif plot_type == "Bar Chart":
            plt.bar(data[x_col], data[y_col])
        elif plot_type == "Scatter Plot":
            plt.scatter(data[x_col], data[y_col])
        elif plot_type == "Bubble Chart":
            plt.scatter(data[x_col], data[y_col], s=data[y_col] * 10, alpha=0.5)
        elif plot_type == "Histogram":
            plt.hist(data[x_col], bins=20, alpha=0.7, label=x_col)
            plt.hist(data[y_col], bins=20, alpha=0.7, label=y_col)
            plt.legend()
        
        elif plot_type == "Heatmap":
            sns.heatmap(data.corr(), annot=True, cmap="coolwarm")
        else:
            raise ValueError("Unsupported plot type")

        plt.title(f'{plot_type}: {y_col} vs {x_col}')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.grid(True)
        plt.show()
    except Exception as e:
        error_var.set(f"Error: {e}")


def file_select():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx;*.xls")])
    file_path_var.set(file_path)

    if file_path:
        try:
            global data
            data = load_data(file_path)
            columns = data.columns.tolist()
            x_column_var.set(columns[0])
            y_column_var.set(columns[1])
            x_menu['menu'].delete(0, 'end')
            y_menu['menu'].delete(0, 'end')
            for col in columns:
                x_menu['menu'].add_command(label=col, command=lambda c=col: x_column_var.set(c))
                y_menu['menu'].add_command(label=col, command=lambda c=col: y_column_var.set(c))
        except Exception as e:
            error_var.set(f"Error: {e}")


def graph():
    try:
        x_col = x_column_var.get()
        y_col = y_column_var.get()
        plot_type = plot_type_var.get()

        if plot_type in ["Pie Chart", "Heatmap"] and not x_col:
            plot(data, None, y_col, plot_type)
        elif x_col and y_col:
            plot(data, x_col, y_col, plot_type)
        else:
            error_var.set("Select valid columns for both axes.")
    except Exception as e:
        error_var.set(f"Error: {e}")

mtp = Tk()
mtp.title('Data Plot')

file_path_var = StringVar()
x_column_var = StringVar()
y_column_var = StringVar()
plot_type_var = StringVar(value="Line Chart")  # Default plot type
error_var = StringVar()
data = None

Label(mtp, text="File:").grid(row=0, column=0, padx=5, pady=5)
Label(mtp, textvariable=file_path_var, width=40, anchor='w').grid(row=0, column=1, padx=5, pady=5)
Button(mtp, text="Browse", command=file_select).grid(row=0, column=2, padx=5, pady=5)

Label(mtp, text="X-Axis:").grid(row=1, column=0, padx=5, pady=5)
x_menu = OptionMenu(mtp, x_column_var, [])
x_menu.grid(row=1, column=1, padx=5, pady=5)

Label(mtp, text="Y-Axis:").grid(row=2, column=0, padx=5, pady=5)
y_menu = OptionMenu(mtp, y_column_var, [])
y_menu.grid(row=2, column=1, padx=5, pady=5)

Label(mtp, text="Plot Type:").grid(row=3, column=0, padx=5, pady=5)
plot_types = ["Line Chart", "Bar Chart", "Scatter Plot", "Bubble Chart", "Histogram", "Pie Chart", "Heatmap"]
plot_type_menu = OptionMenu(mtp, plot_type_var, *plot_types)
plot_type_menu.grid(row=3, column=1, padx=5, pady=5)

Button(mtp, text="Plot", command=graph).grid(row=4, column=1, pady=10)

Label(mtp, textvariable=error_var, fg="red").grid(row=5, column=0, columnspan=3, pady=5)

# Label(mtp, text='plot',command=graph)
mtp.mainloop()
# x_name=[]
# y_name=[]

# n = int(input("No. of values to implement: "))

# for i in range(n):
#     x_name.append(input("x values: "))
#     y_name.append(input("y values: "))

# def manual_plot(x,y):
#     plt.title(f'{x_name} vs {y_name}')
#     plt.xlabel(f'{x_name}')
#     plt.ylabel(f'{y_name}')
#     plt.plot(x_name, y_name)
#     plt.show()