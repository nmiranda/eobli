#!/usr/bin/env python

import random
import numpy as np
import pylab as pl

random.seed(42)
workingDir2 = "Resultados/"


# Main del modelo de Jorge Reyes


# Funcion Cznusselt para calcular el Nusselt en funcion de una interpolacion

def cznusselt(i, Re):

    col = [1, 2, 3, 4, 5, 7, 10, 13, 16, 20]
    cz1 = [0.84, 0.88, 0.91, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1]
    cz2 = [0.64, 0.76, 0.84, 0.89, 0.92, 0.95, 0.97, 0.98, 0.99, 1]

    # print "Re"  + str(Re)
    if Re < 0:
        cz = 0
        return cz

    if i > 20:
        cz = 1
        return cz

    if Re < 1E3:
        cz = 1
        return cz

    if Re >= 1E3:
        cz = np.interp(i, col, cz2)
        return cz


# Funcion nusselt2 para estimar el Nusselt en base a interpolaciones

def nusselt2(re, a):
    Pr = 0.7
    Pr_w = 0.689

    if re <= 0:
        nu = 0
        return nu

    if re <= 1E2:
        c = 0.9
        m = a
        n = 0.37
        nu = c * np.power(re, m) * np.power(Pr, n) * \
            np.power((Pr / Pr_w), 0.25)
        return nu

    if re > 1E2 and re <= 1E3:
        c = 0.51
        m = a
        n = 0.37
        nu = c * np.power(re, m) * np.power(Pr, n) * \
            np.power((Pr / Pr_w), 0.25)
        return nu

    if re > 1E3 and re <= 2E5:
        c = 0.35
        m = a
        n = 0.37
        nu = c * np.power(re, m) * np.power(Pr, n) * \
            np.power((Pr / Pr_w), 0.25)
        return nu

    if re > 2E5:
        c = 0.023
        m = a
        n = 0.37
        nu = c * np.power(re, m) * np.power(Pr, n) * \
            np.power((Pr / Pr_w), 0.25)
        return nu


# Funcion cp para estimar la constante en funcion de una interpolacion

def cp(T):

    T = T + 273.15
    Datos = [1.006E3, 1.007E3, 1.009E3, 1.014E3, 1.021E3]
    Temp = [250, 300, 350, 400, 450]

    if T < 250:
        cp1 = np.interp(T, [Temp[0], Temp[1]], [Datos[0], Datos[1]])
        return cp1

    if T > 450:
        cp1 = np.interp(T, [Temp[3], Temp[4]], [Datos[3], Datos[4]])
        return cp1

    for i in range(len(Temp)):
        if T == Temp[i]:
            cp1 = Datos[i]
            return cp1

    for i in range(len(Temp) - 1):
        if T > Temp[i] and T < Temp[i + 1]:
            cp1 = np.interp(T, [Temp[i], Temp[i + 1]],
                            [Datos[i], Datos[i + 1]])
            return cp1

# Funcion ffriction para calcular el Factor de Friccion con interpolaciones


def ffriction(Re, S):
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

    if Re < 0:
        f = 0
        return f

    if S < coef[0][0]:
        aux1 = np.interp(S, [coef[0][0], coef[1][0]], [coef[0][1], coef[1][1]])
        aux2 = np.interp(S, [coef[0][0], coef[1][0]], [coef[0][2], coef[1][2]])
        f = aux1 * np.power(Re, aux2)
        return f

    if S > coef[3][0]:
        aux1 = np.interp(S, [coef[0][0], coef[1][0], coef[2][0], coef[3][0]], [
                         coef[0][1], coef[1][1], coef[2][1], coef[3][1]])
        aux2 = np.interp(S, [coef[0][0], coef[1][0], coef[2][0], coef[3][0]], [
                         coef[0][2], coef[1][2], coef[2][2], coef[3][2]])
        f = aux1 * np.power(Re, aux2)
        return f

    for i in range(4):
        if S == coef[i][0]:
            f = coef[i][1] * np.power(Re, coef[i][2])
            return f

    for i in range(3):
        if S > coef[i][0] and S < coef[i + 1][0]:
            aux1 = np.interp(S, [coef[i][0], coef[i + 1][0]],
                             [coef[i][1], coef[i + 1][1]])
            aux2 = np.interp(S, [coef[i][0], coef[i + 1][0]],
                             [coef[i][2], coef[i + 1][2]])
            f = aux1 * np.power(Re, aux2)
            return f


# Funcion Viscosidad para calcularla en funcion de una interpolacion

def viscosidad(T):
    T = T + 273.15
    # print T
    Datos = [159.6E-7, 184.6E-7, 208.2E-7, 230.1E-7, 250.7E-7]
    Temp = [250, 300, 350, 400, 450]

    if T < 250:
        visc = np.interp(T, [Temp[0], Temp[1]], [Datos[0], Datos[1]])
        return visc

    if T > 450:
        visc = np.interp(T, [Temp[3], Temp[4]], [Datos[3], Datos[4]])
        return visc

    for i in range(len(Temp)):
        if T == Temp[i]:
            visc = Datos[i]
            return visc

    for i in range(len(Temp) - 1):
        if T > Temp[i] and T < Temp[i + 1]:
            visc = np.interp(T, [Temp[i], Temp[i + 1]],
                             [Datos[i], Datos[i + 1]])
            return visc


# Funcion Reynolds para calcular el Numero de Reynolds a partir de la
# Viscosidad y otras variables

def reynolds(v, T, Diam, rho):
    visc = viscosidad(T)
    re = rho * v * Diam / visc
    return re


# Funcion cdr3

def cdr3(Re):
    if Re < 0:
        cd = -1
        return cd
    c = 3.3481
    n = -0.179
    cd = c * np.power(Re, -n)
    return cd


# Funcion conductividad, como interpolacion de la temperatura

def conductividad(T):

    T = T + 273.15
    Datos = [22.3E-3, 26.3E-3, 30E-3, 33.8E-3, 37.3E-3]
    Temp = [250, 300, 350, 400, 450]

    if T < 250:
        k = np.interp(T, [Temp[0], Temp[1]], [Datos[0], Datos[1]])
        return k

    elif T > 450:
        k = np.interp(T, [Temp[3], Temp[4]], [Datos[3], Datos[4]])
        return k
    else:
        for i in range(len(Temp)):
            if T == Temp[i]:
                k = Datos[i]
                return k

    for i in range(len(Temp) - 1):
        if T > Temp[i] and T < Temp[i + 1]:
            k = np.interp(T, [Temp[i], Temp[i + 1]], [Datos[i], Datos[i + 1]])
            return k



Largo = 6.5 / 1000.0
Diam = 1.8 / 1000.0

def modelo(I, S, Flow, n_fluido, col_celda, col_fluido):

    a = []

    for i in range(3):
        a.append(0)

    b1 = [0.039, 0.028, 0.027, 0.028, 0.005]
    b2 = [3.270, 2.416, 2.907, 2.974, 2.063]
    x = [0.1, 0.25, 0.5, 0.75, 1]

    if S < x[0]:
        a1 = np.interp(S, [x[1], x[2]], [b1[1], b1[2]])
        a2 = np.interp(S, [x[1], x[2]], [b2[1], b2[2]])
    elif S > x[4]:
        a1 = b1[4]
        a2 = b2[4]
    else:
        a1 = np.interp(S, x, b1)
        a2 = np.interp(S, x, b2)
        if a1 < 0:
            a1 = 0
        elif a2 < 0:
            a2 = 0
    a[0] = a1
    a[1] = a2
    a[2] = 0.653

    # definicion de variables necesarias para la operacion del modelo

    r = 0.032  # Resistencia interna [Ohm]
    Flujo = Flow * 0.00047  # Flujo de entrada del fluido [CFM]->[m3/s]
    # Diam = 0.018                   #Diametro de celdas [m] --- cambiar segun corresponda
    # Largo = 0.065                 #Largo de celdas [m]

    # abre el archivo donde se encuentra la libreria de celdas

    # aa = poll()
    # # print aa
    # v = "" + str(aa)
    # sel = list1.get(aa)

    # JEJE comentado para parametrizar
    # fin5 = open("listaCeldas.txt", "r")
    # fin_list5 = fin5.read().splitlines()
    # fin5.close()

    # file1 = fin_list5[0]

    # # busca la celda elegida por el usuario en la libreria

    # for i in range(0, len(fin_list5)):

    #     if sel == fin_list5[i]:
    #         file1 = fin_list5[i]  # revisar
    #         break

    # # print "file1   " +str(file1)

    # fin4 = open(file1 + ".txt", "r")
    # fin_list4 = fin4.read().splitlines()
    # fin4.close()

    # Diam = float(fin_list4[7]) / 1000
    # Largo = float(fin_list4[6]) / 1000

    vol = (np.power(Diam, 2) * np.pi / 4) * Largo  # Volumen celda [m3]
    e = 0.015  # Espaciado entre pared y celda [m]
    z = 0.005  # Corte del estudio [m]
    R = 286.9  # Constante de los gases aire [J/kgK]
    K = 1.4  # K del aire 1,4
    P_atm = 101325  # Presion atmosferica [Pa]
    Q_vol = np.power(I, 2) * r / vol  # Calor volumetrico
    q = Q_vol * (np.power(Diam, 2) * np.pi / 4) * z  # Calor total corte.
    A_sup = np.pi * Diam * z  # /2

    H = 2 * e + Diam * n_fluido + S * Diam * (n_fluido - 1)  # Altura del pack
    A = H * z  # Area de entrada pack
    A_vol = (S + 1) * Diam * z  # Area volumen control eje z
    A_ent = (S) * Diam * z  # Area entrada eje z

    T_fluido = []  # [C]
    P_fluido = []  # [Pa]
    V_fluido = []  # [m/s]
    Vm_fluido = []  # [m/s]
    D_fluido = []  # [kg/m3]
    T_celda = []  # [C]
    F_fluido = []  # N
    C = []  # [m/s]
    M = []  # Mach
    Ta = []  # [C]
    Da = []  # [kg/m3]
    Pa = []  # [Pa]
    Re = []  # Adimensional
    Rem = []  # adimensional
    k_fluido = []  # [W/(m*K)]

    # inicializacion de vectores

    for i in range(col_fluido):
        T_fluido.append(20)
        P_fluido.append(P_atm)
        V_fluido.append((Flujo * z / Largo) / A)
        Vm_fluido.append((Flujo * z / Largo) / A)
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

    # Errores

    error1 = []  # ERROR T CELDAS
    errf = []  # ERROR TFLUIDO
    errv = []  # ERROR VELOCIDAD
    errp = []  # ERROR PRESION
    errd = []  # ERROR DENSIDAD
    errmax = 1E-3  # ERROR CORTE

    for i in range(col_celda + 1):
        errf.append(1E1000)
        errv.append(1E1000)
        errd.append(1E1000)

    for i in range(col_celda):
        errp.append(1E1000)
        error1.append(1E1000)

    # Condiciones de Borde

    T_fluido[0] = 20  # Temperatura entrada [C]
    Vinicio = a[1] * Flujo * (z / Largo) / A  # Velocidad entrada[m/s]
    D_fluido[0] = 1.204  # Densidad de entrada [kg/m3]
    P_fluido[col_fluido - 1] = P_atm  # Presion entrada [Pa]

    Pa[0] = P_fluido[0] / ((1 + K) / (1 + K * np.power(M[0], 2)))
    Da[0] = Pa[0] / (R * Ta[0])

    D_fluido[0] = 1.204  # [kg/m3]
    m_punto = (S + 1) * Diam * z * Vinicio * D_fluido[0]  # [kg/s]
    errv[0] = 0
    errd[0] = 0
    errf[0] = 0

    for i in range(1, col_fluido):
        D_fluido[i] = D_fluido[0] - 0.204 * (i) / col_celda

    # print D_fluido

    #Ecuaciones - Ciclo

    k = 1

    errorp = []
    errorv = []
    errortf = []
    errord = []
    errortc = []

    # Ciclo principal del modelo de desarrollado por Jorge Reyes

    while (max(error1) > errmax) or (max(errf) > errmax) or (max(errp) > errmax) or (max(errv) > errmax) or (max(errd) > errmax):

        # while k<2:	Por si se quiere hacer un ciclo corto y de prueba

        # El primer valor del arreglo se calcula con formulas predefinidas

        cdrag = a[0] * cdr3(Rem[0])

        F_fluido[0] = 0.5 * Diam * z * D_fluido[0] * \
            np.power(Vinicio, 2) * cdrag

        errv[0] = V_fluido[0]

        if m_punto > 0:
            V_fluido[0] = Vinicio - F_fluido[0] / m_punto
        else:
            V_fluido[0] = 0

        if V_fluido[0] > 0:
            errv[0] = abs(errv[0] - V_fluido[0]) / V_fluido[0]
        else:
            errv[0] = 0

        C[0] = np.sqrt(K * R * (T_fluido[0] + 273.15))
        Vm_fluido[0] = (S / (S + 1)) * V_fluido[0]

        M[0] = V_fluido[0] / C[0]
        Ta[0] = T_fluido[0] / (((1 + K) * M[1]) /
                               np.power(np.power(1 + K * M[1], 2), 2))

        Rem[0] = reynolds(Vm_fluido[0], T_fluido[0], Diam, D_fluido[0])

        Re[0] = reynolds(V_fluido[0], T_fluido[0], Diam, D_fluido[0])

        errp[0] = P_fluido[0]
        P_fluido[0] = P_fluido[1] + 0.5 * 0.7 * \
            ffriction(Rem[0], S) * D_fluido[0] * np.power(Vm_fluido[0], 2)
        errp[0] = abs(P_fluido[0] - errp[0]) / P_fluido[0]

        Pa[0] = P_fluido[0] / ((1 + K) / (1 + K * np.power(M[1], 2)))
        Da[0] = Pa[0] / (R * Ta[0])

        D_fluido[0] = 1.204

        # ciclo para todas las columnas

        for i in range(col_fluido - 1):

            Vm_fluido[i] = (S / (S + 1)) * V_fluido[i]

            Rem[i + 1] = reynolds(Vm_fluido[i], T_fluido[i], Diam, D_fluido[i])

            # [m/s]
            C[i + 1] = np.power((K * R * (T_fluido[i + 1] + 273.15)), 0.5)
            M[i + 1] = V_fluido[i + 1] / C[i + 1]

            aux1 = 1 + K * np.power(M[i + 1], 2)
            aux2 = (1 + K) * M[i + 1]

            aux3 = aux2 / aux1

            aux3 = 1

            Ta[i + 1] = T_fluido[i + 1] / np.power(aux3, 2)

            errp[i] = P_fluido[i]

            P_fluido[i] = P_fluido[i + 1] + 0.5 * 0.7 * \
                ffriction(Rem[i], S) * D_fluido[i] * np.power(Vm_fluido[i], 2)
            errp[i] = abs(P_fluido[i] - errp[i]) / P_fluido[i]

            # Calculo de la velocidad

            flujo = V_fluido[i] * A_ent / 0.00047
            cdrag = a[0] * cdr3(Rem[i])

            numerito = np.power(V_fluido[i], 2) * cdrag
            F_fluido[i + 1] = 0.5 * Diam * z * D_fluido[i] * numerito

            errv[i + 1] = V_fluido[i + 1]

            aux4 = P_fluido[i + 1] - P_fluido[i]

            if m_punto > 0:
                V_fluido[i + 1] = (A_vol * (aux4) -
                                   F_fluido[i + 1]) / m_punto + V_fluido[i]
            else:
                V_fluido[i + 1] = 0

            # error de la velocidad

            if V_fluido[i + 1] > 0:
                errv[i + 1] = abs(V_fluido[i + 1] -
                                  errv[i + 1]) / V_fluido[i + 1]
            else:
                errv[i + 1] = 0

            # Calculo de la temperatura fluido
            errf[i + 1] = T_fluido[i + 1]
            aux1 = ((1 + 0 / S) * q / m_punto)
            aux2 = -0.5 * \
                (np.power(V_fluido[i + 1], 2) - np.power(V_fluido[i], 2))
            aux3 = cp(T_fluido[i])

            T_fluido[i + 1] = (aux1 + aux2) / aux3 + T_fluido[i]

            # error de la temperatura de fluido
            errf[i + 1] = abs(errf[i + 1] - T_fluido[i + 1]) / T_fluido[i + 1]

            # Calculo de la densidad
            Pa[i + 1] = P_fluido[i + 1] / \
                ((1 + K) / (1 + K * np.power(M[i + 1], 2)))
            Da[i + 1] = Pa[i + 1] / (R * Ta[i + 1])

            # error de la densidad

            errd[i + 1] = D_fluido[i + 1]
            D_fluido[i + 1] = D_fluido[i] + (Da[i + 1] - Da[i])

            errd[i + 1] = abs(errd[i + 1] - D_fluido[i + 1]) / D_fluido[i + 1]

            # Calculo de Temperatura de celda

            Re[i + 1] = reynolds(V_fluido[i], T_fluido[i], Diam, D_fluido[i])
            nu_ideal = nusselt2(Rem[i], a[2])

            numerito = cznusselt(i * 2, Rem[i])

            nu = numerito * nu_ideal
            k_fluido[i] = conductividad(T_fluido[i])
            h = nu * k_fluido[i] / Diam
            error1[i] = T_celda[i]
            T_celda[i] = q / (A_sup * h) + (T_fluido[i] + T_fluido[i + 1]) / 2
            error1[i] = abs(error1[i] - T_celda[i]) / T_celda[i]

            # argregar errores a los arreglos

            errorp.append(max(errp))
            errorv.append(max(errv))
            errortf.append(max(errf))
            errord.append(max(errd))
            errortc.append(max(error1))

        # calcular potencia mecanica tras la iteracion

        Potencia_Mecanica = (
            P_fluido[0] - P_fluido[col_fluido - 1]) * Flow * 0.00047

        # avanzar una iteracion

        k = k + 1

    # obtener funciones objetivo

    ma = max(T_celda)

    # entregar resultado

    return(ma, Potencia_Mecanica)

# Esta funcion es el algoritmo evolutivo combinado y adaptado para el
# modelo de Jorge Reyes

n_fluido = 45
col_celda = 4
col_fluido = 5


def modelojorgereyes(pop, popvel, num_var, objectives, iteraciones, limiteUp, limiteDown):

    counter = 0

    # leer los resultados de la modularizacion para cargarlos en el modelo

    # JEJE comentado para parametrizar bien
    # f = open('resultadosmodularizacion.txt', 'r')
    # mod_list = f.read().splitlines()
    # f.close()

    # n_fluido = int(mod_list[0]) + 1
    # col_celda = int(mod_list[1])
    # col_fluido = int(mod_list[1]) + 1

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

            # f = open(workingDir2 + 'modelJor' + str(counter) + '.txt', 'w')
            # f.write("" + "id:" + str(counter) + ", " + str(pop[i][0]) + ", " + "" + str(
            #     pop[i][1]) + "," + str(objectives[i][0]) + ", " + str(objectives[i][1]) + "\n")
            # f.close()
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

    return repo, repoObj


if __name__ == "__main__":
    poblacion = 40
    iteraciones = "200"
    max_repo_size = 200
    pop = []
    popvel = []
    objectives = []
    num_var = 2
    num_obj = 2
    limiteUp = [1.312, 40]
    limiteDown = [1.001, 1.05]


    for j in range(poblacion):
        pop.append([random.random() * (limiteUp[i] - limiteDown[i]) + limiteDown[i] for i in range(num_var)])
        popvel.append([0, 0])

    objectives = [[None for i in range(num_obj)] for j in range(len(pop))]

    [repoFin,repoObjFin] = modelojorgereyes(pop, popvel, num_var, objectives,
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