from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import ttk
import matplotlib
import numpy as np
import PIL.ImageTk, PIL.Image
from os import path, chdir
from scipy.misc import imsave
from colour import Color
from scipy.integrate import odeint
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

matplotlib.use("TkAgg")

chdir(path.dirname(__file__))
import gpu
import cpu


# Accueil

class HomeFrame(Frame):

    def __init__(self, master=None, **kwargs):
        Frame.__init__(self, master, kwargs)

        self.configure(bg="#B6B0AD")

        self.Do_Question = Label(self, text="Que voulez-vous faire?")
        self.Do_Hide = Button(self, text="Cacher une image", command=master.Hide)
        self.Do_Detect = Button(self, text="Trouver une image", command=master.Find)
        self.Do_Text = Button(self, text="Cacher du texte", command=master.Hide_Text)
        self.Do_Text_Get = Button(self, text="Récupérer un texte caché", command=master.Find_Text)
        self.Do_Gray = Button(self, text="Griser une image", command=master.Gray_Img)
        self.Do_Border = Button(self, text="Tracer les contours d'une image", command=master.Border_Img)
        self.Do_Blur = Button(self, text="Flouter une image", command=master.Blur_Img)
        self.Do_Pixel = Button(self, text="Pixelliser une image", command=master.Pxl_Img)
        self.Do_Invert = Button(self, text="Faire le négatif d'une image", command=master.Neg_Img)
        self.Do_ThermoSimu = Button(self, text="Faire une simulation thermique", command=master.Simulate_Therm)
        self.Do_SuperThermo = Button(self, text="Faire une simulation thermique 2.0", command=master.Super_Therm)
        self.Do_SolveSys = Button(self, text="Résoudre un système linéaire", command=master.Gauss_Matrix)
        self.Do_Zero = Button(self, text="Trouver le zéro d'une fonction", command=master.Zero_Func)
        self.Do_Deriv = Button(self, text="Approximer une fonction", command=master.Deriv_Func)

        self.Do_Question.grid(row=0, column=0)
        self.Do_Hide.grid(row=1, column=0)
        self.Do_Detect.grid(row=2, column=0)
        self.Do_Text.grid(row=3, column=0)
        self.Do_Text_Get.grid(row=4, column=0)
        self.Do_Gray.grid(row=5, column=0)
        self.Do_Border.grid(row=0, column=1)
        self.Do_Blur.grid(row=1, column=1)
        self.Do_Pixel.grid(row=1, column=2)
        self.Do_ThermoSimu.grid(row=2, column=1)
        self.Do_SuperThermo.grid(row=3, column=1)
        self.Do_SolveSys.grid(row=4, column=1)
        self.Do_Zero.grid(row=5, column=1)
        self.Do_Deriv.grid(row=2, column=2)


### Images

class ImgFrame(Frame):
    """Basic Parent Frame widget for all Frame widgets that manipulate images. Useless on its own."""

    def __init__(self, master=None, options={}):
        Frame.__init__(self, master, options)
        self.displayed_img = None
        self.mask_array = None
        self.displayed_fused = None
        self.fused_array = None
        self.Mask_Choice = Button(self, text="Choisir une image", command=self.Mask_Chose)
        self.Fused_Register = Button(self, text="Sauvegarder", command=self.Register)
        self.Mask_Choice.grid(row=0, column=0, rowspan=2)

        self.Mask_Display = Canvas(self, width=360, height=360, bg="#fff")
        self.Fused_Display = Canvas(self, width=360, height=360, bg="#000")
        self.draw_chess()
        self.Mask_Display.grid(row=2, column=0, rowspan=5)
        self.Fused_Display.grid(row=2, column=3, columnspan=3, rowspan=5)

    def Mask_Chose(self, event=None):
        filename = askopenfilename(title="Choisissez votre image",
                                   filetypes=[("Toute image", (".bmp", ".png", ".jpg", ".ico", ".jpeg", ".raw")),
                                              ("Images Bitmap", ".bmp"), ("Images Jpeg", (".jpg", ".jpeg")),
                                              ("Images PNG", ".png"), ("Icônes", ".ico"), ("Images RAW", ".raw")],
                                   defaultextension=[".bmp", ".jpg", ".png"])

        if filename != "":
            self.Mask_Display.delete("mask")
            pilImage = PIL.Image.open(filename)

            mask_temp = np.asarray(pilImage)
            self.mask_array = mask_temp.copy()

            height_ref = pilImage.height
            width_ref = pilImage.width

            if height_ref > 360 or width_ref > 360:
                if height_ref > width_ref:
                    scale_ratio = 360 / height_ref
                    new_height = 360
                    new_width = int(scale_ratio * width_ref)
                else:
                    scale_ratio = 360 / width_ref
                    new_height = int(scale_ratio * height_ref)
                new_width = 360
                pilImage = pilImage.resize((new_width, new_height))

            self.displayed_img = PIL.ImageTk.PhotoImage(pilImage)

            self.Mask_Display.create_image(182, 182, image=self.displayed_img, tag="mask")
            return True

    def Fused_Draw(self, event=None):

        self.Fused_Display.delete("fused")
        pilImage = PIL.Image.fromarray(self.fused_array)

        height_ref = pilImage.height
        width_ref = pilImage.width

        if height_ref > 360 or width_ref > 360:
            if height_ref > width_ref:
                scale_ratio = 360 / height_ref
                new_height = 360
                new_width = int(scale_ratio * width_ref)
            else:
                scale_ratio = 360 / width_ref
                new_height = int(scale_ratio * height_ref)
                new_width = 360
            pilImage = pilImage.resize((new_width, new_height))

        self.displayed_fused = PIL.ImageTk.PhotoImage(pilImage)

        self.Fused_Display.create_image(182, 182, image=self.displayed_fused, tag="fused")

    def draw_chess(self):
        """ Draws the background composition for the pictures """
        for i in range(0, 18):
            for j in range(0, 18):
                if (i + j) % 2 == 1:
                    self.Mask_Display.create_rectangle(20 * i + 2, 20 * j + 2, 20 * i + 22, 20 * j + 22, width=0,
                                                       fill="#ccc")
                    self.Fused_Display.create_rectangle(20 * i + 2, 20 * j + 2, 20 * i + 22, 20 * j + 22, width=0,
                                                        fill="#ccc")

    def Register(self, event=None):

        filename = asksaveasfilename(title="Enregistrer l'image",
                                     filetypes=[("Toute image", (".bmp", ".png", ".jpg", ".ico", ".jpeg", ".raw")),
                                                ("Images Bitmap", ".bmp"), ("Images Jpeg", (".jpg", ".jpeg")),
                                                ("Images PNG", ".png"), ("Icônes", ".ico"), ("Images RAW", ".raw")],
                                     defaultextension=[".bmp", ".jpg", ".png"], initialfile=["Image"])
        if filename != "":
            if not (self.fused_array.shape[2]>3 and (filename[-4:]==".jpg" or filename[-5:]==".jpeg")):
                imsave(filename, self.fused_array)

            else:
                raise TypeError("Le format JPG ne sait pas gérer la transparence.")

    def grid_forget(self, event=None):
        Frame.grid_forget(self)
        self.mask_array = None
        self.fused_array = None
        self.displayed_img = None
        self.displayed_fused = None
        self.Mask_Display.delete("mask")
        self.Fused_Display.delete("fused")
        self.Fused_Register.grid_forget()


## Cacher une image
class ImgHFrame(ImgFrame):
    """Frame widget to hide an image inside another one"""

    def __init__(self, master=None, **kwargs):

        ImgFrame.__init__(self, master, kwargs)

        self.displayed_hidden = None
        self.hidden_array = None

        self.hider = StringVar()
        self.hider.set("simple")

        self.Hidden_Display = Canvas(self, width=360, height=360, bg="white")
        self.draw_chess_hidden()
        self.Hidden_Choice = Button(self, text="Choisir l'image à cacher", command=self.Hidden_Chose)
        self.Hide_Normal = Radiobutton(self, variable=self.hider, text="Fusion simple", value="simple")
        self.Hide_Plus = Radiobutton(self, variable=self.hider, text="Fusion locale", value="plus")

        self.Hidden_Display.grid(row=2, column=1, columnspan=2, rowspan=5)
        self.Hidden_Choice.grid(row=0, column=1, rowspan=2)
        self.Hide_Normal.grid(row=0, column=2)
        self.Hide_Plus.grid(row=1, column=2)

        self.Fuse_Choice = Button(self, text="Fusionner", command=self.Fuse)

        self.Fuse_Choice.grid(row=0, column=3, rowspan=2, columnspan=3)

    def draw_chess_hidden(self):
        """ Draws the background composition for the pictures """
        for i in range(0, 18):
            for j in range(0, 18):
                if (i + j) % 2 == 0:
                    self.Hidden_Display.create_rectangle(20 * i + 2, 20 * j + 2, 20 * i + 22, 20 * j + 22, width=0,
                                                         fill="#ccc")

    def Hidden_Chose(self, event=None):

        filename = askopenfilename(title="Choisissez votre image",
                                   filetypes=[("Toute image", (".bmp", ".png", ".jpg", ".ico", ".jpeg", ".raw")),
                                              ("Images Bitmap", ".bmp"), ("Images Jpeg", (".jpg", ".jpeg")),
                                              ("Images PNG", ".png"), ("Icônes", ".ico"), ("Images RAW", ".raw")],
                                   defaultextension=[".bmp", ".jpg", ".png"])
        if filename != "":
            self.Hidden_Display.delete("hidden")

            pilImage = PIL.Image.open(filename)
            hidden_temp = np.asarray(pilImage)
            self.hidden_array = hidden_temp.copy()

            height_ref = pilImage.height
            width_ref = pilImage.width

            if height_ref > 360 or width_ref > 360:
                if height_ref > width_ref:
                    scale_ratio = 360 / height_ref
                    new_height = 360
                    new_width = int(scale_ratio * width_ref)
                else:
                    scale_ratio = 360 / width_ref
                    new_height = int(scale_ratio * height_ref)
                    new_width = 360
                pilImage = pilImage.resize((new_width, new_height))

            self.displayed_hidden = PIL.ImageTk.PhotoImage(pilImage)

            self.Hidden_Display.create_image(182, 182, image=self.displayed_hidden, tag="hidden")

    def Fuse(self, event=None):

        if isinstance(self.mask_array, np.ndarray) and isinstance(self.hidden_array, np.ndarray):

            if self.mask_array.shape[0] >= self.hidden_array.shape[0] and self.mask_array.shape[1] >= \
                    self.hidden_array.shape[1]:

                if len(self.mask_array.shape) == len(self.hidden_array.shape):
                    mask_temp = self.mask_array.copy()
                    hidden_temp = self.hidden_array.copy()
                    self.fused_array = gpu.add_im(mask_temp, hidden_temp, self.hider.get())
                    ImgFrame.Fused_Draw(self)

                    self.Fused_Register.grid(row=7, column=3, columnspan=3)

    def grid_forget(self, event=None):
        ImgFrame.grid_forget(self)
        self.displayed_hidden = None

        self.hidden_array = None

        self.hider.set("simple")

        self.Hidden_Display.delete("hidden")


# Trouver une image

class ImgFFrame(ImgFrame):
    """Frame widget to find an image hidden inside another one"""

    def __init__(self, master=None, **kwargs):
        ImgFrame.__init__(self, master, kwargs)

        self.finder = StringVar()
        self.finder.set("simple")

        self.Find_Choice = Button(self, text="Trouver l'image cachée", command=self.Recup_Hidden)

        self.Normal_Find = Radiobutton(self, variable=self.finder, text="Recherche simple", value="simple")
        self.Plus_Find = Radiobutton(self, variable=self.finder, text="Recherche précise", value="plus")

        self.Find_Choice.grid(row=0, column=3, rowspan=2)

        self.Normal_Find.grid(row=0, column=4, columnspan=2)
        self.Plus_Find.grid(row=1, column=4, columnspan=2)

    def Recup_Hidden(self, event=None):

        if isinstance(self.mask_array, np.ndarray):

            self.fused_array = self.mask_array.copy()

            if self.finder.get() == "simple":
                self.fused_array = gpu.bpf_c(self.fused_array)
            elif self.finder.get() == "plus":
                self.fused_array = gpu.bpf_cplus(self.fused_array)

            ImgFrame.Fused_Draw(self)
            self.Fused_Register.grid(row=7, column=3, columnspan=3)

    def grid_forget(self, event=None):
        ImgFrame.grid_forget(self)

        self.finder.set("simple")


# Cacher du texte
class ImgTFrame(ImgFrame):
    """Frame widget to hide text into an image"""

    def __init__(self, master=None, **kwargs):
        ImgFrame.__init__(self, master, kwargs)

        self.Textbox = Text(self, width=40, height=20, wrap="word")
        self.Text_Choice = Button(self, text="Cacher le texte", command=self.Text_Choose)

        self.Textbox.grid(row=2, column=1, columnspan=2, rowspan=5)
        self.Text_Choice.grid(row=0, column=3, rowspan=2, columnspan=3)

    def Text_Choose(self, event=None):

        if isinstance(self.mask_array, np.ndarray):
            text = self.Textbox.get(1.0, "end")
            temp_array = self.mask_array.copy()

            if temp_array.shape[0] * temp_array.shape[1] * temp_array.shape[2] >= len(text):
                self.fused_array = gpu.Txt_In_Image(temp_array, text)

                ImgFrame.Fused_Draw(self)
                self.Fused_Register.grid(row=7, column=3, columnspan=3)

    def grid_forget(self, event=None):
        ImgFrame.grid_forget(self)

        self.Textbox.delete(1.0, "end")


# Trouver du texte


class ImgGTFrame(ImgFrame):
    """Frame widget to find potential text hidden in image"""

    def __init__(self, master=None, **kwargs):
        ImgFrame.__init__(self, master, kwargs)
        self.Fused_Display.grid_forget()

        self.Textbox = Text(self, width=80, height=20, wrap="word")
        self.Text_Finder = Button(self, text="Trouver le texte caché", command=self.GeTxt)

        self.Clear_Button = Button(self, text="Vider le texte", command=self.Text_Clear)

        self.Textbox.grid(row=2, column=1)
        self.Text_Finder.grid(row=0, column=1)
        self.Clear_Button.grid(row=3, column=1)

    def GeTxt(self, event=None):
        if isinstance(self.mask_array, np.ndarray):
            temp_array = self.mask_array.copy()
            text = gpu.Get_Txt(temp_array)
            self.Textbox.insert("end", text)

    def Text_Clear(self, event=None):
        self.Textbox.delete(1.0, "end")

    def grid_forget(self, event=None):
        ImgFrame.grid_forget(self)
        self.Textbox.delete(1.0, "end")


# Griser une image


class ImgGFrame(ImgFrame):
    """Frame widget to convert an RGB colored Image into a Black & White Image"""

    def __init__(self, master=None, **kwargs):
        ImgFrame.__init__(self, master, kwargs)

        self.Gray_Choice = Button(self, text="Griser l'image", command=self.Make_Gray)

        self.Gray_Choice.grid(row=0, column=3, rowspan=2, columnspan=2)
        self.Norm_Choice = Spinbox(self, values=(601, 709))
        Label(self, text="Norme de grisage").grid(row=0, column=5)
        self.Norm_Choice.grid(row=1, column=5)

    def Make_Gray(self, event=None):
        if isinstance(self.mask_array, np.ndarray):
            norm = int(self.Norm_Choice.get())
            self.fused_array = gpu.Rgb_2_Gray(self.mask_array, norm)
            ImgFrame.Fused_Draw(self)
            self.Fused_Register.grid(row=7, column=3, columnspan=3)


# Trouver les contours

class ImgBoFrame(ImgFrame):
    """Frame widget for Border Detection on image"""

    def __init__(self, master=None, **kwargs):
        ImgFrame.__init__(self, master, kwargs)

        self.Border_Choice = Button(self, text="Contouriser l'image", command=self.Draw_Borders)

        self.Threshold_Label = Label(self, text="Seuil de détection:")
        self.Threshold_Choice = Spinbox(self, from_=0, to=255,width=5,state="readonly")

        self.Border_Choice.grid(row=0, column=3, columnspan=2, rowspan=2)
        self.Norm_Label = Label(self, text="Norme de grisage")
        self.Norm_Choice = Spinbox(self, values=(601, 709))
        self.Algorithm_Choice = ttk.Combobox(self, width=18,
                                             values=["Cours d'IPT", "Simple convolution", "Prewitt", "Sobel", "Canny"],
                                             state="readonly")
        self.Algorithm_Choice.current(0)
        self.Algorithm_Choice.bind("<<ComboboxSelected>>", func=self.change_algorithm)
        self.Threshold_Label.grid(row=4, column=6)
        self.Threshold_Choice.grid(row=5, column=6)

        Label(self, text="Choix d'algorithme:").grid(row=2,column=6)
        self.Algorithm_Choice.grid(row=3,column=6)

        self.Goabs_Label = Label(self, text="Absolu?")
        self.Goabs_Choice = Spinbox(self, values=(0, 1))

    def Mask_Chose(self, event=None):
        ImgFrame.Mask_Chose(self, event)
        if len(self.mask_array.shape) == 3:
            self.Norm_Label.grid(row=0, column=5)
            self.Norm_Choice.grid(row=1, column=5)
        else:
            self.Norm_Choice.grid_forget()

    def change_algorithm(self, event=None):
        """ Function that triggers the appearing of the right widgets according to the chosen algorithm """
        val = self.Algorithm_Choice.get()

        if val == "Cours d'IPT":
            for wid in self.grid_slaves(column=6):
                if wid.grid_info()["row"]>=4:
                    wid.grid_forget()

            self.Threshold_Label.grid(row=4,column=6)
            self.Threshold_Choice.grid(row=5,column=6)


        elif val == "Simple convolution":
            for wid in self.grid_slaves(column=6):
                if wid.grid_info()["row"] >= 4:
                    wid.grid_forget()

        elif val == "Prewitt":
            for wid in self.grid_slaves(column=6):
                if wid.grid_info()["row"] >= 4:
                    wid.grid_forget()

        elif val == "Sobel":
            for wid in self.grid_slaves(column=6):
                if wid.grid_info()["row"] >= 4:
                    wid.grid_forget()

            self.Goabs_Label.grid(row=4,column=6)
            self.Goabs_Choice.grid(row=5,column=6)

        elif val == "Canny":
            for wid in self.grid_slaves(column=6):
                if wid.grid_info()["row"] >= 4:
                    wid.grid_forget()


    def Draw_Borders(self, event=None):
        """ Function that calls the border detection functions and displays the result """
        if isinstance(self.mask_array, np.ndarray):
            # todo: adapter pour png
            if len(self.mask_array.shape) == 3:
                norm = int(self.Norm_Choice.get())
                temp_array = gpu.Rgb_2_Gray(self.mask_array, norm)
            else:
                temp_array = self.mask_array.copy()

            val = self.Algorithm_Choice.get()

            if val == "Cours d'IPT":
                seuil = int(self.Threshold_Choice.get())
                self.fused_array = gpu.Shape_Detect(temp_array, seuil)


            elif val == "Simple convolution":
                kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
                self.fused_array = gpu.Convolve2D(temp_array, kernel, 1, 1)

            elif val == "Prewitt":
                self.fused_array = gpu.Prewitt(temp_array)

            elif val == "Sobel":
                self.fused_array = gpu.Sobel(temp_array, int(self.Goabs_Choice.get()))

            elif val == "Canny":
                self.fused_array = gpu.Canny(temp_array)

            ImgFrame.Fused_Draw(self)
            self.Fused_Register.grid(row=7, column=3, columnspan=3)

    def grid_forget(self, event=None):
        ImgFrame.grid_forget(self)
        self.Norm_Choice.grid_forget()


# Flouter une image


class ImgBlFrame(ImgFrame):
    """Frame widget for Bluring Image"""

    def __init__(self, master=None, **kwargs):
        ImgFrame.__init__(self, master, kwargs)

        self.Border_Choice = Button(self, text="Flouter l'image", command=self.Blur_Image)

        self.Border_Choice.grid(row=0, column=3, columnspan=2, rowspan=2)
        self.Norm_Choice = Spinbox(self, values=(601, 709))

        self.Algorithm_Choice = ttk.Combobox(self, width=16,
                                             values=["Filtre Moyenneur", "Gauss 3x3", "Gauss 5x5"],
                                             state="readonly")
        self.Algorithm_Choice.current(0)
        self.Algorithm_Choice.grid(row=1,column=5)

    def Mask_Chose(self, event=None):
        ImgFrame.Mask_Chose(self, event)
        if len(self.mask_array.shape) == 3:
            self.Norm_Choice.grid(row=0, column=5)
        else:
            self.Norm_Choice.grid_forget()

    def Blur_Image(self, event=None):

        if isinstance(self.mask_array, np.ndarray):
            # todo: adapter pour png
            if len(self.mask_array.shape) == 3:
                norm = int(self.Norm_Choice.get())
                temp_array = gpu.Rgb_2_Gray(self.mask_array, norm)
            else:
                temp_array = self.mask_array.copy()

            val = self.Algorithm_Choice.get()

            if val == "Filtre Moyenneur":
                self.fused_array = gpu.Blur(temp_array)
            elif val == "Gauss 3x3":
                self.fused_array = gpu.Blur_Gauss(temp_array,3)
            elif val == "Gauss 3x3":
                self.fused_array = gpu.Blur_Gauss(temp_array,5)

            ImgFrame.Fused_Draw(self)
            self.Fused_Register.grid(row=7, column=3, columnspan=3)

    def grid_forget(self, event=None):
        ImgFrame.grid_forget(self)
        self.Norm_Choice.grid_forget()

# Améliorer la netteté


class ImgSharpFrame(ImgFrame):

    def __init__(self,master=None,**kwargs):
        ImgFrame.__init__(self,master,kwargs)
        self.method=StringVar(value="Netteté")
        self.Proceed_Choice=Button(self, text="Procéder", command=self.Proceed)
        self.Sharpen_Choice=Radiobutton(self, text="Améliorer la netteté", variable=self.method, value="Netteté")
        self.Pike_Choice=Radiobutton(self,text="Améliorer le piqué",variable=self.method, value="Piqué")

        self.Proceed_Choice.grid(row=0, column=3, rowspan=2)
        self.Sharpen_Choice.grid(row=0, column=4, columnspan=2)
        self.Pike_Choice.grid(row=1, column=4, columnspan=2)

    def Proceed(self,event=None):
        if isinstance(self.mask_array, np.ndarray):
            if self.method.get() == "Netteté":
                if len(self.mask_array.shape)==3:
                    self.fused_array = gpu.Sharpen3D(self.mask_array)
                else:
                    self.fused_array = gpu.Sharpen(self.mask_array)

            elif self.method.get() == "Piqué":
                if len(self.mask_array.shape)==3:
                    self.fused_array = gpu.Blur_Mask3D(self.mask_array)
                else:
                    self.fused_array = gpu.Blur_Mask(self.mask_array)

            ImgFrame.Fused_Draw(self)
            self.Fused_Register.grid(row=7, column=3, columnspan=3)

# Pixelliser une image


class ImgPixFrame(ImgFrame):
    """Frame widget to make a thumbnail out of the imported image"""

    def __init__(self, master=None, **kwargs):
        ImgFrame.__init__(self, master, kwargs)

        self.pixel_xrate = DoubleVar()
        self.pixel_xrate.set(2)
        self.pixel_yrate = DoubleVar()
        self.pixel_yrate.set(2)
        self.Pixel_Choice = Button(self, text="Pixelliser", command=self.Pixellize)
        self.Rate_xChoice = Entry(self, textvariable=self.pixel_xrate, width=4)
        self.Rate_yChoice = Entry(self, textvariable=self.pixel_yrate, width=4)

        Label(self, text="Diviser la hauteur par ").grid(row=0, column=3)
        Label(self, text="Diviser la largeur par ").grid(row=1, column=3)
        self.Rate_xChoice.grid(row=1, column=4)
        self.Rate_yChoice.grid(row=0, column=4)
        self.Pixel_Choice.grid(row=0, column=5, rowspan=2)

    def Pixellize(self, event=None):

        if isinstance(self.mask_array, np.ndarray):
            xrate = int(self.pixel_xrate.get())
            yrate = int(self.pixel_yrate.get())
            temp_array = self.mask_array.copy()

            if xrate != 0 and yrate != 0:
                if len(temp_array.shape) == 3:
                    self.fused_array = gpu.pxlzc(temp_array, xrate, yrate)
                else:
                    self.fused_array = gpu.pxlzg(temp_array, xrate, yrate)

                ImgFrame.Fused_Draw(self)
                self.Fused_Register.grid(row=7, column=3, columnspan=3)

# Faire le négatif


class ImgNegFrame(ImgFrame):

    def __init__(self, master=None, **kwargs):
        ImgFrame.__init__(self, master, kwargs)

        self.negref = IntVar()
        self.negref.set(255)
        self.Ref_Choice = Entry(self, textvariable=self.negref)
        self.Invert_Choice = Button(self, text="Inverser", command=self.Invert)

        self.Ref_Choice.grid(row=0, column=3, rowspan=2)
        self.Invert_Choice.grid(row=0, column=4, rowspan=2, columnspan=2)

    def Invert(self, event=None):
        if isinstance(self.mask_array, np.ndarray):
            if self.mask_array.max() <= self.negref.get():
                self.fused_array = gpu.invert(self.mask_array, self.negref.get())
                ImgFrame.Fused_Draw(self)
                self.Fused_Register.grid(row=7, column=3, columnspan=3)

# Rogner une image


class ImgCropFrame(ImgFrame):

    def __init__(self, master=None, **kwargs):
        ImgFrame.__init__(self, master, kwargs)

        self.newheight = IntVar()
        self.newwidth = IntVar()
        self.startpos = TabVar(IntVar(), IntVar())
        self.modifier = TabVar(IntVar(), IntVar(), IntVar())
        self.NewH_Choice = Entry(self, textvariable=self.newheight, width=5)
        self.NewW_Choice = Entry(self, textvariable=self.newwidth, width=5)
        self.Crop_Choice = Button(self, text="Rogner", command=self.Crop)

        self.NewH_Choice.grid(row=0, column=4)
        self.NewW_Choice.grid(row=1, column=4)
        self.Crop_Choice.grid(row=0, column=5, rowspan=2)

        Label(self, text="Nouvelle Hauteur ").grid(row=0, column=3)
        Label(self, text="Nouvelle Largeur ").grid(row=1, column=3)

        Label(self, text="Depuis x=").grid(row=2, column=6)
        Label(self, text="et y=").grid(row=2, column=7)
        Entry(self, textvariable=self.startpos[1], width=4).grid(row=3, column=6)
        Entry(self, textvariable=self.startpos[0], width=4).grid(row=3, column=7)
        Label(self, text="Ajouter hauteur/largeur/transparence (1/0)").grid(row=4, column=6, columnspan=3)
        Entry(self, textvariable=self.modifier[0], width=4).grid(row=5, column=6)
        Entry(self, textvariable=self.modifier[1], width=4).grid(row=5, column=7)
        Entry(self, textvariable=self.modifier[2], width=4).grid(row=5, column=8)

    def Crop(self, event=None):
        if isinstance(self.mask_array, np.ndarray):
            if (self.mask_array.shape[0] >= self.newheight.get() + self.startpos[0].get() and
                    self.mask_array.shape[1] >= self.newwidth.get() + self.startpos[1].get() and self.modifier[
                        0].get() >= 0 and self.modifier[1].get() >= 0 and self.modifier[2].get() in [0, 1]):
                self.fused_array = gpu.crop(self.mask_array, self.newheight.get(), self.newwidth.get(),
                                            self.startpos.get(), self.modifier.get())
                ImgFrame.Fused_Draw(self)
                self.Fused_Register.grid(row=7, column=3, columnspan=3)

    def Mask_Chose(self, event=None):

        if ImgFrame.Mask_Chose(self, event):
            self.newheight.set(self.mask_array.shape[0])
            self.newwidth.set(self.mask_array.shape[1])

# Simulation Thermique


class ThermoFrame(Frame):  # Rendre la disposition plus intuitive voire rajouter des caractéristiques prédéfinies
    """Basic Parent Frame widget for Thermic Simulation.
    It only sets the variables, useless on its own"""

    def __init__(self, master=None, options={}):
        Frame.__init__(self, master, options)
        self.e = DoubleVar()
        self.l = DoubleVar()
        self.cp = IntVar()
        self.rho = IntVar()
        self.Dt = IntVar()
        self.N = IntVar()
        self.ItMax = IntVar()
        self.Tint = DoubleVar()
        self.Text1 = DoubleVar()
        self.Text2 = DoubleVar()

        self.e.set(0.4)
        self.l.set(1.65)
        self.cp.set(1000)
        self.rho.set(2150)
        self.Dt.set(25)
        self.N.set(60)
        self.ItMax.set(2000)
        self.Tint.set(20)
        self.Text1.set(10)
        self.Text2.set(-10)

        self.e_label = Label(self, text="Epaisseur")
        self.rho_label = Label(self, text="Densité")
        self.Dt_label = Label(self, text="Intervalle de temps")
        self.N_label = Label(self, text="Nombre de sections")
        self.cp_label = Label(self, text="Capacité Thermique massique")
        self.ItMax_label = Label(self, text="Itérations")
        self.l_label = Label(self, text="Conductivité Thermique")
        self.Tint_label = Label(self, text="Température Intérieure")
        self.Text1_label = Label(self, text="Température extérieure t<0")
        self.Text2_label = Label(self, text="Température extérieure t>0")

        self.e_input = Entry(self, textvariable=self.e)
        self.l_input = Entry(self, textvariable=self.l)
        self.cp_input = Entry(self, textvariable=self.cp)
        self.rho_input = Entry(self, textvariable=self.rho)
        self.Dt_input = Entry(self, textvariable=self.Dt)
        self.N_input = Entry(self, textvariable=self.N)
        self.ItMax_input = Entry(self, textvariable=self.ItMax)
        self.Tint_input = Entry(self, textvariable=self.Tint)
        self.Text1_input = Entry(self, textvariable=self.Text1)
        self.Text2_input = Entry(self, textvariable=self.Text2)

        self.e_label.grid(row=0, column=0)
        self.l_label.grid(row=0, column=1)
        self.cp_label.grid(row=0, column=2)
        self.rho_label.grid(row=0, column=3)
        self.Dt_label.grid(row=0, column=4)
        self.N_label.grid(row=2, column=0)
        self.ItMax_label.grid(row=2, column=1)
        self.Tint_label.grid(row=2, column=2)
        self.Text1_label.grid(row=2, column=3)
        self.Text2_label.grid(row=2, column=4)

        self.e_input.grid(row=1, column=0)
        self.l_input.grid(row=1, column=1)
        self.cp_input.grid(row=1, column=2)
        self.rho_input.grid(row=1, column=3)
        self.Dt_input.grid(row=1, column=4)
        self.N_input.grid(row=3, column=0)
        self.ItMax_input.grid(row=3, column=1)
        self.Tint_input.grid(row=3, column=2)
        self.Text1_input.grid(row=3, column=3)
        self.Text2_input.grid(row=3, column=4)

    def grid_forget(self, event=None):
        Frame.grid_forget(self)


class SimuTherm(ThermoFrame):
    """Frame widget for graphic thermic simulation"""

    def __init__(self, master=None, **kwargs):
        ThermoFrame.__init__(self, master, kwargs)
        self.simu_array = None
        self.x = None

        self.Simu_Choice = Button(self, text="Simuler", command=self.Simu_Start)

        self.GraphFrame = Frame(self)

        self.Graph = Figure(figsize=(5, 5), dpi=100)
        self.GraphZone = FigureCanvasTkAgg(self.Graph, self.GraphFrame)
        self.SubGraph = self.Graph.add_subplot(111)

        self.Simu_Choice.grid(row=4, column=0, columnspan=5)

        self.GraphFrame.grid(row=5, column=0, columnspan=5)

        self.GraphZone.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
        self.toolbar = NavigationToolbar2Tk(self.GraphZone, self.GraphFrame)
        self.toolbar.update()

    def Simu_Start(self, event=None):
        e = self.e.get()
        rho = self.rho.get()
        l = self.l.get()
        cp = self.cp.get()
        Dt = self.Dt.get()
        N = self.N.get()
        ItMax = self.ItMax.get()
        Tint = self.Tint.get()
        Text1 = self.Text1.get()
        Text2 = self.Text2.get()

        self.SubGraph.clear()

        self.x, self.simu_array = gpu.Thermodynamic_Graph(Tint, Text1, Text2, e, l, cp, rho, Dt, N, ItMax)

        self.SubGraph.plot(self.x, self.simu_array[:, 0], linewidth=2, color="black")

        for kp1 in range(1, ItMax // 100):
            self.SubGraph.plot(self.x, self.simu_array[:, kp1 * 100], linewidth=1, color="red")
        self.GraphZone.draw()

    def grid_forget(self, event=None):
        ThermoFrame.grid_forget(self)
        self.SubGraph.clear()
        self.simu_array = None
        self.x = None


class SuperThSim(ThermoFrame):
    """Frame widget for more visual Thermic simulation"""

    def __init__(self, master=None, **kwargs):
        ThermoFrame.__init__(self, master, kwargs)
        self.super_array = None
        self.displayed_super = None
        self.gradient_array = None
        self.displayed_gradient = None
        self.simu_array = None
        self.it_array = None

        self.ItRange = IntVar()
        self.ItRange.set(100)
        self.currentIt = IntVar()
        self.currentIt.set(0)

        self.CurrenteInfo = StringVar()
        self.CurrentTInfo = StringVar()

        self.LockedInfo = False

        self.Simu_Choice = Button(self, text="Simuler", command=self.SuperSimu_Start)
        self.Simu_Choice.grid(row=4, column=0, columnspan=5)

        self.Simu_Display = Canvas(self, width=360, height=360, bg="#ffffff")
        self.Simu_Display.grid(row=5, column=1, rowspan=3, columnspan=3)

        self.Simu_Display.event_add("<<gettinginfos>>", "<Motion>", "<Leave>", "<Button-1>")

        self.Infose_Display = Label(self, textvariable=self.CurrenteInfo)
        self.Infose_Display.grid(row=8, column=1)

        self.InfosT_Display = Label(self, textvariable=self.CurrentTInfo)
        self.InfosT_Display.grid(row=8, column=3)

        self.Gradient_Display = Canvas(self, width=60, height=360)

        self.ItRange_selector = Entry(self, textvariable=self.ItRange, font="Ubuntu,12", width=4)
        self.currentIt_Display = Label(self, textvariable=self.currentIt, font="Ubuntu,12")
        self.ItPlus = Button(self, text="+", font="Ubuntu,12", command=self.Add_It)
        self.ItLess = Button(self, text="-", font="Ubuntu,12", command=self.Back_It)

    def SuperSimu_Start(self, event=None):
        e = self.e.get()
        rho = self.rho.get()
        l = self.l.get()
        cp = self.cp.get()
        Dt = self.Dt.get()
        N = self.N.get()
        ItMax = self.ItMax.get()
        Tint = self.Tint.get()
        Text1 = self.Text1.get()
        Text2 = self.Text2.get()
        self.currentIt.set(0)
        Tmin = str(min(Tint, Text1, Text2))
        Tmax = str(max(Tint, Text1, Text2))

        temp_colors = np.zeros((N + 1, 3))
        rgbcolors = np.zeros((N + 1, 3), dtype=np.uint8)
        red = Color("red")
        colors = list(red.range_to(Color("blue"), N + 1))
        for i in range(N + 1):
            temp_colors[i] = colors[i].rgb
        temp_colors = np.rint(255 * temp_colors)

        for i in range(N + 1):
            for j in range(3):
                rgbcolors[i, j] = temp_colors[i, j]

        self.Simu_Display.delete("all")
        self.Gradient_Display.delete("all")

        self.super_array, self.gradient_array, self.simu_array = gpu.Thermodynamic_Bitmap(Tint, Text1, Text2, e, l, cp,
                                                                                          rho, Dt, N, ItMax, rgbcolors)
        self.it_array = self.simu_array[0, :, :]

        pilImage = PIL.Image.fromarray(self.super_array[0, :, :, :])
        pilGrad = PIL.Image.fromarray(self.gradient_array)

        height_ref = pilImage.height
        width_ref = pilImage.width

        if height_ref != 360 or width_ref != 360:
            if height_ref > width_ref:
                scale_ratio = 360 / height_ref
                new_height = 360
                new_width = int(scale_ratio * width_ref)
            else:
                scale_ratio = 360 / width_ref
                new_height = int(scale_ratio * height_ref)
                new_width = 360
            pilImage = pilImage.resize((new_width, new_height))

        self.displayed_super = PIL.ImageTk.PhotoImage(pilImage)
        self.displayed_gradient = PIL.ImageTk.PhotoImage(pilGrad)

        self.Simu_Display.create_image(182, 182, image=self.displayed_super)
        self.Simu_Display.create_line(90, 0, 90, 362, fill="black", width="3p")
        self.Simu_Display.create_line(274, 0, 274, 362, fill="black", width="3p")

        self.Gradient_Display.create_image(5, 180, image=self.displayed_gradient)
        self.Gradient_Display.create_line(0, 29, 15, 29, fill="black")
        self.Gradient_Display.create_line(0, 330, 15, 330, fill="black")
        self.Gradient_Display.create_text(18, 29, text=Tmax + "°C", anchor=W)
        self.Gradient_Display.create_text(18, 330, text=Tmin + "°C", anchor=W)
        self.Gradient_Display.grid(row=5, column=0, rowspan=3)

        self.ItRange_selector.grid(row=5, column=4, columnspan=2)
        self.currentIt_Display.grid(row=7, column=4, columnspan=2)
        self.ItPlus.grid(row=6, column=5, sticky=W + E)
        self.ItLess.grid(row=6, column=4, sticky=W + E)
        self.Simu_Display.bind("<<gettinginfos>>", self.Infos)

    def Add_It(self, event=None):
        NewIt = self.currentIt.get() + self.ItRange.get()
        ItMax = self.ItMax.get()

        if NewIt < ItMax:
            self.currentIt.set(NewIt)
            self.it_array = self.simu_array[NewIt, :, :]
            pilImage = PIL.Image.fromarray(self.super_array[NewIt, :, :, :])

            height_ref = pilImage.height
            width_ref = pilImage.width

            if height_ref != 360 or width_ref != 360:
                if height_ref > width_ref:
                    scale_ratio = 360 / height_ref
                    new_height = 360
                    new_width = int(scale_ratio * width_ref)
                else:
                    scale_ratio = 360 / width_ref
                    new_height = int(scale_ratio * height_ref)
                    new_width = 360
                pilImage = pilImage.resize((new_width, new_height))

            self.displayed_super = PIL.ImageTk.PhotoImage(pilImage)

            self.Simu_Display.delete("all")
            self.Simu_Display.create_image(182, 182, image=self.displayed_super)
            self.Simu_Display.create_line(90, 0, 90, 362, fill="black", width="3p")
            self.Simu_Display.create_line(274, 0, 274, 362, fill="black", width="3p")

    def Back_It(self, event=None):
        NewIt = self.currentIt.get() - self.ItRange.get()
        if NewIt >= 0:
            self.currentIt.set(NewIt)
            self.it_array = self.simu_array[NewIt, :, :]
            pilImage = PIL.Image.fromarray(self.super_array[NewIt, :, :, :])

            height_ref = pilImage.height
            width_ref = pilImage.width

            if height_ref != 360 or width_ref != 360:
                if height_ref > width_ref:
                    scale_ratio = 360 / height_ref
                    new_height = 360
                    new_width = int(scale_ratio * width_ref)
                else:
                    scale_ratio = 360 / width_ref
                    new_height = int(scale_ratio * height_ref)
                    new_width = 360
                pilImage = pilImage.resize((new_width, new_height))

            self.displayed_super = PIL.ImageTk.PhotoImage(pilImage)

            self.Simu_Display.delete("all")
            self.Simu_Display.create_image(182, 182, image=self.displayed_super)
            self.Simu_Display.create_line(90, 0, 90, 362, fill="black", width="3p")
            self.Simu_Display.create_line(274, 0, 274, 362, fill="black", width="3p")

    def Infos(self, event):

        if str(event.type) == "Motion" and not self.LockedInfo:
            p = self.it_array.shape[1]
            Nratio = 180 // self.N.get()
            eratio = self.e.get() / 180
            if event.x <= 90:
                self.CurrenteInfo.set("Intérieur")
                xtemp = round(self.it_array[0, 0], 2)
            elif event.x >= 270:
                self.CurrenteInfo.set("Extérieur")
                xtemp = round(self.it_array[0, p - 1], 2)
            else:

                x = (event.x - 90) // (Nratio)
                xe = round((event.x - 90) * eratio, 2)
                self.CurrenteInfo.set("Epaisseur: " + str(xe) + "m")
                xtemp = round(self.it_array[0, x], 2)

            self.CurrentTInfo.set("Température: " + str(xtemp) + "°C")
        elif str(event.type) == "Leave" and not self.LockedInfo:
            self.CurrenteInfo.set("")
            self.CurrentTInfo.set("")

        elif str(event.type) == "ButtonPress":
            if self.LockedInfo:
                self.LockedInfo = False
            else:
                self.LockedInfo = True
                p = self.it_array.shape[1]
                Nratio = 180 // self.N.get()
                eratio = self.e.get() / 180
                if event.x <= 90:
                    self.CurrenteInfo.set("Intérieur")
                    xtemp = round(self.it_array[0, 0], 2)
                elif event.x >= 270:
                    self.CurrenteInfo.set("Extérieur")
                    xtemp = round(self.it_array[0, p - 1], 2)
                else:

                    x = (event.x - 90) // (Nratio)
                    xe = round((event.x - 90) * eratio, 2)
                    self.CurrenteInfo.set("Epaisseur: " + str(xe) + "m")
                    xtemp = round(self.it_array[0, x], 2)

                self.CurrentTInfo.set("Température: " + str(xtemp) + "°C")

    def grid_forget(self, event=None):
        ThermoFrame.grid_forget(self)
        self.super_array = None
        self.displayed_super = None
        self.simu_array = None
        self.it_array = None
        self.LockedInfo = False
        self.Simu_Display.delete("all")

        self.ItRange.set(100)
        self.currentIt.set(0)
        self.ItRange_selector.grid_forget()
        self.currentIt_Display.grid_forget()
        self.ItPlus.grid_forget()
        self.ItLess.grid_forget()

# Résolution de Matrices


class GaussFrame(Frame):
    """Frame widget for resolving of linear systems"""

    def __init__(self, master=None, **kwargs):
        Frame.__init__(self, master, kwargs)
        self.data = {}
        self.dataval = {}

        self.Choice_Label = Label(self, text="Choisissez votre dimension de système:")
        self.Dim_Choice = Spinbox(self, from_=2, to=10)
        self.Aff = Button(self, text="Générer", command=self.Creer_Matrice)

        self.Choice_Label.grid(row=0, column=0, columnspan=3)
        self.Dim_Choice.grid(row=2, column=0)
        self.Aff.grid(row=3, column=0)

        self.Mat_Label = Label(self, text="Votre système à résoudre?")

        self.matrice_field = Frame(self)

        self.Solu_Label = Label(self, text="Solution du système: ")
        self.Solu_field = Frame(self)

        self.New_Matrix_Label = Label(self, text="Changer les dimensions du système.")
        self.New_Dimension = Spinbox(self, from_=2, to=26)
        self.New_Matrix_Choose = Button(self, text="Modifier", command=self.Change_Dim)

        self.Gauss_Choice = Button(self, text='Pivot', command=self.Gauss_Choose)
        self.Jacobi_Choice = Button(self, text='Jacobi', command=self.Jacobi_Choose)
        self.Seidel_Choice = Button(self, text='Gauss-Seidel', command=self.Seidel_Choose)
        self.No_Piv = Label(self, text="Ce n'est pas un système de Cramer'")

    def Creer_Matrice(self, n=0, event=None):

        self.matrice_field.grid(row=1, column=0, columnspan=3)
        if n == 0:
            n = int(self.Dim_Choice.get())

        dataname = [chr(k + 97) + " +" for k in range(n - 1)]
        dataname.append(chr(n + 96) + " =")
        dataname_field = {}
        for i in range(n):
            self.data[i] = {}
            self.dataval[i] = {}
            for j in range(n + 1):
                self.dataval[i][j] = DoubleVar()
                self.data[i][j] = Entry(self.matrice_field, textvariable=self.dataval[i][j], width=4)
                self.data[i][j].grid(row=i, column=2 * j)
                if j != n:
                    dataname_field[j] = Label(self.matrice_field, width=2, text=dataname[j])
                    dataname_field[j].grid(row=i, column=2 * j + 1)

        self.Dim_Choice.grid_forget()
        self.Aff.grid_forget()
        self.Choice_Label.grid_forget()

        self.Mat_Label.grid(row=0, column=0)
        self.Gauss_Choice.grid(row=2, column=0)
        self.Jacobi_Choice.grid(row=3, column=0)
        self.Seidel_Choice.grid(row=4, column=0)
        self.Solu_Label.grid(row=0, column=3)
        self.Solu_field.grid(row=1, column=3)
        self.New_Matrix_Label.grid(row=0, column=4)
        self.New_Dimension.grid(row=1, column=4)
        self.New_Matrix_Choose.grid(row=2, column=4)

    def Gauss_Choose(self, event=None):
        n = len(self.data)
        A = np.zeros((n, n))
        B = np.zeros((1, n))
        for i in range(n):
            for j in range(n):
                A[i, j] = self.dataval[i][j].get()
            B[0, i] = self.dataval[i][n].get()
        try:
            Sol = gpu.Gauss(A, B)
            Soldict_field = {}
            for i in range(n):
                Soldict_field[i] = Label(self.Solu_field, text=chr(i + 97) + " = " + str(round(Sol[i, 0], 2)))
                Soldict_field[i].grid(row=i, column=0)
            self.No_Piv.grid_forget()
        except ValueError:
            self.No_Piv.grid(row=3, column=0)
            pass

    def Jacobi_Choose(self, event=None):
        n = len(self.data)
        A = np.zeros((n, n))
        B = np.zeros((n, 1))
        for i in range(n):
            for j in range(n):
                A[i, j] = self.dataval[i][j].get()
            B[i, 0] = self.dataval[i][n].get()
        try:
            Sol = gpu.Jacobi(A, B)
            Soldict_field = {}
            for i in range(n):
                Soldict_field[i] = Label(self.Solu_field, text=chr(i + 97) + " = " + str(round(Sol[i, 0], 2)))
                Soldict_field[i].grid(row=i, column=0)
            self.No_Piv.grid_forget()
        except ValueError as val:
            self.No_Piv.grid(row=3, column=0)
            print(val)

    def Seidel_Choose(self, event=None):
        n = len(self.data)
        A = np.zeros((n, n))
        B = np.zeros((n, 1))
        for i in range(n):
            for j in range(n):
                A[i, j] = self.dataval[i][j].get()
            B[i, 0] = self.dataval[i][n].get()
        try:
            Sol = gpu.GaussSeidel(A, B)
            Soldict_field = {}
            for i in range(n):
                Soldict_field[i] = Label(self.Solu_field, text=chr(i + 97) + " = " + str(round(Sol[i, 0], 2)))
                Soldict_field[i].grid(row=i, column=0)
            self.No_Piv.grid_forget()
        except ValueError as val:
            self.No_Piv.grid(row=3, column=0)
            print(val)

    def Change_Dim(self, event=None):
        for wid in self.matrice_field.grid_slaves():
            wid.grid_forget()
        self.data = {}
        self.dataval = {}
        n = int(self.New_Dimension.get())
        self.Creer_Matrice(n)

    def grid_forget(self, event=None):
        Frame.grid_forget(self)
        for wid in self.matrice_field.grid_slaves():
            wid.grid_forget()
        for wid in self.grid_slaves():
            wid.grid_forget()
        for wid in self.Solu_field.grid_slaves():
            wid.grid_forget()

        self.data = {}
        self.dataval = {}
        self.Choice_Label.grid(row=0, column=0, columnspan=3)
        self.Dim_Choice.grid(row=2, column=0)
        self.Aff.grid(row=3, column=0)

# Dérivation, équation


class DerivFrame(Frame):
    """Frame widget to find values with differential equation and initial values with Euler"""

    def __init__(self, master=None, **kwargs):
        Frame.__init__(self, master, kwargs)
        self.Order_Select = Spinbox(self, from_=1, to=10)
        self.Order_Select.grid(row=0, column=0)
        self.Order_Choose = Button(self, text="Choisir", command=self.Generate)
        self.Order_Choose.grid(row=1, column=0)
        self.Sup = DoubleVar()
        self.Sup.set(1)
        self.Sup_Input = Entry(self, textvariable=self.Sup, width=5)
        self.Sup_Label = Label(self, text="Dériver jusqu'à x=")
        self.Pts = IntVar()
        self.Pts.set(101)
        self.Pts_Input = Entry(self, textvariable=self.Pts, width=5)
        self.Pts_Label = Label(self, text="Nombre de points:")
        self.y = []
        self.function = StringVar()
        self.datainput = {}
        self.dataval = {}

        self.function_field = Entry(self, textvariable=self.function)
        self.function_deriv = Button(self, text="Lancer", command=self.Deriv)

        self.GraphFrame = Frame(self)

        self.Graph = Figure(figsize=(5, 5), dpi=100)
        self.GraphZone = FigureCanvasTkAgg(self.Graph, self.GraphFrame)
        self.SubGraph = self.Graph.add_subplot(111)
        self.toolbar = NavigationToolbar2Tk(self.GraphZone, self.GraphFrame)

    def Generate(self, event=None):
        order = int(self.Order_Select.get())
        self.Order_Select.grid_forget()
        self.Order_Choose.grid_forget()
        Label(self, text="Y(" + str(order) + ")=").grid(row=0, column=0)
        self.function_field.grid(row=0, column=1)
        self.function_deriv.grid(row=1, column=1)
        for i in range(order):
            self.dataval[i] = DoubleVar()
            self.datainput[i] = Entry(self, textvariable=self.dataval[i], width=5)
            self.datainput[i].grid(row=i, column=3)
            Label(self, text="Y" + str(i)).grid(row=i, column=2)
        self.Sup_Label.grid(row=0, column=4)
        self.Sup_Input.grid(row=0, column=5)
        self.Pts_Label.grid(row=1, column=4)
        self.Pts_Input.grid(row=1, column=5)

        self.GraphFrame.grid(row=max(2, order), column=0, columnspan=6)
        self.GraphZone.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
        self.toolbar.update()

    def Deriv(self, event=None):
        self.SubGraph.clear()
        self.y = []
        sup = self.Sup.get()
        pts = self.Pts.get()
        t = np.linspace(0, sup, pts)
        actions = "]"
        for i in range(len(self.dataval)):
            self.y.append(self.dataval[i].get())
            if i > 0:
                actions = ",y[" + str(i) + "]" + actions
        func = self.function.get()
        actions = func + actions
        actions = "lambda y,t: [" + actions
        F = eval(actions)
        tab = odeint(F, self.y, t)
        self.GraphFrame = Frame(self)
        self.SubGraph.plot(t, tab, color="black")
        self.GraphZone.draw()

    def grid_forget(self):
        Frame.grid_forget(self)
        for wid in self.grid_slaves():
            wid.grid_forget()
        self.dataval = {}
        self.datainput = {}
        self.y = []
        self.Sup.set(1)
        self.Pts.set(101)
        self.function.set("")
        self.Order_Select.grid(row=0, column=0)
        self.Order_Choose.grid(row=1, column=0)


class ZeroFrame(Frame):
    """Frame widget to find the zero of a one-variable function that is strictly monotone on the defined interval"""

    def __init__(self, master=None, **kwargs):
        Frame.__init__(self, master, kwargs)
        self.function = StringVar()
        self.inf = DoubleVar()
        self.sup = DoubleVar()
        self.eps = DoubleVar()
        self.eps.set(0.01)
        self.res = StringVar()

        self.method = StringVar()
        self.method.set("cpu.dichotomie(y,a,b,e)")

        self.ask = Label(self, text="Entrez votre fonction")

        self.function_label = Label(self, text="f : x -->")
        self.function_field = Entry(self, textvariable=self.function)

        self.Submit_Choice = Button(self, text="Trouver le zéro", command=self.Calculate)
        self.Result = Label(self, textvariable=self.res)

        self.Options_Frame = Frame(self)
        self.options_label = Label(self.Options_Frame, text="Options de recherche")
        self.inf_label = Label(self.Options_Frame, text="Borne inférieure")
        self.inf_field = Entry(self.Options_Frame, textvariable=self.inf, width=5)
        self.sup_label = Label(self.Options_Frame, text="Borne supérieure")
        self.sup_field = Entry(self.Options_Frame, textvariable=self.sup, width=5)
        self.epsilon_label = Label(self.Options_Frame, text="Epsilon")
        self.epsilon_field = Entry(self.Options_Frame, textvariable=self.eps, width=5)

        self.ask.grid(row=0, column=0, columnspan=2)
        self.function_label.grid(row=1, column=0)
        self.function_field.grid(row=1, column=1)
        self.Submit_Choice.grid(row=2, column=0, columnspan=2)
        self.Result.grid(row=4, column=0, columnspan=2)

        self.Options_Frame.grid(row=0, column=2, rowspan=6)
        self.options_label.grid(row=0, column=0, columnspan=2)
        self.inf_label.grid(row=1, column=0)
        self.sup_label.grid(row=2, column=0)
        self.epsilon_label.grid(row=3, column=0)
        self.inf_field.grid(row=1, column=1)
        self.sup_field.grid(row=2, column=1)
        self.epsilon_field.grid(row=3, column=1)

        self.dicho_choice = Radiobutton(self.Options_Frame, text="Dichotomie", variable=self.method,
                                        value="cpu.dichotomie(y,a,b,e)")
        self.lag_choice = Radiobutton(self.Options_Frame, text="Lagrange", variable=self.method,
                                      value="cpu.lagrange(y,a,b,e)")
        self.new_choice = Radiobutton(self.Options_Frame, text="Newton", variable=self.method,
                                      value="cpu.newton(y,a,b,e)")

        self.dicho_choice.grid(row=4, column=0)
        self.lag_choice.grid(row=5, column=0)
        self.new_choice.grid(row=6, column=0)

        self.function_field.bind("<Return>", self.Calculate)

    def Calculate(self, event=None):
        func = "lambda x : " + self.function.get()
        y = eval(func)
        a = self.inf.get()
        b = self.sup.get()
        e = self.eps.get()
        action = self.method.get()

        res = eval(action)

        self.res.set("Résultat: " + str(res))

    def grid_forget(self, event=None):
        Frame.grid_forget(self)
        self.method.set("cpu.dichotomie(y,a,b,e)")
        self.res.set("")
        self.function.set("")
        self.inf.set(0.0)
        self.sup.set(0.0)
        self.eps.set(0.01)

# Misc


class TabVar(object):

    def __init__(self, *args):
        object.__init__(self)
        self.values = list(args)

    def __getitem__(self, key):

        return (self.values[key])

    def get(self):

        outputlist = self.values.copy()

        for i in range(len(self.values)):
            try:
                outputlist[i] = outputlist[i].get()

            except:
                pass

        return outputlist
