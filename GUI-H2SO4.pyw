from Tkinter import *
from tkFileDialog import askopenfilename
from datechecktest import SpecificTime
import datetime
import matplotlib.pyplot as plt
import time
import sys
import numpy as np
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *
from H2SO4HarvestGUI import h2so4TimeSeries

def doNothing():
    print("Okay")
    
def openFile():
    #file_list=[]
    filename = askopenfilename(parent=root)
    file_list.insert(0, filename)
    return filename

def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def update_days():
    thirtydays = ['4','6','9','11']
    for mo in thirtydays:
        if monthStart.get() == mo:
            maxdays = 30
            print mo
            break
        elif monthStart.get() == '2':
            if is_leap_year(int(yearStart.get())):            
                maxdays = 29
            else:
                maxdays = 28
            print mo
            break
        else:
            maxdays = 31
            print mo
    dayStart.config(to=maxdays)
    
def update_days_end():
    thirtydays = ['4','6','9','11']
    for mo in thirtydays:
        if monthEnd.get() == mo:
            maxdays = 30
            print mo
            break
        elif monthEnd.get() == '2':
            if is_leap_year(int(yearEnd.get())):            
                maxdays = 29
            else:
                maxdays = 28
            print mo
            break
        else:
            maxdays = 31
            print mo
    dayEnd.config(to=maxdays)

def timein():
    monthStart.delete(0,"end")
    monthStart.insert(0,datetime.datetime.now().month)
    dayStart.delete(0,"end")
    dayStart.insert(0,datetime.datetime.now().day)
    yearStart.delete(0,"end")
    yearStart.insert(0,datetime.datetime.now().year)
    hourStart.delete(0,"end")
    hourStart.insert(0,datetime.datetime.now().hour)
    minuteStart.delete(0,"end")
    minuteStart.insert(0,datetime.datetime.now().minute)
    monthEnd.delete(0,"end")
    monthEnd.insert(0,datetime.datetime.now().month)
    dayEnd.delete(0,"end")
    dayEnd.insert(0,datetime.datetime.now().day)
    yearEnd.delete(0,"end")
    yearEnd.insert(0,datetime.datetime.now().year)
    hourEnd.delete(0,"end")
    hourEnd.insert(0,datetime.datetime.now().hour)
    minuteEnd.delete(0,"end")
    minuteEnd.insert(0,datetime.datetime.now().minute)

def H2SO4Plot():
    fullstart = monthStart.get() + '/' + dayStart.get() + '/' + yearStart.get() + ' ' + hourStart.get() + ':' + minuteStart.get()
    fullend = monthEnd.get() + '/' + dayEnd.get() + '/' + yearEnd.get() + ' ' + hourEnd.get() + ':' + minuteEnd.get()
    dtStart = datetime.datetime.strptime(fullstart, "%m/%d/%Y %H:%M")
    dtEnd = datetime.datetime.strptime(fullend, "%m/%d/%Y %H:%M")
    #dtStart = dtStart + datetime.timedelta(hours=6)
    #dtEnd = dtEnd + datetime.timedelta(hours=6)
    h2so4TimeSeries(dtStart, dtEnd)

file_list=[]
root = Tk()
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

T = Text(root, height=2, width=30)
T.grid(row=0, column=0, columnspan=10)

starttimeLabel=StringVar()
starttimeLabel.set("Start Time: M/D/Y H:M")
starttimeDir=Label(root, textvariable=starttimeLabel, height=1)
starttimeDir.grid(row=2, column=0)

monthVarStart = IntVar(root)
dayVarStart = IntVar(root)
yearVarStart = IntVar(root)
hourVarStart = IntVar(root)
minuteVarStart = IntVar(root)
monthStart = Spinbox(root, from_=1, to=12, width=10, textvariable=monthVarStart, command=update_days)
monthStart.grid(row=3, column=0)
monthStart.delete(0,"end")
monthStart.insert(0,datetime.datetime.now().month)
dayStart = Spinbox(root, from_=1, to=31, width=10, textvariable=dayVarStart)
dayStart.grid(row=3, column=1)
dayStart.delete(0,"end")
dayStart.insert(0,datetime.datetime.now().day)
yearStart = Spinbox(root, from_=2000, to=2100, width=10, textvariable=yearVarStart, command=update_days)
yearStart.delete(0,"end")
yearStart.insert(0,datetime.datetime.now().year)
yearStart.grid(row=3, column=2)
hourStart = Spinbox(root, from_=0, to=23, width=10, textvariable=hourVarStart)
hourStart.grid(row=3, column=3)
minuteStart = Spinbox(root, from_=0, to=59, width=10, textvariable=minuteVarStart)
minuteStart.grid(row=3, column=4)

endtimeLabel=StringVar()
endtimeLabel.set("End Time: M/D/Y H:M")
endtimeDir=Label(root, textvariable=endtimeLabel, height=1)
endtimeDir.grid(row=4, column=0)

monthVarEnd = IntVar(root)
dayVarEnd = IntVar(root)
yearVarEnd = IntVar(root)
hourVarEnd = IntVar(root)
minuteVarEnd = IntVar(root)
monthEnd = Spinbox(root, from_=1, to=12, width=10, textvariable=monthVarEnd, command=update_days_end)
monthEnd.grid(row=5, column=0)
monthEnd.delete(0,"end")
monthEnd.insert(0,datetime.datetime.now().month)
dayEnd = Spinbox(root, from_=1, to=31, width=10, textvariable=dayVarEnd)
dayEnd.grid(row=5, column=1)
dayEnd.delete(0,"end")
dayEnd.insert(0,datetime.datetime.now().day)
yearEnd = Spinbox(root, from_=2010, to=2100, width=10, textvariable=yearVarEnd, command=update_days_end)
yearEnd.grid(row=5, column=2)
yearEnd.delete(0,"end")
yearEnd.insert(0,datetime.datetime.now().year)
hourEnd = Spinbox(root, from_=0, to=23, width=10, textvariable=hourVarEnd)
hourEnd.grid(row=5, column=3)
minuteEnd = Spinbox(root, from_=0, to=59, width=10, textvariable=minuteVarEnd)
minuteEnd.grid(row=5, column=4)

timein()

button = Button(root, text="Make H2SO4 Time Series", command=H2SO4Plot)
button.grid(row=7,columnspan=3)

root.config(menu=menubar)
root.mainloop()
