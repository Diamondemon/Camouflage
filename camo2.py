from os import path,chdir
from tkinter import Tk,Menu,Toplevel,Label,Button
import PIL.ImageTk
from functools import partial
chdir(path.dirname(__file__))
import classes

# ------------------------------------------ Tkinter Functions ------------------------------------------


class CamoWindow(Tk):
    
    def __init__(self):
        Tk.__init__(self)
        self.title("Manipulation d'images")
        icontkinter = PIL.ImageTk.PhotoImage(file='spy.ico')
        self.iconphoto(True, icontkinter)
        
        self.HF=classes.HomeFrame(self)
        self.IMF=classes.ImgFFrame(self)
        self.IMH=classes.ImgHFrame(self)
        self.IMHT=classes.ImgTFrame(self)
        self.IMFT=classes.ImgGTFrame(self)
        self.IMG=classes.ImgGFrame(self)
        self.IMBo=classes.ImgBoFrame(self)
        self.IMBl=classes.ImgBlFrame(self)
        self.IMSh=classes.ImgSharpFrame(self)
        self.IMP=classes.ImgPixFrame(self)
        self.IMN=classes.ImgNegFrame(self)
        self.IMC=classes.ImgCropFrame(self)
        self.IMCv=classes.ImgConvFrame(self)
        self.ThSim=classes.SimuTherm(self)
        self.ThSup=classes.SuperThSim(self)
        self.GF=classes.GaussFrame(self)
        self.ZF=classes.ZeroFrame(self)
        self.DF=classes.DerivFrame(self)
        
        self.menubar = Menu(self)
        self.config(menu=self.menubar)
        self.imgmenu=Menu(self.menubar)
        self.imgmenu.add_command(label="Fusionner des images",command=self.Hide)
        self.imgmenu.add_separator()
        self.imgmenu.add_command(label="Trouver une image cachée",command=self.Find)
        self.imgmenu.add_separator()
        self.imgmenu.add_command(label="Cacher du Texte Dans une image",command=self.Hide_Text)
        self.imgmenu.add_separator()
        self.imgmenu.add_command(label="Trouver du Texte Dans une image",command=self.Find_Text)
        self.imgmenu.add_separator()
        self.imgmenu.add_command(label="Griser une image",command=self.Gray_Img)
        self.imgmenu.add_separator()
        self.imgmenu.add_command(label="Contouriser une image",command=self.Border_Img)
        self.imgmenu.add_separator()
        self.imgmenu.add_command(label="Flouter une image",command=self.Blur_Img)
        self.imgmenu.add_separator()
        self.imgmenu.add_command(label="Améliorer une image (broken)",command=self.Sharpen_Img)
        self.imgmenu.add_separator()
        self.imgmenu.add_command(label="Pixelliser",command=self.Pxl_Img)
        self.imgmenu.add_separator()
        self.imgmenu.add_command(label="Faire le négatif",command=self.Neg_Img)
        self.imgmenu.add_separator()
        self.imgmenu.add_command(label="Rogner une image",command=self.Crop_Img)
        self.imgmenu.add_separator()
        self.imgmenu.add_command(label="Convertir une image",command=self.Conv_Img)
        
        self.jajamenu=Menu(self.menubar)
        self.jajamenu.add_command(label="Simuler la chaleur",command=self.Simulate_Therm)
        self.jajamenu.add_separator()
        self.jajamenu.add_command(label="Thermo 2.0",command=self.Super_Therm)
        
        self.mathsmenu=Menu(self.menubar)
        self.mathsmenu.add_command(label="Gauss",command=self.Gauss_Matrix)
        self.mathsmenu.add_separator()
        self.mathsmenu.add_command(label="Zéro de fonction",command=self.Zero_Func)
        self.mathsmenu.add_separator()
        self.mathsmenu.add_command(label="Approximation de fonction",command=self.Deriv_Func)
        
        self.menubar.add_cascade(label="Jeux d'images",menu=self.imgmenu)
        self.menubar.add_cascade(label="IPT Jaja",menu=self.jajamenu)
        self.menubar.add_cascade(label="Mathématiques",menu=self.mathsmenu)
        
        self.HF.grid(row=0,column=0)

    def Hide(self,event=None):
        """ Sets the main window to merge images"""
        for wid in self.grid_slaves():
            wid.grid_forget()
        self.IMH.grid(row=0,column=0)

    def Find(self,event=None):
        """ Sets the main window to separate images"""
        for wid in self.grid_slaves():
            wid.grid_forget()
        self.IMF.grid(row=0,column=0)

    def Hide_Text(self,event=None):
        """ Sets the main window to hide text in image"""
        for wid in self.grid_slaves():
            wid.grid_forget()
        self.IMHT.grid(row=0,column=0)

    def Find_Text(self,event=None):
        """ Sets the main window to find potential text in image"""
        for wid in self.grid_slaves():
            wid.grid_forget()
        self.IMFT.grid(row=0,column=0)

    def Gray_Img(self,event=None):
        
        for wid in self.grid_slaves():
            wid.grid_forget()
        self.IMG.grid(row=0,column=0)

    def Border_Img(self,event=None):
        
        for wid in self.grid_slaves():
            wid.grid_forget()
        self.IMBo.grid(row=0,column=0)

    def Blur_Img(self,event=None):
        
        for wid in self.grid_slaves():
            wid.grid_forget()
        self.IMBl.grid(row=0,column=0)

    def Sharpen_Img(self, event=None):

        for wid in self.grid_slaves():
            wid.grid_forget()
        self.IMSh.grid(row=0,column=0)


    def Pxl_Img(self,event=None):
        
        for wid in self.grid_slaves():
            wid.grid_forget()
        self.IMP.grid(row=0,column=0)
        
    def Neg_Img(self,event=None):
        
        for wid in self.grid_slaves():
            wid.grid_forget()
        self.IMN.grid(row=0,column=0)
        
    def Crop_Img(self,event=None):
        
        for wid in self.grid_slaves():
            wid.grid_forget()
        self.IMC.grid(row=0,column=0)

    def Conv_Img(self,event=None):

        for wid in self.grid_slaves():
            wid.grid_forget()
        self.IMCv.grid(row=0,column=0)

    def Simulate_Therm(self,event=None):
        
        for wid in self.grid_slaves():
            wid.grid_forget()
        self.ThSim.grid(row=0,column=0)

    def Super_Therm(self,event=None):
        
        for wid in self.grid_slaves():
            wid.grid_forget()
        self.ThSup.grid(row=0,column=0)

    def Gauss_Matrix(self,event=None):
        
        for wid in self.grid_slaves():
            wid.grid_forget()
        self.GF.grid(row=0,column=0)

    def Zero_Func(self,event=None):
        for wid in self.grid_slaves():
            wid.grid_forget()
        self.ZF.grid(row=0,column=0)

    def Deriv_Func(self,event=None):
        for wid in self.grid_slaves():
            wid.grid_forget()
        self.DF.grid(row=0,column=0)


window = CamoWindow()

window.mainloop()
