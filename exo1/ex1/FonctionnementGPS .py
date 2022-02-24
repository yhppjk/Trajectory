# -*- coding: utf-8 -*-
#!/usr/bin/env python


#étape 1, installer utm si pas déjà réalisé
#lancer un shell anaconda
#pip install utm
from cmath import e
import re

import utm

#étape 2, installer pygame si pas déjà réalisé 
#lancer un shell anaconda
#pip install pygame
import pygame

#étape 3, installer pynmea2 si pas déjà réalisé 
#lancer un shell anaconda
#pip install pynmea2
import pynmea2


#étape 4, installer g1fitting si pas déjà réalisé
#lancer un shell anaconda
#conda install py-boost
#lancer un shell anaconda en mode administrateur
#aller dans le répertoire ou se trouve g1fitting (par exemple D:\data\work\carla\installg1fitting\g1fitting-masterWindows\g1fitting-master)
#compiler pyton setup.py build
#installer : python setup.py install

#import g1fitting as gf

import numpy as np
import matplotlib.pyplot as plt

#ouvrir un fichier de trajectoire gps et le parser
myFile=open("./GPS_Proflex800_output.s8","r")
linesOfFile = myFile.readlines()
myFile.close()


utmValues=[]#liste dans laquelle il faut metre utmx, utmy, utmx, utmy,...
for lines in linesOfFile:
    
    matchObj = re.search( r'GPGGA', lines)
    if not matchObj :
        continue
    else:
		msg = pynmea2.parse(lines)
   		if not msg.latitude :
			   continue

utmlist = utm.from_latlon(msg.latitude, msg.longitude)
utmValues.append(utmlist[0])
utmValues.append(utmlist[1]) 


utmValues=np.array(utmValues)
utmValues=utmValues.reshape((-1,2))#for 
np.savetxt("./trajectoryIMU.csv",utmValues)
#plt.subplot(2, 1, 1)
plt.plot(utmValues[:,0],utmValues[:,1],color="r",label='utm')#creation d'un graph avec la trajectoire 
plt.legend()

        
        
myFile2=open("./ImuGpsLikeFilet.s8","r")
linesOfFile = myFile2.readlines()
myFile2.close()


imuValues=[]#liste dans laquelle il faut metre utmx, utmy, utmx, utmy,...
for lines in linesOfFile:
    
    matchObj = re.search( r'GPGGA', lines)
	
    if not matchObj :
		
        continue
    else:
		msg = pynmea2.parse(lines)
		if not msg.lat :
			continue
		
		imulist = utm.from_latlon(msg.latitude, msg.longitude)
		imuValues.append(utmlist[0])
		imuValues.append(utmlist[1]) 
  
    
    
    
#convertion de la liste en tableau numpy, mise en forme puis enregistrement
imuValues=np.array(imuValues)
imuValues=imuValues.reshape((-1,2))#for 
np.savetxt("./trajectoryIMU.csv",imuValues)
#plt.subplot(2, 1, 2)
plt.plot(imuValues[:,0],imuValues[:,1],color="g",label='imu')





#affichage de la trajectoire avec matplotlib

plt.plot(utmValues[:,0],utmValues[:,1],color="r")#creation d'un graph avec la trajectoire 


#Maintenant faire la même chose avec le fichier imu ImuGpsLikeFilet.s8
# Quand vous aurez réussi à afficher les deux trajectoires zoomer sur les virages, essayez de compredre ce qu'il se passe.
#ADD YOUR CODE HERE
#############################


#############################



plt.show()#affichage du graphique