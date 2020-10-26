from os import path,chdir
from tkinter import Tk,Menu,Toplevel,Label,Button
import PIL.ImageTk
from functools import partial
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
        

window=CamoWindow()
# window.title("Manipulation d'images")
# icontkinter = PIL.ImageTk.PhotoImage(file='spy.ico')
# window.iconphoto(True,icontkinter)
# window.wm_iconify()
# 
# menubar = Menu(window)
# window.config(menu=menubar)
# imgmenu=Menu(menubar)
# imgmenu.add_command(label="Fusionner des images",command=Hide)
# imgmenu.add_separator()
# imgmenu.add_command(label="Trouver une image cachée",command=Find)
# imgmenu.add_separator()
# imgmenu.add_command(label="Cacher du Texte Dans une image",command=Hide_Text)
# imgmenu.add_separator()
# imgmenu.add_command(label="Trouver du Texte Dans une image",command=Find_Text)
# imgmenu.add_separator()
# imgmenu.add_command(label="Griser une image",command=Gray_Img)
# imgmenu.add_separator()
# imgmenu.add_command(label="Contouriser une image",command=Border_Img)
# imgmenu.add_separator()
# imgmenu.add_command(label="Flouter une image",command=Blur_Img)
# imgmenu.add_separator()
# imgmenu.add_command(label="Pixelliser",command=Pxl_Img)
# 
# jajamenu=Menu(menubar)
# jajamenu.add_command(label="Simuler la chaleur",command=Simulate_Therm)
# jajamenu.add_separator()
# jajamenu.add_command(label="Thermo 2.0",command=Super_Therm)
# 
# mathsmenu=Menu(menubar)
# mathsmenu.add_command(label="Gauss",command=Gauss_Matrix)
# mathsmenu.add_separator()
# mathsmenu.add_command(label="Zéro de fonction",command=Zero_Func)
# mathsmenu.add_separator()
# mathsmenu.add_command(label="Approximation de fonction",command=Deriv_Func)
# 
# menubar.add_cascade(label="Jeux d'images",menu=imgmenu)
# menubar.add_cascade(label="IPT Jaja",menu=jajamenu)
# menubar.add_cascade(label="Mathématiques",menu=mathsmenu)
# 
# 
# 
# IMF=classes.ImgFFrame(window)
# IMH=classes.ImgHFrame(window)
# IMHT=classes.ImgTFrame(window)
# IMFT=classes.ImgGTFrame(window)
# IMG=classes.ImgGFrame(window)
# IMBo=classes.ImgBoFrame(window)
# IMBl=classes.ImgBlFrame(window)
# IMP=classes.ImgPixFrame(window)
# ThSim=classes.SimuTherm(window)
# ThSup=classes.SuperThSim(window)
# GF=classes.GaussFrame(window)
# ZF=classes.ZeroFrame(window)
# DF=classes.DerivFrame(window)


    
accueil=HomePage()
        

# window.mainloop()