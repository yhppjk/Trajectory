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
odo=np.loadtxt("exo2\VLongiRot.csv")



#affichage position IMU
utmX=[]
utmY=[]
posZ=[]
distanceGPS=0.0
for i in range(positionsIMU.shape[0]):
	x,y,dummy1,dummy2 = utm.from_latlon(positionsIMU[i,1],positionsIMU[i,2])
	z=positionsIMU[i,3]
	if i>0:    #从1开始计算dx,dy,dz
		dx=x-utmX[-1]#-1表示列表最后一位(从后往前数第一位用-1表示)
		dy=y-utmY[-1]
		dz=z-posZ[-1]
		distanceGPS+=math.sqrt(dx*dx+dy*dy+dz*dz)
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
angle1=math.pi/2-positionsIMU[0,6]
distanceOdox1=[0.0]
distanceOdoy1=[0.0]
for i in range(odo.shape[0]-1):
    DeltaT = (odo[i+1,0] - odo[i,0])/1000000.0
    dist = odo[i,1]*DeltaT#位移
    Deltas = odo[i,2]*DeltaT#角度
    dx = dist*math.cos(angle1)
    dy = dist*math.sin(angle1)
    
    distanceOdox1.append(distanceOdox1[-1]+dx)
    distanceOdoy1.append(distanceOdoy1[-1]+dy)
    angle1 = angle1 + Deltas
	
	
#calculer la trajectoire en corrigeant la vitesse longitudinale et corrigant l'erreur statique (bias) du gyro 
#(le bias peut etre calculé sur les premires valeurs ou le véhicule est statique)
angle2=math.pi/2-positionsIMU[0,6]
distanceOdox2=[0.0]
distanceOdoy2=[0.0]
for i in range(odo.shape[0]-1):
    DeltaT = (odo[i+1,0] - odo[i,0])/1000000.0
    dist = odo[i,1]*DeltaT#位移
    Deltas = odo[i,2]*DeltaT#角度
    dx = dist*math.cos(angle2 + Deltas/2)
    dy = dist*math.sin(angle2 + Deltas/2)
    
    distanceOdox2.append(distanceOdox2[-1]+dx)
    distanceOdoy2.append(distanceOdoy2[-1]+dy)
    angle2 = angle2 + Deltas
	

#faire la même chose en version runge kutta
x,y,dummy1,dummy2 = utm.from_latlon(positionsIMU[0,1],positionsIMU[0,2])
angle3=math.pi/2-positionsIMU[0,6]

distanceoDox3=[0.0]
distanceoDoy3=[0.0]
for i in range(odo.shape[0]-1):
    DeltaT = (odo[i+1,0] - odo[i,0])/1000000.0
    dist = odo[i,1]*DeltaT
    Deltas = odo[i,2]*DeltaT
    if not Deltas:
        dx = dist*math.cos(angle3)
        dy = dist*math.sin(angle3)
    else:
        dx = (dist/Deltas)*(math.sin(angle3 + Deltas) - math.sin(angle3))
        dy = -(dist/Deltas)*(math.cos(angle3 + Deltas) - math.cos(angle3))

    distanceoDox3.append(distanceoDox3[-1]+dx)
    distanceoDoy3.append(distanceoDoy3[-1]+dy)
    angle3 = angle3 + Deltas

#faire la même chose en version Arc de cercle.



#affichage
plt.figure()
plt.title("trajectory gps, odo and odo corrected")
plt.plot(utmX,utmY, 'g', label='gpsTrajectory')
plt.plot(distanceOdox1,distanceOdoy1, 'y')
plt.plot(distanceOdox2,distanceOdoy2, 'b')
plt.plot(distanceoDox3,distanceoDoy3, 'r')
#autres affichages à faire (exemble de couleur b=black, c=cyan, m=mauve)

plt.legend(loc="best")

plt.show()
	
		
	