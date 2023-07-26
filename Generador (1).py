import codecs
import random
import pymysql
# -*- coding:utf-8 -*-
from numpy import *
import datetime
import urllib.request
from bs4 import BeautifulSoup
import random
import tkinter
from PIL import ImageTk, Image
from tkinter import *
from tkinter import ttk
import os

MAYUSCULAS = {65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90}
MINUSCULAS = {97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118,
              119, 120, 121, 122}
ACEPTADOS = {32, 33, 34, 40, 41, 44, 45, 46, 58, 59, 63, 64, 91, 93, 123, 125, 191, 161, 171, 187}
ESPECIALES = {241, 209, 225, 233, 237, 243, 250, 193, 201, 205, 211, 218}


def salida(resultado):
    ventana2 = tkinter.Tk()
    ventana2.geometry("500x300")
    ventana2.config(bg="#B7E9F5")
    ventana2.title("Menu Principal")
    miFrame = Frame()
    miFrame.pack()
    bienvenido = Label(miFrame, text="MENU PRINCIPAL")

    bienvenido.config(font=('Arial', 16), width=500, height=800)

    nombre_label = Label(miFrame, text=resultado)
    nombre_label.grid(row=2, column=0)
    nombre_label.config(padx=10, pady=10)


    button = tkinter.Button(text="Regresar", command=lambda: [ventana2.destroy(), menu()])
    button.place(x=220, y=150)

    ventana2.mainloop()

def ponerPal(conection, nueva, anterior,ahora):

    consulta = "select id from palabras where palabra = '{}';".format(anterior)
    cursor = conection.cursor()
    cursor.execute(consulta)
    conection.commit()
    res = cursor.fetchone()
    id = res[0]
    consulta = "select aparicion from siguiente where palabra = '{}' and id = {}; ".format(nueva, id)
    cursor.execute(consulta)
    conection.commit()
    res = cursor.fetchone()
    if res is None:
        consulta = "insert into  siguiente values('{}', 1, {});".format(nueva, id)
        cursor.execute(consulta)
        conection.commit()
        bitacora = "Ejecutando: "+consulta
        bitacora1(bitacora, ahora)
    else:
        n = res[0] + 1
        consulta = "update siguiente set aparicion = {} where palabra = '{}' and id = {};".format(n, nueva, id)
        cursor.execute(consulta)
        conection.commit()
        bitacora = "\nEjecutando: " + consulta
        bitacora1(bitacora, ahora)


def llenar_bd(conection, EX, archivo, bd, ahora):
    bitacora1("\nCreando base de datos", ahora)
    cursor = conection.cursor()
    actualiza = "select count(palabra) from palabras;"
    band = False
    archivo = codecs.open(archivo, "r", "utf-8")
    tot = 0
    if bd == 1:
        tot = 3999
    else: tot = 7999
    actual = ""
    contador = 0
    compro = ""
    compex = ""
    palabra = ""
    extra = ""
    consulta = ""
    anterior = " "
    while contador < tot:
        linea = archivo.readline().rstrip("\n")
        palabra = linea.split(" ")
        for a in palabra:
            for b in a:
                b = b.lower()
                if ord(b) in (MINUSCULAS | MAYUSCULAS | ESPECIALES):
                    actual = actual + b
                elif ord(b) in ACEPTADOS:
                    extra = b
                    compex = "select palabra from palabras where palabra = '{}'".format(extra)
                    cursor.execute(compex)
                    conection.commit()
                    rex = cursor.fetchone()
                    if rex is None:
                        compro = "select palabra from palabras where palabra = '{}'".format(actual)
                        cursor.execute(compro)
                        conection.commit()
                        resul = cursor.fetchone()
                        if resul is None:
                            consulta = "insert into palabras values(default, '{}')".format(actual)
                            cursor.execute(consulta)
                            conection.commit()
                        anterior = actual
                        consulta = "insert into palabras values(default, '{}')".format(extra)
                        cursor.execute(consulta)
                        conection.commit()
                    if EX != 0:
                        ponerPal(conection, extra, anterior,ahora)
                    anterior = extra
                    extra = ""
                    band = True
                else:
                    break
            compro = "select palabra from palabras where palabra = '{}'".format(actual)
            cursor.execute(compro)
            conection.commit()
            resul = cursor.fetchone()
            if resul is None:
                consulta = "insert into palabras values(default, '{}')".format(actual)
                cursor.execute(consulta)
                conection.commit()
            if band == False and EX != 0:
                ponerPal(conection, actual, anterior,ahora)
                anterior = actual
            if not band: anterior = actual
            extra = ""
            actual = ""
            EX = 1
            band = False
            cursor.execute(actualiza)
            lon = cursor.fetchone()
            contador = lon[0]

    print("Hecho\n")


def menu():
    ventana = tkinter.Tk()
    ventana.geometry("400x400")
    ventana.config(bg="#B7E9F5")
    ventana.title("Menu Principal")
    miFrame = Frame()
    miFrame.pack()
    bienvenido = Label(miFrame, text="MENU PRINCIPAL")
    bienvenido.grid(row=0, column=0)
    bienvenido.config(font=('Arial', 16))

    nombre_label = Label(miFrame, text="TEXTO")
    nombre_label.grid(row=1, column=0)
    nombre_label.config(padx=10, pady=10)
    cuadro_nombre = Entry(miFrame)
    cuadro_nombre.grid(row=1, column=1)

    longitud_label = Label(miFrame, text="LONGITUD")
    longitud_label.grid(row=2, column=0)
    longitud_label.config(padx=10, pady=10)
    cuadro_longitud = Entry(miFrame)
    cuadro_longitud.grid(row=2, column=1)

    longitud_label = Label(miFrame, text="Tipo de probabilidad")
    longitud_label.grid(row=3, column=0)
    longitud_label.config(padx=10, pady=10)
    combo = ttk.Combobox(
        state="readonly",
        values=["probabilidad más alta", "probabilidad más baja", "probabilidad intermedia"]
    )
    combo.place(x=220, y=120)

    button = tkinter.Button(text="Obtener texto", command=lambda: [ main(cuadro_nombre.get(), cuadro_longitud.get(),combo.get(), ventana)])
    button.place(x=220, y=150)

    ventana.mainloop()


def siguiente(conection, eleccion, anterior, ahora):
    curso = conection.cursor()
    alto = []
    total = 0
    sql = "Select * from palabras where palabra = '{}';".format(anterior)
    curso.execute(sql)
    conection.commit()
    comprobacion = curso.fetchone()
    if comprobacion is None:
        col = random.randint(1,8000)
        sql = "select palabra from palabras where id = {};".format(col)
        curso.execute(sql)
        conection.commit()
        comprobacion = curso.fetchone()
        anterior = comprobacion[0]
    sql = "SELECT siguiente.palabra, aparicion FROM siguiente join palabras " \
          "on siguiente.id = palabras.id where palabras.palabra = '{}' order by aparicion desc;".format(anterior)
    bitacora1("\nConsultando todas las coincidencias de la palabra anterior en la tabla 'siguiente'", ahora)
    curso.execute(sql)
    conection.commit()
    result = list(curso.fetchall())
    bitacora1("\nRecibiendo lista de coincidencias", ahora)
    if len(result) < 5:
        pal = result[0][0]
    else:
        for i in range(0, len(result)):
            total += result[i][1]
        prob = 0
        bitacora1("\nleyendo ocurrencias de las siguientes palabras", ahora)
        acc = 0
        cuartil1 = total / 4
        cuartil2 = 2 * total / 4
        cuartil3 = 3 * total / 4
        cuartil4 = total
        bitacora1("\nCalculando cuartiles", ahora)
        bitacora1("\nLeyendo seleccion del tipo de texto", ahora)
        if eleccion == 1:
            for i in range(0, len(result)):
                if acc < cuartil1:
                    alto.append(result[i])
                    prob += result[i][1]
                acc += result[i][1]
            bitacora1("\nReduciendo lista", ahora)

        elif eleccion == 2:
            for i in range(0, len(result)):
                if acc >= cuartil1 and acc <= cuartil3:
                    alto.append(result[i])
                    prob += result[i][1]
                acc += result[i][1]
            bitacora1("\nReduciendo lista", ahora)
        elif eleccion == 3:
            for i in range(0, len(result)):
                if acc >= cuartil3:
                    alto.append(result[i])
                    prob += result[i][1]
                acc += result[i][1]
            bitacora1("\nReduciendo lista", ahora)
        pal = ""
        elegido = random.randint(0, prob)
        bitacora1("\nTirando dado", ahora)
        for i in range(0, len(alto)):
            elegido -= alto[i][1]
            if elegido <= 0:
                pal = alto[i][0]
                break
        bitacora1("\nSeleccionando palabra", ahora)
    bitacora = "\nLa iguiente palabra es:" + pal
    bitacora1(bitacora, ahora)
    return pal


def bitacora2(dato, nombre):
    nombre = nombre+ ".txt"
    archivo = codecs.open(nombre, "w", "utf-8")
    archivo.write(dato)
    archivo.close()

def bitacora1(dato, nombre):
    nombre = nombre+ ".txt"
    archivo = codecs.open(nombre, "a", "utf-8")
    archivo.write(dato)
    archivo.close()


def main(oracion, largo, proba, ventana):
    EX = 0
    ahora = datetime.datetime.now()
    oracion = oracion.lower()
    largo = int(largo)
    ahorafor = ahora.strftime('%d-%m-%Y_%H-%M-%S')
    bitacora2("Creando bitácora", ahorafor)
    if proba == "probabilidad más alta":
        tipo = 1
    if proba == "probabilidad intermedia":
        tipo = 2
    if proba == "probabilidad más baja":
        tipo = 3
    conection = pymysql.connect(host='localhost',
                                user='root',
                                password='1234',
                                database='generador')
    ventana.destroy()
    #llenar_bd(conection,EX, "William Goldin - El Señor de las moscas.txt", 1, ahorafor)
    #llenar_bd(conection, EX, "gabriel_garcia_marquez_cien_annos_soledad.txt", 2, ahorafor)
    nuev = siguiente(conection, tipo, oracion, ahorafor)
    oracion = oracion + " " +nuev
    for x in range(1,largo):
        nuev= siguiente(conection, tipo, nuev,ahorafor)
        if len(nuev)==1:
            if ord(nuev) in ACEPTADOS:
                oracion = oracion + nuev
        else:  oracion = oracion +" "+ nuev
    bitacora1("\nOracion final: ", ahorafor)
    bitacora1(oracion,ahorafor)
    print(oracion)
    salida(oracion)


if __name__ == "__main__":
    menu()
