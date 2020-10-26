import os
import scipy.misc as scm
import numpy as np
import time
from tkinter import *
from tkinter.filedialog import *
import PIL.ImageTk,PIL.Image
os.chdir(os.path.dirname(__file__))
import gpu

#------------------------------------------ Tkinter Functions ------------------------------------------
def Hide(event=None):
    """ Sets the main window to merge images"""

    Mask_Display.delete("all")
    Hidden_Display.delete("all")
    Fuse_Display.delete("all")

    Hidden_Choice.grid_forget()
    Hidden_Display.grid_forget()
    Hide_Normal.grid_forget()
    Hide_Plus.grid_forget()

    Fuse_Choice.grid_forget()
    Fuse_Display.grid_forget()

    Find_Choice.grid_forget()
    Normal_Find.grid_forget()
    Plus_Find.grid_forget()

    Fuse_Register.grid_forget()

    Textbox.grid_forget()

    Hidden_Choice.grid(row=0,column=1,rowspan=2)
    Hidden_Display.grid(row=2,column=1,columnspan=2)
    Hide_Normal.grid(row=0,column=2)
    Hide_Plus.grid(row=1,column=2)

    Fuse_Choice.grid(row=0,column=3,rowspan=2)
    Fuse_Display.grid(row=2,column=3)
    window.wm_deiconify()
    accueil.destroy()


def Find(event=None):
    Mask_Display.delete("all")
    Hidden_Display.delete("all")
    Fuse_Display.delete("all")

    Hidden_Choice.grid_forget()
    Hidden_Display.grid_forget()
    Hide_Normal.grid_forget()
    Hide_Plus.grid_forget()

    Fuse_Choice.grid_forget()
    Fuse_Display.grid_forget()

    Find_Choice.grid_forget()
    Normal_Find.grid_forget()
    Plus_Find.grid_forget()

    Fuse_Register.grid_forget()

    Textbox.grid_forget()

    Find_Choice.grid(row=0,column=1,rowspan=2)
    Hidden_Display.grid(row=2,column=1,columnspan=2)
    Normal_Find.grid(row=0,column=2)
    Plus_Find.grid(row=1,column=2)
    window.wm_deiconify()
    accueil.destroy()


def Hide_Text(event=None):
    Mask_Display.delete("all")
    Hidden_Display.delete("all")
    Fuse_Display.delete("all")

    Hidden_Choice.grid_forget()
    Hidden_Display.grid_forget()
    Hide_Normal.grid_forget()
    Hide_Plus.grid_forget()

    Fuse_Choice.grid_forget()
    Fuse_Display.grid_forget()

    Find_Choice.grid_forget()
    Normal_Find.grid_forget()
    Plus_Find.grid_forget()

    Fuse_Register.grid_forget()

    Textbox.grid(row=2,column=1,columnspan=2)
    Text_Choice.grid(row=0,column=3,rowspan=2)
    Fuse_Display.grid(row=2,column=3)
    window.wm_deiconify()
    accueil.destroy()


def Find_Text(event=None):
    Mask_Display.delete("all")
    Hidden_Display.delete("all")
    Fuse_Display.delete("all")

    Hidden_Choice.grid_forget()
    Hidden_Display.grid_forget()
    Hide_Normal.grid_forget()
    Hide_Plus.grid_forget()

    Fuse_Choice.grid_forget()
    Fuse_Display.grid_forget()

    Find_Choice.grid_forget()
    Normal_Find.grid_forget()
    Plus_Find.grid_forget()

    Fuse_Register.grid_forget()

    Textbox.grid(row=2,column=1,columnspan=2)
    Get_Choice.grid(row=0,column=3,rowspan=2)
    Fuse_Display.grid(row=2,column=3)
    window.wm_deiconify()
    accueil.destroy()


def Mask_Choose(event=None):
    global displayed_img
    global mask_array

    filename=askopenfilename(title="Choisissez votre image",filetypes=[("Images Bitmap",".bmp"),("Images Jpeg",".jpg")],initialdir=os.path.dirname(__file__))


    if filename!="":
        Mask_Display.delete("all")
        pilImage=PIL.Image.open(filename)

        mask_temp = np.asarray(pilImage)
        mask_array = mask_temp.copy()


        height_ref=pilImage.height
        width_ref=pilImage.width

        if height_ref>360 or width_ref>360:
            if height_ref>width_ref:
                scale_ratio = 360/height_ref
                new_height = 360
                new_width = int(scale_ratio*width_ref)
            else:
                scale_ratio = 360/width_ref
                new_height = int(scale_ratio*height_ref)
                new_width = 360
            pilImage=pilImage.resize((new_width,new_height))

        displayed_img = PIL.ImageTk.PhotoImage(pilImage)

        Mask_Display.create_image(182,182,image=displayed_img)


def Hidden_Choose(event=None):
    global displayed_hidden
    global hidden_array

    filename=askopenfilename(title="Choisissez votre image",filetypes=[("Images Bitmap",".bmp"),("Images Jpeg",".jpg")],initialdir=os.path.dirname(__file__))


    if filename!="":
        Hidden_Display.delete("all")

        pilImage=PIL.Image.open(filename)
        hidden_temp = np.asarray(pilImage)
        hidden_array = hidden_temp.copy()

        height_ref=pilImage.height
        width_ref=pilImage.width

        if height_ref>360 or width_ref>360:
            if height_ref>width_ref:
                scale_ratio = 360/height_ref
                new_height = 360
                new_width = int(scale_ratio*width_ref)
            else:
                scale_ratio = 360/width_ref
                new_height = int(scale_ratio*height_ref)
                new_width = 360
            pilImage=pilImage.resize((new_width,new_height))

        displayed_hidden = PIL.ImageTk.PhotoImage(pilImage)

        Hidden_Display.create_image(182,182,image=displayed_hidden)


def Fuse(event=None):
    global displayed_fused
    global fused_array
    global mask_array
    global hidden_array

    if isinstance(mask_array,np.ndarray) and isinstance(hidden_array,np.ndarray):

        if mask_array.shape[0] >= hidden_array.shape[0] or mask_array.shape[1] >= hidden_array.shape[1]:

            mask_temp = mask_array.copy()
            hidden_temp = hidden_array.copy()
            fused_array = gpu.add_im(mask_temp,hidden_temp,hider.get())
            pilImage = PIL.Image.fromarray(fused_array)

            height_ref=pilImage.height
            width_ref=pilImage.width

            if height_ref>360 or width_ref>360:
                if height_ref>width_ref:
                    scale_ratio = 360/height_ref
                    new_height = 360
                    new_width = int(scale_ratio*width_ref)
                else:
                    scale_ratio = 360/width_ref
                    new_height = int(scale_ratio*height_ref)
                    new_width = 360
                pilImage=pilImage.resize((new_width,new_height))

            displayed_fused = PIL.ImageTk.PhotoImage(pilImage)

            Fuse_Display.create_image(182,182,image=displayed_fused)
            Fuse_Register.grid(row=3,column=3)


def Recup_Hidden(event=None):
    global fused_array
    global displayed_fused

    fused_array=mask_array.copy()

    if finder.get()=="simple":
        fused_array = gpu.bpf_c(fused_array)
    elif finder.get()=="plus":
        fused_array = gpu.bpf_cplus(fused_array)

    pilImage = PIL.Image.fromarray(fused_array)

    height_ref=pilImage.height
    width_ref=pilImage.width

    if height_ref>360 or width_ref>360:
        if height_ref>width_ref:
            scale_ratio = 360/height_ref
            new_height = 360
            new_width = int(scale_ratio*width_ref)
        else:
            scale_ratio = 360/width_ref
            new_height = int(scale_ratio*height_ref)
            new_width = 360
        pilImage=pilImage.resize((new_width,new_height))

    displayed_fused = PIL.ImageTk.PhotoImage(pilImage)

    Hidden_Display.create_image(182,182,image=displayed_fused)
    Fuse_Register.grid(row=3,column=1,columnspan=2)


def Text_Choose(event=None):
    global fused_array
    global displayed_fused
    text=Textbox.get(1.0,"end")
    textlist=list(text)
    temp_array=mask_array.copy()
    fused_array=gpu.Txt_In_Image(temp_array,textlist)

    pilImage = PIL.Image.fromarray(fused_array)

    height_ref=pilImage.height
    width_ref=pilImage.width

    if height_ref>360 or width_ref>360:
        if height_ref>width_ref:
            scale_ratio = 360/height_ref
            new_height = 360
            new_width = int(scale_ratio*width_ref)
        else:
            scale_ratio = 360/width_ref
            new_height = int(scale_ratio*height_ref)
            new_width = 360
        pilImage=pilImage.resize((new_width,new_height))

    displayed_fused = PIL.ImageTk.PhotoImage(pilImage)

    Fuse_Display.create_image(182,182,image=displayed_fused)
    Fuse_Register.grid(row=3,column=3)

def Get_Text_Choose(event=None):
    global fused_array
    global displayed_fused

def Register(event=None):

    filename=asksaveasfilename(title="Enregistrer l'image",filetypes=[("Images Bitmap",".bmp"),("Images Jpeg",".jpg")],defaultextension=[".bmp",".jpg"],initialfile=["ImageCachee"])
    if filename!="":
        scm.imsave(filename,fused_array)




window=Tk()
window.title("Manipulation d'images")
icontkinter = PIL.ImageTk.PhotoImage(file='spy.ico')
window.iconphoto(True,icontkinter)
window.wm_iconify()

menubar = Menu(window)
window.config(menu=menubar)
optionsmenu=Menu(menubar)
optionsmenu.add_command(label="Fusionner des images",command=Hide)
optionsmenu.add_separator()
optionsmenu.add_command(label="Trouver une image cachée",command=Find)
optionsmenu.add_separator()
optionsmenu.add_command(label="Cacher du Texte Dans une image",command=Hide_Text)
optionsmenu.add_separator()
optionsmenu.add_command(label="Trouver du Texte Dans une image",command=Find_Text)
menubar.add_cascade(label="Options",menu=optionsmenu)

displayed_img=None
displayed_hidden=None
displayed_fused=None

mask_array=None
hidden_array=None
fused_array=None

hider=StringVar()
hider.set("simple")

finder = StringVar()
finder.set("simple")


Mask_Choice = Button(window,text="Choisir une image",command=Mask_Choose)
Mask_Choice.grid(row=0,column=0,rowspan=2)

Mask_Display = Canvas(window,width=360,height=360,bg="#888888")
Mask_Display.grid(row=2,column=0)


Hidden_Choice = Button(window,text="Choisir l'image à cacher",command=Hidden_Choose)
Hide_Normal=Radiobutton(window,variable=hider,text="Fusion simple",value="simple")
Hide_Plus=Radiobutton(window,variable=hider,text="Fusion locale",value="plus")

Find_Choice = Button(window,text="Trouver l'image cachée",command=Recup_Hidden)
Normal_Find = Radiobutton(window,variable=finder,text="Recherche simple",value="simple")
Plus_Find = Radiobutton(window,variable=finder,text="Recherche précise",value="plus")

Text_Choice=Button(window,text="Cacher le texte",command=Text_Choose)
Get_Choice=Button(window,text="Récupérer le texte",command=Get_Text_Choose)

Hidden_Display=Canvas(window,width=360,height=360,bg="white")



Fuse_Choice = Button(window,text="Fusionner",command=Fuse)

Fuse_Display = Canvas(window,width=360,height=360,bg="black")

Fuse_Register = Button(window,text="Sauvegarder",command=Register)

Textbox = Text(window,width=40,height=20)

accueil = Toplevel()
accueil.wm_attributes("-topmost", True)
accueil.title("Accueil CryptoMessenger")
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


window.mainloop()