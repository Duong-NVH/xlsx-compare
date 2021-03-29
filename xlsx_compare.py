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

ERR_INVALID="invalid format"
ERR_SOME_SHIT_WAS_WRONG="Some thing went wrong.\nPlease try again!"

def openFile1():
    global filepath1
    filepath1 = filedialog.askopenfilename(filetypes=[("Excel files", ".xlsx .xls")])
    print(f"Chosen XLSX file from {filepath1}")

def openFile2():
    global filepath2
    filepath2 = filedialog.askopenfilename(filetypes=[("CSV files", ".csv")])
    print(f"Chosen CSV file from {filepath2}")

def compare():
    try:
        print("Loading data...")
        df1=pd.read_excel(filepath1)
        df2=pd.read_csv(filepath2)
        df1.to_sql(name='XLSX_DATA', con=conn)
        df2.to_sql(name='CSV_DATA', con=conn)
        cur = conn.cursor()
        
        print("Comparing...")
        # compare R
        cur.execute("SELECT * FROM CSV_DATA WHERE DEVICE LIKE 'R%'")
        r_csv_data=cur.fetchall()
        for row in r_csv_data:
            q=f"SELECT * FROM XLSX_DATA WHERE DEVICE = '{row[3].strip()}'"
            cur.execute(q)
            result=cur.fetchone()
            if result:
                xlsx=readRFromXLSX(result[2])
                if xlsx== ERR_INVALID:
                    xlsx=readRFromXLSXType2(result[2])
                csv=readRFromCSV(row[4])
                x1=calculateR(xlsx)
                c1=calculateR(csv)
                if x1 != c1:
                    print(f"DIFF: {result[1]}: {xlsx} - {x1} - {result[2]} / {csv} - {c1} - {row[4]}")
            else:
                print("Not found "+row[3]+" in XLSX file")
        print("Done!")
    except:
        print(ERR_SOME_SHIT_WAS_WRONG)

def calculateR(data):
    if data.isdecimal() or data.replace(".","").isdecimal() :
        return float(data)
    if data[-1:] == "K":
        return float(data.replace("K",""))*1000
    return ERR_INVALID

def readRFromXLSX(data):
    s= data.strip().split(",")[1].replace("_OHM","")
    if s[-1:].isdecimal() or s[-1:] == "K":
        return s
    return ERR_INVALID

def readRFromXLSXType2(data):
    s= data.strip().split(",")[0].split(" ")[2]
    
    if s[-4:] == "KOHM":
        return s.replace("OHM","")
    if s[-3:] == "OHM":
        return s.replace("OHM","").replace("_","")

    return ERR_INVALID

    
def readRFromCSV(data):
    s=data.strip().split(".")
    if s[0].isdecimal():
        s[0]=int(s[0])
    if len(data.split(".")) > 1:   
        s1=s[1] if (s[1][:-2].isdecimal() and float(s[1][:-2]))>0 else s[1].replace("0","")
        if s1[0] != "K" and len(s1)>2:
            s1="."+s1
        if s1[-2:]=="Ko":
            return f"{s[0]}{s1[:-1]}"
        return f"{s[0]}{s1[:-2]}"
    return ERR_INVALID

# def readCFromXLSX(data):
#     return 1
# def readCFromCSV(data):
#     return 1
    


button1 = Button(window,text="Select XLSX File",command=openFile1)
button1.pack()
button2 = Button(window,text="Select CSV File",command=openFile2)
button2.pack()
button3 = Button(window,text="Compare",command=compare)
button3.pack()
window.mainloop()



