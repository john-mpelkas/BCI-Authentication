import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, StringVar
import pull_lsl_data
import threading
import time
import os

class BciInterface(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self)
        self.title("Neural Lock")
        container = tk.Frame(self, height=100, width=100)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames={}
        for F in (StartPage, DataPage):
            #Creating object:
            #Container holds frames
            #self allows other classes to access show_frame
            frame = F(container, self)
            self.frames[F] = frame
            #not 100% sure on this
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
        # Self -> StartPage
        # parent -> container
        # controller -> BciInterface Class in order to access show_frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self,text="Neual Lock", height=10, width=20,
                        font=("Courier", 44))

        gatherData = tk.Button(self, text="Gather Training Data",
                        padx=10, pady=5, fg="white", bg="#263D42",
                        command=lambda: controller.show_frame(DataPage))

        authenticate = tk.Button (self, text="Authenticate", padx=10,
                        pady=5, fg="white", bg="#263D42")

        label.pack(side='top')
        gatherData.pack(side='bottom', padx=10, pady=5)
        authenticate.pack(side='bottom', padx=10, pady=5)

class DataPage(tk.Frame, tk.Tk):
    dir=""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.channel_data=[]
        filePath = tk.Label(self, text="Enter File Path To Save To: ", padx=10, pady=10)

        entry= tk.Entry(self)
        entry.insert(0, os.getcwd())

        # print(entry.get()) get text from the entry field

        browse = tk.Button(self, text="Browse", padx=10, pady=5,
                            fg="white", bg="#263D42",
                            command = lambda: self.getFileDir(entry))

        goBack = tk.Button(self, text="Back", padx=10, pady=5,
                            fg="white", bg="#263D42", command=lambda:
                            controller.show_frame(StartPage))

        start = tk.Button(self, text="Start", padx=10, pady=5,
                            fg="white", bg="#263D42", command=lambda:
                            self.vepSlideShow()) #Change to vepSlideShow for show

        filePath.grid(row=0, column=1, columnspan=3, padx= 5, pady=5)
        goBack.grid(row=0,column=0, padx= 5, pady=5)
        browse.grid(row=1, column=0, padx= 5, pady=5)
        entry.grid(row=1, column=1, columnspan=3, padx= 5, pady=5)
        start.grid(row=0, rowspan=2, column=5 , columnspan=3, padx= 5, pady=5)



    def vepSlideShow(self):

        root = tk.Tk()
        root.title("P300")
        root.attributes('-fullscreen', True)

        container = tk.Frame(root)
        container.pack(side="top", fill="both", expand=True)

        frames = {}

        frames[WBChecker] = WBChecker(container, root)
        frames[WBChecker].grid(row=0, column=1, sticky="nsew")
        frames[BWChecker] = BWChecker(container, root)
        frames[BWChecker].grid(row=0, column=1, sticky="nsew")
        frames[InitiateConnection] = InitiateConnection(container, root)
        frames[InitiateConnection].grid(row=0, column=1, sticky="nsew")



        def whtChecker():
            frames[WBChecker].tkraise()
        def blkChecker():
            frames[BWChecker].tkraise()
        def close():
            pull_lsl_data.saveData(self.channel_data)
            root.destroy()
        def updateTime():
            frames[InitiateConnection].updateTime()
        def gatherData():
            time.sleep(4)
            self.channel_data = pull_lsl_data.collectData(inlet)


        inlet = pull_lsl_data.connectEEG()

        threading.Thread(target=gatherData).start()
        root.after(2000, updateTime)
        root.after(4000, updateTime)
        root.after(6000, whtChecker)
        root.after(7000, blkChecker)
        root.after(8000, whtChecker)
        root.after(9000, blkChecker)
        root.after(10000, whtChecker)
        root.after(11000, blkChecker)
        root.after(12000, whtChecker)
        root.after(13000, blkChecker)
        root.after(14000, whtChecker)
        root.after(15000, blkChecker)
        root.after(16000, close)


        root.mainloop()

class InitiateConnection(tk.Frame):

    def __init__(self, parent, controller):
        self.timer = 3
        tk.Frame.__init__(self, parent)
        canvas = tk.Canvas(self)
        canvas.config(height=1080, width=1920)
        canvas.pack()
        self.conLabel = tk.Label(canvas, text="Connected - Begins in:", font=("arial", 24))
        self.beginLab = tk.Label(canvas, text=self.timer, font=("arial", 24))
        self.conLabel.place(relx=0.5, rely=0.45, anchor='center')
        self.beginLab.place(relx=0.5, rely=0.5, anchor='center')

    def updateTime(self):
        self.timer = self.timer - 1
        print ( self.timer)
        self.beginLab['text'] = self.timer
        #self.beginLab.update()


class WBChecker(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        canvas = tk.Canvas(self)
        canvas.config(height=1080, width=1920)
        canvas.pack()
        SIZE=124
        color = 'white'

        for y in range(9):

            for x in range(16):
                x1 = x*SIZE
                y1 = y*SIZE
                x2 = x1 + SIZE
                y2 = y1 + SIZE
                canvas.create_rectangle((x1, y1, x2, y2), fill=color)
                if color == 'white':
                    color = 'black'
                else:
                    color = 'white'

            if color == 'white':
                color = 'black'
            else:
                color = 'white'

class BWChecker(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        canvas2 = tk.Canvas(self)
        canvas2.config(height=1080, width=1920)
        canvas2.pack()

        SIZE=124
        color = 'black'

        for y in range(9):

            for x in range(16):
                x1 = x*SIZE
                y1 = y*SIZE
                x2 = x1 + SIZE
                y2 = y1 + SIZE
                canvas2.create_rectangle((x1, y1, x2, y2), fill=color)
                if color == 'white':
                    color = 'black'
                else:
                    color = 'white'

            if color == 'white':
                color = 'black'
            else:
                color = 'white'

app = BciInterface(tk.Tk)
app.mainloop()
