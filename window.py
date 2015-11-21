#!/usr/bin/python
# -*-coding:utf-8-*-

import Tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "click me"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.QUIT = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.QUIT.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")


root = tk.Tk()
root.title('zhou')

app = Application(master=root)

root.update() # update window ,must do
curWidth =400# root.winfo_reqwidth() # get current width
curHeight =300# root.winfo_height() # get current height
scnWidth,scnHeight = root.maxsize() # get screen width and height
 # now generate configuration information
tmpcnf = '%dx%d+%d+%d'%(curWidth,curHeight,
        (scnWidth-curWidth)/2,(scnHeight-curHeight)/2)
root.geometry(tmpcnf)

app.mainloop()
