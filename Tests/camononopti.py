import os

import scipy.misc as scm
import numpy as np
from random import randrange
import time
from numba import jit

os.chdir(os.path.dirname(__file__))


@jit(nopython=True)
def bpf_m(im_m):
    n=im_m.shape[0]
    p=im_m.shape[1]

    for i in range(n):
        for j in range(p):
            im_m[i,j,0]=im_m[i,j,0]&0b11110000
            im_m[i,j,1]=im_m[i,j,1]&0b11110000
            im_m[i,j,2]=im_m[i,j,2]&0b11110000


    return im_m


def bpf_s(im_s):
    n=im_s.shape[0]
    p=im_s.shape[1]

    for i in range(n):
        for j in range(p):
            im_s[i,j][0]=(im_s[i,j][0]&0b11110000)>>4
            im_s[i,j][1]=(im_s[i,j][1]&0b11110000)>>4
            im_s[i,j][2]=(im_s[i,j][2]&0b11110000)>>4

    return im_s

@jit(nopython=True)
def bpf_c(im_c):
    n=im_c.shape[0]
    p=im_c.shape[1]

    for i in range(n):
        for j in range(p):
            im_c[i,j][0]=(im_c[i,j][0]&0b00001111)<<4
            im_c[i,j][1]=(im_c[i,j][1]&0b00001111)<<4
            im_c[i,j][2]=(im_c[i,j][2]&0b00001111)<<4
    return im_c


def add_im(im_m,im_s):
    if (im_m.shape)==(im_s.shape):
        im_f=im_m+im_s
    else:
        im_f=im_m

        n=im_m.shape[0]
        p=im_m.shape[1]

        q=im_s.shape[0]
        r=im_s.shape[1]

        x=randrange(n-q)
        y=randrange(p-r)

        for i in range(x,x+q):
            for j in range(y,y+r):
                im_f[i,j,0] = im_m[i,j,0]+im_s[i-x,j-y,0]
                im_f[i,j,1] = im_m[i,j,1]+im_s[i-x,j-y,1]
                im_f[i,j,2] = im_m[i,j,2]+im_s[i-x,j-y,2]
    return im_f

@jit(nopython=True)
def bpf_cplus(im_c):
    n=im_c.shape[0]
    p=im_c.shape[1]
    min_i=-1
    max_i=n+1
    min_j=-1
    max_j=p+1

    for i in range(n):
        j=0
        while j<p:
            if im_c[i,j][0]&0b00001111==0 and im_c[i,j][1]&0b00001111==0 and im_c[i,j,2]&0b00001111==0:
                j=j+1
            else:
                if min_i==-1:
                    min_i=i
                else:
                    max_i=i
                j=p

    for j in range(p):
        i=0
        while i<n:
            if im_c[i,j][0]&0b00001111==0 and im_c[i,j][1]&0b00001111==0 and im_c[i,j,2]&0b00001111==0:
                i=i+1
            else:
                if min_j==-1:
                    min_j=j
                else:
                    max_j=j
                i=n
    im_c=bpf_c(im_c[min_i:(max_i+1),min_j:(max_j+1)])

    return im_c

@jit(nopython=True)
def Txt_In_Image(im_m,text):
    """WORK IN PROGRESS"""
    n=im_m.shape[0]
    p=im_m.shape[1]
    q=im_m.shape[2]

    temp_array=np.zeros((n,p,q))
    temp_array.flatten()
    textlist=text.split()
    ordlist=char(textlist)
    s=randrange(n*p*q-2*len(textlist))

    for i in range(len(ordlist)):
            temp_array[s+2*i]=(ordlist[i]&0b11110000)
            temp_array[s+2*i+1]=(ordlist[i]&0b00001111)<<4
    temp_array=temp_array.reshape((n,p,q))

    im_fin=add_im(im_m,temp_array)
    return im_fin

@jit(nopython=True)
def Rgb_Gray(img,norm=601):
    n=img.shape[0]
    p=img.shape[1]

    gray = np.zeros((n,p))
    if norm == 601:
        for i in range(n):
            for j in range(p):
                gray[i,j]=int(0.299*img[i,j,0]+0.587*img[i,j,1]+0.114*img[i,j,2])
    else:
        for i in range(n):
            for j in range(p):
                gray[i,j]=int(0.2126*img[i,j,0]+0.7152*img[i,j,1]+0.0722*img[i,j,2])
    return gray

@jit(nopython=True)
def Shape_Detect(img):
    c=8
    d=-1

    gray=img.copy()

    n=img.shape[0]
    p=img.shape[1]

    detected=np.zeros((n,p))

    for i in range(n):
        for j in range(p):
            border=0
            border=c*gray[i,j]
            if i<n-1 and i>0 and j<p-1 and j>0:
                border = border + d*(int(gray[i-1,j-1])+int(gray[i,j-1])+int(gray[i+1,j-1])+int(gray[i+1,j])+int(gray[i+1,j+1])+int(gray[i,j+1])+int(gray[i-1,j+1])+int(gray[i-1,j]))
            elif i==n-1 and j==p-1:
                border = border + d*(int(gray[i-1,j-1])+int(gray[i,j-1])+int(gray[i-1,j]))
            elif i==0 and j==p-1:
                border = border + d*(int(gray[i,j-1])+int(gray[i+1,j-1])+int(gray[i+1,j]))
            elif i==0 and j==0:
                border = border + d*(int(gray[i+1,j])+int(gray[i+1,j+1])+int(gray[i,j+1]))
            elif i==n-1 and j==0:
                border = border + d*(int(gray[i,j+1])+int(gray[i-1,j+1])+int(gray[i-1,j]))
            elif i==0:
                border = border + d*(int(gray[i,j-1])+int(gray[i+1,j-1])+int(gray[i+1,j])+int(gray[i+1,j+1])+int(gray[i,j+1]))
            elif j==0:
                border = border + d*(int(gray[i+1,j])+int(gray[i+1,j+1])+int(gray[i,j+1])+int(gray[i-1,j+1])+int(gray[i-1,j]))
            elif j==p-1:
                border = border + d*(int(gray[i-1,j-1])+int(gray[i,j-1])+int(gray[i+1,j-1])+int(gray[i+1,j])+int(gray[i-1,j]))
            elif i==n-1:
               border = border + d*(int(gray[i-1,j-1])+int(gray[i,j-1])+int(gray[i,j+1])+int(gray[i-1,j+1])+int(gray[i-1,j]))

            if border<=40:
                detected[i,j]=255

    return detected


def thinkinaboutname(img):
    c=1
    d=-1

    gray=img.copy()

    n=img.shape[0]
    p=img.shape[1]

    detected=np.zeros((n,p))

    for i in range(n):
        for j in range(p):
            border=0
            border=c*gray[i,j]
            if i<n-1 and i>0 and j<p-1 and j>0:
                border = border + d*(int(gray[i-1,j-1])+int(gray[i,j-1])+int(gray[i+1,j-1])+int(gray[i+1,j])+int(gray[i+1,j+1])+int(gray[i,j+1])+int(gray[i-1,j+1])+int(gray[i-1,j]))
            elif i==n-1 and j==p-1:
                border = border + d*(int(gray[i-1,j-1])+int(gray[i,j-1])+int(gray[i-1,j]))
            elif i==0 and j==p-1:
                border = border + d*(int(gray[i,j-1])+int(gray[i+1,j-1])+int(gray[i+1,j]))
            elif i==0 and j==0:
                border = border + d*(int(gray[i+1,j])+int(gray[i+1,j+1])+int(gray[i,j+1]))
            elif i==n-1 and j==0:
                border = border + d*(int(gray[i,j+1])+int(gray[i-1,j+1])+int(gray[i-1,j]))
            elif i==0:
                border = border + d*(int(gray[i,j-1])+int(gray[i+1,j-1])+int(gray[i+1,j])+int(gray[i+1,j+1])+int(gray[i,j+1]))
            elif j==0:
                border = border + d*(int(gray[i+1,j])+int(gray[i+1,j+1])+int(gray[i,j+1])+int(gray[i-1,j+1])+int(gray[i-1,j]))
            elif j==p-1:
                border = border + d*(int(gray[i-1,j-1])+int(gray[i,j-1])+int(gray[i+1,j-1])+int(gray[i+1,j])+int(gray[i-1,j]))
            elif i==n-1:
               border = border + d*(int(gray[i-1,j-1])+int(gray[i,j-1])+int(gray[i,j+1])+int(gray[i-1,j+1])+int(gray[i-1,j]))

            detected[i,j]=border

    return detected

@jit(nopython=True)
def Blur(img):
    c=1
    d=1

    gray=img.copy()

    n=img.shape[0]
    p=img.shape[1]

    detected=np.zeros((n,p))

    for i in range(n):
        for j in range(p):
            border=0
            border=c*gray[i,j]
            if i<n-1 and i>0 and j<p-1 and j>0:
                border = (border + d*(int(gray[i-1,j-1])+int(gray[i,j-1])+int(gray[i+1,j-1])+int(gray[i+1,j])+int(gray[i+1,j+1])+int(gray[i,j+1])+int(gray[i-1,j+1])+int(gray[i-1,j])))//9
            elif i==n-1 and j==p-1:
                border = (border + d*(int(gray[i-1,j-1])+int(gray[i,j-1])+int(gray[i-1,j])))//9
            elif i==0 and j==p-1:
                border = (border + d*(int(gray[i,j-1])+int(gray[i+1,j-1])+int(gray[i+1,j])))//9
            elif i==0 and j==0:
                border = (border + d*(int(gray[i+1,j])+int(gray[i+1,j+1])+int(gray[i,j+1])))//9
            elif i==n-1 and j==0:
                border = (border + d*(int(gray[i,j+1])+int(gray[i-1,j+1])+int(gray[i-1,j])))//9
            elif i==0:
                border = (border + d*(int(gray[i,j-1])+int(gray[i+1,j-1])+int(gray[i+1,j])+int(gray[i+1,j+1])+int(gray[i,j+1])))//9
            elif j==0:
                border = (border + d*(int(gray[i+1,j])+int(gray[i+1,j+1])+int(gray[i,j+1])+int(gray[i-1,j+1])+int(gray[i-1,j])))//9
            elif j==p-1:
                border = (border + d*(int(gray[i-1,j-1])+int(gray[i,j-1])+int(gray[i+1,j-1])+int(gray[i+1,j])+int(gray[i-1,j])))//9
            elif i==n-1:
               border = (border + d*(int(gray[i-1,j-1])+int(gray[i,j-1])+int(gray[i,j+1])+int(gray[i-1,j+1])+int(gray[i-1,j])))//9

            detected[i,j]=border

    return detected
    
    
    
@jit(nopython=True)
def ordchar(order):
    asciitable=['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\t', '\n', '\x0b', '\x0c', '\r', '\x0e', '\x0f', '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\x1a', '\x1b', '\x1c', '\x1d', '\x1e', '\x1f', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '\x7f', '\x80', '\x81', '\x82', '\x83', '\x84', '\x85', '\x86', '\x87', '\x88', '\x89', '\x8a', '\x8b', '\x8c', '\x8d', '\x8e', '\x8f', '\x90', '\x91', '\x92', '\x93', '\x94', '\x95', '\x96', '\x97', '\x98', '\x99', '\x9a', '\x9b', '\x9c', '\x9d', '\x9e', '\x9f', '\xa0', '¡', '¢', '£', '¤', '¥', '¦', '§', '¨', '©', 'ª', '«', '¬', '\xad', '®', '¯', '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»', '¼', '½', '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ']

    corres=[]
    for i in range(len(order)):
        if order[i]!=0:
            corres.append(asciitable[order[i]])
    return corres
    
    
##start = time.time()
##

@jit(nopython=True)
def Get_Txt(im_t):
    n=im_t.shape[0]
    p=im_t.shape[1]
    q=im_t.shape[2]
    ordlist=[]
    text=""

    tem_array=bpf_cplus(im_t)
    tem_array=tem_array.flatten()
    
    r=tem_array.shape[0]
    
    while tem_array[0]==0:
        for i in range(r-1):
            tem_array[i]=tem_array[i+1]
        tem_array[r-1]=0
    
    for i in range(r//2):
        ordlist.append(tem_array[2*i]+(tem_array[2*i+1]>>4))

    charlist=ordchar(ordlist)
    for i in range(len(charlist)):
        text=text+charlist[i]
    
    return(text)
##
##nouar=Rgb_Gray(im_masque)
##

#nouar = Blur(im_masque)
#scm.imsave("bfc2.bmp",nouar)
##
##im_fin=Blur(nouar)
##scm.imsave("blackwhiteflou.bmp",im_fin)

@jit(nopython=True)
def patate():
    a="Tamer"
    b=[]
    for i in range(len(a)):
        b.append(a[i])
    return b
        
##
##
##im_secret=scm.imread("ela.bmp")
##
##im_masque=bpf_m(im_masque)
##scm.imsave("masqonkey.bmp",im_masque)
##im_secret=bpf_s(im_secret)
##
##
##if (im_masque.shape[2])>(im_secret.shape[2]):
##    np.delete(im_masque,im_masque.shape[2]-1,2)
##elif (im_masque.shape[2])<(im_secret.shape[2]):
##    np.delete(im_masque,im_secret.shape[2]-1,2)
##
##im_fin = add_im(im_masque,im_secret)
##
##scm.imsave("camonkey.bmp",im_fin)
##
##im_cach=scm.imread("camonkey.bmp")
##
##im_cach=bpf_cplus(im_cach)
##
##scm.imsave("recuponkey.bmp",im_cach)
##
##end = time.time()
##print("Elapsed (with compilation) = %s" % (end - start))

@jit(nopython=True)
def Augmente(A,B):
    n=A.shape[0]
    C=np.zeros((n,n+1))
    for i in range(n):
        for j in range(n):
            C[i,j]=A[i,j]
        C[i,n]=B[0,i]
    return C
    
@jit(nopython=True)
def Echangeligne(M,i,j):
    """ Index en notation informatique """
    n=M.shape[0]

    E=M[i].copy()
    M[i]=M[j]
    M[j]=E
    return M
A=np.zeros((3,3))
B=np.array([[3],[2],[1]])

C=Augmente(A,B)

print(C)
D=Echangeligne(C,0,2)
input("hey?")