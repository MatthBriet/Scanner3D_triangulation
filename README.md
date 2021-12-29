# Projet POO : Scanner 3D par triangulation

## Auteurs 
* Matthieu Briet : matthieu.briet@student-cs.fr


## Introduction & Description du projet

On souhaite concevoir et implémenter un outil permettant de reconstruire un modèle 3D d’un objet existant à des fins de contrôle dimensionnel sans contact... Dans le cadre de ce projet POO, c’est la stratégie par triangulation qui est retenue parmi les nombreuses solutions disponibles, comme par exemple les approches : par profil, par lumière structurée,stéréoscopiques...

Le principe de fonctionnement de cette approche est illustré par la vidéo Youtube suivante : https://www.youtube.com/watch?v=RVgyyIlQydg. Cette approche est intéressante car elle peut, à faible coût, être mise en œuvre, mais à des niveaux de précisions relativement faibles.

Prise de mesures : Un objet, posé sur une table rotative indexée, est frappé par un laser ligne fixe. Une caméra, fixe également, enregistre l’image (ou la vidéo) ainsi reçue de l’objet éclairé par la ligne laser. Il est ainsi possible de retrouver le profil de cette intersection laser/objet. La table est alors mise en rotation et plusieurs photographies (ou un film) sont alors effectuées et enregistrées.
C’est l’étape de traitement de ces photos (ou de photos extraites du film) qui aboutit à la définition numérique 3D du volume de l’objet ainsi numérisé. Cette étape de traitement est le but de ce projet de l’UEF POO.
Reconstruction du modèle 3D : Les différentes photos de l’objet doivent être analysées pour identifier des points de la surface de l’objet illuminé par le laser. Une fois ces points identifiés, il est nécessaire, en considérant l’angle de la table, la position et l’orientation de la caméra et de ses caractéristiques, d’effectuer un changement de repère et une projection pour passer du repère caméra à celui de l’objet. Une fois ces opérations effectuées, une «tranche» de l’objet est numérisée. La dernière étape consiste à fusionner ce morceau avec l’ensemble des autres tranches provenant des autres vues de ce même objet.

L'énoncé du sujet est donné dans le fichier Projet 2018-S1-V1.0.pdf

## Prise en main 

Il suffit de lancer le fichier image2stl.py et de taper "photo" dans l'invite de commande pour générer un modèle de l'objet au format STL. 


## Améliorations possibles : 

 - Générer un modèle STL à partir de la vidéo 


