#!/usr/bin/python
# -*- coding: utf-8 -*-

#Seccion 1: Importacion
#Importar las diferentes librerias necesarias para correr el programa
#Las mas importantes son las matematicas: Pyplot, Transforms, numpy, pylab y random que hacen los graficos y calculos matriciales de los modelos

import PIL.Image
import PIL.ImageTk
from Tkinter import *
import sys
import subprocess
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import numpy as np
import pylab as P
import random
import time
from operator import itemgetter
import tkMessageBox


#Seccion 2: Declaracion de ventanas
# Declaracion de ventanas que usa el programa Eobli. Tamanos de las diferentes ventanas que se usan en el programa

v0=Tk()
v0.geometry("800x600")
v1=Toplevel(v0)
v1.geometry("500x350")
v2=Toplevel(v0)
v2.geometry("650x400")
v3=Toplevel(v2)
v3.geometry("400x400")
v4=Toplevel(v0)
v4.geometry("650x150")
v5=Toplevel(v0)
v5.geometry("600x400")
v6 = Toplevel(v0)
v6.geometry("800x250")
v7 = Toplevel(v0)
v7.geometry("1100x500")
v8 = Toplevel(v7)
v8.geometry("800x400")
v9 = Toplevel(v2)
v9.geometry("800x400")
v10 = Toplevel(v9)
v10.geometry("600x400")
v11v = Toplevel(v9)
v11v.geometry("600x400")
v12v = Toplevel(v9)
v12v.geometry("600x400")
v13v = Toplevel(v4)
v13v.geometry("600x400")
v14 = Toplevel(v0)
v14.geometry("450x100")
v15 = Toplevel(v0)
v15.geometry("450x100")
v16 = Toplevel(v0)
v16.geometry("600x400")
v17 = Toplevel(v16)
v17.geometry("450x100")
v18 = Toplevel(v2)
v18.geometry("600x400")
v19 = Toplevel(v0)
v19.geometry("450x100")
v20 = Toplevel(v0)
v20.geometry("450x100")
v21 = Toplevel(v20)
v21.geometry("450x100")

current = None
kmeansindex = 0
random.seed(42)


USER_SELECTED_MODULARIZATION = None
USER_HAS_CONSTRUCTED = None

# Seccion 3: Metodos

#funcion RepresentsFloat para correcto funcionamiento de los bloques string/int (bloquea mal uso del software)

def RepresentsFloat(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False	

# elementos ventana v14: Error de llenado de campos

v14.title("Error")
Label(v14,text="").grid(row=0,column=0)
Label(v14,text="").grid(row=0,column=1)
Label(v14,text="Los campos ingresados contienen errores, por favor revisar").grid(row=1,column=1)

Button(v14,text="Volver",command=lambda:ejecutar(ocultar(v14))).grid(row=3,column=1)

# elementos ventana v15: Error de seleccion en listbox

v15.title("Error")
Label(v15,text="").grid(row=0,column=0)
Label(v15,text="").grid(row=0,column=1)
Label(v15,text="No se ha seleccionado elemento en lista, por favor revisar").grid(row=1,column=1)

Button(v15,text="Volver",command=lambda:ejecutar(ocultar(v15))).grid(row=3,column=1)


# Funcion mostrar: Sirve para construir el banco en la primera ventana 

def mostrar(ventana,v11,v12,v13): 

	#lee los valores de potencia, energia y voltaje ingresados por el usuario	

	current = None
	aa = poll()
	v = ""+str(aa)

	try:
		sel = list1.get(aa)
	except TclError:
		abrir(v15)
		sel = 0
	
	print "sel   " +str(sel)

	s11 = v11.get()
	s12 = v12.get()
	s13 = v13.get()

	# revisa que los valores ingresados por el usuario sean numeros, buen uso

	if RepresentsFloat(s11) and RepresentsFloat(s12) and RepresentsFloat(s13):

		potencia = s11
		energia = s12
		voltajeBanco = s13

	else: #despliega ventana de error
		abrir(v14)
		potencia = 0
		energia = 0
		voltajeBanco = 0
		
	#abre el archivo donde se encuentra la libreria de celdas	

	fin5 = open("listaCeldas.txt","r")
	fin_list5 = fin5.read().splitlines()
	fin5.close()

	file1 = fin_list5[0]
	
	#busca la celda elegida por el usuario en la libreria	

	for i in range(0,len(fin_list5)):
		
		if sel == fin_list5[i]:
			file1 = fin_list5[i] #revisar
			break
	
	# print "file1   " +str(file1)

	fin4 = open(file1+".txt", "r")
	fin_list4 = fin4.read().splitlines()
	fin4.close()
	
	# carga la celda escogida por el usuario	

	voltajeCelda= float(fin_list4[0])
	corrienteMaximaCelda = float(fin_list4[1])
	capacidadCelda = float(fin_list4[2])
	pesoCelda = float(fin_list4[3])
	volumenCelda = float(fin_list4[4])
	precioCelda = float(fin_list4[5])
	largoCelda = float(fin_list4[6])
	anchoCelda = float(fin_list4[7])

	# calcula numero de celdas necesarias segun requerimientos
	
	numceldas_potencia = float(potencia)/(voltajeCelda*corrienteMaximaCelda)
	print "celdas.potencia " +str(numceldas_potencia)
	numceldas_energia = float(energia)/(voltajeCelda*capacidadCelda)
	print "celdas.energia "+str(numceldas_energia)

	numceldas = max(numceldas_potencia,numceldas_energia)

	# hace numero entero
	
	if numceldas==numceldas_potencia:


		# if abs(float(potencia)%(voltajeCelda*corrienteMaximaCelda) - voltajeCelda*corrienteMaximaCelda) < 0.0000001:
		if abs(float(potencia)%(voltajeCelda*corrienteMaximaCelda)) < 0.0000001:
			numceldas2 = int(numceldas)
		else:
			numceldas2 = int(numceldas)+1
	else:
		
		# if abs(float(energia)%(voltajeCelda*capacidadCelda) - voltajeCelda*capacidadCelda) < 0.0000001:
		if abs(float(energia)%(voltajeCelda*capacidadCelda)) < 0.0000001:
			numceldas2 = numceldas
		
		else:
			numceldas2 = int(numceldas)+1
	
	print "numceldas2 " + str(numceldas2)

	
		
	numceldas_serie = float(voltajeBanco)/voltajeCelda
	print "numceldas_serie " + str(numceldas_serie)

	if abs(float(voltajeBanco)%(voltajeCelda) - voltajeCelda) < 0.00001:
		numceldas_serie2 = int(numceldas_serie)
		
	else:
		numceldas_serie2 = int(numceldas_serie)+1

	print "numceldas_serie2 " +str(numceldas_serie2)

	#presenta principales valores del banco en ventana
		
	e2.delete(0,10)
	e2.insert(0,str(numceldas_serie2))
	
	print "flag paralelo " +str(numceldas2/numceldas_serie2)


	if (numceldas2)%(numceldas_serie2)==0:
		numceldas_paralelo = int(numceldas2/numceldas_serie2)

	else:
		numceldas_paralelo = int(numceldas2/numceldas_serie2)+1
	
	print "numceldas_paralelo " + str(numceldas_paralelo)

	numceldas_final = numceldas_paralelo*numceldas_serie2		

	e1.delete(0,10)
	e1.insert(0,str(numceldas_final))

	e3.delete(0,10)
	e3.insert(0,str(numceldas_paralelo))
		
	voltajeBanco2 = float(numceldas_serie2*voltajeCelda)

	e4.delete(0,10)
	e4.insert(0,str(voltajeBanco2))

	potenciaBanco2 = numceldas_final*voltajeCelda*corrienteMaximaCelda
	energiaBanco2 = numceldas_final*voltajeCelda*capacidadCelda

	e5.delete(0,10)
	e5.insert(0,str(potenciaBanco2))

	e6.delete(0,10)
	e6.insert(0,str(energiaBanco2))

	e7.delete(0,10)
	e7.insert(0,str(numceldas_final*pesoCelda))

	e8.delete(0,10)
	e8.insert(0,str(numceldas_final*precioCelda))


	#revisa las restricciones antes de abrir la ventana de resultados

	mylist2 = open('restricciones.txt').read().splitlines()
	peso1 = float(mylist2[0])
	volumen1= float(mylist2[1])
	recursos1 = float(mylist2[2])
	impresion = 0

	#impresion guarda 0 si no se cumplen las restricciones (despliega ventana de error) o 1 si se cumplen (despliega ventana de exito)

	if numceldas_final*pesoCelda < peso1 and numceldas_final*volumenCelda < volumen1 and numceldas_final*precioCelda < recursos1:
		impresion = 1

	else:
		
		impresion = 0
		file3 = open('error.txt','w')
		file3.write(str(numceldas_final*pesoCelda)+'\n')
		file3.write(str(peso1)+'\n')
		file3.write(str(numceldas_final*volumenCelda)+'\n')
		file3.write(str(volumen1)+'\n')
		file3.write(str(numceldas_final*precioCelda)+'\n')
		file3.write(str(recursos1)+'\n')
		file3.write(file1+".txt")
		file3.close()
		ejecutar(abrir2(v6))



	if impresion == 1:
	
		f = open('resultados.txt', 'w')
		f.write(sel+'\n')
		f.write(str(numceldas_final)+'\n')
		f.write(str(numceldas_serie2)+'\n')
		f.write(str(numceldas_paralelo)+'\n')
		f.write(str(voltajeBanco2) +'\n')	
		f.write(str(potenciaBanco2) +'\n')
		f.write(str(energiaBanco2) +'\n')
		f.write(str(numceldas_final*pesoCelda) + '\n')
		f.write(str(numceldas_final*precioCelda) + '\n')
		f.write(file1+".txt")
		f.close()
	
		ventana.deiconify()

	global USER_HAS_CONSTRUCTED
	USER_HAS_CONSTRUCTED = True


#Funcion abrir2 sirve para desplegar la ventana de fallo en las restricciones

def abrir2(ventana):

	mylist22 = open('error.txt').read().splitlines()
	pesoObtenido = mylist22[0]
	pesoMaximo = mylist22[1]
	volumenObtenido = mylist22[2]
	volumenMaximo = mylist22[3]
	precioObtenido = mylist22[4]
	precioMaximo = mylist22[5]


	v101.set(pesoObtenido)
	v102.set(pesoMaximo)
	v103.set(volumenObtenido)
	v104.set(volumenMaximo)
	v105.set(precioObtenido)
	v106.set(precioMaximo)

	ventana.deiconify()

#Funcion reiniciar para borrar los valores de potencia, voltaje, energia y valores generados del banco.

def reiniciar(ventana):
	e1.delete(0,END)
	e2.delete(0,20)
	e3.delete(0,20)	
	e4.delete(0,20)
	e5.delete(0,20)
	e6.delete(0,20)
	v11.set('0')
	v12.set('0')
	v13.set('0')
	ee2.delete(0,20)


#Funciones de control: Ocultar para tapar la ventana, Ejecutar para correr un programa con desfase para cargar la ventana, Abrir para desplegar la ventana

def ocultar(ventana):

	#if ventana is v2:
	#	if USER_SELECTED_MODULARIZATION == False:
	#		tkMessageBox.showerror("Error de modularización", "Por favor, seleccione y guarde una configuración de modularización.")
	#		return
	ventana.withdraw()

def ejecutar(f): v0.after(200,f)

def abrir(ventana):

	if ventana is v2:
		if not e11.get().strip():
			tkMessageBox.showerror("Error de valores", "Escoja una potencia, jeje")
			return
		if not e12.get().strip():
			tkMessageBox.showerror("Error de valores", "Escoja una energía, jeje")
			return
		if not e13.get().strip():
			tkMessageBox.showerror("Error de valores", "Escoja un voltaje, jeje")
			return
		if USER_HAS_CONSTRUCTED == False:
			tkMessageBox.showerror("Error de construcción", "Por favor, seleccione \"Construir\" para construir el banco de baterías.")
			return

	if ventana is v4:
		if USER_HAS_CONSTRUCTED == False:
			tkMessageBox.showerror("Error de construcción", "Por favor, seleccione \"Construir\" para construir el banco de baterías.")
			return
		if USER_SELECTED_MODULARIZATION == False:
			tkMessageBox.showerror("Error de modularización", "Por favor, seleccione \"Pasar a Etapa 2\" y guarde una configuración de modularización.")
			return

	ventana.deiconify()


#Esta funcion permite cargar la ventana de tamano de poblacion y numero de iteraciones

def cerrar(ventana):
	abrir(v13v)
	v4.withdraw()

# Esta funcion permite mantener funcionando python mientras se abre un subproceso, Ironpython para controlar ANSYS

def cerrar2(ventana): 
	# sys.exit()
	print "start shell"
	#subprocess.call("./script02", shell=True) JEJE
	print "regreso a la realidad"
		

#Esta funcion permite abrir la ventana de configuracion (ventiladores, geometria) del banco
	
def mostrar2(v11,v12,v13): 
	current = None
	aa = poll3()
	bb = poll4()
	v = ""+str(aa)
	sel = list3.get(aa)
	sel2 = list4.get(bb)
	

	#abre los valores de la etapa 1 para ser utilizados en la etapa 2

	mylist = open('resultados.txt').read().splitlines()
	numceldas = str(mylist[1])
	ee2.insert(0,numceldas)
	global configuracion
	NombreArchivo = numceldas + "celdas.wbpj"

	configuracion = sel2.lower()
	
	

	# antigua programacion sin buscar en lista en archivo
	#if sel=="PCF 80 mm":
	#	maxFlujo = 0.03
	#elif sel=="Thermaltake 80 mm":
	#	maxFlujo = 0.035
	#elif sel=="Thermaltake 120 mm":
	#	maxFlujo = 0.05
	#else:
	#	maxFlujo = 0.035

	# abre la lista de ventiladores y compara la seleccion con la lista para abrir el archivo de ventilador correcto

	
	fin6 = open("listaVentiladores.txt")
	fin_list6 = fin6.read().splitlines()
	fin6.close()

	file11 = fin_list6[0]
	
	#busca la celda elegida por el usuario en la libreria	

	for i in range(0,len(fin_list6)):
		if sel == fin_list6[i]:
			file11 = fin_list6[i] #revisar
			break

	file11 = file11 + '.txt'
	print "Leyendo parametros tamano ventana y flujo maximo desde archivo \"%s\"" % file11
	fin44 = open(file11, "r")
	fin_list44 = fin44.read().splitlines()
	fin44.close()	

	tamVentana = fin_list44[0] #tamano ventana
	maxFlujo = fin_list44[1] #max Flujo
		
	#guarda los valores de la etapa en un archivo de configuracion para usar en otras etapas
	
	f = open('resultadosetapa2.txt', 'w')
	f.write(NombreArchivo +'\n')
	f.write(str(numceldas) +'\n')
	f.write(str(maxFlujo) + '\n')
	f.write(configuracion + '\n')
	#f.write(str(numceldas_serie2)+'\n')
	#f.write(str(numceldas_paralelo)+'\n')
	#f.write(str(voltajeBanco2) +'\n')	
	#f.write(str(potenciaBanco2) +'\n')
	#f.write(str(energiaBanco2) +'\n')
	f.close()

	g = open('config','w')
	g.write(NombreArchivo + '\n')

        print "Configuracion  guardada:", configuracion
        
	g.close()
	


#genera el codigo para poder cargar el scrollbar para las listas que lo necesitan

def colocar_scrollbar(listbox,scrollbar):
	scrollbar.config(command=listbox.yview)
	listbox.config(yscrollcommand=scrollbar.set)


#ingresa las restricciones y las escribe en un archivo de configuracion para uso en una siguiente etapa

def ingresar(ventana):

	vv11 = v55.get() #peso
	vv121 = v661.get() #largo
	vv122 = v662.get() #ancho
	vv123 = v663.get() #volumen

	# revisa que los valores ingresados sean numeros (buen uso de la herramienta)

	if RepresentsFloat(vv121) and RepresentsFloat(vv122) and RepresentsFloat(vv123): 
		vv124 = float(vv121)*float(vv122)*float(vv123)
		ancho = vv121
		largo = vv122
		alto = vv123
	else:
		vv124= "0"
		ancho = "0"
		largo = "0"
		alto = "0"
		abrir(v14)
		
	
	v664.set(vv124)  #volumen
	vv13 = v77.get() #recursos
	
	# buen uso: peso
	
	if RepresentsFloat(vv11):
		peso = vv11

	else:
		peso = "0"		
		abrir(v14)

	volumen = str(vv124)

	# buen uso: recursos

	if RepresentsFloat(vv13):
		recursos = vv13
	else:
		recursos = "0"
		abrir(v14)

	print recursos+str(recursos)

	# graba archivo de configuracion con los valores de las restricciones, que puede ser usado en la etapa siguiente
	
	file1 = open('restricciones.txt','w')
	file1.write(peso +'\n')
	file1.write(volumen + '\n')
	file1.write(recursos + '\n')
	file1.write(ancho + '\n')
	file1.write(largo + '\n')
	file1.write(alto + '\n')	


	file1.close()

	# ejecutar(ocultar(ventana))

arregloTiempo = []
arregloPotencia = []


#va guardando el tiempo y la potencia que se van escribiendo a mano cuando se decide cargar el requerimiento de potencia paso a paso (Etapa 1)

def guardar(ventana):

	tiempo = f711.get()
	potencia = f712.get()

	if RepresentsFloat(tiempo) and RepresentsFloat(potencia):

		arregloTiempo.append(tiempo)
		arregloPotencia.append(potencia)
	else:
		abrir(v14)

	print arregloTiempo
	print arregloPotencia


#sirve para graficar al potencia y generar histograma cuando se ingresaron los datos a mano

def graficar(arregloT,arregloP):
	energia = 0
	for i in range(len(arregloP)-1):
		energia = energia + float(arregloP[i])*(float(arregloT[i+1])-float(arregloT[i]))
	

	for i in range(len(arregloP)):
		arregloP[i] = float(arregloP[i])

	
	potencia = max(arregloP)

	v11.set(potencia)
	v12.set(energia/3600)

	P.figure()
	ax = P.subplot(1,2,1)
	ax.set_ylabel('Frecuencia (1/100)')
	ax.set_xlabel('Potencia (W)')
	bins = [10,20,30,40,50,60,70,80,90]
	n, bins, patches = P.hist(arregloP, bins, normed=1, histtype='bar', rwidth=0.8)
	
	ax2 = P.subplot(1,2,2)
	ax2.set_xlabel('Tiempo (s)')
	ax2.set_ylabel('Potencia (W)')
	P.plot(arregloT,arregloP)
	P.show()

#para borrar el arreglo generado a mano de potencia y tiempo

def borrar(ventana):
	del arregloTiempo[:] 
	del arregloPotencia[:] 


#Seccion 4: Modelos
#Primero viene el modelo de Pablo Espinoza
#Este modelo sirve para estimar la potencia y energia necesaria para completar un recorrido de un vehiculo electrico


def calculoPotencia(archivoTiempo,archivoVel,autonomy,m,Ecrit):


	#carga de archivos

	choice0 = archivoVel

	file1 = open(archivoTiempo, "r")
	tiempo_list = file1.read().splitlines()
	file1.close()
		

	file2 = open(choice0, "r")
	velocidad_list = file2.read().splitlines()
	file2.close()


	for i in range(len(velocidad_list)):
		velocidad_list[i] = float(velocidad_list[i])*1.608   # in km/h

	velocidad_list_copia = []
	tiempo_listcopia = []
	tiempo_aux = []



	for i in range(len(tiempo_list)):
		tiempo_aux.append(0)

	#generar arreglo de tamano grande para ajustarlo a la autonomia

	for k in range(50):
		for i in range(len(velocidad_list)):
			velocidad_list_copia.append(velocidad_list[i])

		for j in range(len(tiempo_list)):
			tiempo_aux[j] = (float(tiempo_list[len(tiempo_list)-1])+1)*i+float(tiempo_list[j])
			

		for j in range(len(tiempo_aux)):
			tiempo_listcopia.append(tiempo_aux[j])

	
	for i in range(len(tiempo_listcopia)):
		tiempo_listcopia[i] = tiempo_listcopia[i]/3600


	#calcular autonomia
 
	k = 10

	while np.trapz(velocidad_list_copia[0:k], x=tiempo_listcopia[0:k], dx=1.0) < autonomy:
		k = k+10
		
	
		
	tiempo_listcopia = tiempo_listcopia[0:k]
	velocidad_list_copia = velocidad_list_copia[0:k]

	# print tiempo_listcopia
	# print len(tiempo_listcopia)


	#calcular rango

	range1 = []

	for j in range(len(tiempo_listcopia)):
		range1.append(0)

	for i in range(2,len(tiempo_listcopia)):
		range1[i] = np.trapz(velocidad_list_copia[:i],x= tiempo_listcopia[:i],dx=1.0)

	#calcular aceleracion

	dv = np.diff(np.array(velocidad_list_copia))
	dt = np.diff(np.array(tiempo_listcopia))

	acc = []

	for i in range(len(dv)):
		acc.append(0)


	for i in range(len(dv)):
		acc[i] = (dv[i]*1000)/(3600*dt[i])


	#mapear gps

	height = []
	slope = []
	angle_deg = []
	angle_rad = []

	for i in range(len(velocidad_list_copia)):
		height.append(0)
		slope.append(0)
		angle_deg.append(0)
		angle_rad.append(0)

	#fuerzas

	f_g = []
	f_aero = []
	f_r_sta = []
	f_r_dyn = []

	g = 10
	
	# Cd = 0.15
	# rho_a = 1.2
	# A = 2
	# vw = 0.5
	# coeff_r1 = 1
	# coeff_r2 = 1

	Cd = f812.get()
	rho_a = f813.get()
	A = f814.get()
	vw = f815.get()
	coeff_r1 = f816.get()
	coeff_r2 = f817.get()

	if RepresentsFloat(Cd) and RepresentsFloat(rho_a) and RepresentsFloat(A) and RepresentsFloat(vw) and RepresentsFloat(coeff_r1) and RepresentsFloat(coeff_r2):
		aaa = 0
	else:
		m = 2000
		Cd = 0.15
		rho_a = 1.2
		A = 2
		vw = 0.5
		coeff_r1 = 1
		coeff_r2 = 1
		


	for i in range(len(velocidad_list_copia)):
	
		f_g.append(m*g*np.sin(angle_rad[i]))                               # gravity, in N
		f_aero.append((1/2)*float(Cd)*float(rho_a)*float(A)*(velocidad_list_copia[i]*(1000/3600)+float(vw))*(velocidad_list_copia[i]*(1000/3600)+float(vw)))           # aerodynamic force, in N
		f_r_sta.append(float(m)*g*np.cos(angle_rad[i])*(float(coeff_r1)))                    # static drag force, in N
		f_r_dyn.append(float(m)*g*np.cos(angle_rad[i])*(float(coeff_r2))*velocidad_list_copia[i]*(1000/3600))   # dynamic drag force, in N 

	

	# Kinetic Energy
	Kin_energy = []
	meq = float(m)

	for i in range(len(velocidad_list_copia)):
		# Kin_energy.append(0.5*meq*(np.power(velocidad_list_copia[i]*(1000/3600),2)))

		a = 0.5*meq

		b = np.power(velocidad_list_copia[i]*1000/3600,2)
		
		Kin_energy.append(a*b)


	dK = np.diff(Kin_energy)
	dt = np.diff(tiempo_listcopia)

	dKdt = []
	dKdt.append(0)
	# print dt

	for i in range(len(dK)):
		dKdt.append(dK[i]/dt[i])

	bat_eff = 0.9	
	Preq = []
	Pdis = []
	P = [] 

	# Required Power
	for i in range(len(dKdt)):

		Preq.append(dKdt[i]+(f_g[i]+f_aero[i]+f_r_sta[i]+f_r_dyn[i])*velocidad_list_copia[i]*(1000/3600)) #in J/s
		Pdis.append((f_g[i]+f_aero[i]+f_r_sta[i]+f_r_dyn[i])*velocidad_list_copia[i]*(1000/3600))
		Preq[i] = Preq[i]/bat_eff

	
	limninf_power = 0

	for i in range(len(Preq)):
		if Preq[i] < limninf_power: 
			P.append(limninf_power)

		else:
			P.append(Preq[i])

 	# print P
		
	Preq_total  = np.trapz(P,x = tiempo_listcopia)/(3600*1000)
	E_total = Ecrit/(3600*1000)


	for i in range(len(P)):
		P[i] = P[i]/(3600*1000)

	return [Preq_total,E_total,P,tiempo_listcopia]


#Codigos para el uso de cluster k-means

def cluster_points(X, mu):
    clusters  = {}
    for x in X:
        bestmukey = min([(i[0], np.linalg.norm(x-mu[i[0]])) \
                    for i in enumerate(mu)], key=lambda t:t[1])[0]
        try:
            clusters[bestmukey].append(x)
        except KeyError:
            clusters[bestmukey] = [x]
    return clusters
 
def reevaluate_centers(mu, clusters):
    newmu = []
    keys = sorted(clusters.keys())
    for k in keys:
        newmu.append(np.mean(clusters[k], axis = 0))
    return newmu
 
def has_converged(mu, oldmu):
    return (set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu]))
 
def find_centers(X, K):
    # Inicializar a K centros aleatorios
    oldmu = random.sample(X, K)
    mu = random.sample(X, K)
    while not has_converged(mu, oldmu):
        oldmu = mu
        # Asignar todos los puntos a X clusters
        clusters = cluster_points(X, mu)
        # Reevaluar los centros con los puntos asignados
        mu = reevaluate_centers(oldmu, clusters)
    return(mu, clusters)


# Funciones para cargar las curvas predisenadas us06, hudds, udds, etc.


def us06(ventana):

	file1 = open("us06tiempo.txt", "r")
	archivo1_list = file1.read().splitlines()
	file1.close()

	file2 = open("us06potencia.txt", "r")
	archivo2_list = file2.read().splitlines()
	file2.close()

	arregloT= archivo1_list
	arregloP= archivo2_list
	
	m = f811.get()
	autonomia = f818.get()	

	if RepresentsFloat(autonomia) and RepresentsFloat(m):
		aaa = 0 
	else:
		m = 2000
		autonomia = 164.5
	
	[Preq_total,E_total,arregloP,arregloT] = calculoPotencia("us06tiempo.txt","us06potencia.txt",float(autonomia),float(m),24*3600*1000)

	#print Preq_total
	#print E_total

	energia = Preq_total*1000
	potencia = max(arregloP)*1000
	# energia = E_total

	# print len(arregloP)
	# print len(arregloT)

	v11.set(potencia)
	v12.set(energia)

	P.figure()
	ax = P.subplot(1,2,1)
	ax.set_ylabel('Frecuencia')
	ax.set_xlabel('Potencia (kW)')
	bins = [10,20,30,40,50,60,70,80,90]
	n, bins, patches = P.hist(arregloP, bins, histtype='bar', rwidth=0.8)
	
	ax2 = P.subplot(1,2,2)
	ax2.set_xlabel('Tiempo (s)')
	ax2.set_ylabel('Potencia (kW)')
	P.plot(arregloT,arregloP)
	P.show()


def udds(ventana):

	file1 = open("uddstiempo.txt", "r")
	archivo1_list = file1.read().splitlines()
	file1.close()

	file2 = open("uddspotencia.txt", "r")
	archivo2_list = file2.read().splitlines()
	file2.close()

	arregloT= archivo1_list
	arregloP= archivo2_list
	
	m = f811.get()
	autonomia = f818.get()

	if RepresentsFloat(autonomia) and RepresentsFloat(m):
		aaa = 0 
	else:
		m = 2000
		autonomia = 164.5


	[Preq_total,E_total,arregloP,arregloT] = calculoPotencia("uddstiempo.txt","uddspotencia.txt",float(autonomia),float(m),24*3600*1000)

	energia = Preq_total*1000
	potencia = max(arregloP)*1000
	# energia = E_total

	v11.set(potencia)
	v12.set(energia)

	P.figure()
	ax = P.subplot(1,2,1)
	ax.set_ylabel('Frecuencia')
	ax.set_xlabel('Potencia (kW)')
	bins = [10,20,30,40,50,60,70,80,90]
	n, bins, patches = P.hist(arregloP, bins, histtype='bar', rwidth=0.8)
	
	ax2 = P.subplot(1,2,2)
	ax2.set_xlabel('Tiempo (s)')
	ax2.set_ylabel('Potencia (kW)')
	P.plot(arregloT,arregloP)
	P.show()

def hwfet(ventana):

	file1 = open("hwfettiempo.txt", "r")
	archivo1_list = file1.read().splitlines()
	file1.close()

	file2 = open("hwfetpotencia.txt", "r")
	archivo2_list = file2.read().splitlines()
	file2.close()

	arregloT= archivo1_list
	arregloP= archivo2_list

	m = f811.get()
	autonomia = f818.get()

	if RepresentsFloat(autonomia) and RepresentsFloat(m):
		aaa = 0 
	else:
		m = 2000
		autonomia = 164.5


	[Preq_total,E_total,arregloP,arregloT] =  calculoPotencia("hwfettiempo.txt","hwfetpotencia.txt",float(autonomia),float(m),24*3600*1000)

	energia = Preq_total*1000
	potencia = max(arregloP)*1000
	# energia = E_total

	v11.set(potencia)
	v12.set(energia)

	P.figure()
	ax = P.subplot(1,2,1)
	ax.set_ylabel('Frecuencia')
	ax.set_xlabel('Potencia (kW)')
	bins = [10,20,30,40,50,60,70,80,90]
	n, bins, patches = P.hist(arregloP, bins, histtype='bar', rwidth=0.8)
	
	ax2 = P.subplot(1,2,2)
	ax2.set_xlabel('Tiempo (s)')
	ax2.set_ylabel('Potencia (kW)')
	P.plot(arregloT,arregloP)
	P.show()


def hudds(ventana):

	file1 = open("huddstiempo.txt", "r")
	archivo1_list = file1.read().splitlines()
	file1.close()

	file2 = open("huddspotencia.txt", "r")
	archivo2_list = file2.read().splitlines()
	file2.close()

	arregloT= archivo1_list
	arregloP= archivo2_list

	m = f811.get()
	autonomia = f818.get() 

	if RepresentsFloat(autonomia) and RepresentsFloat(m):
		aaa = 0 
	else:
		m = 2000
		autonomia = 164.5


	[Preq_total,E_total,arregloP,arregloT] =  calculoPotencia("huddstiempo.txt","huddspotencia.txt",float(autonomia),float(m),24*3600*1000)

	energia = Preq_total*1000
	potencia = max(arregloP)*1000
	# energia = E_total

	v11.set(potencia)
	v12.set(energia)

	P.figure()
	ax = P.subplot(1,2,1)
	ax.set_ylabel('Frecuencia')
	ax.set_xlabel('Potencia (kW)')
	bins = [10,20,30,40,50,60,70,80,90]
	n, bins, patches = P.hist(arregloP, bins, histtype='bar', rwidth=0.8)
	
	ax2 = P.subplot(1,2,2)
	ax2.set_xlabel('Tiempo (s)')
	ax2.set_ylabel('Potencia (kW)')
	P.plot(arregloT,arregloP)
	P.show()


	# ocultar(ventana)

# Opcion para cargar archivos preexistentes

def cargarArchivos(v1,v2):
	
	archivo1 = "" + v1.get()
	archivo2 = ""+ v2.get() 

	file1 = open(archivo1, "r")
	archivo1_list = file1.read().splitlines()
	file1.close()

	file2 = open(archivo2, "r")
	archivo2_list = file2.read().splitlines()
	file2.close()

	arregloT = archivo1_list
	arregloP = archivo2_list

	# print str(len(arregloT))
	# print str(len(arregloP))

	energia = 0
	for i in range(len(arregloP)-1):
		energia = energia + float(arregloP[i])*(float(arregloT[i+1])-float(arregloT[i]))

	potencia = max(arregloP)

	v11.set(potencia)
	v12.set(energia)	# v12.set(energia/3600)

	P.figure()
	ax = P.subplot(1,2,1)
	ax.set_ylabel('Frecuencia (1/100)')
	ax.set_xlabel('Potencia (W)')
	bins = [10,20,30,40,50,60,70,80,90]
	n, bins, patches = P.hist(arregloP, bins, normed=1, histtype='bar', rwidth=0.8)
	
	ax2 = P.subplot(1,2,2)
	ax2.set_xlabel('Tiempo (s)')
	ax2.set_ylabel('Potencia (W)')

	P.plot(arregloT,arregloP)
	P.show()

#Parte 4.2: Modelo de Sebastian Fuenzalida
# Primero vienen las funciones de soporte para el main del programa

# Funcion Ro

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

#Funcion Viscosidad

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

#funcion getIJ para obtener indices de la matriz de conversion

def getIJ(k,conv):
	i = conv[k,0]
	j = conv[k,1]

	return i,j

#funcion getK para obtener indices de la matriz de conversion

def getK(i,j,conv):

	k=-1
    	for n in range(len(conv)):
		
        	if i==conv[n,0] and j==conv[n,1]:
            		k=n
			return k
			
	if k==-1:
        	print 'indice no existe'	

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


# bancostubosT_G es el main del modelo de Sebastian Fuenzalida. Recibe todos los parametros geometricos, electricos y fisicos necesarios para simular 

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
    
	
	if fluido=='aire':
		Cp=1007                       # Capacidad calorifica
		Deni=Ro(Tfluido_in)            # Densidad fluido [kg/m3]
		Visc=Viscosidad(Tfluido_in)    # Viscosidad dinamica fluido [kg/ms]
		Condflu=kfluido(Tfluido_in)    # Conductividad fluido [W/mK]
		Prandt=NPran(Tfluido_in)       #Numero Prandt


	if fluido == 'agua':    
		Deni=998.2                     # Densidad fluido [kg/m3]
		Visc=0.001002                  # Viscosidad dinamica fluido [kg/ms]
		Condflu=0.59                   # Conductividad fluido [W/mK]
		Prandt=7.07                    # Numero Prandt
		Cp=4186                        # Capacidad calorifica


	


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

	# 
	T = np.zeros((filas,columnas)) #Temperatura celdas tiempo t [C]


	for i in range(filas):
		for j in range(columnas): 
			T[i,j] = T0celdas - 273.15 # Temperatura celdas tiempo t [C]



	#tiempo de simulacion

	if corriente>0 or Ifluido>0:
		Segundos=(Ah/(corriente+Ifluido))*3600   #Tiempo de descarga celda [s]   
		# print Segundos	
	else:
    		Segundos=10

        if Segundos < 1:
            Segundos = 10

	# y = min(np.floor(Segundos), 20)
	y = np.floor(Segundos)


	Grafico = []
	Tiempo = []

	
	for i in range(int(y)):
		Grafico.append(1)        #Contador para guardar Temperatura Maxima en cada segundo
		Tiempo.append(1)          # Contador de tiempo para graficar al finalizar los calculos



	# ciclo de simulacion 

	for t in range(int(y)):
		
		#print t
		for k in range(N):

			[i,j] = getIJ(k,conv)

			NuD = Nuss(ReDmax, m(St, SL), Prandt, i+1, C(St,SL)) #Numero de Nusselt
			h = NuD*Condflu/diametro  #Coeficiente de conveccion

			#Constantes
    			a=h*diametro+2*cont
    			b=h*diametro+cont
    			Fo=float(cont*h*dt)/float(RoAl*CpAl*diametro)
    			c=float(dt)/float(RoAl*CpAl)

			# print 'calorgen' + str(Calorgen)
			#print 'c' + str(c)
			#print 'Fo' + str(Fo)
			#print 'dt' + str(dt)
			#print 'RoAl' + str(RoAl)
			#print 'CpAl' + str(CpAl)


			# Temperatura de Salida del Fluido
			if fluido=='aire':    
				
				# Aqui se cae
				# T[j,1] está accediendo a la segunda columna de la matriz
				# Pero si columnas == 1 entonces T tiene solo una columna.          WTF!

				#raw_input("Press enter to crash the application...")

				Tout=(T[j,columnas-1]+273.15)-((T[j,columnas-1]+273.15)-(T[j,0]+273.15+Tfluido_in)/2)*np.exp((-1*3.14*diametro*columnas*filas*h)/(Ro((T[j,1]+273.15+Tfluido_in)/2)*Velocidadfluido*filas*St*diametro*Cp))
			
			if fluido=='agua':
				Tout=(T[j,columnas-1]+273.15)-((T[j,columnas-1]+273.15)-(T[j,0]+273.15+Tfluido_in)/2)*np.exp((-1*3.14*diametro*columnas*filas*h)/(Deni*Velocidadfluido*filas*St*diametro*Cp))

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
			if i==0 and j>0 and j<filas-1:

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
    
  		if fluido=='aire':
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

		#print 'dP' + str(DeltaPresion)
		#print 'f' + str(f)
		#print 'Deni' +str(Deni)
		#print 'Vmax' + str(np.power(Vmax,2))
		#print 'Flujo' + str(Flujo)
		#print 'Potencia_Mecanica' + str(Potencia_Mecanica)
		

		Pot_Ventilador=float(Potencia_Mecanica)/float(0.25)                 # Potencia del Ventilador [W]
		Potencia_Electrica=filas*columnas*corriente*Voltaje    # Potencia Electrica aportada por el Banco de Baterias [W]

		Eficiencia=(Potencia_Electrica-Pot_Ventilador)/Potencia_Electrica      # Eficiencia del Sistema

		Tiempo[t]=t
		Grafico[t]=ma
		#print "Ma" + str(ma) 
   		Tp=U

		toc = time.time()
	
		Tiempo_Simulacion = toc - tic 
    
	#salida del programa una vez completadas todas las iteraciones del modelo


        #print range(int(y))
	return [T,Velocidadfluido,DeltaPresion,Potencia_Mecanica,Potencia_Electrica,Eficiencia,Ifluido,ma,mi,Tiempo_Simulacion,delta_T,Pot_Ventilador]




# La funcion Transiente_Func controla los calculos de la funcion BancosTubos que es la principal del modelo de Sebastian.


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



# En esta funcion se itera el algoritmo evolutivo adaptado para correr el modelo de Sebastian Fuenzalida 

def modelosebafuenzalida(pop,popvel,num_var,objectives,iteraciones,limiteUp,limiteDown):

	counter = 0

	#abre resultados de modularizacion para obtener filas y columnas

	f = open('resultadosmodularizacion.txt', 'r')
	mod_list = f.read().splitlines()
	f.close()

	filas = mod_list[0]

	# OJO: si columnas == 1 la aplicación se cae en bancotubosT_G
	columnas = mod_list[1]

	#aca esta la seccion para usar diferentes tamanos de celda


	#abre el archivo donde se encuentra la libreria de celdas	

	fin5 = open("listaCeldas.txt","r")
	fin_list5 = fin5.read().splitlines()
	fin5.close()

	file1 = fin_list5[0]
	
	aa = poll()

	# JEJE
	#aa = 0
	

	v = ""+str(aa)
	sel = list1.get(aa)
	
	#busca la celda elegida por el usuario en la libreria	

	for i in range(0,len(fin_list5)):
		
		if sel == fin_list5[i]:
			file1 = fin_list5[i] #revisar
			break
	
	# print "file1   " +str(file1)

	fin4 = open(file1+".txt", "r")
	fin_list4 = fin4.read().splitlines()
	fin4.close()


	diametro = float(fin_list4[7])/1000
	altura = float(fin_list4[6])/1000
	
	# diametro = 0.026                    #codigo original sin cambios

	# altura = 0.065                       # Altura celda en [m]
	corriente = 8                       # Corriente celda [A]
	resistencia_interna = 0.032          # Resistencia celda [Ohm] podria variarse por datasheet
	Tfluido_in = 273.15+20 

	# Caudal = 100
	# St = 1.5
	# SL = 1.5
	
	T0celdas = 273.15+20

	Ah = float(fin_list4[2])            #Capacidad de la celda [Ah]
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
       			# SL = pop[i][0]
			# Caudal = pop[i][1]

			SL = pop[i][1]
			Caudal = 40

			[matriz,T] = Transiente_func(diametro,filas,columnas,altura,corriente,resistencia_interna,Tfluido_in,Caudal,T0celdas,St,SL,Ah,dt,Voltaje)

			Objetivo1 = matriz[6]
			Objetivo2 = matriz[11]

			objectives[i][0] = Objetivo1
			objectives[i][1] = Objetivo2


			# Guardar el resultado de cada simulacion para respaldo

			f = open(workingDir2 + 'model' + str(counter)+'.txt', 'w')
			f.write(""+"id:"+str(counter)+ ", " + str(pop[i][0]) + ", "+"" + str(pop[i][1]) + "," + str(objectives[i][0]) + ", " + str(objectives[i][1]) + "\n")
			f.close() 
			print 'counter  ' + str(counter)
	 	 	counter = counter + 1
		

		
		
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

# Fin del ciclo del programa de Sebastian Fuenzalida

#Modelo de Jorge Reyes
#Primero vienen las funciones auxiliares del Modelo

#Funcion conductividad, como interpolacion de la temperatura

def conductividad(T):

	T = T+273.15
	Datos = [22.3E-3, 26.3E-3, 30E-3, 33.8E-3, 37.3E-3];
	Temp = [250, 300, 350, 400, 450];

	if T<250:
    		k = np.interp(T,[Temp[0],Temp[1]],[Datos[0],Datos[1]])
		return k
	
	elif T>450:
    		k = np.interp(T,[Temp[3],Temp[4]],[Datos[3],Datos[4]])
		return k
 	else:
		for i in range(len(Temp)):
		   if T == Temp[i]:
        		k = Datos[i]
        		return k

	for i in range(len(Temp)-1):
    		if T > Temp[i] and T<Temp[i+1]:
        		k = np.interp(T,[Temp[i],Temp[i+1]],[Datos[i],Datos[i+1]])
        		return k

#Funcion nusselt2 para estimar el Nusselt en base a interpolaciones

def nusselt2(re,a):
	Pr = 0.7
	Pr_w = 0.689


	if re<=0:
		nu = 0
		return nu

	if re <= 1E2:
    		c = 0.9
    		m = a
   		n = 0.37
    		nu = c*np.power(re,m)*np.power(Pr,n)*np.power((Pr/Pr_w),0.25)
		return nu
	
	if re > 1E2 and re<=1E3:
    		c = 0.51
    		m = a
   		n = 0.37
    		nu = c*np.power(re,m)*np.power(Pr,n)*np.power((Pr/Pr_w),0.25)
		return nu

	
	if re > 1E3 and re<=2E5:
    		c = 0.35
    		m = a
   		n = 0.37
    		nu = c*np.power(re,m)*np.power(Pr,n)*np.power((Pr/Pr_w),0.25)
		return nu
	

	if re > 2E5:
    		c = 0.023
    		m = a
   		n = 0.37
    		nu = c*np.power(re,m)*np.power(Pr,n)*np.power((Pr/Pr_w),0.25)
		return nu


#Funcion Cznusselt para calcular el Nusselt en funcion de una interpolacion

def cznusselt(i,Re):

	col = [1, 2, 3, 4, 5, 7, 10, 13, 16, 20]
	cz1 = [0.84, 0.88, 0.91, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1]
	cz2 = [0.64, 0.76, 0.84, 0.89, 0.92, 0.95, 0.97, 0.98, 0.99, 1]

	# print "Re"  + str(Re)
	if Re<0:
    		cz = 0
    		return cz

	if i>20:
    		cz = 1
    		return cz

	if Re<1E3:
    		cz = 1
    		return cz

	if Re >=1E3:
    		cz = np.interp(i,col,cz2)
    		return cz
    
		

#Funcion cdr3

def cdr3(Re):

	if Re<0:
		cd = -1
		return cd

	c = 3.3481
	n = -0.179

	cd = c*np.power(Re,-n)

	return cd


#Funcion Viscosidad para calcularla en funcion de una interpolacion

def viscosidad(T):
	T = T+273.15
	# print T
	Datos = [159.6E-7, 184.6E-7, 208.2E-7, 230.1E-7, 250.7E-7]
	Temp = [250, 300, 350, 400, 450]

	
	if T<250:
		visc = np.interp(T,[Temp[0],Temp[1]],[Datos[0],Datos[1]])
		return visc
			
	if T>450:
    		visc = np.interp(T,[Temp[3],Temp[4]],[Datos[3],Datos[4]])
    		return visc

	for i in range(len(Temp)):
    		if T == Temp[i]:
        		visc = Datos[i];
        		return visc
    

	for i in range(len(Temp)-1):
    		if T > Temp[i] and T < Temp[i+1]:
        		visc = np.interp(T,[Temp[i],Temp[i+1]],[Datos[i],Datos[i+1]]);
        		return visc


#Funcion Reynolds para calcular el Numero de Reynolds a partir de la Viscosidad y otras variables


def reynolds(v,T,Diam,rho):
	visc = viscosidad(T)
	
	re = rho*v*Diam/visc
	
	return re 

#Funcion cp para estimar la constante en funcion de una interpolacion

def cp(T):

	T = T+273.15
	Datos = [1.006E3, 1.007E3, 1.009E3, 1.014E3, 1.021E3]
	Temp = [250, 300, 350, 400, 450]

	if T < 250:
    		cp1 = np.interp(T,[Temp[0],Temp[1]],[Datos[0],Datos[1]])
    		return cp1

	if T > 450:
    		cp1 = np.interp(T,[Temp[3],Temp[4]],[Datos[3],Datos[4]])
    		return cp1

	for i in range(len(Temp)):
    		if T == Temp[i]:
        		cp1 = Datos[i]
        		return cp1


	for i in range(len(Temp)-1):
    		if T> Temp[i] and T<Temp[i+1]:
        		cp1 = np.interp(T,[Temp[i],Temp[i+1]],[Datos[i],Datos[i+1]])
        		return cp1


#Funcion ffriction para calcular el Factor de Friccion con interpolaciones

def ffriction(Re,S):
	coef = [[0 for x in xrange(3)] for x in xrange(4)]
	coef[0][0] = 0.25
	coef[0][1] = 82.188
	coef[0][2] = -0.605

	coef[1][0] = 0.5
	coef[1][1] = 38.446
	coef[1][2] = -0.54
	
	coef[2][0] = 1
	coef[2][1] = 11.728
	coef[2][2] = -0.402

	coef[3][0] = 1.5
	coef[3][1] = 1.2095
	coef[3][2] = -0.211

	if Re<0:
		f = 0
    		return f

	if S<coef[0][0]:
    		aux1 = np.interp(S,[coef[0][0], coef[1][0]],[coef[0][1], coef[1][1]])
    		aux2 = np.interp(S,[coef[0][0], coef[1][0]],[coef[0][2], coef[1][2]])
    		f = aux1*np.power(Re,aux2)
    		return f

	if S>coef[3][0]:
		aux1 = np.interp(S,[coef[0][0],coef[1][0],coef[2][0],coef[3][0]],[coef[0][1],coef[1][1],coef[2][1],coef[3][1]])
		aux2 = np.interp(S,[coef[0][0],coef[1][0],coef[2][0],coef[3][0]],[coef[0][2],coef[1][2],coef[2][2],coef[3][2]])
		f = aux1*np.power(Re,aux2)
    		return f

	for i in range(4):
		if S == coef[i][0]:
			f = coef[i][1]*np.power(Re,coef[i][2])
			return f

	for i in range(3):
		if S > coef[i][0] and S < coef[i+1][0]:
			aux1 = np.interp(S,[coef[i][0],coef[i+1][0]],[coef[i][1],coef[i+1][1]])
			aux2 = np.interp(S,[coef[i][0],coef[i+1][0]],[coef[i][2],coef[i+1][2]])
			f = aux1*np.power(Re,aux2)
    			return f			


#Main del modelo de Jorge Reyes 

def modelo(I, S, Flow, n_fluido, col_celda, col_fluido, Diam, Largo):

	a = [0, 0, 0]

	b1 = [0.039, 0.028, 0.027, 0.028, 0.005]
	b2 = [3.270, 2.416, 2.907, 2.974, 2.063]
	x = [0.1, 0.25, 0.5, 0.75, 1];

	if S<x[0]:
		a1 = np.interp(S,[x[1],x[2]],[b1[1],b1[2]])
		a2 = np.interp(S,[x[1],x[2]],[b2[1],b2[2]])
	elif  S>x[4]:
		a1 = b1[4]
		a2 = b2[4]
	else:
		a1 = max(np.interp(S,x,b1), 0);
		a2 = max(np.interp(S,x,b2), 0);
	a[0] = a1
	a[1] = a2
	a[2] = 0.653

	# definicion de variables necesarias para la operacion del modelo

	r = 0.032                     #Resistencia interna [Ohm]
	Flujo = Flow*0.00047          #Flujo de entrada del fluido [CFM]->[m3/s]

	#abre el archivo donde se encuentra la libreria de celdas

	# aa = poll()
	# #print aa 
	# v = ""+str(aa)
	# sel = list1.get(aa)

	# fin5 = open("listaCeldas.txt","r")
	# fin_list5 = fin5.read().splitlines()
	# fin5.close()

	# file1 = fin_list5[0]
	
	# #busca la celda elegida por el usuario en la libreria	

	# for i in range(0,len(fin_list5)):
		
	# 	if sel == fin_list5[i]:
	# 		file1 = fin_list5[i] #revisar
	# 		break
	
	# # print "file1   " +str(file1)

	# fin4 = open(file1+".txt", "r")
	# fin_list4 = fin4.read().splitlines()
	# fin4.close()

	# Diam = float(fin_list4[7])/1000
	# Largo = float(fin_list4[6])/1000
	# I = float(fin_list4[1])

	vol = (np.power(Diam, 2) * np.pi / 4.0) * Largo     #Volumen celda [m3]
	e = 0.015                      #Espaciado entre pared y celda [m]
	z = 0.005                       #Corte del estudio [m]
	R = 286.9                     #Constante de los gases aire [J/kgK]
	K = 1.4                        #K del aire 1,4
	P_atm = 101325                 #Presion atmosferica [Pa]
	Q_vol = np.power(I , 2) * r / vol              #Calor volumetrico
	q = Q_vol * (np.power(Diam, 2) * np.pi / 4) * z      #Calor total corte.
	A_sup = np.pi * Diam * z  # /2

	H = 2 * e + Diam * n_fluido + S * Diam * (n_fluido - 1)  #Altura del pack
	A = H * z                                        #Area de entrada pack
	A_vol = (S + 1) * Diam * z                           #Area volumen control eje z
	A_ent = S * Diam *z                             #Area entrada eje z

	T_fluido = []  # [C]
	P_fluido = []  # [Pa]
	V_fluido = [] # [m/s]
	Vm_fluido = [] #[m/s]
	D_fluido = [] #[kg/m3]
	T_celda = [] #[C]
	F_fluido = [] #N
	C = []   #[m/s]
	M = []  #Mach
	Ta = [] #[C]
	Da = [] #[kg/m3]
	Pa = [] #[Pa]
	Re = [] #Adimensional
	Rem = [] #adimensional
	k_fluido = [] #[W/(m*K)]
	
	
	# inicializacion de vectores

	for i in range(col_fluido):
		T_fluido.append(20)
		P_fluido.append(P_atm)
		V_fluido.append((Flujo * z / Largo) / A)
		Vm_fluido.append((Flujo* z / Largo) / A)
		D_fluido.append(1.204)
		F_fluido.append(0)
		C.append(1)
		M.append(1)
		Ta.append(1)
		Da.append(1)
		Pa.append(1)
		Re.append(1)
		Rem.append(1)
		k_fluido.append(conductividad(T_fluido[0]))

	for i in range(col_celda):
		T_celda.append(20)

	#Errores
	
	error1 = []  #ERROR T CELDAS
	errf = []    #ERROR TFLUIDO
	errv = []    #ERROR VELOCIDAD
	errp = []    #ERROR PRESION
	errd = []     #ERROR DENSIDAD
	errmax = 1E-3  #ERROR CORTE 
	
	for i in range(col_celda+1):
		errf.append(1E1000)
		errv.append(1E1000)
		errd.append(1E1000)

	for i in range(col_celda):
		errp.append(1E1000)
		error1.append(1E1000)


	#Condiciones de Borde

	T_fluido[0] = 20                           #Temperatura entrada [C]
	Vinicio = a[1] * Flujo * (z / Largo) / A           #Velocidad entrada[m/s]
	D_fluido[0] = 1.204                        #Densidad de entrada [kg/m3]
	P_fluido[col_fluido - 1] = P_atm                       #Presion entrada [Pa]
	
	Pa[0] = P_fluido[0] / ((1 + K)/(1 + K * np.power(M[0], 2)))
	Da[0] = Pa[0] / (R * Ta[0])

	D_fluido[0] = 1.204                        #[kg/m3]
	m_punto = (S + 1) * Diam * z * Vinicio * D_fluido[0] #[kg/s]
	errv[0] = 0
	errd[0] = 0
	errf[0] = 0

	for i in range(1,col_fluido):
		D_fluido[i] = D_fluido[0] - 0.204*(i) / col_celda


	k = 1

	errorp = []
	errorv = []
	errortf = [] 
	errord = [] 
	errortc = [] 

	# Ciclo principal del modelo de desarrollado por Jorge Reyes 

	while (max(error1)>errmax) or (max(errf)>errmax) or (max(errp)>errmax) or (max(errv)>errmax) or (max(errd)>errmax):
	
		#El primer valor del arreglo se calcula con formulas predefinidas 
		cdrag = a[0] * cdr3(Rem[0])
		F_fluido[0] = 0.5 * Diam * z * D_fluido[0] * np.power(Vinicio, 2) * cdrag
		errv[0] = V_fluido[0]

		if m_punto > 0:
			V_fluido[0] = Vinicio - F_fluido[0]/m_punto
		else:
			V_fluido[0] = 0
		if V_fluido[0]>0:
    			errv[0] = abs(errv[0] - V_fluido[0])/V_fluido[0]
		else:
			errv[0] = 0


		C[0] = np.sqrt(K*R*(T_fluido[0]+273.15))
		Vm_fluido[0] = (S/(S+1))*V_fluido[0]


    		M[0] = V_fluido[0]/C[0]    
		Ta[0] = T_fluido[0]/(((1+K)*M[1])/np.power(np.power(1+K*M[1],2),2))

    		Rem[0] = reynolds(Vm_fluido[0],T_fluido[0],Diam,D_fluido[0])

    		Re[0] = reynolds(V_fluido[0],T_fluido[0],Diam,D_fluido[0])


		errp[0] = P_fluido[0]
    		P_fluido[0] = P_fluido[1] + 0.5*0.7*ffriction(Rem[0],S)*D_fluido[0]*np.power(Vm_fluido[0],2)
    		errp[0] = abs(P_fluido[0] - errp[0])/P_fluido[0]
    
    		Pa[0] = P_fluido[0]/((1+K)/(1+K*np.power(M[1],2)))
    		Da[0] = Pa[0]/(R*Ta[0])
  
    		D_fluido[0] = 1.204
	

		# ciclo para todas las columnas 

		for i in range(col_fluido-1):
			
			Vm_fluido[i] = (S/(S+1))*V_fluido[i]


       			Rem[i+1] = reynolds(Vm_fluido[i],T_fluido[i],Diam,D_fluido[i])
	
			
       			C[i+1] = np.power((K*R*(T_fluido[i+1]+273.15)),0.5)               #[m/s]
       			M[i+1] = V_fluido[i+1]/C[i+1]

			aux1 = 1+K*np.power(M[i+1],2)
			aux2 = (1+K)*M[i+1]

			aux3 = aux2/aux1  


			aux3 = 1

       			Ta[i+1] = T_fluido[i+1]/np.power(aux3,2)

			errp[i] = P_fluido[i]


			P_fluido[i] = P_fluido[i+1] + 0.5*0.7*ffriction(Rem[i],S)*D_fluido[i]*np.power(Vm_fluido[i],2)
      			errp[i] = abs(P_fluido[i] - errp[i])/P_fluido[i]

			

       
       			#Calculo de la velocidad

       			flujo = V_fluido[i]*A_ent/0.00047
       			cdrag = a[0]*cdr3(Rem[i])

			numerito = np.power(V_fluido[i],2)*cdrag
       			F_fluido[i+1] = 0.5*Diam*z*D_fluido[i]*numerito
			
       			errv[i+1] = V_fluido[i+1]
			
			aux4 = 	P_fluido[i+1]-P_fluido[i]
			
			if m_punto>0:
       				V_fluido[i+1] = (A_vol*(aux4)-F_fluido[i+1])/m_punto  + V_fluido[i]
			else:
				V_fluido[i+1] = 0
			
			# error de la velocidad

			if V_fluido[i+1]>0:
       				errv[i+1] = abs(V_fluido[i+1]-errv[i+1])/V_fluido[i+1]
       			else:
				errv[i+1] = 0


       			#Calculo de la temperatura fluido
       			errf[i+1] = T_fluido[i+1]
			aux1 = ((1+0/S)*q/m_punto)
			aux2 = -0.5*(np.power(V_fluido[i+1],2)-np.power(V_fluido[i],2))
			aux3 = cp(T_fluido[i])

			
       			T_fluido[i+1] = (aux1 + aux2)/aux3 + T_fluido[i]

			# error de la temperatura de fluido
       			errf[i+1] = abs(errf[i+1]-T_fluido[i+1])/T_fluido[i+1]
       
       			#Calculo de la densidad
       			Pa[i+1] = P_fluido[i+1]/((1+K)/(1+K*np.power(M[i+1],2)))
       			Da[i+1] = Pa[i+1]/(R*Ta[i+1])

			#error de la densidad	

       			errd[i+1] = D_fluido[i+1]
       			D_fluido[i+1] = D_fluido[i] + (Da[i+1]-Da[i])

       			errd[i+1] = abs(errd[i+1]-D_fluido[i+1])/D_fluido[i+1]

			#Calculo de Temperatura de celda

			Re[i+1] = reynolds(V_fluido[i],T_fluido[i],Diam,D_fluido[i])
       			nu_ideal = nusselt2(Rem[i],a[2])

			numerito = cznusselt(i*2,Rem[i])

       			nu = numerito*nu_ideal
      			k_fluido[i] = conductividad(T_fluido[i])
       			h = nu*k_fluido[i]/Diam
       			error1[i] = T_celda[i]
       			T_celda[i] = q/(A_sup*h) + (T_fluido[i]+T_fluido[i+1])/2
       			error1[i] = abs(error1[i]-T_celda[i])/T_celda[i]
		
			#argregar errores a los arreglos

			errorp.append(max(errp))
    			errorv.append(max(errv))
    			errortf.append(max(errf))
    			errord.append(max(errd))
    			errortc.append(max(error1))

		# calcular potencia mecanica tras la iteracion

		Potencia_Mecanica = (P_fluido[0]-P_fluido[col_fluido-1])*Flow*0.00047
		
		#avanzar una iteracion

		k=k+1
	
	#obtener funciones objetivo

	ma = max(T_celda)

	#entregar resultado	

	return(ma,Potencia_Mecanica)


# Esta funcion es el algoritmo evolutivo combinado y adaptado para el modelo de Jorge Reyes

def modelojorgereyes(pop, popvel, num_var, objectives, iteraciones, limiteUp, limiteDown):

    counter = 0

    # leer los resultados de la modularizacion para cargarlos en el modelo

    # JEJE comentado para parametrizar bien
    f = open('resultadosmodularizacion.txt', 'r')
    mod_list = f.read().splitlines()
    f.close()

    n_fluido = int(mod_list[0]) + 1
    col_celda = int(mod_list[1])
    col_fluido = int(mod_list[1]) + 1

    max_repo_size = pop

    repo = []
    repoObj = []
    personalbest = pop
    personalbestObj = objectives
    numobj = 2

    I = 3

    # inicio del ciclo por iteraciones

    for j in range(int(iteraciones)):
        print "iteracion %d" % j
        print "repo: %d" % len(repo)
        # update velocity: Con la poblacion creada, el primer paso es
        # recalcular la velocidad de las partciculas

        if j > 0:

            w = 0.6
            r1 = random.random()
            r2 = random.random()

            if len(repo) > 1:
                h = random.randint(0, len(repo) - 1)
            else:
                h = 0
            for i in range(len(pop)):
                for j in range(num_var):
                    if len(repo) > 0:
                        popvel[i][j] = w * popvel[i][j] + r1 * \
                            (personalbest[i][j] - pop[i][j]) + \
                            r2 * (repo[h][j] - pop[i][j])
                    else:
                        popvel[i][j] = w * popvel[i][j] + r1 * \
                            (personalbest[i][j] - pop[i][j])

                    pop[i][j] = pop[i][j] + popvel[i][j]

                    if pop[i][j] > limiteUp[j]:
                        pop[i][j] = limiteUp[j]
                    elif pop[i][j] < limiteDown[j]:
                        pop[i][j] = limiteDown[j]

        # evaluate solution: Obtener valores de funciones objetivo

        for i in range(len(pop)):
            S = pop[i][0]
            Flow = pop[i][1]

            [T, PMec] = modelo(I, S, Flow, n_fluido, col_celda, col_fluido)

            Objetivo1 = T
            Objetivo2 = PMec

            objectives[i][0] = Objetivo1
            objectives[i][1] = Objetivo2

            f = open(workingDir2 + 'modelJor' + str(counter) + '.txt', 'w')
            f.write("" + "id:" + str(counter) + ", " + str(pop[i][0]) + ", " + "" + str(
                pop[i][1]) + "," + str(objectives[i][0]) + ", " + str(objectives[i][1]) + "\n")
            f.close()
            counter = counter + 1

        # non dominated search: Busqueda de soluciones no dominadas en la
        # poblacion y comparacion con anteriores que estan en el repositorio

        cuenta = []
        cuentaRepo = []

        for i in range(len(pop)):
            cuenta.append(0.0)

        for i in range(len(pop)):
            for j in range(len(pop)):

                out = False
                for k in range(numobj):
                    if i == j:
                        aa = 0
                    else:

                        if objectives[i][k] < objectives[j][k]:
                            out = False
                            break
                        elif objectives[i][k] > objectives[j][k]:
                            out = True

                if out == True:
                    cuenta[i] = cuenta[i] + 1

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

        for i in range(len(repo)):
            cuentaRepo.append(0.0)

        if len(repo) > 1:
            for i in range(len(repo)):
                for j in range(len(repo)):

                    outRepo = False
                    for k in range(numobj):
                        if i == j:
                            aa = 0
                        else:
                            if repoObj[i][k] < repoObj[j][k]:
                                out = False
                                break
                            elif repoObj[i][k] >= repoObj[j][k]:
                                out = True

                    if out == True:
                        cuentaRepo[i] = cuentaRepo[i] + 1

            for i in range(len(repo) - 1, -1, -1):
                if cuentaRepo[i] > 0:
                    del repo[i]
                    del repoObj[i]

        if len(repo) > max_repo_size:
            surviving_indices = [random.randint(0, len(repo) - 1) for _ in range(max_repo_size)]
            repo = [repo[i] for i in surviving_indices]
            repoObj = [repoObj[i] for i in surviving_indices]

        # update best: Actualizar la mejor solucion en el historial

        respaldo = personalbest
        respaldoobj = personalbestObj
        personalbest = []
        personalbestObj = []

        for i in range(len(pop)):
            out = False
            for k in range(numobj):
                if respaldoobj[i][k] < objectives[i][k]:
                    out = False
                    break
                elif respaldoobj[i][k] > objectives[i][k]:
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

    print "objetivos" +str(objectives)
    return repo, repoObj
	

def mopso(funcion_objetivo, pop, popvel, num_var, objectives, iteraciones, limiteUp, limiteDown):

    counter = 0

    max_repo_size = len(pop)

    repo = []
    repoObj = []
    personalbest = pop
    personalbestObj = objectives
    numobj = 2

    # inicio del ciclo por iteraciones

    for j in range(int(iteraciones)):
        print "iteracion %d" % j
        print "repo: %d" % len(repo)
        # update velocity: Con la poblacion creada, el primer paso es
        # recalcular la velocidad de las partciculas

        if j > 0:

            w = 0.6
            r1 = random.random()
            r2 = random.random()

            if len(repo) > 1:
                h = random.randint(0, len(repo) - 1)
            else:
                h = 0
            for i in range(len(pop)):
                for j in range(num_var):
                    if len(repo) > 0:
                        popvel[i][j] = w * popvel[i][j] + r1 * \
                            (personalbest[i][j] - pop[i][j]) + \
                            r2 * (repo[h][j] - pop[i][j])
                    else:
                        popvel[i][j] = w * popvel[i][j] + r1 * \
                            (personalbest[i][j] - pop[i][j])

                    pop[i][j] = pop[i][j] + popvel[i][j]

                    if pop[i][j] > limiteUp[j]:
                        pop[i][j] = limiteUp[j]
                    elif pop[i][j] < limiteDown[j]:
                        pop[i][j] = limiteDown[j]

        # evaluate solution: Obtener valores de funciones objetivo

        for i in range(len(pop)):
            S = pop[i][0]
            Flow = pop[i][1]

            [T, PMec] = funcion_objetivo(S, Flow)

            Objetivo1 = T
            Objetivo2 = PMec

            objectives[i][0] = Objetivo1
            objectives[i][1] = Objetivo2

            f = open(workingDir2 + 'modelJor' + str(counter) + '.txt', 'w')
            f.write("" + "id:" + str(counter) + ", " + str(pop[i][0]) + ", " + "" + str(
                pop[i][1]) + "," + str(objectives[i][0]) + ", " + str(objectives[i][1]) + "\n")
            f.close()
            counter = counter + 1

        # non dominated search: Busqueda de soluciones no dominadas en la
        # poblacion y comparacion con anteriores que estan en el repositorio

        cuenta = []
        cuentaRepo = []

        for i in range(len(pop)):
            cuenta.append(0.0)

        for i in range(len(pop)):
            for j in range(len(pop)):

                out = False
                for k in range(numobj):
                    if i == j:
                        aa = 0
                    else:

                        if objectives[i][k] < objectives[j][k]:
                            out = False
                            break
                        elif objectives[i][k] > objectives[j][k]:
                            out = True

                if out == True:
                    cuenta[i] = cuenta[i] + 1

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

        for i in range(len(repo)):
            cuentaRepo.append(0.0)

        if len(repo) > 1:
            for i in range(len(repo)):
                for j in range(len(repo)):

                    outRepo = False
                    for k in range(numobj):
                        if i == j:
                            aa = 0
                        else:
                            if repoObj[i][k] < repoObj[j][k]:
                                out = False
                                break
                            elif repoObj[i][k] >= repoObj[j][k]:
                                out = True

                    if out == True:
                        cuentaRepo[i] = cuentaRepo[i] + 1

            for i in range(len(repo) - 1, -1, -1):
                if cuentaRepo[i] > 0:
                    del repo[i]
                    del repoObj[i]

        if len(repo) > max_repo_size:
            surviving_indices = [random.randint(0, len(repo) - 1) for _ in range(max_repo_size)]
            repo = [repo[i] for i in surviving_indices]
            repoObj = [repoObj[i] for i in surviving_indices]

        # update best: Actualizar la mejor solucion en el historial

        respaldo = personalbest
        respaldoobj = personalbestObj
        personalbest = []
        personalbestObj = []

        for i in range(len(pop)):
            out = False
            for k in range(numobj):
                if respaldoobj[i][k] < objectives[i][k]:
                    out = False
                    break
                elif respaldoobj[i][k] > objectives[i][k]:
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

    print "objetivos" +str(objectives)
    return repo, repoObj


#CorrerModelo comunica el programa principal con los modelos.
# Crea la poblacion inicial
# Elige grilla o escalonado (y el modelo que corresponde)

def correrModelo(ventana,configuracion):
	v13v.withdraw()
	pop = []
	popvel = []
	objectives = []
	num_var = 2
	num_obj= 2
	vv13v1 = v13v1.get()
	vv13v2 = v13v2.get()
	s = []
	g = []



	file11 = list3.get(list3.curselection()[0])

	fin44 = open(file11 + ".txt", "r")
	fin_list44 = fin44.read().splitlines()
	fin44.close()

	tamVentana = float(fin_list44[0]) #tamano ventana
	maxFlujo = float(fin_list44[1]) #max Flujo

	f = open('resultadosmodularizacion.txt', 'r')
	mod_list = f.read().splitlines()
	f.close()
	n_fluido = int(mod_list[0]) + 1
	col_celda = int(mod_list[1])
	col_fluido = int(mod_list[1]) + 1

	file12 = list1.get(list1.curselection()[0])
	fin44 = open(file12 + ".txt", "r")
	fin_list44 = fin44.read().splitlines()
	fin44.close()

	Diam = float(fin_list44[7])/1000
	Largo = float(fin_list44[6])/1000
	I = float(fin_list44[1])
	Ah = float(fin_list44[2])

	resistencia_interna = 0.032          # Resistencia celda [Ohm] podria variarse por datasheet
	Tfluido_in = 273.15+20 

	T0celdas = 273.15+20
	dt = 1                             # Paso de simulacion [s]
	Voltaje=3.3 

	if configuracion == "escalonado":
		funcion_objetivo = lambda S, Flow: modelo(I, S, Flow, n_fluido, col_celda, col_fluido, Diam, Largo)
	if configuracion == "grilla":
		funcion_objetivo = lambda S, Flow: itemgetter(7, 11)((BancoTubosT_G("aire", Diam, col_celda, n_fluido, Largo, I, resistencia_interna, Tfluido_in, Flow, T0celdas, S, S, Ah, Voltaje, dt)))

	# Ajusta los limites de la poblacion para futuras iteraciones

	print maxFlujo * 2118.880003

	limiteUp = [1.312,  maxFlujo * 2118.880003]
	limiteDown = [1.05, 1.05]

	poblacion = vv13v1
	iteraciones = vv13v2
	 
	# creacion de la poblacion inicial

	for j in range(int(poblacion)):
		pop.append([random.random() * (limiteUp[i] - limiteDown[i]) + limiteDown[i] for i in range(num_var)])
		popvel.append([0, 0])

	for j in range(len(pop)):
		h = []
		for i in range(num_obj):
			h.append(None)
		objectives.append(h)

	[repoFin,repoObjFin] =  mopso(funcion_objetivo, pop, popvel, num_var, objectives, iteraciones, limiteUp, limiteDown)
	repoOX = []
	repoOY = []

	for i in range(len(repoObjFin)):
		repoOX.append(repoObjFin[i][0])
		repoOY.append(repoObjFin[i][1])

	P.plot(repoOX, repoOY,'bo')
	P.xlabel('Temperatura (C)')
	P.ylabel('Potencia Mecanica')
	P.title('Frente de Pareto')
	P.show()

	print "terminado"
	#print repoFin
	# print repoObjFin

	# Decision de usar KMEANS o no

	if kmeansindex == 0:	

		f = open('repoFinEtapa1.txt', 'w')
		for i in range(len(repoFin)):
			f.write(""+str(repoFin[i][0])+'\n')
			f.write(""+str(repoFin[i][1])+'\n')

		f.close()

	
		f = open('repoObjEtapa1.txt', 'w')
		for i in range(len(repoObjFin)):
			f.write(""+str(repoObjFin[i][0])+'\n')
			f.write(""+str(repoObjFin[i][1])+'\n')

		f.close()


	else:
		
	# numero de centros = 10
		
		puntitos = []

		for i in range(len(repoFin)):
			puntitos.append([repoFin[i][0],repoFin[i][1]])
			puntitos.extend(puntitos)
   		dots = np.array(puntitos)[:len(repoFin)]
			
		print 'puntitos' + str(puntitos)
		print 'dots' + str(dots)
		print 'repoFin' + str(repoFin)
		[Mu,clustersT] = find_centers(dots,10)

		f = open('repoFinEtapa1.txt', 'w')
		for i in range(len(Mu)):
			f.write(""+str(Mu[i][0])+'\n')
			f.write(""+str(Mu[i][1])+'\n')

		f.close()

		

	ejecutar(cerrar2(v13v))
	


#Funcion guardarv9 calcula la modularizacion y evalua disenos de ventiladores

def guardarv9(ventana):
	opcion = varRadio.get()
	eleccionVentilacion = varVentilacion.get()
	
	
	"""
	aa = poll()
	print "Aqui es donde se cae"
	print "asdfoajdsfajspdioj " + str(list1.curselection())
	v = ""+str(aa)
	import pdb;pdb.set_trace()
	"""
	
	aa = list1.curselection()[0]
	sel = list1.get(aa)
	print ""+sel

	fin5 = open("listaarchivos.txt","r")
	fin_list5 = fin5.read().splitlines()
	fin5.close()

	print "fin_list5" + str(len(fin_list5))
	
	file1 = fin_list5[0]
	
	for i in range(0,len(fin_list5)):
		if sel == fin_list5[i]:  #revisar
			file1 = fin_list5[i]
			break
	
	fin = open(file1, "r")
	fin_list6 = fin.read().splitlines()
	fin.close()
	
	
	if opcion == 1:
		altoMax = e661.get()
		
		altoCelda = float(fin_list6[7])
		i = 0 
		numeroCeldas = e1.get()

		print "altoMax:", altoMax
		print "altoCelda:", altoCelda
		print "numeroCeldas", numeroCeldas
						
		while float(i*altoCelda) < float(altoMax) and float(i) < float(numeroCeldas):
			i= i+1
		
		if i==0:
			mostrar(v6)

		else:
			# numeroCeldas= e1.get()
			# celdasRestantes = int(float(numeroCeldas)/i)

			anchoMax = e662.get()
			anchoCelda = float(fin_list6[6])
			j=0

			while float(j*anchoCelda) < float(anchoMax) and float(j) < float(float(numeroCeldas)):
				j = j+1

			if j==0:
				mostrar(v6)
			else:

				largoMax = e663.get()
				largoCelda = float(fin_list6[6])
				m=0

				while float(m*largoCelda) < float(anchoMax) and float(m) < float(float(numeroCeldas)):
					m = m+1

				if m==0:					
					mostrar(v6)

				else: 
					print "i:"+ str(i)
					print "j:" + str(j)
					print "m:" + str(m)

		maxX=i
		maxY=j
		maxZ=m

		aa = poll3()
		sel2 = list3.get(aa)
		print sel2

		# abre la lista de ventiladores y compara la seleccion con la lista para abrir el archivo de ventilador correcto

		fin6 = open("listaVentiladores.txt")
		fin_list6 = fin6.read().splitlines()
		fin6.close()

		file11 = fin_list6[0]
	
		#busca la celda elegida por el usuario en la libreria	

		for i in range(0,len(fin_list6)):
			if sel2 == fin_list6[i]:
				file11 = fin_list6[i] #revisar
				break

		file11 = file11 + '.txt'
		print file11
	
		fin44 = open(file11, "r")
		fin_list44 = fin44.read().splitlines()
		fin44.close()	

		tamVentana = fin_list44[0] #tamano ventana
		maxFlujo = fin_list44[1] #max Flujo


		numeroCeldas = float(e1.get())
		alternativas = []

		print "maxX" +str(maxX)
		print "maxY" +str(maxY)
		print "maxZ" + str(maxZ)

		for k in range(maxX):
			for l in range(maxY):
				for n in range(maxZ):
					if k*l*n == numeroCeldas:
						ab = [k,l,n]
						print "k" + str(k) + "  l"  + str(l) + "n  " + str(n)
						alternativas.append(ab)

		print "alternativas" + str(alternativas)

		diferencia = []
		if eleccionVentilacion == "x":
			for ii in range(len(alternativas)):
				# if tamVentana == 80 :
			
				dimensionX = alternativas[ii][0] * altoCelda
				kk = 0
				while float(tamVentana)*kk < dimensionX:
					kk = kk + 1
					
				diferencia.append(float(tamVentana)*kk - dimensionX)


		elif eleccionVentilacion == "y":
			for ii in range(len(alternativas)):
				# if tamVentana == 80 :
			
				dimensionX = alternativas[ii][1] * anchoCelda
				kk = 0
				while float(tamVentana)*kk < dimensionX:
					kk = kk + 1
					
				diferencia.append(float(tamVentana)*kk - dimensionX)

		else:
			for ii in range(len(alternativas)):


				# version antigua del codigo, sin leer los archivos. Cambia en TamVentana

				#if sel2 == "Thermaltake 80 mm" or sel2 == "PCF 80 mm":
				#	dimensionX = alternativas[ii][2] * largoCelda
				#	kk = 0
				#	while 80*kk < dimensionX:
				#		kk = kk + 1
					
				#	diferencia.append(80*kk - dimensionX)

				#else: 

				#	dimensionX = alternativas[ii][2] * largoCelda
				#	kk = 0
				#	while 120*kk < dimensionX:
				#		kk = kk + 1
					
				#	diferencia.append(120*kk - dimensionX)
				
				# if tamVentana == 80 :
			
				dimensionX = alternativas[ii][2] * largoCelda
				kk = 0
				while tamVentana*kk < dimensionX:
					kk = kk + 1
					
				diferencia.append(tamVentana*kk - dimensionX)

                if not diferencia:
                    tkMessageBox.showerror("Error de dimensionamiento", "El tipo de celda seleccionada excede las dimensiones del banco. Por favor volver al paso 1 y seleccionar otra celda.")
                    return
                                
		index1 = diferencia.index(min(diferencia))
		numeroVent = kk
		arregloEsc = alternativas[index1]

				
					
	else:
		altoMax = e662.get()
		altoCelda = float(fin_list6[7])	
		i = 0 
		numeroCeldas = e1.get()
						
		while float(i*altoCelda) < float(altoMax) and float(i) < float(numeroCeldas):
			i= i+1
		
		if i==0:
			mostrar(v6)

		else:
			# numeroCeldas= e1.get()
			# celdasRestantes = int(float(numeroCeldas)/i)

			anchoMax = e661.get()
			anchoCelda = float(fin_list6[6])
			j=0

			while float(j*anchoCelda) < float(anchoMax) and float(j) < float(float(numeroCeldas)):
				j = j+1

			if j==0:
				mostrar(v6)
			else:

				#numeroCeldas = e1.get()
				#celdasRestantes = int(float(numeroCeldas)/(i*j))
				
				largoMax = e663.get()
				largoCelda = float(fin_list6[6])
				m=0

				while float(m*largoCelda) < float(anchoMax) and float(m) < float(float(numeroCeldas)):
					m = m+1



				#largoMax = e663.get()
				#largoCelda = float(fin_list6[6])
					

				# if largoCelda*celdasRestantes > largoMax:
				if m==0:					
					mostrar(v6)

				else: 
					print "i:"+ str(i)
					print "j:" + str(j)
					print "m:" + str(m)
					
		maxX=i
		maxY=j
		maxZ=m

		aa = poll3()
		sel2 = list3.get(aa)
		numeroCeldas = float(e1.get())
		alternativas = []

		for k in range(maxX):
			for l in range(maxY):
				for n in range(maxZ):
					if k*l*n == numeroCeldas:
						ab = [k,l,n]
						alternativas.append(ab)

		print alternativas
	
		diferencia = []
		kk = 0
		
		if eleccionVentilacion == "x":
			for ii in range(len(alternativas)):
				if sel2 == "Thermaltake 80 mm" or sel2 == "PCF 80 mm":
					dimensionX = alternativas[ii][0] * altoCelda

					while 80*kk < dimensionX:
						kk = kk + 1
					
					diferencia.append(80*kk - dimensionX)

				else: 

					dimensionX = alternativas[ii][0] * altoCelda
					kk = 0
					while 120*kk < dimensionX:
						kk = kk + 1
					
					diferencia.append(120*kk - dimensionX)

		elif eleccionVentilacion == "y":
			for ii in range(len(alternativas)):
				if sel2 == "Thermaltake 80 mm" or sel2 == "PCF 80 mm":
					dimensionX = alternativas[ii][1] * anchoCelda
					kk = 0
					while 80*kk < dimensionX:
						kk = kk + 1
					
					diferencia.append(80*kk - dimensionX)

				else: 

					dimensionX = alternativas[ii][1] * anchoCelda
					kk = 0
					while 120*kk < dimensionX:
						kk = kk + 1
					
					diferencia.append(120*kk - dimensionX)

		else:
			for ii in range(len(alternativas)):
				if sel2 == "Thermaltake 80 mm" or sel2 == "PCF 80 mm":
					dimensionX = alternativas[ii][2] * largoCelda
					kk = 0
					while 80*kk < dimensionX:
						kk = kk + 1
					
					diferencia.append(80*kk - dimensionX)

				else: 

					dimensionX = alternativas[ii][2] * largoCelda
					
					while 120*kk < dimensionX:
						kk = kk + 1
					
					diferencia.append(120*kk - dimensionX)

	
                if not diferencia:
                    tkMessageBox.showerror("Error de dimensionamiento", "El tipo de celda seleccionada excede las dimensiones del banco. Por favor volver al paso 1 y seleccionar otra celda.")
                    return
                
		index1 = diferencia.index(min(diferencia))
		arregloEsc = alternativas[index1]
		numeroVent = kk

	
	print arregloEsc
	print numeroVent

	f = open('resultadosmodularizacion.txt', 'w')
	f.write(str(arregloEsc[0])+'\n')
	f.write(str(arregloEsc[1])+'\n') # OJO: si arregloEsc[1] == 1 la aplicación se cae en bancotubosT_G
	f.write(str(arregloEsc[2])+'\n')
	f.write(str(numeroVent)+'\n')
	f.close()

	global USER_SELECTED_MODULARIZATION
	USER_SELECTED_MODULARIZATION = True
		
							

#Funcion mostrarimagen para desplegar las imagenes de los bancos con la direccion de ventilacion

def mostrarimagen(string1):
	if string1 == "x":
		ejecutar(abrir(v10))
		varVentilacion.set("x")	
			
	elif string1 == "y":
		ejecutar(abrir(v11v))
		varVentilacion.set("y")
		
	else:
		ejecutar(abrir(v12v))
		varVentilacion.set("z")
	
	print varVentilacion.get()	

# funcion num para transformar strings a numeros

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)	

# funcion guardar celda para almacenar celdas en la biblioteca, ventana v16

def guardarcelda(v16):
	
	scelda00 = ecelda00.get()  #nombre celda
	scelda01 = ecelda01.get()  #voltaje
	scelda02 = ecelda02.get()  #corriente maxima
	scelda03 = ecelda03.get()  #capacidad
	scelda04 = ecelda04.get()  #peso
	scelda05 = ecelda05.get()  #volumen
	scelda06 = ecelda06.get()  #precio
	scelda07 = ecelda07.get()  #largo
	scelda08 = ecelda08.get()  #ancho

	nombrecelda = scelda00 + '.txt'
	f = open(nombrecelda, 'w')


	if RepresentsFloat(scelda01) and RepresentsFloat(scelda02) and RepresentsFloat(scelda03) and RepresentsFloat(scelda04) and RepresentsFloat(scelda05) and RepresentsFloat(scelda06) and RepresentsFloat(scelda07) and RepresentsFloat(scelda08):
		
		f.write(scelda01+'\n')
		f.write(scelda02+'\n')
		f.write(scelda03+'\n')
		f.write(scelda04+'\n')
		f.write(scelda05+'\n')
		f.write(scelda06+'\n')
		f.write(scelda07+'\n')
		f.write(scelda08+'\n')

		with open("listaarchivos.txt","r+") as ff:
		
			old = ff.read()
		
			ff.seek(0)
			stringaux = old + str(nombrecelda+'\n')
			ff.write(stringaux)
			ff.close()

		with open("listaCeldas.txt","r+") as ff:
		
			old = ff.read()
		
			ff.seek(0)
			stringaux = old + str(scelda00+'\n')
			ff.write(stringaux)
			ff.close()

		fin = open("listaCeldas.txt", "r")
		fin_list = fin.read().splitlines()
		fin.close()
	
		ListaNombre = []
		ListaNombre.append(fin_list[len(fin_list)-1])
		

		cargarlistbox(ListaNombre,list1)

		ocultar(v16)

	else:
		abrir(v17) #error de llenado de campos!

	f.close()  #celda guardada en archivo, ahora toca guardarla en la lista


# funcion guardarvent para guardar un nuevo ventilador 

def guardarvent(ventana):

	# ocultar(v18)
	svent00 = vent00.get()
	svent01 = vent01.get()
	svent02 = vent02.get()
	
	nombrevent = svent00 + '.txt'
	f = open(nombrevent, 'w')

	f.write(svent01+'\n')
	f.write(svent02+'\n')

	f.close()

	with open("listaVentiladores.txt","r+") as ff:
		
			old = ff.read()
		
			ff.seek(0)
			stringaux = old + str(svent00+'\n')
			ff.write(stringaux)
			ff.close()

	ListaNombre = []
	ListaNombre.append(svent00)
		
	cargarlistbox(ListaNombre,list3)

	ocultar(v18)


# programa seleccionar listbox para cargar archivo .eobli

def abrireobli0(ventana):
	
	abrir(v20)

def abrireobli1(ventana):

	nombrecaso = stringv20.get() + '.eobli'

	try:
		f = open(nombrecaso,'r')

	except IOError: 
		abrir(v21)
		# f = open('bpo.txt','r')


	listv20 = f.read().splitlines()
	f.close()

	v11.set(listv20[0]) #potencia
	v12.set(listv20[1]) #energia
	v13.set(listv20[2]) #voltaje

	bb11.set(listv20[3]) #celdas totales
	bb12.set(listv20[4]) #celdas serie 
	bb13.set(listv20[5]) #celdas paralelo
	bb14.set(listv20[6]) #voltaje
	bb15.set(listv20[7]) #potencia
	bb16.set(listv20[8]) #energia

	v55.set(listv20[9])  #peso
	v661.set(listv20[10]) #ancho
	v662.set(listv20[11]) #largo
	v663.set(listv20[12]) #alto
	v664.set(listv20[13]) #volumen
	v77.set(listv20[14]) #recursos

	celda = listv20[15]
	ventilador = listv20[16]
	configuracion = listv20[17]

	bb17.set(listv20[18]) #peso
	bb18.set(listv20[19]) #precio

	lista_list1 = list1.get(0,END)
	largo_list1 = len(lista_list1)

	
	for i in range(0,largo_list1):
		if celda == lista_list1[i]:
			list1.select_set(i) 
			break

	lista_list3 = list3.get(0,END)
	largo_list3 = len(lista_list3)
	
	
	for i in range(0,largo_list3):
		if ventilador == lista_list3[i]:
			list3.select_set(i) 
			break

	lista_list4 = list4.get(0,END)
	largo_list4 = len(lista_list4)
	
	for i in range(0,largo_list4):
		if configuracion == lista_list4[i]:
			list4.select_set(i) 
			break

	ocultar(v20)	
	print "archivo leido"


# captura todos los valores de entry y listbox, para guardarlos y asi poder cargarlos en otra sesion

def guardareobli0(ventana):

	abrir(v19)

def guardareobli1(ventana):

	string00 = v11.get() #potencia 
	string01 = v12.get() #energia
	string02 = v13.get() #voltaje
		
	string03 = bb11.get() #celdas totales
	string04 = bb12.get() #celdas serie 
	string05 = bb13.get() #celdas paralelo
	string06 = bb14.get() #voltaje
	string07 = bb15.get() #potencia
	string08 = bb16.get() #energia

	string09 = v55.get()  #peso
	string10 = v661.get() #ancho
	string11 = v662.get() #largo
	string12 = v663.get() #alto
	string13 = v664.get() #volumen
	string14 = v77.get() #recursos

	
	aux1= poll()
	sel01 = list1.get(aux1)
	string15 = sel01  #lista de celdas

	aux2 = poll3()
	sel02 = list3.get(aux2)
	string16 = sel02 #ventilador

	aux3 = poll4()
	sel03 = list4.get(aux3)
	string17 = sel03 #configuracion

	string18 = bb17.get() #peso
	string19 = bb18.get() #precio

	#escritura de archivo .eobli

	nombrecaso = stringv19.get() + '.eobli'

	f = open(nombrecaso, 'w')
	
	f.write(string00+'\n')
	f.write(string01+'\n')
	f.write(string02+'\n')
	f.write(string03+'\n')
	f.write(string04+'\n')
	f.write(string05+'\n')
	f.write(string06+'\n')
	f.write(string07+'\n')
	f.write(string08+'\n')
	f.write(string09+'\n')
	f.write(string10+'\n')
	f.write(string11+'\n')
	f.write(string12+'\n')
	f.write(string13+'\n')
	f.write(string14+'\n')
	f.write(string15+'\n')
	f.write(string16+'\n')
	f.write(string17+'\n')
	f.write(string18+'\n')
	f.write(string19+'\n')	


	f.close()

	ocultar(v19)
	
	

# inicializacion del programa y de cada una de las ventanas

configuracion = "escalonado"
ocultar(v2)
ocultar(v3)
scroll1=Scrollbar(v0)
list1=Listbox(v0)
list1.configure(exportselection=0) # JEJE
mitexto=StringVar()
textoSc=0

colocar_scrollbar(list1,scroll1)

#titulos de las ventanas

v0.title("Paso 1: Dimensionamiento del pack y selecccion de celda")
v1.title("Resultados")
v2.title("Etapa 2")
v4.title("Atencion!")
v5.title("Restricciones")
v6.title("Atencion!")
v7.title("Ingreso de curva de potencia")
v9.title("Modularizacion")
v10.title("Modularizacion")
v11v.title("Modularizacion")
v12v.title("Modularizacion")
v3.title("Resultados")
v8.title("Cargar desde archivo")
v13v.title("Configuracion Modelo")
v16.title("Carga de celda a directorio")
v17.title("Error")
v18.title("Carga de ventilador a directorio")
v19.title("Guardar archivo .eobli")
v20.title("Cargar archivo .eobli")
v21.title("Error")

#configuracion de la ventana v17: Error de carga de datos para celda
Label(v17,text="").grid(row=0,column=0)
Label(v17,text="").grid(row=0,column=1)
Label(v17,text="Los campos ingresados contienen errores, por favor revisar").grid(row=1,column=1)

Button(v17,text="Volver",command=lambda:ejecutar(ocultar(v17))).grid(row=3,column=1)



#configuracion de la ventana v18: Ingreso de un nuevo ventilador a la biblioteca

vent00 = StringVar() #nombre ventilador
vent01 = StringVar() #voltaje
vent02 = StringVar() #corriente maxima

Label(v18,text="").grid(row=0,column=0)
Label(v18,text="").grid(row=0,column=4)
Label(v18,text="").grid(row=1,column=4)
Label(v18,text="").grid(row=3,column=4)

Label(v18,text="Nombre Ventilador").grid(row=2,column=5)
Label(v18,text="Tamano Ventana").grid(row=3,column=5)
Label(v18,text="Flujo maximo").grid(row=4,column=5) 

event00 = Entry(v18,textvariable=vent00)
event00.grid(row=2,column=6)
event01 = Entry(v18,textvariable=vent01)
event01.grid(row=3,column=6)
event02= Entry(v18,textvariable=vent02)
event02.grid(row=4,column=6)

Label(v18,text="").grid(row=9,column=7)
Label(v18,text="").grid(row=10,column=7)

Button(v18,text="Guardar Ventilador",command=lambda:ejecutar(guardarvent(v18)), height = 1, width = 15).grid(row=9,column=8)
Button(v18,text="Ocultar",command=lambda:ejecutar(ocultar(v18)), height = 1, width = 15).grid(row=10,column=8)


#configuracion de la ventana v19: Ingreso de nombre para archivo .eobli

stringv19 = StringVar()

Label(v19,text="").grid(row=0,column=0)
Label(v19,text="Nombre archivo").grid(row=1,column=1)

nombrearchivo19 = Entry(v19,textvariable=stringv19)
nombrearchivo19.grid(row=1,column=2)

Button(v19,text="Guardar",command=lambda:ejecutar(guardareobli1(v19)), height = 1, width = 15).grid(row=1,column=3)
Button(v19,text="Volver",command=lambda:ejecutar(ocultar(v19)), height = 1, width = 15).grid(row=2,column=3)

#configuracion de la ventana v20: Ingreso de nombre para archivo .eobli

stringv20 = StringVar()

Label(v20,text="").grid(row=0,column=0)
Label(v20,text="Nombre archivo").grid(row=1,column=1)

nombrearchivo20 = Entry(v20,textvariable=stringv20)
nombrearchivo20.grid(row=1,column=2)

Button(v20,text="Abrir",command=lambda:ejecutar(abrireobli1(v20)), height = 1, width = 15).grid(row=1,column=3)
Button(v20,text="Volver",command=lambda:ejecutar(ocultar(v20)), height = 1, width = 15).grid(row=2,column=3)

#configuracion de la ventana v21: Error de archivo

Label(v21,text="").grid(row=0,column=0)
Label(v21,text="").grid(row=0,column=1)
Label(v21,text="Archivo no encontrado").grid(row=1,column=1)

Button(v21,text="Volver",command=lambda:ejecutar(ocultar(v21))).grid(row=3,column=1)



#configuracion de la ventana v16: Ingreso de celda nueva a la biblioteca

celda00 = StringVar() #nombre celda
celda01 = StringVar() #voltaje
celda02 = StringVar() #corriente maxima
celda03 = StringVar() #capacidad
celda04 = StringVar() #peso
celda05 = StringVar() #volumen
celda06 = StringVar() #precio
celda07 = StringVar() #largo
celda08 = StringVar() #ancho


Label(v16,text="").grid(row=0,column=0)
Label(v16,text="").grid(row=0,column=4)
Label(v16,text="").grid(row=1,column=4)
Label(v16,text="").grid(row=3,column=4)

Label(v16,text="Nombre Celda").grid(row=2,column=5)
Label(v16,text="Voltaje nominal").grid(row=3,column=5)
Label(v16,text="Corriente maxima").grid(row=4,column=5) 
Label(v16,text="Capacidad").grid(row=5,column=5)
Label(v16,text="Peso").grid(row=6,column=5)
Label(v16,text="Volumen").grid(row=7,column=5) 
Label(v16,text="Precio").grid(row=8,column=5)
Label(v16,text="Largo").grid(row=9,column=5)
Label(v16,text="Ancho").grid(row=10,column=5) 

ecelda00 = Entry(v16,textvariable=celda00)
ecelda00.grid(row=2,column=6)
ecelda01 = Entry(v16,textvariable=celda01)
ecelda01.grid(row=3,column=6)
ecelda02= Entry(v16,textvariable=celda02)
ecelda02.grid(row=4,column=6)
ecelda03 = Entry(v16,textvariable=celda03)
ecelda03.grid(row=5,column=6)
ecelda04 = Entry(v16,textvariable=celda04)
ecelda04.grid(row=6,column=6)
ecelda05= Entry(v16,textvariable=celda05)
ecelda05.grid(row=7,column=6)
ecelda06 = Entry(v16,textvariable=celda06)
ecelda06.grid(row=8,column=6)
ecelda07 = Entry(v16,textvariable=celda07)
ecelda07.grid(row=9,column=6)
ecelda08= Entry(v16,textvariable=celda08)
ecelda08.grid(row=10,column=6)

Label(v16,text="").grid(row=9,column=7)
Label(v16,text="").grid(row=10,column=7)

Button(v16,text="Guardar Celda",command=lambda:ejecutar(guardarcelda(v16)), height = 1, width = 15).grid(row=9,column=8)
Button(v16,text="Volver",command=lambda:ejecutar(ocultar(v16)), height = 1, width = 15).grid(row=10,column=8)


#configuracion de la ventana v7: Ingreso de curva de potencia

f711 = StringVar()
f712 = StringVar()

f811 = StringVar()
f812 = StringVar()
f813 = StringVar()
f814 = StringVar()
f815 = StringVar()
f816 = StringVar()
f817 = StringVar()
f818 = StringVar()

Label(v7,text="").grid(row=0,column=0)
Label(v7,text="Ingrese tiempo").grid(row=1,column=1)
Label(v7,text="Ingrese potencia (W)").grid(row=2,column=1)
Label(v7,text="").grid(row=2,column=2)
e711 = Entry(v7,textvariable=f711)
e711.grid(row=1,column=3)
e712 = Entry(v7,textvariable=f712)
e712.grid(row=2,column=3)
Button(v7,text="Guardar",command=lambda:ejecutar(guardar(v7)), height = 1, width = 15).grid(row=3,column=2)
Button(v7,text="Ocultar",command=lambda:ejecutar(ocultar(v7)), height = 1, width = 15).grid(row=6,column=2)
Button(v7,text="Graficar",command=lambda:ejecutar(graficar(arregloTiempo,arregloPotencia)), height = 1, width = 15).grid(row=4,column=2)
Button(v7,text="Borrar arreglo",command=lambda:ejecutar(borrar(v7)), height = 1, width = 15).grid(row=5,column=2)

Label(v7,text="").grid(row=1,column=4)
Button(v7,text="Cargar US06",command=lambda:ejecutar(us06(v7)), height = 1, width = 15).grid(row=1,column=5)
Button(v7,text="Cargar UDDS",command=lambda:ejecutar(udds(v7)), height = 1, width = 15).grid(row=2,column=5)
Button(v7,text="Cargar HWFET", command=lambda:ejecutar(hwfet(v7)), height = 1, width = 15).grid(row=3,column=5)
Button(v7,text="Cargar HUDDS",command=lambda:ejecutar(hudds(v7)), height = 1, width = 15).grid(row=4,column=5)
Button(v7,text="Cargar desde archivo",command=lambda:ejecutar(abrir(v8)), height = 1, width = 15).grid(row=5,column=5)

Label(v7,text="Parametros para modelo").grid(row=1,column=6)
Label(v7,text="Masa (m)").grid(row=2,column=6)
Label(v7,text="Cd").grid(row=3,column=6)
Label(v7,text="Rho_a").grid(row=4,column=6)
Label(v7,text="Area (A)").grid(row=5,column=6)
Label(v7,text="vw").grid(row=6,column=6)
Label(v7,text="coef_r1").grid(row=7,column=6)
Label(v7,text="coef_r2").grid(row=8,column=6)
Label(v7,text="Autonomia").grid(row=9,column=6)

Label(v7,text="Default: 2000 kg").grid(row=2,column=8)
Label(v7,text="Default: 0.15").grid(row=3,column=8)
Label(v7,text="Default: 1.2").grid(row=4,column=8)
Label(v7,text="Default: 2").grid(row=5,column=8)
Label(v7,text="Default: 0.5").grid(row=6,column=8)
Label(v7,text="Default: 1").grid(row=7,column=8)
Label(v7,text="Default: 1").grid(row=8,column=8)
Label(v7,text="Default: 164.5 km.").grid(row=9,column=8)

e811 = Entry(v7,textvariable=f811)
e811.grid(row=2,column=7)
e812 = Entry(v7,textvariable=f812)
e812.grid(row=3,column=7)
e813 = Entry(v7,textvariable=f813)
e813.grid(row=4,column=7)
e814 = Entry(v7,textvariable=f814)
e814.grid(row=5,column=7)
e815 = Entry(v7,textvariable=f815)
e815.grid(row=6,column=7)
e816 = Entry(v7,textvariable=f816)
e816.grid(row=7,column=7)
e817 = Entry(v7,textvariable=f817)
e817.grid(row=8,column=7)
e818 = Entry(v7,textvariable=f818)
e818.grid(row=9,column=7)


#configuracion de la ventana v5: Restricciones

# JEJE VERSION DEVELOPMENT DEFAULTS

v55 = StringVar()
v55.set("55000")
v661 = StringVar()
v661.set("80")
v662 = StringVar()
v662.set("30")
v663 = StringVar()
v663.set("80")
v664 = StringVar()
v77 = StringVar()
v77.set("8000")

Label(v5,text="").grid(row=0, column=0)
Label(v5,text=" ").grid(row=0,column=4)
Label(v5,text="Peso").grid(row=2,column=5)
e55 = Entry(v5,textvariable=v55)
e55.grid(row=2,column=6)
Label(v5,text="Ancho").grid(row=3,column=5)
e661 = Entry(v5,textvariable=v661)
e661.grid(row=3,column=6)
Label(v5,text="Largo").grid(row=4,column=5)
e662 = Entry(v5,textvariable=v662)
e662.grid(row=4,column=6)
Label(v5,text="Alto").grid(row=5,column=5)
e663 = Entry(v5,textvariable=v663)
e663.grid(row=5,column=6)
Label(v5,text="Volumen").grid(row=6,column=5)
e664 = Entry(v5,textvariable=v664)
e664.grid(row=6,column=6)
Label(v5,text="Recursos").grid(row=7,column=5)
e77 = Entry(v5,textvariable=v77)
e77.grid(row=7,column=6)

Label(v5,text="gramos").grid(row=2,column=7)
Label(v5,text="cm").grid(row=3,column=7)
Label(v5,text="cm").grid(row=4,column=7)
Label(v5,text="cm").grid(row=5,column=7)
Label(v5,text="cm3").grid(row=6,column=7)
Label(v5,text="dolares").grid(row=7,column=7)

Label(v5,text="").grid(row=5,column=7)
Button(v5,text="Ingresar datos",command=lambda:ejecutar(ingresar(v5)), height = 1, width = 15).grid(row=7,column=8)
Button(v5,text="Volver",command=lambda:ejecutar(ocultar(v5)), height = 1, width = 15).grid(row=8,column=8)

#configuracion de la ventana v4: advertencia de paso a simulacion


Label(v4,text="").grid(row=0,column=0)
Label(v4,text="").grid(row=0,column=1)
Label(v4,text="Esta seguro de que desea continuar? No pueden hacerse cambios de configuracion en el proximo paso").grid(row=1,column=1)

Button(v4,text="Continuar",command=lambda:ejecutar(cerrar(v4)), height = 1, width = 15).grid(row=2,column=1)
Button(v4,text="Volver",command=lambda:ejecutar(ocultar(v4)), height = 1, width = 15).grid(row=3,column=1)


#configuracion de la ventana v6: Deteccion de sobrepaso de restricciones

Label(v6,text="").grid(row=0,column=0)
Label(v6,text="").grid(row=0,column=1)
Label(v6,text="Su diseno excede las restricciones. Revisar!").grid(row=1,column=3)
Label(v6,text="").grid(row=2,column=3)




v101 = StringVar()
v102 = StringVar()
v103 = StringVar()
v104 = StringVar()
v105 = StringVar()
v106 = StringVar()


e101 = Entry(v6,textvariable=v101)
e101.grid(row=3,column=2)
e102 = Entry(v6,textvariable=v102)
e102.grid(row=3,column=4)
e103 = Entry(v6,textvariable=v103)
e103.grid(row=4,column=2)
e104 = Entry(v6,textvariable=v104)
e104.grid(row=4,column=4)
e105 = Entry(v6,textvariable=v105)
e105.grid(row=5,column=2)
e106 = Entry(v6,textvariable=v106)
e106.grid(row=5,column=4)
Label(v6,text="Peso obtenido").grid(row=3,column=1)
Label(v6,text="Volumen obtenido").grid(row=4,column=1)
Label(v6,text="Precio obtenido").grid(row=5,column=1)
Label(v6,text="Peso maximo").grid(row=3,column=3)
Label(v6,text="Volumen maximo").grid(row=4,column=3)
Label(v6,text="Precio maximo").grid(row=5,column=3)

Button(v6,text="Cerrar",command=lambda:ejecutar(ocultar(v6))).grid(row=6,column=3)


#configuracion de la ventana v2: Paso2 solucion de ventilacion, modularizacion

scroll3=Scrollbar(v2)
scroll4=Scrollbar(v2)
list3=Listbox(v2,exportselection=0)
list4=Listbox(v2,exportselection=0)
mitexto3=StringVar()
mitexto4=StringVar()
textoSc2=0

colocar_scrollbar(list3,scroll3)
colocar_scrollbar(list4,scroll4)

Label(v2,text="").grid(row=0, column=0)
list3.grid(row=2, column=1, rowspan=4, columnspan=1, sticky=N+E+S+W)
Label(v2,text= "          ").grid(row=2,column=2)
list4.grid(row=2,column=3, rowspan=4,columnspan=1, sticky =N+E+S+W)
scroll1.grid(row=2, column=3, rowspan=4, sticky=N+S)
label3=Label(v2,textvar=mitexto3)
label3.grid(row=7,column=1)
label4=Label(v2,textvar=mitexto4)
label4.grid(row=7,column=3)

b11 = StringVar()
b12 = StringVar()
b13 = StringVar()

Label(v2,text="            ").grid(row=7,column=4)
ss11 = b11.get()
ss12 = b12.get()
ss13 = b13.get()

Button(v2,text="Agregar Ventilador",command=lambda:ejecutar(abrir(v18)), height = 1, width = 15).grid(row=8,column=2)
Button(v2,text="Guardar",command=lambda:ejecutar(mostrar2(b11,b12,b13)), height = 1, width = 15).grid(row=9,column=2)
Button(v2,text="Modularizacion",command=lambda:ejecutar(abrir(v9)), height = 1, width = 15).grid(row=10,column=2)
Button(v2,text="Continuar",command=lambda:ejecutar(abrir(v3)), height = 1, width = 15).grid(row=11,column=2)
Button(v2,text="Cerrar",command=lambda:ejecutar(ocultar(v2)), height = 1, width = 15).grid(row=12,column=2)


# Button(v0,text="Reiniciar",command=lambda:ejecutar(reiniciar(v1))).grid(row=9,column=2)



#configuracion de la ventana v8: Cargar valores de la curva de potencia desde archivo


ve801 = StringVar()
ve802 = StringVar()


Label(v8,text="").grid(row=0,column=0)
Label(v8,text="Nombre de archivo de tiempo").grid(row=1,column=1)
Label(v8,text="Nombre de archivo de potencia").grid(row=2,column=1)
e801 = Entry(v8,textvariable=ve801)
e801.grid(row=1,column=3)
e802 = Entry(v8,textvariable=ve802)
e802.grid(row=2,column=3)
Button(v8,text="Cargar",command=lambda:ejecutar(cargarArchivos(ve801,ve802))).grid(row=3,column=2)
Button(v8,text="Salir",command=lambda:ejecutar(ocultar(v8))).grid(row=4,column=2)

# configuracion ventana v3: Resultados de la Etapa 2

Button(v3,text="Cerrar",command=lambda:ejecutar(ocultar(v3))).grid(row=6,column=2)

Label(v3,text=" ").grid(row=0,column=0)
Label(v3,text=" ").grid(row=1,column=1)
Label(v3,text=" ").grid(row=5,column=2)
Label(v3,text="Tipo de ventilador").grid(row=2,column=1)
Label(v3,text="Tipo de configuracion").grid(row=3,column=1)
Label(v3,text="Numero de celdas").grid(row=4,column=1)

ee0=Label(v3,textvar=mitexto3)
ee0.grid(row=2,column=3)
ee1 = Label(v3,textvar=mitexto4)
ee1.grid(row=3,column=3)
ee2 = Entry(v3)
ee2.grid(row=4,column=3)

# configuracion de la ventana v13v: Configuracion de iteraciones y poblacion para el modelo

Label(v13v,text=" ").grid(row=0,column=0)
Label(v13v,text="Uso del Modelo").grid(row=1,column=1)
Label(v13v,text="Ingresa tamano de poblacion").grid(row=2,column=1)
v13v1 = StringVar()
v13v2 = StringVar()
e11v = Entry(v13v,textvariable=v13v1)
e11v.grid(row=3,column=1)
Label(v13v,text=" ").grid(row=5,column=1)
e12v = Entry(v13v,textvariable=v13v2)
e12v.grid(row=6,column=1)
Label(v13v,text="Ingresa numero de iteraciones").grid(row=5,column=1)
Button(v13v,text="Volver",command=lambda:ejecutar(ocultar(v13v)), height = 1, width = 15).grid(row=8,column=1)
Button(v13v,text="Continuar",command=lambda:ejecutar(correrModelo(v13v,configuracion)), height = 1, width = 15).grid(row=7,column=1)
Label(v13v,text="Tener en cuenta: Cada simulacion con el modelo toma alrededor de 0,2 segundos").grid(row=9,column=1)

index1 = 0
numeroVent = 0 
arregloEsc = []

varVentilacion = StringVar()

#configuracion de locacion para escribir los archivos 

workingDir2 = "Resultados/"

#Configuracion ventana v9: Decision de direccion de ventilacion 
	
Label(v9,text="").grid(row=0,column=0)
Label(v9,text="Direccion de la ventilacion").grid(row=1,column=0)
Button(v9,text="Seleccionar ventilacion por X",command=lambda:ejecutar(mostrarimagen("x")),height=1,width=20).grid(row=2,column=0)
Button(v9,text="Seleccionar ventilacion por Y",command=lambda:ejecutar(mostrarimagen("y")),height=1,width=20).grid(row=3,column=0)
Button(v9,text="Seleccionar ventilacion por Z",command=lambda:ejecutar(mostrarimagen("z")),height=1,width=20).grid(row=4,column=0)
Label(v9,text="").grid(row=1,column=1)

Button(v9,text="Guardar",command=lambda:ejecutar(guardarv9(v9)), height = 1, width = 15).grid(row=5,column=1)
Button(v9,text="Cerrar",command=lambda:ejecutar(ocultar(v9)), height = 1, width = 15).grid(row=6,column=1)

varRadio = IntVar()

Label(v9,text="Orientacion de la celda").grid(row=1,column=2)
Radiobutton(v9, text="Horizontal", variable=varRadio, value=1,justify="left").grid(row=2,column=2)
Radiobutton(v9, text="Vertical", variable=varRadio, value=2,justify="left").grid(row=3,column=2)

# image1 = ImageTk.PhotoImage(Image.open(imageFile))
# 

# image1 = PIL.Image.open("paralelepipedo.png")
# tkpi = PIL.ImageTk.PhotoImage(image1)
# label_image = Label(v9, image=tkpi).grid(row=0,column=1)

image2 = PIL.Image.open("paralelepipedoX.png")
tkpi1 = PIL.ImageTk.PhotoImage(image2)
label_image = Label(v10, image=tkpi1).grid(row=0,column=1)
Button(v10,text="Cerrar",command=lambda:ejecutar(ocultar(v10))).grid(row=1,column=1)

image3 = PIL.Image.open("paralelepipedoY.png")
tkpi2 = PIL.ImageTk.PhotoImage(image3)
label_image = Label(v11v, image=tkpi2).grid(row=0,column=1)
Button(v11v,text="Cerrar",command=lambda:ejecutar(ocultar(v11v))).grid(row=1,column=1)

image4 = PIL.Image.open("paralelepipedoZ.png")
tkpi3 = PIL.ImageTk.PhotoImage(image4)
label_image = Label(v12v, image=tkpi3).grid(row=0,column=1)
Button(v12v,text="Cerrar",command=lambda:ejecutar(ocultar(v12v))).grid(row=1,column=1)

# label_image.place(x=0,y=0,width=image1.size[0],height=image1.size[1])

#Configuracion de la ventana v0, ventana inicial del programa, Dimensionamiento del Pack y seleccion de la celda


Button(v0,text="Guardar archivo Eobli",command=lambda:ejecutar(guardareobli0(v0)),height = 1, width = 20).grid(row=8,column=4)
Button(v0,text="Abrir archivo Eobli",command=lambda:ejecutar(abrireobli0(v0)),height = 1, width = 20).grid(row=9,column=4) 
Button(v0,text="Cargar celda",command=lambda:ejecutar(abrir(v16)),height = 1, width = 20).grid(row=10,column=4)
Button(v0,text="Ingresar restricciones",command=lambda:ejecutar(abrir(v5)),height = 1, width = 20).grid(row=11,column=4)
Button(v0,text="Ingresar curva de potencia",command=lambda:ejecutar(abrir(v7)),height = 1, width = 20).grid(row=12,column=4)
Button(v0,text="Construir",command=lambda:ejecutar(mostrar(v1,v11,v12,v13)),height = 1, width = 20).grid(row=13,column=4)
Button(v0,text="Reiniciar",command=lambda:ejecutar(reiniciar(v1)),height = 1, width = 20).grid(row=14,column=4)
Button(v0,text="Pasar a Etapa 2",command=lambda:ejecutar(abrir(v2)),height = 1, width = 20).grid(row=15,column=4)
Button(v0,text="Pasar a Etapa 3",command=lambda:ejecutar(abrir(v4)),height = 1, width = 20).grid(row=16,column=4) 

v11 = StringVar()
v12 = StringVar()
v13 = StringVar()

# VALORES DEFAULT CODIGO NUEVO DEVELOPER JEJE
v11.set("7500")
v12.set("7000")
v13.set("651")



e11 = Entry(v0,textvariable=v11)
e11.grid(row=2,column=6)
e12 = Entry(v0,textvariable=v12)
e12.grid(row=3,column=6)
e13= Entry(v0,textvariable=v13)
e13.grid(row=4,column=6)
Label(v0,text="            ").grid(row=7,column=4)
s11 = v11.get()
s12 = v12.get()
s13 = v13.get()

Label(v0,text="").grid(row=0, column=0)
Label(v0,text=" ").grid(row=0,column=4)
Label(v0,text="            ").grid(row=1, column=0)
Label(v0,text="            ").grid(row=1,column=4)
list1.grid(row=2, column=1, rowspan=4, columnspan=1, sticky=N+E+S+W)
scroll1.grid(row=2, column=3, rowspan=4, sticky=N+S)
Label(v0,text="            ").grid(row=3,column=4)
Label(v0,text="Potencia").grid(row=2,column=5)
label1=Label(v0,textvar=mitexto)
label1.grid(row=6,column=1)
Label(v0,text="Energia").grid(row=3,column=5)
Label(v0,text="Voltaje").grid(row=4,column=5)
Label(v0,text="Wh").grid(row=3,column=7)
Label(v0,text="W").grid(row=2,column=7)
Label(v0,text="Volt").grid(row=4,column=7)

#configuracion de la ventana v1: Ventana de resultados de la construccion del banco

Label(v1,text=" ").grid(row=0,column=0)
Label(v1,text=" ").grid(row=1,column=1)
Label(v1,text="Tipo de celda").grid(row=2,column=1)
Label(v1,text="Numero de celdas").grid(row=3,column=1)
Label(v1,text="Celdas en serie").grid(row=4,column=1)
Label(v1,text="Celdas en paralelo").grid(row=5,column=1)
Label(v1,text="Voltaje").grid(row=6,column=1)
Label(v1,text="Potencia").grid(row=7,column=1)
Label(v1,text="Energia").grid(row=8,column=1)
Label(v1,text="Peso").grid(row=9,column=1)
Label(v1,text="Precio").grid(row=10,column=1)

bb11 = StringVar()
bb12 = StringVar()
bb13 = StringVar()
bb14 = StringVar()
bb15 = StringVar()
bb16 = StringVar()
bb17 = StringVar()
bb18 = StringVar()

e0=Label(v1,textvar=mitexto)
e0.grid(row=2,column=3)
e1 = Entry(v1,textvar=bb11)
e1.grid(row=3,column=3)
e2 = Entry(v1,textvar=bb12)
e2.grid(row=4,column=3)
e2.insert(0,"50")
e3 = Entry(v1,textvar=bb13)
e3.grid(row=5,column=3)
e3.insert(0,"20")
Label(v1,text=" ").grid(row=9,column=1)
e4 = Entry(v1,textvar=bb14)
e4.grid(row=6,column=3)
e4.insert(0,"360")
e5 = Entry(v1,textvar=bb15)
e5.grid(row=7,column=3)
e5.insert(0,"4000")
e6 = Entry(v1,textvar=bb16)
e6.grid(row=8,column=3)
e6.insert(0,"5000")
e7 = Entry(v1,textvar=bb17)
e7.grid(row=9,column=3)
e7.insert(0,"1000")
e8 = Entry(v1,textvar=bb18)
e8.grid(row=10,column=3)
e8.insert(0,"1000")

Label(v1,text="celdas").grid(row=3,column=4)
Label(v1,text="celdas").grid(row=4,column=4)
Label(v1,text="celdas").grid(row=5,column=4)
Label(v1,text="Volt").grid(row=6,column=4)
Label(v1,text="W").grid(row=7,column=4)
Label(v1,text="Wh").grid(row=8,column=4)
Label(v1,text="g").grid(row=9,column=4)
Label(v1,text="$ USD").grid(row=10,column=4)



Button(v1,text="Cerrar",command=lambda:ejecutar(ocultar(v1))).grid(row=11,column=2)


# ListaNombres=['ICR 18650 3000 mAh','BC 26650 3800 mAh','ZX 18650 2800 mAh','SX 26650 3000 mAh','ZX 26650 4000 mAh','DJ 22650 3400 mAh','DJ 18650 1800 mAh']

# f = open('listaCeldas.txt', 'w')
# for i in range(0,len(ListaNombres)):
#	f.write(ListaNombres[i] + '\n')

# f.close()

fin = open("listaCeldas.txt", "r")
fin_list = fin.read().splitlines()
fin.close()

fin2 = open("listaVentiladores.txt", "r")
fin_list2 = fin2.read().splitlines()
fin2.close()

fin3 = open("listaDisposiciones.txt", "r")
fin_list3 = fin3.read().splitlines()
fin3.close()

ListaNombres=fin_list
ListaNombres2=fin_list2
ListaNombres3=fin_list3

# funciones para cargar las listas en las ventanas 

def cargarlistbox(lista,listbox):
    ind,largo=0,len(lista)
    while ind < largo:
        listbox.insert(END,lista[ind])
        ind+=1

# Imprimir en label se usa para grabar el resultado de una seleccion en la pantalla

def imprimir_en_label():

    label1.after(100, imprimir_en_label) # Llamada recursiva con .after
    ind3 = list3.curselection() # Acá se cae. Qué es list3???
    ind4 = list4.curselection()
    ind = list1.curselection()

    if list1.curselection() != ():	
	sel = list1.get(ind)
	mitexto.set(sel)

    if list3.curselection() != ():
        sel3 = list3.get(ind3)
        mitexto3.set(sel3)
     
    if list4.curselection() != ():
    	sel4 = list4.get(ind4)
        mitexto4.set(sel4)



# Poll se utiliza para revisar las listas y ver si el resultado ha cambiado

def poll():
	current = None
        now = list1.curselection()
        if now != current:
            aa = list_has_changed(now)
            current = now
        return aa

def poll3():
	current = None
        now = list3.curselection()
        if now != current:
            aa = list_has_changed(now)
            current = now
        return aa
    



def poll4():
	current = None
        now = list4.curselection()
        if now != current:
            aa = list_has_changed(now)
            current = now
        return aa

def list_has_changed(selection):
	return selection

	

cargarlistbox(ListaNombres,list1)
list1.select_set(0)
list1.event_generate("<<ListboxSelect>>")
cargarlistbox(ListaNombres2,list3)
list3.select_set(0)
list3.event_generate("<<ListboxSelect>>")
cargarlistbox(ListaNombres3,list4)
list4.select_set(0)
list4.event_generate("<<ListboxSelect>>")
imprimir_en_label()

#todas las ventanas parten escondidas y solo se abren cuando son llamadas
def nope():
	pass

v1.withdraw()
v1.protocol("WM_DELETE_WINDOW", nope)
v2.protocol("WM_DELETE_WINDOW", nope)
v4.withdraw()
v4.protocol("WM_DELETE_WINDOW", nope)
v5.withdraw()
v5.protocol("WM_DELETE_WINDOW", nope)
v6.withdraw()
v6.protocol("WM_DELETE_WINDOW", nope)
v7.withdraw()
v7.protocol("WM_DELETE_WINDOW", nope)
v8.withdraw()
v8.protocol("WM_DELETE_WINDOW", nope)
v9.withdraw()
v9.protocol("WM_DELETE_WINDOW", nope)
v10.withdraw()
v10.protocol("WM_DELETE_WINDOW", nope)
v11v.withdraw()
v11v.protocol("WM_DELETE_WINDOW", nope)
v12v.withdraw()
v12v.protocol("WM_DELETE_WINDOW", nope)
v13v.withdraw()
v13v.protocol("WM_DELETE_WINDOW", nope)
v14.withdraw()
v14.protocol("WM_DELETE_WINDOW", nope)
v15.withdraw()
v15.protocol("WM_DELETE_WINDOW", nope)
v16.withdraw()
v16.protocol("WM_DELETE_WINDOW", nope)
v17.withdraw()
v17.protocol("WM_DELETE_WINDOW", nope)
v18.withdraw()
v18.protocol("WM_DELETE_WINDOW", nope)
v19.withdraw()
v19.protocol("WM_DELETE_WINDOW", nope)
v20.withdraw()
v20.protocol("WM_DELETE_WINDOW", nope)
v21.withdraw()
v21.protocol("WM_DELETE_WINDOW", nope)


USER_SELECTED_MODULARIZATION = False
USER_HAS_CONSTRUCTED = False

v0.mainloop()
