import tkinter as tk
from tkinter import *
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog
# -----------------------------------
# TODO: Restructure this entire file
# -Change display graph to class to hold
# each graph canvas.
# -Cleanup syntax
# -Display each individual channel with
# the option to cycle through frames
# -----------------------------------
def compareWindow():
    root = tk.Tk()
    root.configure(background="purple")
    root.geometry("1200x850")
    frame = tk.Frame(root, background="yellow")
    frame.grid(row=0)
    canvas = tk.Canvas(root)
    canvas.configure(width=1000, height=700, background="red")
    canvas.grid(row=1, sticky='nesw')

    fileBut1 = tk.Button (frame,text="File 1:", padx=10,
                    pady=5, fg="white", bg="#263D42",
                    command=lambda: getFile(filePath1))
    filePath1 = tk.Entry(frame)

    fileBut2 = tk.Button (frame,text="File 2:", padx=10,
                    pady=5, fg="white", bg="#263D42",
                    command=lambda: getFile(filePath2))
    filePath2 = tk.Entry(frame)

    display = tk.Button(frame,text="Display", padx=10,
                    pady=5, fg="white", bg="#263D42",
                    command=lambda:getGraphs)

    def getGraphs():
        graphDic = displayGraph(filePath1.get(), filePath2.get(), canvas)

        print(graphDic)

    fileBut1.grid(row=0, column=0)
    filePath1.grid(row=0,column=1)
    fileBut2.grid(row=0,column=2)
    filePath2.grid(row=0,column=3)
    display.grid(row=0,column=4)

    root.mainloop()

class getFile(filePath):
    filename = filedialog.askopenfilename()
    filePath.delete(0, 'end')
    filePath.insert(0, filename)


def displayGraph(file1, file2, frame):
    file1Data = np.load(file1)
    file2Data = np.load(file2)
# TODO Make graphs
    graphs = {}
    for i in range(3):
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot(file1Data[i][1])
        a.plot(file2Data[i][1])
        graphs["graph{0}".format(i)] = f

    canvasDic = {}
    for i in range(3):
        canvas2 = FigureCanvasTkAgg(graphs["graph{0}".format(i)], frame)
        canvas2.get_tk_widget().grid(row=1, column=i)
        canvasDic["canvas{0}".format(i)] = canvas2
    return (canvasDic)

compareWindow()
