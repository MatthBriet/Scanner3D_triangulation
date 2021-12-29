#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 14:27:13 2019

@author: matthieubriet
"""
"""
On importe les differents modules necessaires à la realisation du programme
"""

import PIL
from PIL import Image
from PIL import ImageOps
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2


"""
etape 0 extraction des videos  grace au module opencv 

"""


def video_to_image(monfichier):
    video=cv2.VideoCapture(monfichier)
    j=0
    for i in range(800):
        a , image= video.read()
        cv2.imwrite("%d.jpg" %j, image)
        j+=1

#video_to_image("Piece 1 - Appareil 2.mp4") 

  
""" etape 1: Traitement des images """


'Paramètres Piece1'

"On ressence l'ensemble des parametres pour avoir une modification plus aisé du programme"
hauteur_piece=197 # hauteur piece independant de 1 ou 2
"appareil1"
Y1min=2700  #rognage de l'image
Y1max=3400  #rognage de l'image
X1min=2300  #rognage de l'image
X1max=3300  #rognage de l'image

h1=625      # valeur du tableau excel
l1=1430     # valeur tableau excel
alpha1=20   # valeur tableau excel
beta1=30    # valeur tableau excel
f1=52       # valeur tableau excel
hi1=4000    #hauteur de l'image en pixel
ci1=3089    #coordonnee en largeur du trou dans la piece 
hp1=1290    # hauteur de la piece en pixel
k1 = (hp1/hauteur_piece)*(l1/f1)

"appareil 2 photo "
Y2min=1900
Y2max=3000          #coordonnées utiles au rognage de l'image
X2min=1100
X2max=2800

h2=550
l2=1295
alpha2=18           #parametres propre à l'appareil 2
beta2=18.8
f2=42
hi2=3456    #hauteur de l'image en pixel
ci2=2550    #coordonnee en largeur du trou dans la piece 
hp2=1096    #hauteur de la piece en pixel

k2=(hp2/hauteur_piece)*(l2/f2)

"données video appareil 2"

Ymin=420            #coordonnées utile au rognage de l'image
Ymax=920
Xmin=860
Xmax=1200 

hiv=1080    #hauteur de l'image issue des videos en pixel
hpv=408     #coordonnee en largeur du trou dans la piece pour les images issus des vidéos 
civ=1030     #hauteur de la piece en pixel pour les images issus des vidéos 

kv=(hpv/hauteur_piece)*(l2/f2)      #k de la video



def calcul_normale(a,b,c,d,e,f,g,h,i):
    """
    cette fonction nous permet d'éffectuer un produit vectoriel
    """
    return [(b-e)*(f-i)-(c-f)*(e-h),(c-f)*(d-g)-(f-i)*(a-d),(a-d)*(f-h)-(b-e)*(d-g)]



class Piece():
    def __init__(self):
        self.Mapiece=[]
               
    
    def ajouter_ligne_a_ma_piece(self,ligne):
        if isinstance(ligne,Ligne):
            self.Mapiece.append(ligne.Repere)
            
            
    def STL(self):
        """
        cette methode permet d'afficher la representation de la piece sur STL
        """
        longueur=0
        triangle_tot=[]
        n=len(self.Mapiece)
        for i in range(n-1): # nbre de ligne
            longueur=min(len(self.Mapiece[i][0]),len(self.Mapiece[i+1][0]))
            for j in range(longueur-1): # pas avoir de +1 en fin de ligne
                triangle1=[[self.Mapiece[i][0][j],self.Mapiece[i][1][j],self.Mapiece[i][2][j]],[self.Mapiece[i][0][j+1],self.Mapiece[i][1][j+1],self.Mapiece[i][2][j+1]],[self.Mapiece[i+1][0][j],self.Mapiece[i+1][1][j],self.Mapiece[i+1][2][j]]]
                triangle2=[[self.Mapiece[i+1][0][j],self.Mapiece[i+1][1][j],self.Mapiece[i+1][2][j]],[self.Mapiece[i+1][0][j+1],self.Mapiece[i+1][1][j+1],self.Mapiece[i+1][2][j+1]],[self.Mapiece[i][0][j+1],self.Mapiece[i][1][j+1],self.Mapiece[i][2][j+1]]]
                triangle_tot.append(triangle1)
                triangle_tot.append(triangle2)
        
        longueur2=min(len(self.Mapiece[len(self.Mapiece)-1][0]),len(self.Mapiece[0][0])) # raccolement premiere et derniere ligne
        for j in range(longueur2-1): # pas avoir de +1 en fin de ligne
                triangle1=[[self.Mapiece[n-1][0][j],self.Mapiece[n-1][1][j],self.Mapiece[n-1][2][j]],[self.Mapiece[n-1][0][j+1],self.Mapiece[n-1][1][j+1],self.Mapiece[n-1][2][j+1]],[self.Mapiece[0][0][j],self.Mapiece[0][1][j],self.Mapiece[0][2][j]]]
                triangle2=[[self.Mapiece[0][0][j],self.Mapiece[0][1][j],self.Mapiece[0][2][j]],[self.Mapiece[0][0][j+1],self.Mapiece[0][1][j+1],self.Mapiece[0][2][j+1]],[self.Mapiece[n-1][0][j+1],self.Mapiece[n-1][1][j+1],self.Mapiece[n-1][2][j+1]]]
                triangle_tot.append(triangle1)
                triangle_tot.append(triangle2)
        fichier=open("STL.stl",'w')
        fichier.write("solid Piece1\n")
        for i in triangle_tot:
            a=i[0][0][0]
            b=i[0][1][0]
            c=i[0][2][0]
            d=i[1][0][0]
            e=i[1][1][0]
            f=i[1][2][0]
            g=i[2][0][0]
            h=i[2][1][0]
            i=i[2][2][0]
            normale=calcul_normale(a,b,c,d,e,f,g,h,i)           #on effcetue le produit vectoriel pour determiner la normale
            fichier.write("facet normal "+str(normale[0])+" "+str(normale[1])+" "+str(normale[2])+"\n")
            fichier.write("\touter loop\n")
            fichier.write("\t\tvertex "+str(a)+" "+str(b)+" "+str(c)+"\n")
            fichier.write("\t\tvertex "+str(d)+" "+str(e)+" "+str(f)+"\n")
            fichier.write("\t\tvertex "+str(g)+" "+str(h)+" "+str(i)+"\n")
            fichier.write("\tendloop\n")
            fichier.write("endfacet\n")
        fichier.write("endsolid Piece1\n")
        fichier.close()
 
Xtot=[]
Ytot=[]
Ztot=[]           
class Ligne(Piece):
    
    
    def __init__(self,tonimage):
        self.Image=str(tonimage)
        print(self.Image)
        a,b=str(tonimage).split(".")
        if type_traitement=="video":
            val=str(a)#.split("/")[2]
        elif type_traitement=="image":
            val=str(a).split("/")[2]
        if type_traitement=="video":
            self.Angle=float(val)*np.pi/180*360/799
        elif type_traitement=="image":
            self.Angle=float(val)*np.pi/180
        self.Matrice=[]
        self.ligne=[]
        self.Camera=[]
        self.Monde=[]
        self.Repere=[]
        
        
         
    def ImporterImage(self):
        image=PIL.Image.open(self.Image,mode='r')
        self.Matrice=np.array(image)
        
        

                    
    def changement_repere_camera(self,Xmin,Xmax,Ymin,Ymax,hi,ci,k):
        """
        avec cette fonction on passe dans le repere camera en mm depuis le repere image en pixel
        """
        Xcamera=[]
        Ycamera=[]
        if type_traitement=="video":        #Ces filtres nous permettent d'enlever les points trop loin
            filtre=0.5
        elif type_traitement=="image":      
            filtre=0.2
       
        for i in range(Ymin,Ymax):
            L=[]
            
            for j in range(Xmin,Xmax):
                if int(self.Matrice[i,j][0])>int(254):      #on effectue un premier filtrage: on s'interesse que au pixels rouge  
                    L.append(j)
            if len(L)>0:
                n=len(L)
                y=sum(L)
                position=int(y/n)                   #on prend la moyenne des positions des pixels rouges lorsqu'il y en a trop 
                if len(Xcamera)==0:
                    Ycamera.append((-i+hi/2)/k)         #On change l'origine du repère puis on passe en mm 
                    Xcamera.append((position-ci)/k)
                elif abs((position-ci)/k-Xcamera[-1])<filtre :      #On effectue un second filtre pour supprimer les points parasites
                    Ycamera.append((-i+hi/2)/k)
                    Xcamera.append((position-ci)/k)
        self.Camera.append(Xcamera)
        self.Camera.append(Ycamera)
        #plt.plot(Xcamera,Ycamera,".")
        #plt.show()
                    
    
    def changement_repere_monde(self,f,beta,alpha,h,l): #alpha = angle d'inclinaison de la camera; beta=angle entre le laser et la camera (alpha= 20,b=30 f=52) a mettre en radian
        """
        Cette fonction permet de projeter les points du repere camera dans le plan laser
    
    
        pour determiner les coordonnes dans le plan laser, nous resolvons un systeme XP=Y avec P la matrice de rotation et Y le vecteur directeur du plan laser
        """
        Xm=[]
        Ym=[]
        Zm=[]
        alpharad=alpha*np.pi/180        #On passe les angles en radian pour les utiliser dans les cos et sin 
        betarad=beta*np.pi/180
        n=len(self.Camera[0])
        
        z=[-f]*n
        self.Camera.append(z)
        P=np.array([[-np.cos(betarad),-np.sin(betarad),0],[np.sin(betarad)*np.sin(alpharad),-np.cos(betarad)*np.sin(alpharad),np.cos(alpharad)],[-np.cos(alpharad)*np.sin(betarad),np.cos(alpharad)*np.cos(betarad),np.sin(alpharad)]])
        P2=np.linalg.inv(P)    #P2 est la matrice inversé de P (On a besoin de P2 pour resoudre le systeme)*
        
        vecteur=[]
        for i in range(n):
    
            vecteur=np.array([[self.Camera[0][i]],[self.Camera[1][i]],[-f]])
            vecteur=np.dot(P2,vecteur)      #On inverse la matrice de rotation 3*3
            t=(l1**2-h1**2)**0.5*np.sin(betarad)/(vecteur[0])
            
        
            Xm.append(0)
            Ym.append((l1**2-h1**2)**0.5*np.cos(betarad)+t*vecteur[1][0])
            Zm.append(h1+t*vecteur[2][0])
        self.Monde.append(Xm)
        self.Monde.append(Ym)
        self.Monde.append(Zm)
        
        
    def passage_3D(self):
        """
        Une fois les coordonnées dans le plan laser, on effectue une derniere rotation pour passer en 3D: On prend en compte la rotation de la piece entre chaque photo 
        """
        X3=[]
        Y3=[]
        Z3=[]
        for i in range (len(self.Monde[0])):
            X3.append(self.Monde[1][i]*np.sin(self.Angle))
            Xtot.append(self.Monde[1][i]*np.sin(self.Angle))
            Y3.append(self.Monde[1][i]*np.cos(self.Angle))
            Ytot.append(self.Monde[1][i]*np.cos(self.Angle))
            Z3.append(self.Monde[2][i])
            Ztot.append(self.Monde[2][i])
        self.Repere.append(X3)
        self.Repere.append(Y3)
        self.Repere.append(Z3)
        
    def transfo_array(self):
        self.Monde=np.array(self.Monde)
        
    def affichage_ligne(self):
        plt.plot(self.Repere[0],self.Repere[1],self.Repere[2],figure="1")
        

""" petite interface graphique"""
print("Veuillez choisir entre traitement d'image ou de video :")
type_traitement=input()
type_traitement=str(type_traitement)        

if type_traitement=="video":
    print("Extraction des images de la vidéo")
    video_to_image("Piece 1 - Appareil 2.mp4")
    print("fin de l'extraction")
    Piece1=Piece()
    print("traitement des lignes")
    for i in range(0,799,10):

        ligne2=Ligne("{}.JPG".format(str(i)))
        ligne2.ImporterImage() 
        ligne2.changement_repere_camera(Xmin,Xmax,Ymin,Ymax,hiv,civ,kv)
        ligne2.changement_repere_monde(f2,beta2,alpha2,h2,l2)
        ligne2.passage_3D()
        Piece1.ajouter_ligne_a_ma_piece(ligne2)
    Piece1.STL() 
    print("Création du fichier STL réalisée")
        
        
elif type_traitement=="image":
    Piece1=Piece()
    print("traitement des lignes")
    for i in range(0,360,10):
#    ligne1=Ligne("piece 1/Piece 1 - Appareil 1/{}.JPG".format(str(i)))
#    ligne1.ImporterImage() 
#    ligne1.changement_repere_camera(X1min,X1max,Y1min,Y1max,hi1,ci1,k1)
#    ligne1.changement_repere_monde(f1,beta1,alpha1,h1,l1)
#    ligne1.passage_3D()
#    Piece1.ajouter_ligne_a_ma_piece(ligne1)
        ligne2=Ligne("piece 1/Piece 1 - Appareil 2/{}.JPG".format(str(i)))
        ligne2.ImporterImage() 
        ligne2.changement_repere_camera(X2min,X2max,Y2min,Y2max,hi2,ci2,k2)
        ligne2.changement_repere_monde(f2,beta2,alpha2,h2,l2)
        ligne2.passage_3D()
        Piece1.ajouter_ligne_a_ma_piece(ligne2)
    Piece1.STL() 
    print("Création du fichier STL réalisée")
    
else:
    print("erreur il faut taper image ou video")
##fig=plt.figure()
##ax=fig.add_subplot(111,projection='3d')
##ax.scatter(Xtot,Ytot,Ztot,c='r',marker='.')
##plt.show()    
    


