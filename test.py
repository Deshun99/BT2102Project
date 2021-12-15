from tkinter import *
import tkinter as tk
from tkinter import ttk

def btn_clicked():
    print("Button Clicked")


window = Tk()

window.geometry("436x896")
window.configure(bg = "#FFFFFF")
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 896,
    width = 436,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

canvas.create_text(
    2207.5, -1918.5,
    text = "Item Id",
    fill = "#ffffff",
    font = ("Montserrat-Bold", int(18.0)))

canvas.create_text(
    2126.5, -2006.5,
    text = "Category",
    fill = "#ffffff",
    font = ("Montserrat-Bold", int(18.0)))

canvas.create_text(
    2302.5, -2006.5,
    text = "Model",
    fill = "#ffffff",
    font = ("Montserrat-Bold", int(18.0)))

canvas.create_text(
    2207.5, -1918.5,
    text = "Item Id",
    fill = "#ffffff",
    font = ("Montserrat-Bold", int(18.0)))

canvas.create_text(
    2207.5, -1918.5,
    text = "Item Id",
    fill = "#ffffff",
    font = ("Montserrat-Bold", int(18.0)))

canvas.create_text(
    2204.0, -2137.5,
    text = "Product Search",
    fill = "#000000",
    font = ("Montserrat-Regular", int(48.0)))

canvas.create_text(
    2210.0, -2080.5,
    text = "Search via",
    fill = "#000000",
    font = ("Montserrat-Regular", int(24.0)))

window.resizable(False, False)
window.mainloop()