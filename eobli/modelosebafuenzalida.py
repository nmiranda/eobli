#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import numpy as np
import pylab as pl
import time

random.seed(42)
workingDir2 = "Resultados/"


filas = 44
columnas = 4

altura = 6.5 / 1000.0
diametro = 1.8 / 1000.0
Ah = 3.0

def modelosebafuenzalida(pop,popvel,num_var,objectives,iteraciones,limiteUp,limiteDown):

	counter = 0

	# #abre resultados de modularizacion para obtener filas y columnas

	# f = open('resultadosmodularizacion.txt', 'r')
	# mod_list = f.read().splitlines()
	# f.close()

	# filas = mod_list[0]

	# # OJO: si columnas == 1 la aplicación se cae en bancotubosT_G
	# columnas = mod_list[1]

	#aca esta la seccion para usar diferentes tamanos de celda


	#abre el archivo donde se encuentra la libreria de celdas	

	# fin5 = open("listaCeldas.txt","r")
	# fin_list5 = fin5.read().splitlines()
	# fin5.close()

	# file1 = fin_list5[0]
	
	# aa = poll()

	# # JEJE
	# #aa = 0
	

	# v = ""+str(aa)
	# sel = list1.get(aa)
	
	# #busca la celda elegida por el usuario en la libreria	

	# for i in range(0,len(fin_list5)):
		
	# 	if sel == fin_list5[i]:
	# 		file1 = fin_list5[i] #revisar
	# 		break
	
	# # print "file1   " +str(file1)

	# fin4 = open(file1+".txt", "r")
	# fin_list4 = fin4.read().splitlines()
	# fin4.close()


	# diametro = float(fin_list4[7])/1000
	# altura = float(fin_list4[6])/1000
	
	# diametro = 0.026                    #codigo original sin cambios

	# altura = 0.065                       # Altura celda en [m]
	corriente = 8                       # Corriente celda [A]
	resistencia_interna = 0.032          # Resistencia celda [Ohm] podria variarse por datasheet
	Tfluido_in = 273.15+20 

	# Caudal = 100
	# St = 1.5
	# SL = 1.5
	
	T0celdas = 273.15+20

	# Ah = float(fin_list4[2])            #Capacidad de la celda [Ah]
	dt = 1                             # Paso de simulacion [s]
	Voltaje=3.3 


	repo = []
	repoObj = []
	personalbest = pop
	personalbestObj = objectives
	numobj = 2
	

	#ciclo del programa de optimizacion	

	for j in range(int(iteraciones)):

		#con la poblacion ya creada lo primero en la iteracion es actualizar la velocidad

		#update velocity

		if j>0:

			w = 0.6
			r1 = random.random()
			r2 = random.random()
        
			if len(repo)>1:
				h = random.randint(0,len(repo)-1)
			else:
                     		h = 0

	
			#calculo de la velocidad 
                        
                
                	for i in range(len(pop)):
                        	for j in range(num_var):
                                	if len(repo) > 0:
                                        	popvel[i][j] = w*popvel[i][j]+r1*(personalbest[i][j]-pop[i][j])+r2*(repo[h][j]-pop[i][j])
                                        	pop[i][j] = round(pop[i][j]+popvel[i][j],4)

                                        	if pop[i][j] > limiteUp[j]:
                                                	pop[i][j] = limiteUp[j]
                                        	elif pop[i][j] < limiteDown[j]:
                                                	pop[i][j] = limiteDown[j]
                                        
                                        
                                	else:
                                        	popvel[i][j] = w*popvel[i][j]+r1*(personalbest[i][j]-pop[i][j])
                                        	pop[i][j] = round(pop[i][j] + popvel[i][j],4)

                                        	if pop[i][j] > limiteUp[j]:
                                                	pop[i][j] = limiteUp[j]
                                        	elif pop[i][j] < limiteDown[j]:
                                                	pop[i][j] = limiteDown[j]

		#evaluate solution: Llamar al modelo de Sebastian Fuenzalida

		for i in range(len(pop)):
			St = pop[i][0]
			SL = pop[i][0]
			Caudal = pop[i][1]

			# SL = pop[i][1]
			# Caudal = 40

			[matriz,T] = Transiente_func(diametro,filas,columnas,altura,corriente,resistencia_interna,Tfluido_in,Caudal,T0celdas,St,SL,Ah,dt,Voltaje)

			Objetivo1 = matriz[6]
			Objetivo2 = matriz[11]

			objectives[i][0] = Objetivo1
			objectives[i][1] = Objetivo2


			# Guardar el resultado de cada simulacion para respaldo

			# f = open(workingDir2 + 'model' + str(counter)+'.txt', 'w')
			# f.write(""+"id:"+str(counter)+ ", " + str(pop[i][0]) + ", "+"" + str(pop[i][1]) + "," + str(objectives[i][0]) + ", " + str(objectives[i][1]) + "\n")
			# f.close() 
			# print 'counter  ' + str(counter)
	 	#  	counter = counter + 1
		

		
		
		#non dominated search: Busqueda de elementos no dominados en la poblacion y comparacion con soluciones en repositorio

		cuenta = []
                cuentaRepo = []
                
                
                for i in range(len(pop)):
                        cuenta.append(0.0)
        
                for i in range(len(pop)):
                        for j in range(len(pop)):
                                
                                out = False
                                for k in range(numobj):
                                        if i==j:
                                                aa = 0
                                        else:

                                                if objectives[i][k] < objectives[j][k]:
                                                        out = False
                                                        break
                                                elif objectives[i][k] > objectives[j][k]:
                                                        out = True
                        
                                if out==True:
                                        cuenta[i]=cuenta[i]+1

		# con la cuenta de cuantas soluciones que lo dominan encontro para un cierto individuo, el algoritmo decide guardar al individuo en un repositorio transitorio si la cuenta fue cero.
        
                for i in range(len(pop)):        
                        if cuenta[i] == 0:
                                c = []
                                d = []
                           
                                for k in range(num_var):
                                        c.append(pop[i][k])

                                for j in range(numobj):
                                        d.append(objectives[i][j])

                            
                                
                                repo.append(c)
                                repoObj.append(d)

		# El siguiente paso, es ordenar el repositorio. Al agregar soluciones nuevas, puede que algunas hayan dejado de ser optimas y deben ser limpiadas. Eso se hace con un proceso de cuenta, similar al anterior.
                               

                
                
                for i in range(len(repo)):
                        cuentaRepo.append(0.0)

                if len(repo)>1:
                        for i in range(len(repo)):
                                for j in range(len(repo)):
                                
                                        outRepo = False
                                        for k in range(numobj):
                                                if i==j:
                                                        aa = 0
                                                else:
                                                        if repoObj[i][k] < repoObj[j][k]:
                                                                out = False
                                                                break
                                                        elif repoObj[i][k] >= repoObj[j][k]:
                                                                out = True
                                
                                        if out==True:
                                                cuentaRepo[i]=cuentaRepo[i]+1
                        
                        
             # si la cuenta resulta mayor a cero, simplemente se borra ese elemento de la lista

                        for i in range(len(repo)-1,-1,-1):
                                if cuentaRepo[i] > 0:
                                        del repo[i]
                                        del repoObj[i]
                                        

             
		#update best: Actualizar historial de mejores posiciones para cada particula

		respaldo = personalbest
                respaldoobj = personalbestObj
                personalbest = []
                personalbestObj = []
                
                for i in range(len(pop)):
                        out = False
                        for k in range(numobj):
                                if respaldoobj[i][k]<objectives[i][k]:
                                        out = False
                                        break
                                elif respaldoobj[i][k]>objectives[i][k]:
                                        out = True
                        
                        if out == True:
                                e = []
                                f = []
                                for j in range(num_var):
                                        e.append(pop[i][j])
                                for l in range(numobj):
                                        f.append(objectives[i][l])

                                personalbestObj.append(f)
                                personalbest.append(e)
                        else:
                                g = []
                                h = []
                                for j in range(num_var):
                                        g.append(respaldo[i][j])
                                for l in range(numobj):
                                        h.append(respaldoobj[i][l])
                                        
                                personalbest.append(g)
                                personalbestObj.append(h)

	return repo,repoObj

def Transiente_func(diametro,filas,columnas,altura,corriente,resistencia_interna,Tfluido_in,Caudal,T0celdas,St,SL,Ah,dt,Voltaje):
		
		matriz = [] 

		for i in range(16):
			matriz.append(0)
 
		fluido = 'aire'
		l=1

		for i in range(1):
    			for z in range(1):
        			for j in range(1):
            				for k in range(1):
						[T,Velocidadfluido,DeltaPresion,Potencia_Mecanica,Potencia_Electrica,Eficiencia,Ifluido,ma,mi,Tiempo_Simulacion,delta_T,Pot_Ventilador] = BancoTubosT_G(fluido,diametro,columnas,filas,altura,corriente,resistencia_interna,Tfluido_in,Caudal,T0celdas,St,SL,Ah,Voltaje,dt)

					matriz[0]=filas  
					matriz[1]=columnas
					matriz[2]=Caudal
					matriz[3]=St
					matriz[4]=SL
					matriz[5]=Velocidadfluido
					matriz[6]=ma
					matriz[7]=mi
					matriz[8]=delta_T
					matriz[9]=DeltaPresion
					matriz[10]=Ifluido
					matriz[11]=Potencia_Mecanica
					matriz[12]=Pot_Ventilador
					matriz[13]=Potencia_Electrica
					matriz[14]=Eficiencia
					matriz[15]=Tiempo_Simulacion

	
		return [matriz,T]

def BancoTubosT_G(fluido,diametro,columnas,filas,altura,corriente,resistencia_interna,Tfluido_in,Caudal,T0celdas,St,SL,Ah,Voltaje,dt):


	"""
	fluido = 'aire'

	"""



	# Inicio de conteo de tiempo y transformacion de filas y columnas
	tic = time.time()
	columnas = int(columnas)
	filas = int(filas)
	
	# Cantidad de puntos
	N=(columnas)*(filas)
	
	#Armando tabla de conversion
	conv = np.zeros((N,2))
	ind=0

	for i in range(columnas):
		for j in range(filas):
        		conv[ind,0]=i
        		conv[ind,1]=j
        		ind=ind+1
	

	A = np.zeros((N,N))

	B = np.zeros((N,1))


	# setting de constantes dependiendo de tipo de fluido
    
	
	Cp=1007                       # Capacidad calorifica
	Deni=Ro(Tfluido_in)            # Densidad fluido [kg/m3]
	Visc=Viscosidad(Tfluido_in)    # Viscosidad dinamica fluido [kg/ms]
	Condflu=kfluido(Tfluido_in)    # Conductividad fluido [W/mK]
	Prandt=NPran(Tfluido_in)       #Numero Prandt

	Area=altura*(diametro*filas+(filas+1)*diametro*(St-1))   # Area de entrada flujo [m2]
	Flujo=0.0004719474*Caudal                                # Caudal  [CFM]
	Velocidadfluido=Flujo/Area                                # Velocidad de entrada del fluido [m/s]
	Flujo_masico=Deni*Velocidadfluido*Area                   # Flujo Masico del fluido [kg/s]
	Vmax=Velocidadfluido*St*diametro/(St*diametro-diametro)  # Velocidad Maxima del fluido dentro del banco de baterias [m/s]
	ReDmax=Deni*Vmax*diametro/Visc                           # Numero de Reynolds
	

	razon=(St-1)/(SL-1)                 
	x=xi(razon,ReDmax)         # Coeficiente de correlacion
	f=friccion(SL,ReDmax)      # Coeficiente de friccion

	if Caudal==0:
		f=0

	#variables mecanicas y electricas del modelo
	
	DeltaPresion=float((f*x*columnas*Deni*(np.power(Vmax,2))))/float(2)            # Caida de Presion [Pa]
	Potencia_Mecanica=Flujo*DeltaPresion                   # Potencia Mecanica debido a DeltaP [W]
	Pot_Ventilador=Potencia_Mecanica/0.25                  # Potencia Ventilador [W]
	Ifluido=Pot_Ventilador/(columnas*filas*Voltaje)        # Corriente aplicada para el funcionamiento del ventilador [W]
	Vcelda=altura*3.14*np.power((diametro/2),2)                        # Volumen de una celda [m3]
	Volumen_total=Vcelda*filas*columnas                   # Volumen total celdas del banco [m3] 
	Calorgen=(corriente+Ifluido)*(corriente+Ifluido)*resistencia_interna/Vcelda     # Calor generado por una celda
	print 'Calorgen' + str(Calorgen)
	Calorgentotal=Calorgen*Volumen_total                                                # Calor generado por todas las celdas
	
	cont=202.4  # Conductividad Aluminio [W/mK]

#Ecuaciones del modelo

	Tp = []
	U = []

	for i in range(N):
		Tp.append(T0celdas)
		U.append(T0celdas)
	
	RoAl = 2719
	CpAl = 871

	T = np.ones((filas,columnas)) * (T0celdas - 273.15) #Temperatura celdas tiempo t [C]


	#tiempo de simulacion

	if corriente>0 or Ifluido>0:
		Segundos=(Ah/(corriente+Ifluido))*3600   #Tiempo de descarga celda [s]   
		# print Segundos	
	else:
    		Segundos=10

        # if Segundos < 1:
        #     Segundos = 10

	y=np.floor(Segundos)


	Grafico = [1] * int(y) #Contador para guardar Temperatura Maxima en cada segundo
	Tiempo = [1] * int(y) # Contador de tiempo para graficar al finalizar los calculos


	#Constantes

	# ciclo de simulacion 

	for t in range(int(y)):
		
		#print t
		for k in range(N):

			[i,j] = getIJ(k,conv)

			NuD = Nuss(ReDmax, m(St, SL), Prandt, i+1, C(St,SL)) #Numero de Nusselt
			h = NuD*Condflu/diametro  #Coeficiente de conveccion
			a=h*diametro+2*cont
			b=h*diametro+cont
			Fo=float(cont*h*dt)/float(RoAl*CpAl*diametro)
			c=float(dt)/float(RoAl*CpAl)

			# Temperatura de Salida del Fluido
			Tout=(T[j,columnas-1]+273.15)-((T[j,columnas-1]+273.15)-(T[j,0]+273.15+Tfluido_in)/2)*np.exp((-1*3.14*diametro*columnas*filas*h)/(Ro((T[j,1]+273.15+Tfluido_in)/2)*Velocidadfluido*filas*St*diametro*Cp))

			# Temperatura Fluido por Columna para Filas Interiores
			numerito = (np.exp((-1*3.14*diametro*i*filas*h)/(Deni*Velocidadfluido*filas*St*diametro*Cp))) 
			Tempaux=(T[j,i]+273.15)-((T[j,i]+273.15)-(T[j,0]+273.15+Tfluido_in)/2)
			Tlad = Tempaux*numerito

			# Temperatura Fluido por Columna para Filas Superior e Inferior
			Tx=Tfluido_in+((Tout-Tfluido_in)/(columnas))*(i)

			#Calculo de puntos de la matriz A y el vector B que resuelven el sistema lineal

			#Punto1
			if i==0 and j==filas-1:

				A[k,getK(i,j-1,conv)]=-Fo/b
				A[k,getK(i+1,j,conv)]=-Fo/b
				B[k,0]=(2*Fo*Tlad/a)+Tp[k]+2*Fo*(Tx+(Tlad+Tfluido_in)/2)/a+Calorgen*c
				A[k,k]=(2*Fo/a)+(4*Fo/a)+(2*Fo/b)+1
			
			#Punto2
			if i==0 and j>0 and j<filas -1:

				A[k,getK(i,j+1,conv)]=-Fo/b
				A[k,getK(i,j-1,conv)]=-Fo/b
				A[k,getK(i+1,j,conv)]=-Fo/b
				B[k,0]=4*Fo*Tlad/a+Tp[k]+2*Fo*((Tlad+Tfluido_in)/2)/a+Calorgen*c
				A[k,k]=(4*Fo/a)+(2*Fo/a)+(3*Fo/b)+1


			#Punto3
			if i==0 and j==0:

				A[k,getK(i,j+1,conv)]=-Fo/b
				A[k,getK(i+1,j,conv)]=-Fo/b
				B[k,0]=(2*Fo*Tlad/a)+Tp[k]+2*Fo*(Tx+(Tlad+Tfluido_in)/2)/a+Calorgen*c
				A[k,k]=(2*Fo/a)+(4*Fo/a)+(2*Fo/b)+1



			#Punto 4
			if j==0 and i<columnas-1 and i>0:

				A[k,getK(i,j+1,conv)]=-Fo/b
				A[k,getK(i-1,j,conv)]=-Fo/b
				A[k,getK(i+1,j,conv)]=-Fo/b
				B[k,0]=2*Fo*Tlad/a+Tp[k]+2*Fo*(Tx)/a+Calorgen*c
				A[k,k]=(2*Fo/a)+(2*Fo/a)+(3*Fo/b)+1

			#Punto 5
			if i==columnas-1 and j==0:

				A[k,getK(i,j+1,conv)]=-Fo/b
				A[k,getK(i-1,j,conv)]=-Fo/b
				B[k,0]=(2*Fo*Tlad/a)+Tp[k]+2*Fo*((Tx))/a+Calorgen*c
				A[k,k]=(4*Fo/a)+(2*Fo/b)+1


			#Punto 6
			if i==columnas-1 and j>0 and j<filas-1:

				A[k,getK(i,j+1,conv)]=-Fo/b
				A[k,getK(i,j-1,conv)]=-Fo/b
				A[k,getK(i-1,j,conv)]=-Fo/b
				B[k,0]=4*Fo*Tlad/a+Tp[k]+Calorgen*c
				A[k,k]=(4*Fo/a)+(3*Fo/b)+1


			#Punto 7 
			if i==columnas-1 and j==filas-1:

				A[k,getK(i,j-1,conv)]=-Fo/b
				A[k,getK(i-1,j,conv)]=-Fo/b
				B[k,0]=(2*Fo*Tlad/a)+Tp[k]+2*Fo*((Tx))/a+Calorgen*c
				A[k,k]=(4*Fo/a)+(2*Fo/b)+1

			#punto 8
			if j==filas-1 and i>0 and i<columnas-1:

				A[k,getK(i,j-1,conv)]=-Fo/b
				A[k,getK(i-1,j,conv)]=-Fo/b
				A[k,getK(i+1,j,conv)]=-Fo/b
				B[k,0]=2*Fo*Tlad/a+Tp[k]+2*Fo*(Tx)/a+Calorgen*c
				A[k,k]=(2*Fo/a)+(2*Fo/a)+(3*Fo/b)+1
			
			#puntos interiores
			if i>0 and i<columnas-1 and j>0 and j<filas-1:

				A[k,getK(i,j-1,conv)]=-Fo/b
				A[k,getK(i,j+1,conv)]=-Fo/b
				A[k,getK(i+1,j,conv)]=-Fo/b
				A[k,getK(i-1,j,conv)]=-Fo/b
				B[k,0]=(4*Fo*Tlad/a)+Tp[k]+Calorgen*c
				A[k,k]=(4*Fo/a)+(4*Fo/b)+1


		
		# intenta resovler el sistema lineal, si la matriz es singular asigna temperatura "infinita" y desecha el caso

		try:
			U = np.linalg.solve(A, B)

		except:	
			print 'estoy en el except'
			for i in range(len(B)):
				U[i] = 393.15

		# print 'U' + str(U)
	
		
		

		u1=np.zeros((columnas,filas))

		for k in range(N):
    			[i,j]=getIJ(k,conv)
    			u1[i,j]=U[k]
   		 

		u1= np.transpose(u1)


		mm = filas
		nn = columnas

		for mm1 in range(mm):
			for n in range(nn):
				u1[mm1,n] = u1[mm1,n] - 273.15

		ma = max(U) #tmax
		if ma - Grafico[t - 1] < 0.01:
			break
		mi = min(U) #tmin
		delta_T = ma - mi  #deltaT
		Tpelicula = (Tfluido_in - 273.15 + Tout - 273.15)/2	


		#guardar variables para la siguiente iteracion
		Prandt=NPran(Tpelicula+273.15)         # Numero de Prandt
		Deni=Ro(Tpelicula+273.15)             # Densidad [kg/m3]
		Viscosi=Viscosidad(Tpelicula+273.15) # Viscosidad Dinamica [kg/ms]
		Condflu=kfluido(Tpelicula+273.15)      # Conductividad [W/mK]
		ReDmax=Deni*Vmax*diametro/Viscosi       # Numero de Reynolds
		T=u1

		x=xi(razon,ReDmax)                                    # Coeficiente de Correlacion
		f=friccion(SL,ReDmax)                                  # Coeficiente de friccion
		DeltaPresion=float((f*x*columnas*Deni*(np.power(Vmax,2))))/float(2)            # Caida de Presion [Pa]
		Potencia_Mecanica=Flujo*DeltaPresion       # Potencia Mecanica debido a DeltaP [W]

		Pot_Ventilador=float(Potencia_Mecanica)/float(0.25)                 # Potencia del Ventilador [W]
		Potencia_Electrica=filas*columnas*corriente*Voltaje    # Potencia Electrica aportada por el Banco de Baterias [W]

		Eficiencia=(Potencia_Electrica-Pot_Ventilador)/Potencia_Electrica      # Eficiencia del Sistema

		Tiempo[t]=t
		Grafico[t]=ma
		#print "Ma" + str(ma) m
   		Tp=U

		toc = time.time()
	
		Tiempo_Simulacion = toc - tic 
    
	#salida del programa una vez completadas todas las iteraciones del modelo


        #print range(int(y))
	return [T,Velocidadfluido,DeltaPresion,Potencia_Mecanica,Potencia_Electrica,Eficiencia,Ifluido,ma,mi,Tiempo_Simulacion,delta_T,Pot_Ventilador]

def Ro(Temperatura):
	if Temperatura<=273.15 or Temperatura>=573.15:
    		Ro1=1.292
    
    	if Temperatura>273.15 and Temperatura<283.15:
    		Ro1=1.292+((1.247-1.292)/10)*(Temperatura-273.15)
     
    	if Temperatura>=283.15 and Temperatura<293.15:
    		Ro1=1.247+((1.204-1.247)/10)*(Temperatura-283.15)
    
    	if Temperatura>=293.15 and Temperatura<303.15:
    		Ro1=1.204+((1.164-1.204)/10)*(Temperatura-293.15)
    
    	if Temperatura>=303.15 and Temperatura<313.15:
    		Ro1=1.164+((1.117-1.164)/10)*(Temperatura-303.15)
    
    	if Temperatura>=313.15 and Temperatura<323.15:
    		Ro1=1.117+((1.092-1.117)/10)*(Temperatura-313.15)
    
    	if Temperatura>=323.15 and Temperatura<333.15:
    		Ro1=1.092+((1.060-1.092)/10)*(Temperatura-323.15)
    
    	if Temperatura>=333.15 and Temperatura<343.15:
    		Ro1=1.060+((1.029-1.060)/10)*(Temperatura-333.15)
    
    	if Temperatura>=343.15 and Temperatura<353.15:
    		Ro1=1.029+((0.9996-1.029)/10)*(Temperatura-343.15)
    
   	if Temperatura>=353.15 and Temperatura<363.15:
        	Ro1=0.9996+((0.9721-0.9996)/10)*(Temperatura-353.15)
    
   	if Temperatura>=363.15 and Temperatura<373.15:
    		Ro1=0.9721+((0.9460-0.9721)/10)*(Temperatura-363.15)

    	if Temperatura>=373.15 and Temperatura<473.15:
    		Ro1=0.9460+((0.7461-0.9460)/100)*(Temperatura-373.15)

    	if Temperatura>=473.15 and Temperatura<573.15:
    		Ro1=0.7461+((0.6159-0.7461)/100)*(Temperatura-473.15)

	return Ro1

def Viscosidad(Temperatura):

	if Temperatura<=273.15 or Temperatura >=573.15 :
    		Viscosidad1=0.00001729
    
    	if Temperatura>273.15 and Temperatura<283.15:
    		Viscosidad1=0.00001729+((0.00001778-0.00001729)/10)*(Temperatura-273.15)
     
    	if Temperatura>=283.15 and Temperatura<293.15:
    		Viscosidad1=0.00001778+((0.00001825-0.00001778)/10)*(Temperatura-283.15)
    
    	if Temperatura>=293.15 and Temperatura<303.15:
    		Viscosidad1=0.00001825+((0.00001872-0.00001825)/10)*(Temperatura-293.15)
    
    	if Temperatura>=303.15 and Temperatura<313.15:
    		Viscosidad1=0.00001872+((0.00001918-0.00001872)/10)*(Temperatura-303.15)
    
    	if Temperatura>=313.15 and Temperatura<323.15:
    		Viscosidad1=0.00001918+((0.00001963-0.00001918)/10)*(Temperatura-313.15)
    
    	if Temperatura>=323.15 and Temperatura<333.15:
    		Viscosidad1=0.00001963+((0.00002008-0.00001963)/10)*(Temperatura-323.15)
    
    	if Temperatura>=333.15 and Temperatura<343.15:
    		Viscosidad1=0.00002008+((0.00002052-0.00002008)/10)*(Temperatura-333.15)
    
    	if Temperatura>=343.15 and Temperatura<353.15:
    		Viscosidad1=0.00002052+((0.00002096-0.00002052)/10)*(Temperatura-343.15)
    
    	if Temperatura>=353.15 and Temperatura<363.15:
   	 	Viscosidad1=0.00002096+((0.00002139-0.00002096)/10)*(Temperatura-353.15)
    
    	if Temperatura>=363.15 and Temperatura<373.15:
   		Viscosidad1=0.00002139+((0.00002181-0.00002139)/10)*(Temperatura-373.15)

    	if Temperatura>=373.15 and Temperatura<473.15:
    		Viscosidad1=0.00002181+((0.00002577-0.00002181)/100)*(Temperatura-373.15)

    	if Temperatura>=473.15 and Temperatura<573.15:
    		Viscosidad1=0.00002577+((0.00002934-0.00002577)/100)*(Temperatura-473.15)

	return Viscosidad1

#Funcion coeficiente de fluido 

def kfluido(Temperatura):

	if Temperatura<=273.15 or Temperatura >=573.15:
    		kfluido1=0.02364
    
    	if Temperatura>273.15 and Temperatura<283.15:
    		kfluido1=0.02364+((0.02439-0.02364)/10)*(Temperatura-273.15)
     
    	if Temperatura>=283.15 and Temperatura<293.15:
    		kfluido1=0.02439+((0.02514-0.02439)/10)*(Temperatura-283.15)
    
    	if Temperatura>=293.15 and Temperatura<303.15:
    		kfluido1=0.02514+((0.02588-0.02514)/10)*(Temperatura-293.15)
    
    	if Temperatura>=303.15 and Temperatura<313.15:
    		kfluido1=0.02588+((0.02662-0.02588)/10)*(Temperatura-303.15)
    
    	if Temperatura>=313.15 and Temperatura<323.15:
    		kfluido1=0.02662+((0.02735-0.02662)/10)*(Temperatura-313.15)
    
    	if Temperatura>=323.15 and Temperatura<333.15:
    		kfluido1=0.02735+((0.02808-0.02735)/10)*(Temperatura-323.15)
    
    	if Temperatura>=333.15 and Temperatura<343.15:
    		kfluido1=0.02808+((0.02881-0.02808)/10)*(Temperatura-333.15)
    
    	if Temperatura>=343.15 and Temperatura<353.15:
    		kfluido1=0.02881+((0.02953-0.02881)/10)*(Temperatura-343.15)
    
    	if Temperatura>=353.15 and Temperatura<363.15:
    		kfluido1=0.02953+((0.03024-0.02953)/10)*(Temperatura-353.15)
    
    	if Temperatura>=363.15 and Temperatura<373.15:
    		kfluido1=0.03024+((0.03095-0.03024)/10)*(Temperatura-373.15)

    	if Temperatura>=373.15 and Temperatura<473.15:
    		kfluido1=0.03095+((0.03779-0.03095)/100)*(Temperatura-373.15)

    	if Temperatura>=473.15 and Temperatura<573.15:
    		kfluido1=0.03779+((0.04418-0.03779)/100)*(Temperatura-473.15)

	return kfluido1

# Funcion Numero de Prandt

def NPran(Temperatura):

	if Temperatura>273.15 and Temperatura<283.15:
    		NPran1=0.7362+((0.7336-0.7362)/10)*(Temperatura-273.15)
     
    	if Temperatura>=283.15 and Temperatura<293.15:
    		NPran1=0.7336+((0.7309-0.7336)/10)*(Temperatura-283.15)
    
    	if Temperatura>=293.15 and Temperatura<303.15:
    		NPran1=0.7309+((0.7282-0.7309)/10)*(Temperatura-293.15)
    
    	if Temperatura>=303.15 and Temperatura<313.15:
    		NPran1=0.7282+((0.7255-0.7282)/10)*(Temperatura-303.15)
    
    	if Temperatura>=313.15 and Temperatura<323.15:
    		NPran1=0.7255+((0.7228-0.7255)/10)*(Temperatura-313.15)
    
    	if Temperatura>=323.15 and Temperatura<333.15:
    		NPran1=0.7228+((0.7202-0.7228)/10)*(Temperatura-323.15)
    
    	if Temperatura>=333.15 and Temperatura<343.15:
    		NPran1=0.7202+((0.7177-0.7202)/10)*(Temperatura-333.15)
    
    	if Temperatura>=343.15 and Temperatura<353.15:
    		NPran1=0.7177+((0.7154-0.7177)/10)*(Temperatura-343.15)
    
    	if Temperatura>=353.15 and Temperatura<363.15:
    		NPran1=0.7154+((0.7132-0.7154)/10)*(Temperatura-353.15)
    
    	if Temperatura>=363.15 and Temperatura<373.15:
    		NPran1=0.7132+((0.7111-0.7132)/10)*(Temperatura-363.15)

    	if Temperatura>=373.15 and Temperatura<473.15:
    		NPran1=0.7111+((0.6974-0.7111)/100)*(Temperatura-373.15)

    	if Temperatura>=473.15 and Temperatura<573.15:
    		NPran1=0.6974+((0.6935-0.6974)/100)*(Temperatura-473.15)

    	if Temperatura>=573.15 and Temperatura<673.15:
    		NPran1=0.6935+((0.6948-0.6935)/100)*(Temperatura-573.15)

	else:
		NPran1=0.7362

	return NPran1

# Funcion xi, coeficiente de correlacion
      
def xi(razon,ReDmax):

	x=1

	if razon==1:
    		x=1
	else:
		if ReDmax<600:
    			x=1.006*np.power(razon,(-0.8))

		if ReDmax>=600 and ReDmax<10000:
    			x=1.005*np.power(razon,(-0.74))+(0.967*np.power(razon,(-0.62))-1.005*np.power(razon,(-0.74)))*(ReDmax-600)/(10000-600)

		if ReDmax>=10000 and ReDmax<100000:
    			x=0.967*np.power(razon,(-0.62))+(1.031*np.power(razon,(-0.40))-0.967*np.power(razon,(-0.62)))*(ReDmax-10000)/(100000-10000)

		if ReDmax>=1000000 and ReDmax<=1000000:
    			x=1.031*np.power(razon,(-0.40))+(0.977*np.power(razon,(-0.49))-1.031*np.power(razon,(-0.40)))*(ReDmax-100000)/(1000000-100000)
	
	return x

# Funcion para el factor de friccion

def friccion(SL,ReDmax):


	if SL>=1.05 and SL<1.5: #SL>=1.25
		if ReDmax<600:
        		f=(-0.00002*ReDmax+0.484)+((-0.00002*ReDmax+0.311)-(-0.00002*ReDmax+0.484))*(SL-1.25)/(1.5-1.25)
    
     		if ReDmax>=600:     
        		f=1.798*np.power(ReDmax,(-0.1974))+((0.77*np.power(ReDmax,(-0.137))-1.798*np.power(ReDmax,(-0.1974)))/(1.5-1.25))*(SL-1.25);
    
    
	if SL>=1.5 and SL<2.0:
      		if ReDmax<600:
        		f=(-0.00002*ReDmax+0.311)+((-0.00001*ReDmax+0.229)-(-0.00002*ReDmax+0.311))*(SL-1.5)/(2.0-1.5)
      
      		if ReDmax>=600:
        		f=0.77*np.power(ReDmax,(-0.137))+((0.540*np.power(ReDmax,(-0.13))-0.77*np.power(ReDmax,(-0.137)))/(2.0-1.5))*(SL-1.5)
     

	if SL>=2.0: #SL<=3.0
      		if ReDmax<600:
        		f=(-0.00001*ReDmax+0.229)+(0.780*np.power(ReDmax,(-0.23))-(-0.00001*ReDmax+0.229))*(SL-2.0)/(3.0-2.0)    

      
      		if ReDmax>=600 and ReDmax<30000:
        		f=0.540*np.power(ReDmax,(-0.13))+((0.158-0.540*np.power(ReDmax,(-0.13)))/(3.0-2.0))*(SL-2.0)
      
      
      		if ReDmax>=30000:
        		f=0.540*np.power(ReDmax,(-0.13))+(((0.17+((0.14-0.17)/(200000-30000))*(ReDmax-30000))-0.540*np.power(ReDmax,(-0.13)))/(3.0-2.0))*(SL-2.0)

	return f

#funcion getIJ para obtener indices de la matriz de conversion

def getIJ(k,conv):
	i = conv[k,0]
	j = conv[k,1]

	return i,j

#funcion Nuss para estimar el valor del Numero de Nusselt dependiendo del numero de columnas del banco	

def Nuss(ReDmax,mu,Prandt,columna,C1):

	if columna == 1:
    		Nuss1=0.64*1.13*C1*(np.power(ReDmax,mu))*(np.power(Prandt,(0.33)))    

	if columna == 2:
		if ReDmax > 0:
    			Nuss1=0.80*1.13*C1*(np.power(ReDmax,mu))*(np.power(Prandt,(0.33)))
		else:
			Nuss1=0.80*1.13*C1*(-np.power(-ReDmax,mu))*(np.power(Prandt,(0.33)))
		
		
	if columna == 3:
    		Nuss1=0.87*1.13*C1*(np.power(ReDmax,mu))*(np.power(Prandt,(0.33)))

	if columna == 4:
    		Nuss1=0.90*1.13*C1*(np.power(ReDmax,mu))*(np.power(Prandt,(0.33)))

	if columna == 5:
    		Nuss1=0.92*1.13*C1*(np.power(ReDmax,mu))*(np.power(Prandt,(0.33)))

	if columna == 6:
    		Nuss1=0.94*1.13*C1*(np.power(ReDmax,mu))*(np.power(Prandt,(0.33)))
	
	if columna == 7:
    		Nuss1=0.96*1.13*C1*(np.power(ReDmax,mu))*(np.power(Prandt,(0.33)))

	if columna == 8:
    		Nuss1=0.98*1.13*C1*(np.power(ReDmax,mu))*(np.power(Prandt,(0.33)))

	if columna == 9:
    		Nuss1=0.99*1.13*C1*(np.power(ReDmax,mu))*(np.power(Prandt,(0.33)))

	if columna >= 10:
    		Nuss1=1.13*C1*(np.power(ReDmax,mu))*(np.power(Prandt,(0.33)))

	return Nuss1

# funcion m para determinar la constante en funcion de St, Sl y Ctem

def m(St, SL):

	if St>=1.00 or St<=1.25:
		m1=ctem(1.00,SL)+((ctem(1.25,SL)-ctem(1.00,SL))/(1.25-1.00))*(St-1.00)

	if St>1.25 or St<=1.5:
		m1=ctem(1.25,SL)+((ctem(1.5,SL)-ctem(1.25,SL))/(1.5-1.25))*(St-1.25)

	if St>1.5 or St<=2.0:
    		m1=ctem(1.5,SL)+((ctem(2.0,SL)-ctem(1.5,SL))/(2.0-1.5))*(St-1.5)

	if St>2.0 or St<=3.0: 
   		m1=ctem(2.0,SL)+((ctem(3.0,SL)-ctem(2.0,SL))/(3.0-2.0))*(St-2.0)

	return m1

# funcion ctem dependiendo de los valores de St y Sl

	
def ctem(ST,SL):
	if ST==1.00:
    
    		if SL>=1.00 or SL<=1.25:
        		ctem1=0+((0.576-0)/(1.25-1.00))*(SL-1.00)   
    		
		if SL>=1.25 or SL<=1.5:
        		ctem1=0.576+((0.552-0.576)/(1.5-1.25))*(SL-1.25) 
    
    		if SL>1.5 or SL<=2.0:
        		ctem1=0.552+((0.538-0.552)/(2.0-1.5))*(SL-1.5)
    
    		if SL>2.0 or SL<=3.0:
        		ctem1=0.538+((0.618-0.538)/(3.0-2.0))*(SL-2.0)
		
	if ST==1.25: 
   		
		if SL>=1.00 or SL<=1.25:
         		ctem1=0.598+((0.592-0.598)/(1.25-1.00))*(SL-1.00) 
        
    		if SL>=1.25 or SL<=1.5:
        		ctem1=0.592+((0.586-0.592)/(1.5-1.25))*(SL-1.25) 
    
    		if SL>1.5 or SL<=2.0:
        		ctem1=0.586+((0.57-0.586)/(2.0-1.5))*(SL-1.5);
    
    		if SL>2.0 or SL<=3.0:
        		ctem1=0.57+((0.601-0.57)/(3.0-2.0))*(SL-2.0);
   

	if ST==1.5: 
    
     		if SL>=1.00 or SL<=1.25:
         		ctem1=0.596+((0.608-0.596)/(1.25-1.00))*(SL-1.00) 
     
    		if SL>1.25 or SL<=1.5:
        		ctem1=0.608+((0.62-0.608)/(1.5-1.25))*(SL-1.25) 
    
    		if SL>1.5 or SL<=2.0:
        		ctem1=0.62+((0.602-0.62)/(2.0-1.5))*(SL-1.5)
    
    		if SL>2.0 or SL<=3.0:
        		ctem1=0.602+((0.584-0.602)/(3.0-2.0))*(SL-2.0)


	if ST==2.0: 
    
     		if SL>=1.00 or SL<=1.25:
         		ctem1=0.706+((0.704-0.706)/(1.25-1.00))*(SL-1.00); 
        
    		if SL>1.25 or SL<=1.5:
        		ctem1=0.704+((0.702-0.704)/(1.5-1.25))*(SL-1.25); 
    
    		if SL>1.5 or SL<=2.0:
        		ctem1=0.702+((0.632-0.702)/(2.0-1.5))*(SL-1.5);
    
    		if SL>2.0 or SL<=3.0:
        		ctem1=0.632+((0.581-0.632)/(3.0-2.0))*(SL-2.0);
    

	if ST==3.0: 
    
     		if SL>=1.00 or SL<=1.25:
         		ctem1=0.76+((0.752-0.76)/(1.25-1.00))*(SL-1.00) 
       
    		if SL>1.25 or SL<=1.5:
        		ctem1=0.752+((0.744-0.752)/(1.5-1.25))*(SL-1.25) 
   
    		if SL>1.5 or SL<=2.0:
       	 		ctem1=0.744+((0.648-0.744)/(2.0-1.5))*(SL-1.5)
    
    		if SL>2.0 or SL<=3.0:
        		ctem1=0.648+((0.608-0.648)/(3.0-2.0))*(SL-2.0)

	return ctem1

# Funcion C para calcular la constante C dependiendo de St y Sl

def C(St,SL):

	if St>=1.00 or St<=1.25:
     		C1=cte(1.00,SL)+((cte(1.25,SL)-cte(1.00,SL))/(1.25-1.00))*(St-1.00)
	

	if St>1.25 or St<=1.5: 
    
		C1=cte(1.25,SL)+((cte(1.5,SL)-cte(1.25,SL))/(1.5-1.25))*(St-1.25)
    
	if St>1.5 or St<=2.0: 
    		C1=cte(1.5,SL)+((cte(2.0,SL)-cte(1.5,SL))/(2.0-1.5))*(St-1.5)
    
	if St>2.0 or St<=3.0: 
    		C1=cte(2.0,SL)+((cte(3.0,SL)-cte(2.0,SL))/(3.0-2.0))*(St-2.0)
		
	return C1

#funcion cte para definir la constante en funcion de St y SL

def cte(ST,SL):
	if ST==1.00:
    		if SL>=1.00 or SL<=1.25:

        		cte1=0+((0.421-0)/(1.25-1.00))*(SL-1.00) 
      
    		if SL>=1.25 or SL<=1.5:
        		cte1=0.421+((0.484-0.421)/(1.5-1.25))*(SL-1.25) 
    
    		if SL>1.5 or SL<=2.0:
        		cte1=0.484+((0.537-0.484)/(2.0-1.5))*(SL-1.5)
   
    		if SL>2.0 or SL<=3.0:
        		cte1=0.537+((0.223-0.537)/(3.0-2.0))*(SL-2.0)
    
	if ST==1.25: 
    
     		if SL>=1.00 or SL<=1.25:
         		cte1=0.325+((0.348-0.325)/(1.25-1.00))*(SL-1.00)   
    		
		if SL>=1.00 or SL<=1.5:
        		cte1=0.348+((0.367-0.348)/(1.5-1.25))*(SL-1.25) 
    
    		if SL>1.5 or SL<=2.0:
        		cte1=0.367+((0.418-0.367)/(2.0-1.5))*(SL-1.5)
    
    		if SL>2.0 or SL<=3.0:
        		cte1=0.418+((0.29-0.418)/(3.0-2.0))*(SL-2.0)
   

	if ST==1.5: 
    
    		if SL>=1.00 or SL<=1.25:
        		cte1=0.302+((0.275-0.302)/(1.25-1.00))*(SL-1.00)

    		if SL>1.25 or SL<=1.5:
        		cte1=0.275+((0.25-0.275)/(1.5-1.25))*(SL-1.25) 
    
    		if SL>1.5 or SL<=2.0:
        		cte1=0.25+((0.299-0.25)/(2.0-1.5))*(SL-1.5)
    
    		if SL>2.0 or SL<=3.0:
        		cte1=0.299+((0.357-0.299)/(3.0-2.0))*(SL-2.0)

	if ST==2.0: 
    
    		if SL>=1.00 or SL<=1.25:
        		cte1=0.099+((0.1-0.099)/(1.25-1.00))*(SL-1.00) 
      
    		if SL>1.25 or SL<=1.5:
        		cte1=0.1+((0.101-0.1)/(1.5-1.25))*(SL-1.25) 
   
    		if SL>1.5 or SL<=2.0:
        		cte1=0.101+((0.229-0.101)/(2.0-1.5))*(SL-1.5)
        	
		if SL>2.0 or SL<=3.0:
        		cte1=0.229+((0.374-0.229)/(3.0-2.0))*(SL-2.0)
    

	if ST==3.0: 
    
    		if SL>=1.00 or SL<=1.25:
        		cte1=0.058+((0.0633-0.058)/(1.25-1.00))*(SL-1.00) 
    
    		if SL>1.25 or SL<=1.5:
        		cte1=0.0633+((0.0678-0.0633)/(1.5-1.25))*(SL-1.25) 
   
    		if SL>1.5 or SL<=2.0:
        		cte1=0.0678+((0.198-0.0678)/(2.0-1.5))*(SL-1.5)
    
    		if SL>2.0 or SL<=3.0:
        		cte1=0.198+((0.286-0.198)/(3.0-2.0))*(SL-2.0)

	return cte1

#funcion getK para obtener indices de la matriz de conversion

def getK(i,j,conv):

	k=-1
    	for n in range(len(conv)):
		
        	if i==conv[n,0] and j==conv[n,1]:
            		k=n
			return k
			
	if k==-1:
        	print 'indice no existe'

if __name__ == "__main__":
    poblacion = 100
    iteraciones = "100"
    max_repo_size = 100
    pop = []
    popvel = []
    objectives = []
    num_var = 2
    num_obj = 2
    limiteUp = [1.312, 20]
    limiteDown = [1.05, 1.05]


    for j in range(poblacion):
        pop.append([random.random() * (limiteUp[i] - limiteDown[i]) + limiteDown[i] for i in range(num_var)])
        popvel.append([0, 0])

    objectives = [[None for i in range(num_obj)] for j in range(len(pop))]

    [repoFin,repoObjFin] = modelosebafuenzalida(pop, popvel, num_var, objectives,
                     iteraciones, limiteUp, limiteDown)


    repoOX = []
    repoOY = []

    for i in range(len(repoObjFin)):
        repoOX.append(repoObjFin[i][0])
        repoOY.append(repoObjFin[i][1])

    pl.plot(repoOX, repoOY, 'bo')
    pl.xlabel('Temperatura (C)')
    pl.ylabel('Potencia Mecanica')
    pl.title('Frente de Pareto')
    pl.show()