#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 14:34:49 2018

@author: matthieubriet et PIERRECASTRESSAINTMARTIN
"""

import PIL
from PIL import Image
from PIL import ImageOps
import numpy as np
import matplotlib.pyplot as plt
#import cv2
#
#'etape 0 : extraction des images' 
#""" fonction d'extraction des images de la video """
#def extractionimage(nom):  # nom = 'video.mp4' par exemple 
#    cap=cv2.VideoCapture(nom)
#    path_img='images/'
#    os.mkdir(path_img)
#    
#    nb_frames=cap.get(cv2.CAP_PROP_FRAME_COUNT)
#    longueur= len(str(int(nb_frames)))
#    
#    fps=cap.get(cv2.CAP_PROP_FPS)
#    
#    print('extraction des images')
#    while  (cap.get(cv2.CAP_PROP_POS_FRAMES)!=nb_frames):
#        ret, frame=cap.read()
#        nom=path_img+'images_'+str(int(cap.get(cv2.CAP_PROP_POS_FRAMES))).zfill(longueur)+'.jpg'
#        cv2.imwrite(nom,frame)
#    cap.release()
#    print('extraction des images terminée')
#    
#""" etape 1: Traitement des images """
#
#def seuil(L): # fonction applicable a une ligne
#    R=200
#    V=250
#    for i in range(len(L)):
#        if L[i][0]>=R and L[i][1]<V:
#            L[i]=(255,255,255)
#        else:
#            L[i]=(0,0,0)
#    return L
#
#
#def subpixel_ligne(L): #sur une ligne on fait le barycente de chaque ligne 
#    somme1=0
#    somme2=0
#    n=len(L)
#    for i in range(n):
#        for j in range(3):    #RVB
#            if (L[i][j]!=[0,0,0]).all(): # verifier egalite sur des array
#                somme1+=i*i
#                somme2+=i
#    if somme2==0:  # cas ligne noire
#        u=None
#        L2=[]
#        for i in range(n):
#            L2.append([0,0,0])
#    else:
#        u=int(somme1/somme2)              #barycentre
#        L2=[]
#        for i in range(n):
#            if i!=u:
#                L2.append([0,0,0])
#            else:
#                L2.append([255,255,255])
#    return np.array(L2),u   # nouvelle ligne 
#
#
#class Piece():
#    def __init__(self,tonimage,tonangle):
#        self.Image=str(tonimage)
#        self.Angle=float(tonangle)
#        self.Matrice=[]
#        self.x=0    #x pour ligne
#        self.y=0    # y pour colonne
#        
#    def ImporterImage(self):
#        image=PIL.Image.open(self.Image,mode='r')
#        self.Matrice=np.array(image)
#        
#    def SizeImage(self):
#        self.x=self.Matrice.shape[0]
#        self.y=self.Matrice.shape[1]
#        
#    def matrice_seuil(self):
#        for i in range(self.x):
#            self.Matrice[i]=seuil(self.Matrice[i])
#            
#    def subpixel_matrice(self):
#        M2=[]
#        for i in range(self.x):
#            L,u=subpixel_ligne(self.Matrice[i])
#            M2.append(L)
#        self.Matrice=np.array(M2)
#        
#    
#    def affichage(self):
#        plt.imshow(self.Matrice)
#        plt.show()
#
# 
#           
#class Ligne(Piece):
#    
#    def __init__(self,tonimage,tonangle):
#        super().__init__(tonimage,tonangle)
#        self.ligne=[]
#        
#    def ligne_laser(self):
#        print("a")
#        for i in range(self.x):
#            a=i
#            for j in range(self.y):
#                b=j
#                if self.Matrice[i][j][0]==255:
#                    self.ligne.append([a,b])
#
#
#   
#            
#        
#        
#        
#
#b=Ligne("0.JPG","0")
#
#b.ImporterImage()  
#b.SizeImage() 
#
#b.matrice_seuil()
#b.subpixel_matrice()
#b.affichage()
#b.ligne_laser()
#print(b.ligne)

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
    #plt.plot(Xcamera,Ycamera)
    return [Xcamera,Ycamera]



def changement_repere_monde(coordonnée_camera,f,beta,alpha):  #alpha = angle d'inclinaison de la camera; beta=angle entre le laser et la camera (alpha= 20,b=30 f=52) a mettre en radian
    Xm=[]
    Ym=[]
    Zm=[]
    n=len(coordonnée_camera[0])
    z=[-f]*n
    
    coordonnée_camera.append(z)
    
    P=np.array([[-np.cos(beta),-np.sin(beta),0],[np.sin(beta)*np.sin(alpha),-np.cos(beta)*np.sin(alpha),np.cos(alpha)],[-np.cos(alpha)*np.sin(beta),np.cos(alpha)*np.cos(beta),np.sin(alpha)]])
    P2=np.linalg.inv(P)    #P2 est la matrice inversé de P (On a besoin de P2 pour resoudre le systeme)*
    coordonnées_repere_monde=[]
    vecteur=[]
    for i in range(len(coordonnée_camera[0])):
    
        vecteur=np.array([[coordonnée_camera[0][i]],[coordonnée_camera[1][i]],[-f]])
        vecteur=np.dot(P2,vecteur)
        t=(l1**2-h1**2)**0.5*np.sin(beta)/(vecteur[0])
        #print(i)
        
        Xm.append(0)
        Ym.append((l1**2-h1**2)**0.5*np.cos(beta)+t*vecteur[1][0])
        Zm.append(h1+t*vecteur[2][0])
    #print(Ym)
    
    return [Xm,Ym,Zm]
plt.plot(changement_repere_monde(changement_repere_camera('0.jpg'),52,0.523,0.349)[1],changement_repere_monde(changement_repere_camera('0.jpg'),52,0.523,0.349)[2],".")   
#test :   changement_repere_monde(changement_repere_camera('0.jpg'),52,0.523,0.349)
#print(changement_repere_monde(changement_repere_camera('0.jpg'),52,0.523,0.349)[1][12])


def passage_3D (coordonnées_repere_monde,angle_table):
    X3=[]
    Y3=[]
    Z3=[]
    for i in range (len(coordonnées_repere_monde[0])):
        X3.append(coordonnées_repere_monde[1][i]*np.sin(angle_table))
        Y3.append(coordonnées_repere_monde[1][i]*np.cos(angle_table))
        Z3.append(coordonnées_repere_monde[2][i])
    return [X3,Y3,Z3]

#passage_3D(changement_repere_monde(changement_repere_camera('0.jpg'),52,0.523,0.349),0)
#plt.plot(passage_3D(changement_repere_monde(changement_repere_camera('0.jpg'),52,0.523,0.349),0)[0],passage_3D(changement_repere_monde(changement_repere_camera('0.jpg'),52,0.523,0.349),0)[1],passage_3D(changement_repere_monde(changement_repere_camera('0.jpg'),52,0.523,0.349),0)[2],".")
print(passage_3D(changement_repere_monde(changement_repere_camera('0.jpg'),52,0.523,0.349),0.4)[2])


        
        
        
        
        
