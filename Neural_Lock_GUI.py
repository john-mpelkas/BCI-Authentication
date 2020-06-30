import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import PanedWindow
import pull_lsl_data
import os

class BciInterface(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self)
        self.title("Neural Lock")
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(12, weight=1)
        container.grid_columnconfigure(12, weight=1)

        self.frames={}

        for F in (StartPage, DataPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)

            canvas = tk.Canvas(self, height=700, width=800)
            canvas.grid(row=1, column=0, sticky='nwe')

            canvas.create_text(400, 350, text="Neural Lock", font=("Helvetica", 42))

            gatherData = tk.Button(self, text="Gather Training Data", padx=10, pady=5,
                                    fg="white", bg="#263D42",
                                    command=lambda: controller.show_frame(DataPage)) #TODO: add 'command="action"'
            gatherData.grid(row=2, column=0, sticky='s')
            authenticate = tk.Button (self, text="Authenticate", padx=10, pady=5,
                                        fg="white", bg="#263D42") #TODO: add 'command="action"'
            authenticate.grid(row=3, column=0, sticky='s')

def collectData():
    inlet = pull_lsl_data.connectEEG()
    a = pull_lsl_data.collectData(inlet)
    print (a)

def fileDialog():
    pwd = os.path.dirname(os.path.abspath(__file__))
    filename = filedialog.askopenfilename(initialdir = getFilePath,
                    title = "Select a File", filetype= (("jpeg", "*.jpg"),
                    ("All Files", "*.*")))
def getFilePath():
    pwd = os.path.dirname(os.path.abspath(__file__))
    return (pwd)

class DataPage(tk.Frame):
#TODO: Really need to fix this shit show
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        filePath = tk.Label(self, text="Enter File Path To Save To: ", padx=10, pady=10)
        filePath.grid(row=0, column=2, sticky='e')

        browse = tk.Button(self, text="Browse", padx=10, pady=5,
                            fg="white", bg="#263D42", command=fileDialog)
        browse.grid(row=2, column=1, sticky='nsew')

        entry= tk.Entry(self)
        entry.insert(0, getFilePath())
        entry.grid(row=2, column=2, padx=10, pady=5, ipadx= 5)

        goBack = tk.Button(self, text="Back", padx=10, pady=5,
                            fg="white", bg="#263D42", command=lambda:
                            controller.show_frame(StartPage))
        goBack.grid(row=3, column=1, sticky='nsew')

        start = tk.Button(self, text="Start", padx=10, pady=5,
                        fg="white", bg="#263D42", command=fileDialog)
        start.grid(row=3, column=2, sticky='nsew')


#class AuthenticatePage(): TODO: When model done

app = BciInterface(tk.Tk)
app.mainloop()
