import numpy as np


def lagrange(f, a, b, e):
    if a > b:
        c = a
        a = b
        b = c
    elif a == b:
        raise ValueError("Les bornes doivent être différentes.")

    if f(a) == 0:
        b = a
    elif f(b) == 0:
        a = b

    if f(a) * f(b) > 0:
        raise ValueError("Les valeurs aux bornes doivent être de signe différent")
    # found=False
    # 
    # if f(a)*f(b)>0:
    #     for x in range(int(a),int(b)):
    #         if f(x)*f(a)<0:
    #             found=True
    #             b=x
    #             break
    #         elif f(x)==0:
    #             found=True
    #             a=x
    #             b=x
    # 
    # if not found:
    #     raise ValueError("La fonction ne s'annule pas sur l'intervalle.")
    i = 0
    while b - a > e and i < 500:
        m = (a * f(b) - b * f(a)) / (f(b) - f(a))
        if f(m) == 0:
            a = m
            b = m
        elif f(m) * f(a) < 0:
            b = m
        else:
            a = m
        i += 1

    return (a, b)


"""
def newtontry(f,a,b,e):
    if a>b:
        c=a
        a=b
        b=c
    elif a==b:
        raise ValueError("Les bornes doivent être différentes.")
    
    if f(a)==0:
        b=a
    elif f(b)==0:
        a=b
    
    if f(a)*f(b)>0:
        raise ValueError("Les valeurs aux bornes doivent être de signe différent")
        
    h=max((b-a)/1000,0.01)
    
    while abs(b-a)>e:
        da=(f(a+h)-f(a))/h
        db=(f(b+h)-f(b))/h
        
        if f(a)>0:
            if da>db:
                x1=b-(f(b)/db)
                x0=a
                if x1<a:
                    x1=b
                    x0=a-(f(a)/da)
                
            else:
                x0=a-(f(a)/da)
                x1=b
                if x0>b:
                    x1=b-(f(b)/db)
                    x0=a
            a=x0
            b=x1
                    
        elif f(a)<0:
            if da<db:
                x1=b-(f(b)/db)
                x0=a
                if x1<a:
                    x1=b
                    x0=a-(f(a)/da)
                
            else:
                x0=a-(f(a)/da)
                x1=b
                if x0>b:
                    x1=b-(f(b)/db)
                    x0=a
            a=x0
            b=x1
        else:
            b=a
        print(f(a),f(b))
    return a,b              
    """


def dichotomie(f, a, b, e):
    if a > b:
        c = a
        a = b
        b = c
    elif a == b:
        raise ValueError("Les bornes doivent être différentes.")

    if f(a) == 0:
        b = a
    elif f(b) == 0:
        a = b

    if f(a) * f(b) > 0:
        raise ValueError("Les valeurs aux bornes doivent être de signe différent")

    while b - a > e:
        m = (a + b) / 2
        if f(m) == 0:
            a = m
            b = m
        elif f(m) * f(a) < 0:
            b = m
        else:
            a = m

    return (a, b)


def newton(f, a, b, e):
    if a > b:
        c = a
        a = b
        b = c
    elif a == b:
        raise ValueError("Les bornes doivent être différentes.")

    if f(a) == 0:
        b = a
    elif f(b) == 0:
        a = b

    if f(a) * f(b) > 0:
        raise ValueError("Les valeurs aux bornes doivent être de signe différent")

    x0 = a
    x1 = b
    h = max(x0 / 100, 0.001)
    while abs(x1 - x0) > e:
        x0 = x1
        d = (f(x0 + h) - f(x0)) / h
        x1 = x0 - f(x0) / d
    return x1
