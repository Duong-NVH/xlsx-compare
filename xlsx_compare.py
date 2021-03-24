import pandas as pd
import numpy as np
from tkinter import *
from tkinter import filedialog

filepath1=""
filepath1=""
window = Tk()
def openFile1():
    global filepath1
    filepath1 = filedialog.askopenfilename(initialdir="./",title="Open file?")
    print(f"Loaded file 1 from {filepath1}")

def openFile2():
    global filepath2
    filepath2 = filedialog.askopenfilename(initialdir="./", title="Open file?")
    print(f"Loaded file 2 from {filepath2}")

def compare():
    print("Comparing...")
    try:
        df1=pd.read_excel(filepath1)
        df2=pd.read_excel(filepath2)

        df1.equals(df2)
        comparison_values = df1.values == df2.values
        rows,cols=np.where(comparison_values==False)
        for item in zip(rows,cols):
            df1.iloc[item[0], item[1]] = '{} --> {}'.format(df1.iloc[item[0], item[1]],df2.iloc[item[0], item[1]])

        def color_diff_red(val):
            bgcolor = 'red' if ">" in str(val) else 'none'
            return f'background-color: {bgcolor}'
        final=df1.style.applymap(color_diff_red)

        savefile = filedialog.asksaveasfilename(filetypes=(("Excel files", "*.xlsx"),("All files", "*.*") ))               
        
        final.to_excel(savefile + ".xlsx", index=False, sheet_name="Results")         
        print("Done!")
    except:
        print("An exception occurred")


button1 = Button(window,text="Select File 1",command=openFile1)
button1.pack()
button2 = Button(window,text="Select File 2",command=openFile2)
button2.pack()
button3 = Button(window,text="Compare",command=compare)
button3.pack()
window.mainloop()



