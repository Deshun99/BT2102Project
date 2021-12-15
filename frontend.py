from tkinter import *


root = Tk()

etest = Entry(root)
etest.pack()
etest.insert(0, "Enter Username")


def myclick():
    hello = "Hello " + etest.get()
    label1 = Label(root, text=hello)
    label1.pack()


mybutton = Button(root, text="Enter", command=myclick)

myquitbutton = Button(root, text="Quit", command=root.destroy)
myquitbutton.pack()

mybutton.pack()


root.mainloop()
