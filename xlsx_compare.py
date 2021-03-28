print("Starting...")
import pandas as pd
import numpy as np
from tkinter import *
from tkinter import filedialog
import sqlite3
conn = sqlite3.connect(':memory:')
filepath1=""
filepath1=""
window = Tk()
def openFile1():
    global filepath1
    filepath1 = filedialog.askopenfilename(filetypes=[("Excel files", ".xlsx .xls")])
    print(f"Chosen XLSX file from {filepath1}")

def openFile2():
    global filepath2
    filepath2 = filedialog.askopenfilename(filetypes=[("CSV files", ".csv")])
    print(f"Chosen CSV file from {filepath2}")

def compare():
    print("Loading data...")
    df1=pd.read_excel(filepath1)
    df2=pd.read_csv(filepath2)
    df1.to_sql(name='XLSX_DATA', con=conn)
    df2.to_sql(name='CSV_DATA', con=conn)
    cur = conn.cursor()
    cur.execute("SELECT * FROM CSV_DATA WHERE DEVICE LIKE 'C%' OR DEVICE LIKE 'R%'")
    csv_data=cur.fetchall()
    print("Comparing...")
    for row in csv_data:
        q=f"SELECT * FROM XLSX_DATA WHERE DEVICE = '{row[3].strip()}'"
        cur.execute(q)
        result=cur.fetchone()
        if result:
            print("Found "+result[1])
        else:
            print("Not found "+row[3])
    

    print("Done!")
    


button1 = Button(window,text="Select XLSX File",command=openFile1)
button1.pack()
button2 = Button(window,text="Select CSV File",command=openFile2)
button2.pack()
button3 = Button(window,text="Compare",command=compare)
button3.pack()
window.mainloop()



