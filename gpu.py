from numba import jit
import numpy as np
from random import randrange

## Jeux d'images
@jit(nopython=True)
def bpf_m(im_m):
    """ Fonction qui garde les bits de poids fort de l'image masque """
    n=im_m.shape[0]
    p=im_m.shape[1]

    for i in range(n):
        for j in range(p):
            im_m[i,j,0]=im_m[i,j,0]&0b11110000
            im_m[i,j,1]=im_m[i,j,1]&0b11110000
            im_m[i,j,2]=im_m[i,j,2]&0b11110000


    return im_m


@jit(nopython=True)
def bpf_mplus(im_m,x,y,n,p):
    """ Fonction qui garde les bits de poids fort de l'image masque sur un certain cadre uniquement"""

    for i in range(x,n+x):
        for j in range(y,p+y):
            im_m[i,j,0]=im_m[i,j,0]&0b11110000
            im_m[i,j,1]=im_m[i,j,1]&0b11110000
            im_m[i,j,2]=im_m[i,j,2]&0b11110000


    return im_m


@jit(nopython=True)
def bpf_s(im_s):
    """ fonction qui garde les bits de poids fort de l'image à cacher et les place en poids faible """
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
def add_im(im_m,im_s,treatment="simple"):
    """ Fonction qui ajoute l'image masque et l'image à cacher """
    
    if (im_m.shape)==(im_s.shape):
        im_m=bpf_m(im_m)
        im_s=bpf_s(im_s)
        im_f=im_m+im_s

    elif treatment=="simple":

        n=im_m.shape[0]
        p=im_m.shape[1]

        q=im_s.shape[0]
        r=im_s.shape[1]

        x=randrange(n-q)
        y=randrange(p-r)

        im_m=bpf_m(im_m)
        im_s=bpf_s(im_s)
        im_f=im_m

        for i in range(x,x+q):
            for j in range(y,y+r):
                im_f[i,j,0] = im_m[i,j,0]+im_s[i-x,j-y,0]
                im_f[i,j,1] = im_m[i,j,1]+im_s[i-x,j-y,1]
                im_f[i,j,2] = im_m[i,j,2]+im_s[i-x,j-y,2]
    else:

        n=im_m.shape[0]
        p=im_m.shape[1]

        q=im_s.shape[0]
        r=im_s.shape[1]

        x=randrange(n-q)
        y=randrange(p-r)

        im_m=bpf_mplus(im_m,x,y,q,r)
        im_s=bpf_s(im_s)
        im_f=im_m

        for i in range(x,x+q):
            for j in range(y,y+r):
                im_f[i,j,0] = im_m[i,j,0]+im_s[i-x,j-y,0]
                im_f[i,j,1] = im_m[i,j,1]+im_s[i-x,j-y,1]
                im_f[i,j,2] = im_m[i,j,2]+im_s[i-x,j-y,2]

    return im_f


@jit(nopython=True)
def Txt_In_Image(im_m,text):
    """ Fonction pour mettre du texte dans une image """
    n=im_m.shape[0]
    p=im_m.shape[1]
    q=im_m.shape[2] # q=4 si png (transparence)
    
    textlist=[]
    
    # on transforme le texte en liste de caractères
    for i in range(len(text)):
        textlist.append(text[i])

    temp_array=np.zeros((n,p,q),dtype=np.uint8)
    temp_array=temp_array.flatten()
    ordlist=char(textlist)
    s=randrange(n*p*q-2*len(textlist))

    for i in range(len(ordlist)):
            temp_array[s+2*i]=(ordlist[i]&0b11110000)
            temp_array[s+2*i+1]=(ordlist[i]&0b00001111)<<4

    temp_array=temp_array.reshape((n,p,q))
    im_m=bpf_m(im_m)

    im_fin=add_im(im_m,temp_array)

    return im_fin


@jit(nopython=True)
def Get_Txt(im_t):

    ordlist=[]
    text=""
    
    tem_array=bpf_cplus(im_t)
    tem_array=tem_array.flatten()
    
    r=tem_array.shape[0]
    
    while tem_array[0]==0:
        tem_array[0:r-2]=tem_array[1:r-1].copy()
        tem_array[r-1]=0
    
    for i in range(r//2):
        ordlist.append(tem_array[2*i]+(tem_array[2*i+1]>>4))

    charlist=ordchar(ordlist)
    for i in range(len(charlist)):
        text=text+charlist[i]
    
    return(text)


@jit(nopython=True)
def ordchar(order):
    asciitable=['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\t', '\n', '\x0b', '\x0c', '\r', '\x0e', '\x0f', '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\x1a', '\x1b', '\x1c', '\x1d', '\x1e', '\x1f', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '\x7f', '\x80', '\x81', '\x82', '\x83', '\x84', '\x85', '\x86', '\x87', '\x88', '\x89', '\x8a', '\x8b', '\x8c', '\x8d', '\x8e', '\x8f', '\x90', '\x91', '\x92', '\x93', '\x94', '\x95', '\x96', '\x97', '\x98', '\x99', '\x9a', '\x9b', '\x9c', '\x9d', '\x9e', '\x9f', '\xa0', '¡', '¢', '£', '¤', '¥', '¦', '§', '¨', '©', 'ª', '«', '¬', '\xad', '®', '¯', '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»', '¼', '½', '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ']

    corres=[]
    for i in range(len(order)):
        if order[i]!=0:
            corres.append(asciitable[order[i]])
    return corres


@jit(nopython=True)
def char(order):
    asciitable=['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\t', '\n', '\x0b', '\x0c', '\r', '\x0e', '\x0f', '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\x1a', '\x1b', '\x1c', '\x1d', '\x1e', '\x1f', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '\x7f', '\x80', '\x81', '\x82', '\x83', '\x84', '\x85', '\x86', '\x87', '\x88', '\x89', '\x8a', '\x8b', '\x8c', '\x8d', '\x8e', '\x8f', '\x90', '\x91', '\x92', '\x93', '\x94', '\x95', '\x96', '\x97', '\x98', '\x99', '\x9a', '\x9b', '\x9c', '\x9d', '\x9e', '\x9f', '\xa0', '¡', '¢', '£', '¤', '¥', '¦', '§', '¨', '©', 'ª', '«', '¬', '\xad', '®', '¯', '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»', '¼', '½', '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ']

    corres=[]
    for i in range(len(order)):
        corres.append(asciitable.index(order[i]))
    return corres


@jit(nopython=True)
def Rgb_2_Gray(img,norm=601):
    n=img.shape[0]
    p=img.shape[1]

    gray = np.zeros((n,p))
    if norm == 601:
        for i in range(n):
            for j in range(p):
                gray[i,j]=0.299*img[i,j,0]+0.587*img[i,j,1]+0.114*img[i,j,2]
    elif norm==709:
        for i in range(n):
            for j in range(p):
                gray[i,j]=0.2126*img[i,j,0]+0.7152*img[i,j,1]+0.0722*img[i,j,2]
    return gray


@jit(nopython=True)
def Shape_Detect(img,seuil=40):
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

            if abs(border)<=seuil:
                detected[i,j]=255

    return detected

@jit(nopython=True)
def fliplines(kernel):
    newkernel=np.zeros(kernel.shape)
    n=kernel.shape[0]
    
    for i in range(newkernel.shape[0]):
        newkernel[i]=kernel[n-1-i]
    
    return newkernel
    
    
@jit(nopython=True)
def flipcols(kernel):
    newkernel=np.zeros(kernel.shape)
    n=kernel.shape[1]
    
    for j in range(newkernel.shape[1]):
        newkernel[:,j]=kernel[:,n-1-j]
    
    return newkernel



@jit(nopython=True)
def Convolve2D(image,kernel,pad,strides):
    
    kernel=fliplines(flipcols(kernel))
    
    n,p=image.shape[:2]
    l,m=kernel.shape[:2]
    
    nOutput=(n-l+2*pad)//strides+1
    pOutput=(p-m+2*pad)//strides+1
    output=np.zeros((nOutput,pOutput))
    
    padded_image=np.zeros((n+2*pad,p+2*pad))
    padded_image[pad:pad+n,pad:pad+p]=image.copy()
    
    
    for i in range(padded_image.shape[0]-l):
        for j in range(padded_image.shape[1]-m):
            
            if i%strides==0 and j%strides==0:
                output[i, j] = ((kernel * padded_image[i: i + l, j: j + m]).sum())
    
    return output
    

@jit(nopython=True)
def Convolve2Dabs(image,kernel,pad,strides):
    
    kernel=fliplines(flipcols(kernel))
    
    n,p=image.shape[:2]
    l,m=kernel.shape[:2]
    
    nOutput=(n-l+2*pad)//strides+1
    pOutput=(p-m+2*pad)//strides+1
    output=np.zeros((nOutput,pOutput))
    
    padded_image=np.zeros((n+2*pad,p+2*pad))
    padded_image[pad:pad+n,pad:pad+p]=image.copy()
    
    
    for i in range(padded_image.shape[0]-l):
        for j in range(padded_image.shape[1]-m):
            
            if i%strides==0 and j%strides==0:
                output[i, j] = abs((kernel * padded_image[i: i + l, j: j + m]).sum())
    
    return output
    
@jit(nopython=True)
def Prewitt(image):
    
    Gradx=np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
    Grady=np.array([[-1,-1,-1],[0,0,0],[1,1,1]])
    
    Gdex=Convolve2D(image,Gradx,1,1)
    Gdey=Convolve2D(image,Grady,1,1)
    
    G=np.sqrt((Gdex**2)+(Gdey**2))
    
    return G
    
    
    

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
def pxlzc(img,xrate,yrate):
    """ Pixellize colorful images """
    n,p,q=img.shape

    t=n%xrate
    u=p%yrate
    
    if t!=0:
        r=n//xrate+1
    else:
        r=n//xrate
    
    if u!=0:
        s=p//yrate+1
    else:
        s=p//yrate
        
    pxld=np.zeros((r,s,q),dtype=np.uint8)
    

    for i in range(n//xrate):
        for j in range(p//yrate):
            for k in range(q):
                temp=0
                for l in range(xrate):
                    for m in range(yrate):
                        temp=temp+int(img[xrate*i+l,yrate*j+m,k])
                temp=int(temp/(xrate*yrate))
                pxld[i,j,k]=temp
    
    if t!=0:
        for j in range(p//yrate):
            for k in range(q):
                temp=0
                for l in range(n-t,n):
                    for m in range(yrate):
                        temp=temp+int(img[l,yrate*j+m,k])
                temp=int(temp/(t*yrate))
                pxld[r-1,j,k]=temp
    
    if u!=0:
        for i in range(n//xrate):
            for k in range(q):
                temp=0
                for l in range(xrate):
                    for m in range(p-u,p):
                        temp=temp+int(img[xrate*i+l,m,k])
                temp=int(temp/(u*xrate))
                pxld[i,s-1,k]=temp
    
    if u!=0 and t!=0:
        for k in range(q):
            temp=0
            for l in range(n-t,n):
                for m in range(p-u,p):
                    temp=temp+int(img[l,m,k])
            temp=int(temp/(t*u))
            pxld[r-1,s-1,k]=temp
    
    return pxld


@jit(nopython=True)
def pxlzg(img,xrate,yrate):
    """ Pixellize greyscale images"""
    n=img.shape[0]
    p=img.shape[1]
    t=n%xrate
    u=p%yrate
    if t!=0:
        r=n//xrate+1
    else:
        r=n//xrate
    
    if u!=0:
        s=p//yrate+1
    else:
        s=p//yrate
    
    pxld=np.zeros((r,s),dtype=np.uint8)
    
    for i in range(n//xrate):
        for j in range(p//yrate):
            temp=0
            for l in range(xrate):
                for m in range(yrate):
                    temp=temp+int(img[xrate*i+l,yrate*j+m])
            temp=int(temp/(xrate*yrate))
            pxld[i,j]=temp
            
    if t!=0:
        for j in range(p//yrate):
            temp=0
            for l in range(n-t,n):
                for m in range(yrate):
                    temp=temp+int(img[l,yrate*j+m])
            temp=int(temp/(t*yrate))
            pxld[r-1,j]=temp
    
    if u!=0:
        for i in range(n//xrate):
            temp=0
            for l in range(xrate):
                for m in range(p-u,p):
                    temp=temp+int(img[xrate*i+l,m])
            temp=int(temp/(u*xrate))
            pxld[i,s-1]=temp
    
    if u!=0 and t!=0:
        temp=0
        for l in range(n-t,n):
            for m in range(p-u,p):
                temp=temp+int(img[l,m])
        temp=int(temp/(t*u))
        pxld[r-1,s-1]=temp
    
    return pxld
    

@jit(nopython=True)
def invert(tab,ref):
    """ A function to invert the colors of a picture """
    img=tab.copy()
    n,p=img.shape[:2]
    for i in range(n):
        for j in range(p):
            if len(img.shape)==3 and img.shape[2]==4:
                img[i,j][:3]=ref-img[i,j][:3]
            else:
                img[i,j]=ref-img[i,j]
    return img


@jit(nopython=True)
def crop(img,h,w,startingPos,modifier):
    """ crops image, can be used to make it bigger with no color. It is supposed that the new dimensions fit into the older ones"""
    q = img.shape[2]
    padx = modifier[0]//2
    pady = modifier[1]//2
    newpix = modifier[2]
    startx=startingPos[0]
    starty=startingPos[1]
    
    new=np.zeros((h+2*padx,w+2*pady,q+newpix),dtype=np.uint8)
    
    if newpix==1:
        new[padx:padx+h,pady:pady+w,3]=255+new[padx:padx+h,pady:pady+w,3]
    
    for i in range(0,h):
        for j in range(0,w):
            new[i+padx,j+pady,:q]=img[i+startx,j+starty]
    
    return new



## Thermodynamics Simulation

@jit(nopython=True)
def CalcTkp1(M,d):
    N=M.shape[0]
    U=np.zeros((N))
    C=np.zeros((N-1))
    D_p=np.zeros((N))
    
    for i in range(N-1):
        if i==0:
            C[i]=M[i,i+1]/M[i,i]
        else:
            C[i]=M[i,i+1]/(M[i,i]-M[i,i-1]*C[i-1])
    
    for i in range(N):
        if i==0:
            D_p[i]=d[i]/M[i,i]
        else:
            D_p[i]=(d[i]-M[i,i-1]*D_p[i-1])/(M[i,i]-M[i,i-1]*C[i-1])
    
    for i in range(N):
        if i==0:
            U[N-1]=D_p[N-1]
        else:
            U[N-1-i]=D_p[N-1-i]-C[N-1-i]*U[N-i]

    return U

@jit(nopython=True)
def Thermodynamic_Graph(Tint,Text1,Text2,e,l,cp,rho,Dt,N,ItMax):
    alpha=(rho*cp)/l
    a=(Text1-Tint)/e
    b=Tint
    deltaX=e/N

    r=Dt/(alpha*(deltaX)**2)
    
    x=np.zeros(N+1)
    T_tous_k=np.zeros((N+1,ItMax))
    for i in range(N+1):
        x[i]=i*deltaX
        T_tous_k[i,0]=a*x[i]+b
        
    M=np.zeros((N+1,N+1))
    
    for i in range(N+1):
        M[i,i]=1+2*r
        if i<N:
            M[i,i+1]=-r
        if i>0:
            M[i,i-1]=-r
            
    nu=np.zeros((N+1))
    nu[0]=Tint
    nu[N]=Text2
    
    for i in range(1,ItMax):
        T_tous_k[:,i]=CalcTkp1(M,T_tous_k[:,i-1]+r*nu)
        
    return x,T_tous_k




@jit(nopython=True)
def Thermodynamic_Bitmap(Tint,Text1,Text2,e,l,cp,rho,Dt,N,ItMax,colors):
    
    x,temp_array=Thermodynamic_Graph(Tint,Text1,Text2,e,l,cp,rho,Dt,N,ItMax)
    
    Super_array=np.zeros((ItMax,2*N,N+1))
    super_coloured=np.zeros((ItMax,2*N,N+1,3),dtype=np.uint8)
    gradient=np.zeros((300,10,3),dtype=np.uint8)
    
    
    for j in range(ItMax):
    
        for i in range(N+1):
            Super_array[j,0,i]=temp_array[i,j]
        
        for i in range(1,2*N):
            Super_array[j,i,:]=Super_array[j,0,:]
    
    Tmin=min(Tint,Text1,Text2)
    Tmax=max(Tint,Text1,Text2)
    
    delta_color=(Tmax-Tmin)/N
    
    for i in range(ItMax):
        for k in range(N+1):
            if Super_array[i,0,k]<(Tmin):
                super_coloured[i,0,k]=colors[N]
            elif Super_array[i,0,k]>=(Tmax-delta_color):
                super_coloured[i,0,k]=colors[0]
            else:
                j=0
                while j<N:
                    if Super_array[i,0,k]<(Tmin+(j+1)*delta_color) and Super_array[i,0,k]>=(Tmin+j*delta_color):
                        super_coloured[i,0,k]=colors[N-j]
                        j=N
                    else:
                        j=j+1
        
        for k in range(1,2*N):
            super_coloured[i,k,:]=super_coloured[i,0,:]
            
            
    colorspan=300//N
            
    for i in range(300):
        index=i//colorspan
        gradient[i,0]=colors[index]
        
    for i in range(1,10):
        gradient[:,i]=gradient[:,0]
            
    return super_coloured,gradient,Super_array


## Matrix Functions

@jit(nopython=True)
def Augmente(A,B):
    """Concaténation de la matrice de variables et la matrice de résultat"""
    n=A.shape[0]
    C=np.zeros((n,n+1))
    for i in range(n):
        for j in range(n):
            C[i,j]=A[i,j]
        C[i,n]=B[0,i]
    return C

@jit(nopython=True)
def Echangeligne(M,i,j):
    """ Opération élémentaire de permutation """
    Matrix=M.copy()
    n=Matrix.shape[0]



    E=Matrix[i,:].copy()
    Matrix[i,:]=Matrix[j,:].copy()
    Matrix[j,:]=E.copy()
    return Matrix

@jit(nopython=True)
def Elimine(M,i,j,l):
    """ Opération élémentaire de transvection """
    Matrix=M.copy()
    n=Matrix.shape[0]

    Matrix[j,:]=Matrix[j,:]+l*Matrix[i,:]
    return Matrix

@jit(nopython=True)
def Normalise(M,i,l):
    """ Opération élémentaire de dilatation """
    Matrix=M.copy()
    n=Matrix.shape[0]



    Matrix[i,:]=l*Matrix[i,:]
    return Matrix

@jit(nopython=True)
def Pivot(M,i):
    """ Détection du pivot """
    n=M.shape[0]

    max=0
    maxindex=0
    for j in range(i,n):
        if abs(M[j,i])>max:
            max=abs(M[j,i])
            maxindex=j
    if max==0:
        raise ValueError("Aucun pivot trouvé")
        
    return(maxindex)

@jit(nopython=True)
def Secondmb(M):
    """Retourne la dernière colonne de la matrice"""
    n=M.shape[0]

    D=M[:,n].copy().reshape(n,1)
    return(D)

@jit(nopython=True)
def Gauss(A,B):
    """Fonction qui automatise la résolution de la mtrice, si elle est inversible"""
    n=A.shape[0]
    M=Augmente(A,B)
    for i in range(0,n):
        i_piv = Pivot(M,i)
        if i!=i_piv:
            M=Echangeligne(M,i,i_piv)
        for j in range(0,n):
            if j!=i:
                l=-M[j,i]/M[i,i]
                M=Elimine(M,i,j,l)
        l=1/M[i,i]
        M=Normalise(M,i,l)
    return(Secondmb(M))
    
@jit(nopython=True)
def F(A):
    n,p=A.shape
    F=np.zeros((n,p))
    for i in range(n):
        for j in range(p):
            if i<j:
                F[i,j]=A[i,j]
    return F

@jit(nopython=True)
def E(A):
    n,p=A.shape
    E=np.zeros((n,p))
    for i in range(n):
        for j in range(p):
            if i>j:
                E[i,j]=A[i,j]
    return E

@jit(nopython=True)
def D(A):
    n,p=A.shape
    D=np.zeros((n,p))
    for i in range(n):
        for j in range(p):
            if i==j:
                D[i,j]=A[i,j]
    return D

@jit(nopython=True)
def Jacobi(A,B):
    G=D(A)
    H= -F(A)-E(A)
    X=np.zeros((B.shape[0],1))
    G1=np.linalg.inv(G)
    M=np.dot(G1,H)
    N=np.dot(G1,B)
    for i in range(1000000):
        X=np.dot(M,X)+N
    return X

@jit(nopython=True)
def GaussSeidel(A,B):
    G=D(A) + E(A)
    H= -F(A)
    X=np.zeros((B.shape[0],1))
    G1=np.linalg.inv(G)
    M=np.dot(G1,H)
    N=np.dot(G1,B)
    for i in range(100):
        X=np.dot(M,X)+N
    return X
