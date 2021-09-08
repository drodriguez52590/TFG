
#++++++++++++++++++++++++++++++++++++++++++++++++++++
#+                                                  +
#+              Archivo: control.py                 +
#+                                                  +
#+       Fecha última modificación: 05/09/2021      +
#+                                                  +
#+          Autor: Daniel Rodríguez Ruiz            +
#+                                                  +
#++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+                            Descripción                             +
#+                                                                    +
#+       Script para el análisis y posterior control de  calidad      +
#+       de las variables meteorológicas medidas en el Instituto      +
#+       Energía Solar de la Universidad Politécnica de Madrid,       +
#+       desarrollado en lenguaje Python.                             +
#+                                                                    +
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#********************
# Módulos y librerías
#********************

import pandas as pd
import argparse
from datetime import datetime
import numpy as np
import json
import utils


#Variables globales gestión de Alertas

Variables_Afectadas_Alertas = ['Alerta01-1','Alerta01-2','Alerta02', 'Alerta03',
 'Alerta04', 'Alerta05','Alerta06','Alerta07']

Total_Casos_Alertas = ['Alerta01-1', 'Alerta01-2', 'Alerta02', 'Alerta03', 'Alerta04',
 'Alerta05','Alerta06','Alerta07']

#Variable global path ubicación directorio de ejecución del proyecto 
#Configurable por el usuario  
path = '/opt/proyecto52590/ejecucion/resultados_csv/'

#**********************
# Funciones de control
#**********************


def contenido_csv(datos):
    '''Función de control de pérdida de datos

    Comprueba si la dimensión de filas y de las columnas del archivo de datos 
    leído coincide con el valor esperado de 1440 filas y 30 columnas. 
    Corresponde a una fila por minuto (24h x 60min = 1440)
    
    Parámetros
    ----------
    datos :  Dataframe con los datos leídos.

    '''
#Inicialización de variables de alerta
    casos_Alerta011 = 0
    casos_Alerta012 = 0

#Lectura del número filas y columnas    
    filas = datos.shape[0]
    columnass = datos.shape[1]

#Comprobación con el valor de referencia
    if filas != 1440:
        casos_Alerta011 = 1
    if columnass != 30:
        casos_Alerta012 = 1

#Asignación de resultados en el sistema de alertas
    Variables_Afectadas_Alertas[0] = 0
    Variables_Afectadas_Alertas[1] = 0
    Total_Casos_Alertas[0] = casos_Alerta011
    Total_Casos_Alertas[1] = casos_Alerta012 
 



def control_na(datos):
    '''Función de control de valores NaN

    Comprueba si existen valores NaN en las mediciones de las variables
    indicadas en la lista Variables_NaN (Configuracion_control.json).
    
    Parámetros
    ----------
    datos : Dataframe con los datos leídos.

    '''
#Inicialización de variables de alerta
    variables_Alerta02 = 0
    casos_Alerta02 = 0

#Lectura del lista 'Variables_NaN' (Configuracion_control.json)
    with open('configuracion_control.json') as file:
        data = json.loads(file.read())
    Variables_NaN = (data[0]['Control_NaN'])

#Bucle de control    
    for i in Variables_NaN: 
        suma_filas_no_NA = (datos[i].count())
        if suma_filas_no_NA != datos.shape[0]:
            variables_Alerta02 += 1
            casos_Alerta02 += 1

#Asignación de resultados en el sistema de alertas  
    Variables_Afectadas_Alertas[2] = variables_Alerta02
    Total_Casos_Alertas[2] = casos_Alerta02



     
def control_rangos_limites_fisicos(datos):
    '''Función de control de valores fuera de rango de los límites
    físicos. 
 
    Analiza si existen valores que excedan el mínimo o el máximo de los 
    valores límite físicos de las variables de estudio.
    
    Parámetros
    ----------
    datos : Dataframe con los datos leídos.
    
    '''  

#Inicialización de variables de alerta
    variables_Alerta03 = 0
    casos_Alerta03 = 0

#Lectura del diccionario 'Control_Limites_Fisicos'(Configuracion_control.json)
    with open('configuracion_control.json') as file:
        data = json.load(file)
    for x in (data[3]['Control_Rangos_Limites']):

 #Comparación con valor de referencia máximo y filtrado de resultados       
        datos_mask = datos[x['Variable']]> float(x['Limite_fisico_max'])
        filtered_datos = datos[datos_mask]
        
        #Comprobar resultados encontrados
        if filtered_datos.shape[0] > 0:
            #Generar archivo CSV resultados    
            filtered_datos.to_csv(path + 'r_' + x['Variable'] + 
             '_rango_limite_fisico_max.csv', sep=';', na_rep=0 , index = False)

            #Indexar resultados en base de datos
            filename = "r_" +  str(x['Variable']) + "_rango_limite_fisico_max.csv"
            table = "r_" +  str(x['Variable']).lower() + "_rango_limite_fisico_max"
            utils.indexdatos_db(path + filename,table)

            #Asignación de errores encontrados
            variables_Alerta03 += 1
            Suma = filtered_datos.shape[0]
            casos_Alerta03 = Suma + casos_Alerta03

 #Comparación con valor de referencia mínimo y filtrado de resultados            
        datos_mask = datos[x['Variable']]< float(x['Limite_fisico_min'])
        filtered_datos = datos[datos_mask]
        
       #Comprobar resultados encontrados
        if filtered_datos.shape[0] > 0:
            #Generar archivo CSV resultados 
            filtered_datos.to_csv(path + 'r_' + x['Variable'] + 
             '_rango_limite_fisico_min.csv', sep=';',na_rep=0 , index = False)

            #Indexar resultados en base de datos
            filename = "r_" +  str(x['Variable']) + "_rango_limite_fisico_min.csv"
            table = "r_" +  str(x['Variable']).lower() + "_rango_limite_fisico_min"
            utils.indexdatos_db(path + filename,table)

            #Asignación de errores encontrados
            variables_Alerta03 += 1
            Suma = filtered_datos.shape[0]
            casos_Alerta03 = Suma + casos_Alerta03

#Asignación de resultados en el sistema de alertas
    Variables_Afectadas_Alertas[3] = variables_Alerta03
    Total_Casos_Alertas[3] = casos_Alerta03





def control_rangos_limites_esperados(datos):
    '''Función de control de  valores fuera de rango de los límites
    establecidos

    Analiza si existen valores que excedan el mínimo o el máximo de los 
    valores establecidos como valores límite esperados.
    
    Parámetros
    ----------
    datos : Dataframe con los datos leídos.
    
    '''  
 
 #Inicialización de variables de alerta
    variables_Alerta04 = 0
    casos_Alerta04 = 0
    
#Lectura del diccionario 'Control_Limites'(Configuracion_control.json)
    with open('configuracion_control.json') as file:
        data = json.load(file)
    for x in (data[3]['Control_Rangos_Limites']):

    #Comparación con valor de referencia máximo y filtrado de resultados   
        datos_mask = datos[x['Variable']]> float(x['Limite_esperado_max'])
        filtered_datos = datos[datos_mask]
        
       #Comprobar resultados encontrados
        if filtered_datos.shape[0] > 1:
            #Generar archivo CSV resultados 
            filtered_datos.to_csv(path +  'r_' + x['Variable'] + 
             '_rango_limite_max.csv', sep=';', na_rep=0 , index = False)
 
            #Indexar resultados en base de datos
            filename = "r_" + str(x['Variable']) + "_rango_limite_max.csv"
            table = "r_" + str(x['Variable']).lower() + "_rango_limite_max"
            utils.indexdatos_db(path + filename,table)

            #Asignación de errores encontrados
            variables_Alerta04 += 1
            Suma = filtered_datos.shape[0]
            casos_Alerta04 = Suma + casos_Alerta04

     #Comparación con valor de referencia mínimo y filtrado de resultados  
        datos_mask = datos[x['Variable']]< float(x['Limite_esperado_min'])
        filtered_datos = datos[datos_mask]
        
       #Comprobar resultados encontrados    
        if filtered_datos.shape[0] > 1:
            #Generar archivo CSV resultados 
            filtered_datos.to_csv(path + 'r_' + x['Variable'] +
             '_rango_limite_min.csv', sep=';',na_rep=0 , index = False)

            #Indexar resultados en base de datos
            filename = "r_" + str(x['Variable']) + "_rango_limite_min.csv"
            table = "r_" + str(x['Variable']).lower() + "_rango_limite_min"
            utils.indexdatos_db(path + filename,table)

            #Asignación de errores encontrados
            variables_Alerta04 += 1
            Suma = filtered_datos.shape[0]
            casos_Alerta04 = Suma + casos_Alerta04
#Asignación de resultados en el sistema de alertas
    Variables_Afectadas_Alertas[4] = variables_Alerta04
    Total_Casos_Alertas[4] = casos_Alerta04

    


def control_correlacion_variables(datos):
    '''Función de control de  variación entre variables redundantes.

    Analiza la diferencia en valor absoluto de los valores que toma la
    variable en ambos sensores y la compara con un valor de referencia
    
    Parámetros
    ----------
    datos : Dataframe con los datos leídos.
    
    ''' 
#Inicialización de variables de alerta y valor de referencia
    variables_Alerta05 = 0
    casos_Alerta05 = 0
    #Valor de referencia del control
    referencia_limite = 5
#Lectura del lista 'Control_Variables_Redundantes1' y
#'Control_Variables_Redundantes2' (Configuracion_control.json)
    with open('configuracion_control.json') as file:
        data = json.loads(file.read())
    Variables_Redundantes1 = (data[1]['Control_Variables_Redundantes1'])
    Variables_Redundantes2 = (data[2]['Control_Variables_Redundantes2'])
#Bucle de control
    for x,i in zip (Variables_Redundantes1, Variables_Redundantes2):
        #Cálculo de la diferencia
        diferencia = abs(datos[x] - datos[i])
        #Comparación de la diferencia con valor de referencia
        df_mask = diferencia > referencia_limite
        #Filtrado de datos
        filtered_df = diferencia[df_mask]
        #Comprobación de resultados
        if filtered_df.shape[0] > 0:
            #Asignación de errores encontrados
            variables_Alerta05 += 1
            Suma = filtered_df.shape[0]
            casos_Alerta05 = Suma + casos_Alerta05
#Asignación de resultados en el sistema de alertas           
    Variables_Afectadas_Alertas[5] = variables_Alerta05
    Total_Casos_Alertas[5] = casos_Alerta05




def control_mediamovil(datos):
    '''Función de control de cambios bruscos.

    Analiza la diferencia de medias móviles de las variables indicadas
    y la compara con un valor límite de referencia.

    Parámetros
    ----------
    datos :  Dataframe con los datos leídos.
    
    ''' 
#Inicialización de variables de alerta  
    variables_Alerta06 = 0
    casos_Alerta06 = 0
#Lectura del lista 'Control_MediaMovil' (Configuracion_control.json)
    with open('configuracion_control.json') as file:
        data = json.load(file)
#Bucle del control       
    for x in (data[4]['Control_MediaMovil']):
        #Cálculo de la diferencia entre medias móviles
        mediamovil = datos[x['Variable']].rolling(5).mean()
        resultado = mediamovil.diff().abs()
        #Comparación de la diferencia con valor límite de referencia 
        df_mask = resultado > float(x['Limite'])
        #Filtrado de datos
        filtered_df = resultado[df_mask]
        #Comprobación de resultados
        if filtered_df.shape[0] > 0:
            #Asignación de errores encontrados
            variables_Alerta06 += 1  
            Suma = filtered_df.shape[0]
            casos_Alerta06 = Suma + casos_Alerta06
#Asignación de resultados en el sistema de alertas           
    Variables_Afectadas_Alertas[6] = variables_Alerta06
    Total_Casos_Alertas[6] = casos_Alerta06
 



def control_irradiancia_teorica(datos):
    '''Función de control de cambios bruscos.

    Analiza la diferencia de medias móviles de las variables
    indicadas y la compara con un valor límite de referencia.

    Parámetros
    ----------
    datos : Dataframe con los datos leídos.
    
    ''' 
#Inicialización de variables de alerta   
    variables_Alerta07 = 0
    casos_Alerta07 = 0
 #Cálculo de la irradiancia teórica, cálculo de la diferencia 
 #entre valor teórico y valor experimental y cálculo del valor
 #de referencia  
    df_sin_nan = datos.dropna(how='any')
    gh_teorica = df_sin_nan['Dh'] + (df_sin_nan['Bn']*
    (np.cos((90 - df_sin_nan['ElevSol1'])*(np.pi/180))))
    diferencia = abs(df_sin_nan['Gh'] - gh_teorica)
    #Valor de tolerancia del control
    tolerancia = abs(0.5*df_sin_nan['Gh'])
#Filtrado de datos según los resultados
    df_mask = diferencia > tolerancia
    filtered_df = diferencia[df_mask]
    #Comprobación de resultados
    if filtered_df.shape[0] > 0:
        #Asignación de error
        casos_Alerta07 = filtered_df.shape[0]
        variables_Alerta07 = 1
#Asignación de resultados en el sistema de alertas 
    Total_Casos_Alertas[7] = casos_Alerta07   
    Variables_Afectadas_Alertas[7] = variables_Alerta07
    



def alertas():
    '''Función volcado de resultados en dataframe de alertas.

    Genera un dataframe con los resultados obtenidos en cada uno de
    los controles.

    Accede a las variables globales:
      Variables_Afectadas_Alertas
      Total_Casos_Alertas

    Return
    ----------
    alertas : Dataframe con las alertas generadas.   
    ''' 
#Creación dataframe alertas
    columnas = ['Fecha', 'Alerta','Descripcion', 'VariablesAfectadas',
     'TotaldeCasos']
    alertas = pd.DataFrame(columns=columnas)
 #Lectura del diccionario 'Alertas' (Configuracion_alertas.json)   
    with open('configuracion_alertas.json',encoding='utf-8') as file:
        alertasjson = json.load(file)
#Indexación de resultados en el dataframe
    for x,i,j in zip(alertasjson[0]['Alertas'], Variables_Afectadas_Alertas,
    Total_Casos_Alertas):    
        nueva_fila = { 'Fecha': datetime.today(), 'Alerta': x['Alerta'],
         'Descripcion' : x['Descripcion'], 'VariablesAfectadas' : i, 
         'TotaldeCasos': j}
        alertas = alertas.append(nueva_fila, ignore_index=True)
    #Salida por pantalla de las alertas
    print(alertas)

    return alertas


#***************
# Función main
#***************


def main():
    '''Función main o función principal

    Realiza las operaciones principales y llamadas 
    a las diferentes funciones. 

    '''
#Variable path ubicación resultados del proyecto 
#Configurable por el usuario   
    path = '/opt/proyecto52590/ejecucion/resultados_csv/'
# Archivo de datos como argumento de ejecución    
    parser = argparse.ArgumentParser()
    parser.add_argument('txt',type=str, help='Ruta del fichero TXT')
    args = parser.parse_args()
 #Llamada a la función de normalización del módulo 'utils'   
    csv_normalizado = utils.normalizacion(args.txt)
#Lectura de datos normalizados
    datos = pd.read_csv(csv_normalizado, sep=';', decimal=',', thousands='.',
     header=0, na_values=[''])
#Llamada a la función de indexdatos del módulo 'utils'
    datos.to_csv(path + 'datos.csv', sep=';',na_rep=0, index = False)
#Introducción de los datos normalizados en PostgreSQL
    utils.indexdatos_db(path + 'datos.csv','datos')
#Llamada a las funciones de control
    contenido_csv(datos) 
    control_na(datos)
    control_rangos_limites_fisicos(datos)
    control_rangos_limites_esperados(datos)
    control_correlacion_variables(datos)
    control_mediamovil(datos)
    control_irradiancia_teorica(datos)
#Llamada a la función alerta
    dfalertas = alertas()
#Creación de archivo CSV de alertas
    dfalertas.to_csv(path + 'resumen_alertas.csv', encoding='utf-8', sep=';',
     index = False)
#Introducción de alertas en PostqreSQL
    utils.indexdatos_db(path + 'resumen_alertas.csv','alertas')
    

#Ejecución del main
if __name__ == '__main__':
    main()
