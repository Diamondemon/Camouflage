from os import path,chdir
import time
from tkinter import Tk,Menu,Toplevel,Label,Button
import PIL.ImageTk
chdir(path.dirname(__file__))
import classes

#------------------------------------------ Tkinter Functions ------------------------------------------
class CamoWindow(Tk):
    pass

def Hide(event=None):
    """ Sets the main window to merge images"""
    for wid in window.grid_slaves():
        wid.grid_forget()
    IMH.grid(row=0,column=0)
    window.wm_deiconify()
    accueil.destroy()


def Find(event=None):
    """ Sets the main window to separate images"""
    for wid in window.grid_slaves():
        wid.grid_forget()
    IMF.grid(row=0,column=0)
    window.wm_deiconify()
    accueil.destroy()


def Hide_Text(event=None):
    """ Sets the main window to hide text in image"""
    for wid in window.grid_slaves():
        wid.grid_forget()
    IMHT.grid(row=0,column=0)
    window.wm_deiconify()
    accueil.destroy()


def Find_Text(event=None):
    """ Sets the main window to find potential text in image"""
    for wid in window.grid_slaves():
        wid.grid_forget()
    IMFT.grid(row=0,column=0)
    window.wm_deiconify()
    accueil.destroy()
    
def Gray_Img(event=None):
    
    for wid in window.grid_slaves():
        wid.grid_forget()
    IMG.grid(row=0,column=0)
    window.wm_deiconify()
    accueil.destroy()
    
def Border_Img(event=None):
    
    for wid in window.grid_slaves():
        wid.grid_forget()
    IMBo.grid(row=0,column=0)
    window.wm_deiconify()
    accueil.destroy()
    
def Blur_Img(event=None):
    
    for wid in window.grid_slaves():
        wid.grid_forget()
    IMBl.grid(row=0,column=0)
    window.wm_deiconify()
    accueil.destroy()
    
def Pxl_Img(event=None):
    
    for wid in window.grid_slaves():
        wid.grid_forget()
    IMP.grid(row=0,column=0)
    window.wm_deiconify()
    accueil.destroy()
    
def Simulate_Therm(event=None):
    
    for wid in window.grid_slaves():
        wid.grid_forget()
    ThSim.grid(row=0,column=0)
    window.wm_deiconify()
    accueil.destroy()
    
def Super_Therm(event=None):
    
    for wid in window.grid_slaves():
        wid.grid_forget()
    ThSup.grid(row=0,column=0)
    window.wm_deiconify()
    accueil.destroy()
    
def Gauss_Matrix(event=None):
    
    for wid in window.grid_slaves():
        wid.grid_forget()
    GF.grid(row=0,column=0)
    window.wm_deiconify()
    accueil.destroy()

def Zero_Func(event=None):
    for wid in window.grid_slaves():
        wid.grid_forget()
    ZF.grid(row=0,column=0)
    window.wm_deiconify()
    accueil.destroy()

def Deriv_Func(event=None):
    for wid in window.grid_slaves():
        wid.grid_forget()
    DF.grid(row=0,column=0)
    window.wm_deiconify()
    accueil.destroy()
        

window=Tk()
window.title("Manipulation d'images")
icontkinter = PIL.ImageTk.PhotoImage(file='spy.ico')
window.iconphoto(True,icontkinter)
window.wm_iconify()

menubar = Menu(window)
window.config(menu=menubar)
imgmenu=Menu(menubar)
imgmenu.add_command(label="Fusionner des images",command=Hide)
imgmenu.add_separator()
imgmenu.add_command(label="Trouver une image cachée",command=Find)
imgmenu.add_separator()
imgmenu.add_command(label="Cacher du Texte Dans une image",command=Hide_Text)
imgmenu.add_separator()
imgmenu.add_command(label="Trouver du Texte Dans une image",command=Find_Text)
imgmenu.add_separator()
imgmenu.add_command(label="Griser une image",command=Gray_Img)
imgmenu.add_separator()
imgmenu.add_command(label="Contouriser une image",command=Border_Img)
imgmenu.add_separator()
imgmenu.add_command(label="Flouter une image",command=Blur_Img)
imgmenu.add_separator()
imgmenu.add_command(label="Pixelliser",command=Pxl_Img)

jajamenu=Menu(menubar)
jajamenu.add_command(label="Simuler la chaleur",command=Simulate_Therm)
jajamenu.add_separator()
jajamenu.add_command(label="Thermo 2.0",command=Super_Therm)

mathsmenu=Menu(menubar)
mathsmenu.add_command(label="Gauss",command=Gauss_Matrix)
mathsmenu.add_separator()
mathsmenu.add_command(label="Zéro de fonction",command=Zero_Func)
mathsmenu.add_separator()
mathsmenu.add_command(label="Approximation de fonction",command=Deriv_Func)

menubar.add_cascade(label="Jeux d'images",menu=imgmenu)
menubar.add_cascade(label="IPT Jaja",menu=jajamenu)
menubar.add_cascade(label="Mathématiques",menu=mathsmenu)



IMF=classes.ImgFFrame(window)
IMH=classes.ImgHFrame(window)
IMHT=classes.ImgTFrame(window)
IMFT=classes.ImgGTFrame(window)
IMG=classes.ImgGFrame(window)
IMBo=classes.ImgBoFrame(window)
IMBl=classes.ImgBlFrame(window)
IMP=classes.ImgPixFrame(window)
ThSim=classes.SimuTherm(window)
ThSup=classes.SuperThSim(window)
GF=classes.GaussFrame(window)
ZF=classes.ZeroFrame(window)
DF=classes.DerivFrame(window)


accueil = Toplevel()
accueil.wm_attributes("-topmost", True)
accueil.title("Accueil Images")
accueil.configure(bg="#B6B0AD")


Do_Question = Label(accueil,text="Que voulez-vous faire?")
Do_Question.grid(row=0,column=0)


Do_Hide = Button(accueil,text="Cacher une image",command=Hide)
Do_Hide.grid(row=1,column=0)


Do_Detect = Button(accueil,text="Trouver une image",command=Find)
Do_Detect.grid(row=2,column=0)

Do_Text = Button(accueil,text="Cacher du texte",command=Hide_Text)
Do_Text.grid(row=3,column=0)

Do_Text_Get= Button(accueil,text="Récupérer un texte caché",command=Find_Text)
Do_Text_Get.grid(row=4,column=0)

Do_Gray = Button(accueil,text="Griser une image",command=Gray_Img)
Do_Gray.grid(row=5,column=0)

Do_Border = Button(accueil,text="Tracer les contours d'une image",command=Border_Img)
Do_Border.grid(row=0,column=1)

Do_Blur = Button(accueil,text="Flouter une image",command=Blur_Img)
Do_Blur.grid(row=1,column=1)

Do_Pixel = Button(accueil,text="Pixelliser une image",command=Pxl_Img)
Do_Pixel.grid(row=1,column=2)

Do_ThermoSimu = Button(accueil,text="Faire une simulation thermique",command=Simulate_Therm)
Do_ThermoSimu.grid(row=2,column=1)

Do_SuperThermo = Button(accueil,text="Faire une simulation thermique 2.0",command=Super_Therm)
Do_SuperThermo.grid(row=3,column=1)

Do_SuperThermo = Button(accueil,text="Résoudre un système linéaire",command=Gauss_Matrix)
Do_SuperThermo.grid(row=4,column=1)

Do_Zero = Button(accueil,text="Trouver le zéro d'une fonction",command=Zero_Func)
Do_Zero.grid(row=5,column=1)

Do_Deriv = Button(accueil,text="Approximer une fonction",command=Deriv_Func)
Do_Deriv.grid(row=2,column=2)

window.mainloop()