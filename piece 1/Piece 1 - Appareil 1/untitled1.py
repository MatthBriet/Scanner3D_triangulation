#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 01:19:11 2019

@author: matthieubriet
"""
import PIL
from PIL import Image
from PIL import ImageOps
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
h1=625
l1=1430



"""base de l'etape 2 quelques petites choses a modifier pour que ca soir correct en POO..."""
def changement_repere_camera(img):      #img = image sur laquelle on travaille
    Xcamera=[]
    Ycamera=[]
    imgpil=Image.open(img)
    image=np.asarray(imgpil)
    k = (1290/197)*(1430/52)
    for i in  range (2700,3400):          #les pixels comprenant la piece pour pas faires des calculs long sur des étapes innutiles...
        for j in  range(2300,3300):
            if int(image[i,j][0])>int(254):        #on verifie que le pixel est rouge
                Ycamera.append((-i+4000/2)/k)
                Xcamera.append((j-3089)/k)
            else:
                pass                #si le pixel est pas rouge on ne le passe pas dans le repere car innutile
    plt.plot(Xcamera,Ycamera)
    return [Xcamera,Ycamera]



def changement_repere_monde(coordonnée_camera,f,alpha,beta):  #alpha = angle d'inclinaison de la camera; beta=angle entre le laser et la camera (alpha= 20,b=30 f=52) a mettre en radian
    Xm=[]
    Ym=[]
    Zm=[]
    alpharad=alpha*np.pi/180
    betarad=beta*np.pi/180
    n=len(coordonnée_camera[0])
    z=[-f]*n
    
    coordonnée_camera.append(z)
    
    P=np.array([[-np.cos(betarad),-np.sin(betarad),0],[np.sin(betarad)*np.sin(alpharad),-np.cos(betarad)*np.sin(alpharad),np.cos(alpharad)],[-np.cos(alpharad)*np.sin(betarad),np.cos(alpharad)*np.cos(betarad),np.sin(alpharad)]])
    P2=np.linalg.inv(P)    #P2 est la matrice inversé de P (On a besoin de P2 pour resoudre le systeme)*
    coordonnées_repere_monde=[]
    vecteur=[]
    for i in range(len(coordonnée_camera[0])):
    
        vecteur=np.array([[coordonnée_camera[0][i]],[coordonnée_camera[1][i]],[-f]])
        vecteur=np.dot(P2,vecteur)
        t=(l1**2-h1**2)**0.5*np.sin(betarad)/(vecteur[0])
        #print(i)
        
        Xm.append(0)
        Ym.append((l1**2-h1**2)**0.5*np.cos(betarad)+t*vecteur[1][0])
        Zm.append(h1+t*vecteur[2][0])
        plt.plot(Ym,Zm)
    #print(Ym)
    
    return [Xm,Ym,Zm]

def affichage_3D(L):
    fig=plt.figure()
    ax=fig.add_subplot(111,projection="3d")
    X,Y,Z=[],[],[]
    for x in L:
        X.append(x[0])
        Y.append(x[1])
        Z.append(x[2])
    ax.scatter(X,Y,Z)
    plt.show()
 
camera=changement_repere_camera('0.jpg') 
   
monde=changement_repere_monde(camera,52,20,30)   
print(monde)
affichage_3D(monde)
#print(changement_repere_monde(changement_repere_camera('0.jpg'),52,0.523,0.349)[1],changement_repere_monde(changement_repere_camera('0.jpg'),52,0.523,0.349)[2],".")   
#plt.plot(changement_repere_monde(changement_repere_camera('0.jpg'),52,0.523,0.349)[1],changement_repere_monde(changement_repere_camera('0.jpg'),52,0.523,0.349)[2],".")   
#test :   changement_repere_monde(changement_repere_camera('0.jpg'),52,0.523,0.349)

