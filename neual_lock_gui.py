import tkinter as tk
import pull_lsl_data
import os


def onGatherDataClick():
    inlet = pull_lsl_data.connectEEG()

    pull_lsl_data.collectData(inlet)



root = tk.Tk()
root.title("Neural Lock")

canvas = tk.Canvas(root, height=700, width=700)
canvas.pack()

canvas.create_text(350, 350, text="Neural Lock", font=("Helvetica", 42))

gatherData = tk.Button(root, text="Gather Training Data", padx=10, pady=5,
                        fg="white", bg="#263D42", command=onGatherDataClick) #TODO: add 'command="action"'
gatherData.pack()

authenticate = tk.Button (root, text="Authenticate", padx=10, pady=5,
                            fg="white", bg="#263D42") #TODO: add 'command="action"'
authenticate.pack()

root.mainloop()
