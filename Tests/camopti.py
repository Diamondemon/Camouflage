import os
from pylab import *
import scipy.misc as scm
import numpy as np
from random import randrange
import time
from numba import njit

os.chdir(os.path.dirname(__file__))


@njit
def bpf_m(im_m):
    n=im_m.shape[0]
    p=im_m.shape[1]

    for i in range(n):
        for j in range(p):
            im_m[i,j,0]=im_m[i,j,0]&0b11110000
            im_m[i,j,1]=im_m[i,j,1]&0b11110000
            im_m[i,j,2]=im_m[i,j,2]&0b11110000


    return im_m

@njit
def bpf_s(im_s):
    n=im_s.shape[0]
    p=im_s.shape[1]

    for i in range(n):
        for j in range(p):
            im_s[i,j][0]=(im_s[i,j][0]&0b11110000)>>4
            im_s[i,j][1]=(im_s[i,j][1]&0b11110000)>>4
            im_s[i,j][2]=(im_s[i,j][2]&0b11110000)>>4

    return im_s

@njit
def bpf_c(im_c):
    n=im_c.shape[0]
    p=im_c.shape[1]

    for i in range(n):
        for j in range(p):
            im_c[i,j][0]=(im_c[i,j][0]&0b00001111)<<4
            im_c[i,j][1]=(im_c[i,j][1]&0b00001111)<<4
            im_c[i,j][2]=(im_c[i,j][2]&0b00001111)<<4
    return im_c

@njit
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

@njit
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

start = time.time()

im_masque=scm.imread("monkey.bmp")


im_secret=scm.imread("ela.bmp")

im_masque=bpf_m(im_masque)
scm.imsave("masqonkey.bmp",im_masque)
im_secret=bpf_s(im_secret)


if (im_masque.shape[2])>(im_secret.shape[2]):
    np.delete(im_masque,im_masque.shape[2]-1,2)
elif (im_masque.shape[2])<(im_secret.shape[2]):
    np.delete(im_masque,im_secret.shape[2]-1,2)

im_fin = add_im(im_masque,im_secret)

scm.imsave("camonkey.bmp",im_fin)

im_cach=scm.imread("camonkey.bmp")

im_cach=bpf_cplus(im_cach)

scm.imsave("recuponkey.bmp",im_cach)

end = time.time()
print("Elapsed (with compilation) = %s" % (end - start))



input("hey?")