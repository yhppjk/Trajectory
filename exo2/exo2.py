# -*- coding: utf-8 -*-
#!/usr/bin/env python



import numpy as np
import math
import utm
import matplotlib.pyplot as plt


#chargement du fichier de position
#timestamp us
#latitude (degrés)
#longitude (degrés)
#altitude en m
#roll (rad)
#pitch (rad)
#yaw (rad) orienté ver le nord, faire pi/2-angle pour passer en utm
positionsIMU = np.loadtxt("exo2\positionsIMU.csv")

#chargement du fichier d'odométrie
#timestamp us
#vitesse longitudinale (m/s)
#taux de rotation du gyro esp en (r/s)
odo=np.loadtxt("exo2\LongiRot.csv")



#affichage position IMU
utmX=[]
utmY=[]
posZ=[]
angle=[]
distanceGPS=0.0
for i in range(positionsIMU.shape[0]):
	x,y,dummy1,dummy2 = utm.from_latlon(positionsIMU[i,1],positionsIMU[i,2])
	z=positionsIMU[i,3]
	an=positionsIMU[i,6]
	if i>0:
		dx=x-utmX[-1]
		dy=y-utmY[-1]
		dz=z-posZ[-1]
		distanceGPS+=math.sqrt(dx*dx+dy*dy+dz*dz)

		#


	utmX.append(x)
	utmY.append(y)
	posZ.append(z)
	
print (" distanceGPS ="+str(distanceGPS))

utmX=np.array(utmX)
utmY=np.array(utmY)
utmX=utmX-utmX[0]
utmY=utmY-utmY[0]


#calcul traj normale à partir de l'odometrie
#penser a inverser l'angle math.pi/2-angle
#en profiter pour calculer la distance odométrie en mode euler
odoTrajectoryX=[0.0]
odoTrajectoryY=[0.0]
angle = math.pi/2-positionsIMU[0,6]
distance=0.0
for i in range(odo.shape[0]-1):
	deltaT=(odo[i+1,0]-odo[i,0])/1000000.0
	distance=odo[i,1]*deltaT
	distanceOdo=distance



	dx=distance*math.cos(angle)
	dy=distance*math.sin(angle)
	deltaTheta=odo[i,2]*deltaT
	odoTrajectoryX.append(odoTrajectoryX[-1]+dx)
	odoTrajectoryY.append(odoTrajectoryY[-1]+dy)
	angle= angle+deltaTheta


#calculer la trajectoire en corrigeant la vitesse longitudinale et corrigant l'erreur statique (bias) du gyro 
#(le bias peut etre calculé sur les premires valeurs ou le véhicule est statique)

KuttaX=[0.0]
KuttaY=[0.0]
angle = math.pi/2-positionsIMU[0,6]
distance=0.0
for i in range(odo.shape[0]-1):
	deltaT=(odo[i+1,0]-odo[i,0])/1000000.0
	distance=odo[i,1]*deltaT
	distanceKutta=distance


	deltaTheta=odo[i,2]*deltaT
	dx=distance*math.cos(angle+deltaTheta/2)
	dy=distance*math.sin(angle+deltaTheta/2)
	


	KuttaX.append(KuttaX[-1]+dx)
	KuttaY.append(KuttaY[-1]+dy)
	angle= angle+deltaTheta
	


#faire la même chose en version runge kutta


#faire la même chose en version Arc de cercle.



#affichage
plt.figure()
plt.title("trajectory gps, odo and odo corrected")
plt.plot(utmX,utmY, 'g', label='gpsTrajectory')
plt.plot(odoTrajectoryX,odoTrajectoryY,'o',label = 'odoTrajectory')
plt.plot(KuttaX,KuttaY,'r',label = 'Kutta')
#autres affichages à faire (exemble de couleur b=black, c=cyan, m=mauve)

plt.legend(loc="best")

plt.show()
	
		
	