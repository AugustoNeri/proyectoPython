import urllib.request
from bs4 import BeautifulSoup
import random
import tkinter
from PIL import ImageTk, Image
from tkinter import *
from tkinter import ttk
import os

def main():
    ventana = tkinter.Tk()
    ventana.geometry("500x300")
    ventana.config(bg="#B7E9F5")
    ventana.title("Menu Principal")
    miFrame= Frame()
    miFrame.pack()
    bienvenido = Label(miFrame, text="MENU PRINCIPAL")
   
    bienvenido.config(font=('Arial', 16),width=500,height=800)
    
    
    nombre_label= Label(miFrame, text="Resultado")
    nombre_label.grid(row=2, column=0)
    nombre_label.config(padx=10, pady=10)
    cuadro_nombre=tkinter.Entry(miFrame)
    
    cuadro_nombre.grid(row=1,
               column=0,
               padx=10,
               pady=10,
               ipadx=20,
               ipady=30)
    
   
    
    button = tkinter.Button(text="Regresar", command=lambda: print(entry.get()))
    button.place(x=220, y=150)

    ventana.mainloop()

if __name__ == '__main__':
    main()