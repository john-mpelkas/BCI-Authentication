import tkinter as tk
from tkinter import *
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog
# -----------------------------------
# Script which allows for comparing two files split up between each channel
# -----------------------------------
class GraphObjects():

    def __init__(self, file1, file2, root):

        self.file1Data = np.load(file1)
        self.file2Data = np.load(file2)
        print (self.file1Data)
        self.counter = 0
        self.figures = {}
        self.plots = {}
        self.canvas = {}

        button = tk.Button(root, text="NEXT", command=lambda: self.nextGraph())
        button.grid(row=2, column = 3)

        button = tk.Button(root, text="PREVIOUS", command=lambda: self.previousGraph())
        button.grid(row=2, column = 2)

    def displayGraph(self, dataFrame, frame):

        for i in range(8):
            self.figures["channel{0}F".format(i)] = Figure(figsize=(4,4), dpi=100)
            self.plots["channel{0}A".format(i)] = self.figures["channel{0}F".format(i)].add_subplot(111)
            self.plots["channel{0}A".format(i)].set_title("Channel {0}".format(i+1))
            self.plots["channel{0}A".format(i)].plot(self.file1Data[dataFrame][i], 'b-')
            self.plots["channel{0}A".format(i)].plot(self.file2Data[dataFrame][i], 'r-')

            self.canvas["channel{0}Canvas".format(i)] = FigureCanvasTkAgg(self.figures["channel{0}F".format(i)], frame)
            self.canvas["channel{0}Canvas".format(i)].draw()
            if (i < 4):
                columnNum = i + 1
                self.canvas["channel{0}Canvas".format(i)].get_tk_widget().grid(row=0, column=columnNum)
            else:
                columnNum = i - 3
                self.canvas["channel{0}Canvas".format(i)].get_tk_widget().grid(row=1, column=columnNum)


    def updateGraph(self, dataFrame):

        for i in range(8):
            self.plots["channel{0}A".format(i)].lines[0].remove()
            self.plots["channel{0}A".format(i)].lines[0].remove()
            self.plots["channel{0}A".format(i)].plot(self.file1Data[dataFrame][i], 'b-')
            self.plots["channel{0}A".format(i)].plot(self.file2Data[dataFrame][i], 'r-')
            self.canvas["channel{0}Canvas".format(i)].draw()
            if (i < 4):
                columnNum = i + 1
                self.canvas["channel{0}Canvas".format(i)].get_tk_widget().grid(row=0, column=columnNum)
            else:
                columnNum = i - 3
                self.canvas["channel{0}Canvas".format(i)].get_tk_widget().grid(row=1, column=columnNum)

# TODO: Add edge condition
    def nextGraph(self):
        self.counter = self.counter+1
        self.updateGraph(self.counter)

    def previousGraph(self):
        if(self.counter>0):
            self.counter = self.counter-1
            self.updateGraph(self.counter)


file1 = r"C:\Users\mpelkasj\Desktop\EEG_Data\B&W Data - Correct\JohnCorrect1595619934.npy"
file2 = r"C:\Users\mpelkasj\Desktop\EEG_Data\Y&P Data - Incorrect\JohnY&P1595622367.npy"

root = tk.Tk()

x = GraphObjects(file1, file2, root)

x.displayGraph(x.counter, root)

root.mainloop()
