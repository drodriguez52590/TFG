import pandas as pd
import psycopg2

def normalizacion(txt):
    '''Función de normalización de los datos iniciales
    
    Realiza transformaciones de signos de puntuación
    y formato para el posterior correcto procesamiento de 
    los datos. Convierte el archivo inicial TXT en CSV normalizado. 

    Returns
    ----------
    archivo.csv : CSV normalizado

    '''
#Apertura de fichero
# Primera transformación    
    nombre = txt[:17]
    ies_input = open (txt,"rt")
    ies_output = open (nombre + "t.txt","wt")
    for line in ies_input:
        ies_output.write(line.replace('\t',';'))
#Segunda transformación
    ies_input = open (nombre + "t.txt","rt")
    ies_output = open (nombre + "tt.txt","wt")
    for line in ies_input:
        ies_output.write(line.replace('.',','))
 #Tercera transformación
    ies_output = open (nombre + "tt.txt","r")
    list_of_lines = ies_output.readlines()
#Restablecimiento de la cabezera del archivo (variables)
    list_of_lines[0]= "fecha;TempAi1;Bn;Gh;Dh;CelulaTop;CelulaMid;CelulaBot;TopCal;MidCal;BotCal;Presion;VVien1;DVien1;ElevSol1;OrientSol1;TempAi2;HumRel;Bn2;G41;Gn;Pirgeo;TempPirgeo;Auxil;VVien2;DVien2;Lluvia;Limpieza;ElevSol2;OrientSol2\n"
    ies_output = open (nombre + "tt.txt","w")
    ies_output.writelines(list_of_lines)
#Cierre de los archivos
    ies_input.close()
    ies_output.close()
#Transformación a formato CSV
    dataframe1 = pd.read_csv(nombre + "tt.txt", sep=";")
    dataframe1.to_csv(nombre + "tt.csv", index = None, sep=";")

    return nombre + "tt.csv"


def indexdatos_db(file,table):
    '''Función para indexar datos en la base de 
       datos PostgreSQL.
    
    Indexa de forma segura el contenido del archivo "file"
    en la tabla "table" de la base de datos PostgreSQL. 

    Parámetros
    ----------
    file : Archivo CSV a indexar
    table : Tabla de PostgreSQL donde se indexa
    
    Return
    ----------
    archivo.csv : CSV normalizado

    '''
#Conecta con PostgreSQL 
    connection = psycopg2.connect("host=172.17.0.1 port=5432 dbname=meteo user=danirr password=52590")
#Inicializa cursor de operaciones 
    cursor = connection.cursor()
#Abre archivo a indexar   
    with open(file, 'r') as f:
        next(f) # Omite fila de cabecera
        #Indexa en table
        cursor.copy_from(f, table, sep=';')
#Cierra la conexión de forma segura
    connection.commit()