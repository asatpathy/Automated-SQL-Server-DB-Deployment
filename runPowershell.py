# import subprocess
#
# subprocess.call('sqlcmd -S localhost -d newSQLPackage1 -i C:\\Users\\asatpathy\\Desktop\\localtestSQLServer\\NewTests\\insertNewSQLPackage1.sql', shell=True)
#
# from tkinter import *
# from tkinter import ttk
#
# root = Tk()
#
# tree = ttk.Treeview(root)
#
# tree["columns"] = ("one", "two")
# tree.column("one", width=100)
# tree.column("two", width=100)
# tree.heading("one", text="coulmn A")
# tree.heading("two", text="column B")
#
# tree.insert("", 0, text="Line 1", values=("1A", "1b"))
#
# id2 = tree.insert("", 1, "dir2", text="Dir 2")
# tree.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A", "2B"))
#
# ##alternatively:
# tree.insert("", 3, "dir3", text="Dir 3")
# tree.insert("dir3", 3, text=" sub dir 3", values=("3A", " 3B"))
#
# tree.pack()
# root.mainloop()




# -*- coding: utf-8 -*-
# from tkinter import *
# import datetime

# class Planificador(Frame):
#     def __init__(self,master):
#         Frame.__init__(self, master)
#         self.master = master
#         self.initUI()
#
#     def initUI(self):
#         self.master.title("Plan")
#         self.frameOne = Frame(self.master)
#         self.frameOne.grid(row=0,column=0)
#
#         self.frameTwo = Frame(self.master)
#         self.frameTwo.grid(row=1, column=0)
#
#         #Creating of a new frame, inside of "frameTwo" to the objects to be inserted
#         #Creating a scrollbar
#
#         #The reason for this, is to attach the scrollbar to "FrameTwo", and when the size of frame "ListFrame" exceed the size of frameTwo, the scrollbar acts
#         self.canvas=Canvas(self.frameTwo)
#         self.listFrame=Frame(self.canvas)
#         self.scrollb=Scrollbar(self.master, orient="vertical",command=self.canvas.yview)
#         self.scrollb.grid(row=1, column=1, sticky='nsew')  #grid scrollbar in master, but
#         self.canvas['yscrollcommand'] = self.scrollb.set   #attach scrollbar to frameTwo
#
#         self.canvas.create_window((0,0),window=self.listFrame,anchor='nw')
#         self.listFrame.bind("<Configure>", self.AuxscrollFunction)
#         self.scrollb.grid_forget()                         #Forget scrollbar because the number of pieces remains undefined by the user. But this not destroy it. It will be "remembered" later.
#
#         self.canvas.pack(side="left")
#         self.frameThree = Frame(self.master)
#         self.frameThree.grid(row=2, column=0)
#
#         # Borrar esto?
#         self.txt = Text(self)
#         self.txt.pack(fill=BOTH, expand=1)
#
#         self.piezastext = Label(self.frameOne, text = " Amount of pieces ", justify="center")
#         self.piezastext.grid(row=1, column=0)
#         self.entrypiezas = Entry(self.frameOne,width=3)
#         self.entrypiezas.grid(row=2, column=0, pady=(5,5))
#         self.aceptarnumpiezas = Button(self.frameOne,text="Click me", command=self.aceptar_piezas,width=8)
#         self.aceptarnumpiezas.grid(row=6, column=0, pady=(5,5))
#
#     def AuxscrollFunction(self,event):
#         #You need to set a max size for frameTwo. Otherwise, it will grow as needed, and scrollbar do not act
#         self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=600,height=500)
#
#     def aceptar_piezas(self):
#
#
#
#         #IMPORTANT!!! All the objects are now created in "ListFrame" and not in "frameTwo"
#         #I perform the alterations. Check it out
#         try:
#             val = int(self.entrypiezas.get())
#             self.aceptar_piezas_ok()
#             self.scrollb.grid(row=1, column=1, sticky='nsew')  #grid scrollbar in master, because user had defined the numer of pieces
#         except ValueError:
#             print("hello")
#
#     def aceptar_piezas_ok(self):
#         self.num_piezas = self.entrypiezas.get()
#
#         self.piezastext.grid_remove()
#         self.entrypiezas.grid_remove()
#         self.aceptarnumpiezas.grid_remove()
#
#         self.optionmenus_piezas = list()
#         self.numpiezas = []
#         self.numerolotes = []
#         self.optionmenus_prioridad = list()
#         self.lotes = list()
#
#         self.mispiezas = ['One', 'Two', 'Three', 'Four', 'Five']
#
#         self.n = 1
#         while self.n <= int(self.num_piezas):
#             self.textopieza = Label(self.listFrame, text = "Pieza: ", justify="left")
#             self.textopieza.grid(row=self.n, column=0)
#
#             var = StringVar()
#             menu = OptionMenu(self.listFrame, var, *self.mispiezas)
#             menu.config(width=10)
#             menu.grid(row=self.n, column=1)
#             var.set("One")
#             self.optionmenus_piezas.append((menu, var))
#
#             self.numpiezastext = Label(self.listFrame, text = "Numero de piezas: ", justify="center")
#             self.numpiezastext.grid(row=self.n, column=2, padx=(10,0))
#             self.entrynumpiezas = Entry(self.listFrame,width=6)
#             self.entrynumpiezas.grid(row=self.n, column=3, padx=(0,10))
#             self.entrynumpiezas.insert(0, "0")
#
#             self.textoprioridad = Label(self.listFrame, text = "Prioridad: ", justify="center")
#             self.textoprioridad.grid(row=self.n, column=4)
#             var2 = StringVar()
#             menu2 = OptionMenu(self.listFrame, var2, "Normal", "Baja", "Primera pieza", "Esta semana")
#             menu2.config(width=10)
#             menu2.grid(row=self.n, column=5)
#             var2.set("Normal")
#             self.optionmenus_prioridad.append((menu2, var2))
#
#             self.lotestext = Label(self.listFrame, text = "Por lotes?", justify="center")
#             self.lotestext.grid(row=self.n, column=6, padx=(10,0))
#             self.var1 = IntVar()
#             self.entrynumlotes = Checkbutton(self.listFrame, variable=self.var1)
#             self.entrynumlotes.grid(row=self.n, column=7, padx=(5,10))
#             self.lotes.append(self.var1)
#             self.numpiezas.append(self.entrynumpiezas)
#
#             self.n += 1
#
#         self.anadirpiezas = Button(self.frameThree, text="Add row", command=self.addpieza, width=10)
#         self.anadirpiezas.grid(row=0, column=2, pady=(10,10))
#
#         self.calculotext = Label(self.frameThree, text = "Other stuff ")
#         self.calculotext.grid(row=1, column=2, padx=(10,0), pady=(10,10))
#
#         self.graspbutton = Button(self.frameThree, text="OPT 1", width=10)
#         self.graspbutton.grid(row=2, column=1)
#
#         self.parettobutton = Button(self.frameThree, text="OPT 2",width=10)
#         self.parettobutton.grid(row=2, column=2, pady=(10,10), padx=(10,0))
#
#         self.parettoEvolbutton = Button(self.frameThree, text="OPT 2", width=10)
#         self.parettoEvolbutton.grid(row=2, column=3, pady=(10,10), padx=(10,0))
#
#
#     def addpieza(self):
#             self.textopiezanuevo = Label(self.listFrame, text = "Pieza: ", justify="left")
#             self.textopiezanuevo.grid(row=int(self.num_piezas)+1, column=0)
#
#             var = StringVar()
#             menu = OptionMenu(self.listFrame, var, *self.mispiezas)
#             menu.grid(row=self.n, column=1)
#             menu.config(width=10)
#             menu.grid(row=int(self.num_piezas)+1, column=1)
#             var.set("One")
#             self.optionmenus_piezas.append((menu, var))
#
#             self.numpiezastext = Label(self.listFrame, text = "Numero de piezas: ", justify="center")
#             self.numpiezastext.grid(row=int(self.num_piezas)+1, column=2, padx=(10,0))
#             self.entrynumpiezas = Entry(self.listFrame,width=6)
#             self.entrynumpiezas.grid(row=int(self.num_piezas)+1, column=3, padx=(0,10))
#             self.entrynumpiezas.insert(0, "0")
#
#             self.textoprioridad = Label(self.listFrame, text = "Prioridad: ", justify="center")
#             self.textoprioridad.grid(row=int(self.num_piezas)+1, column=4)
#             var2 = StringVar()
#             menu2 = OptionMenu(self.listFrame, var2, "Normal", "Baja", "Primera pieza", "Esta semana")
#             menu2.config(width=10)
#             menu2.grid(row=int(self.num_piezas)+1, column=5)
#             var2.set("Normal")
#             self.optionmenus_prioridad.append((menu2, var2))
#
#             self.lotestext = Label(self.listFrame, text = "Por lotes?", justify="center")
#             self.lotestext.grid(row=int(self.num_piezas)+1, column=6, padx=(10,0))
#             self.var1 = IntVar()
#             self.entrynumlotes = Checkbutton(self.listFrame, variable=self.var1)
#             self.entrynumlotes.grid(row=int(self.num_piezas)+1, column=7, padx=(5,10))
#             self.lotes.append(self.var1)
#
#             self.numpiezas.append(self.entrynumpiezas)
#             self.num_piezas = int(self.num_piezas)+1
#
# if __name__ == "__main__":
#     root = Tk()
#     aplicacion = Planificador(root)
#     root.mainloop()









# from tkinter import *
#
# def data():
#     for i in range(50):
#        Label(frame,text=i).grid(row=i,column=0)
#        Label(frame,text="my text"+str(i)).grid(row=i,column=1)
#        Label(frame,text="..........").grid(row=i,column=2)
#
# def myfunction(event):
#     canvas.configure(scrollregion=canvas.bbox("all"),width=200,height=200)
#
# root=Tk()
# sizex = 800
# sizey = 600
# posx  = 100
# posy  = 100
# root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
#
# myframe=Frame(root,relief=GROOVE,width=50,height=100,bd=1)
# myframe.place(x=10,y=10)
#
# canvas=Canvas(myframe)
# frame=Frame(canvas)
# myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
# canvas.configure(yscrollcommand=myscrollbar.set)
#
# myscrollbar.pack(side="right",fill="y")
# canvas.pack(side="left")
# canvas.create_window((0,0),window=frame,anchor='nw')
# frame.bind("<Configure>",myfunction)
# data()
# root.mainloop()


# import json
# import tkinter as tk
# from tkinter import filedialog
#
# x = 'new'
# y = True
# z = 1234
#
# data = {
#     'x' : x,
#     'y' : y,
#     'z' : z
# }
#
# options = {}
# options['defaultextension'] = '.json'
# options['filetypes'] = [('JSON files', '.json'),('All files', '.*')]
#
# save_file_path=filedialog.asksaveasfilename(**options)
#
# with open(save_file_path, 'w') as f:
#     json.dump(data,f, indent=4)
#
# print(options)
# print(data)
#
# open_file_path = filedialog.askopenfilename(**options)
#
# with open(open_file_path, 'r') as f:
#     config = json.load(f)
#
# print(config["x"])
#
# root = tk.Tk()
# root.withdraw()




# # !/usr/bin/env python
#
# import tkinter as tk
# import time
#
# top = tk.Tk()
#
#
# def addText():
#     # make first change
#     oldText = L.cget("text")
#     newText = oldText + '\nfirst change'
#     L.configure(text=newText)
#
#     # wait 2 seconds
#     top.update_idletasks()
#     time.sleep(2)
#
#     # make second change
#     newText += '\nsecond change'
#     L.configure(text=newText)
#
#
# B = tk.Button(top, text="Change text", command=addText)
# L = tk.Label(top, text='orignal text')
#
# B.pack()
# L.pack()
# top.mainloop()



# from tkinter import *
#
# class Application(Frame):
#     def __init__(self, master):
#         Frame.__init__(self, master)
#         self.grid()
#         self.Create_Widgets()
#
#     def Create_Widgets(self):
#         for i in range(1, 11):
#             self.newmessage = Button(self, text="Button ID: %d" % i, command=lambda i=i: self.access(i))
#             self.newmessage.config(height=3, width=100)
#             self.newmessage.grid(column=0, row=i, sticky=NW)
#
#     def access(self,i):
#         print("hello",i)
#
# root=Tk()
# app = Application(root)
# root.mainloop()


# from tkinter import *
# # from tkinter import ttk
# import xml.etree.ElementTree as ET
#
# root = Tk()
#
# def Readstatus(key):
#     print(var.get(key))
#
# listTree = ET.parse('test.xml')
# listRoot = listTree.getroot()
#
# var = dict()
# count=1
# for child in listRoot:
#     var[child]=IntVar()
#     chk = Checkbutton(root, text='Text'+str(count), variable=var[child],
#                       command=lambda key=child: Readstatus(key))
#     count += 1
#     chk.pack()
#
# root.mainloop()



