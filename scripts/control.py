import csv

#Declaracion de variables

#Funcion lectura de datos
def leer_datos():
    global fecha
    with open('tmeteo2020_09_02.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fecha = str(row['fecha'])
            control_na(row['Elev.Sol1'])
     

def control_na(variable):
    busqueda = 'NaN'
    if (variable == busqueda ):
        print('Control Aplicado: Valor NaN encontrado en la fila con fecha ' + fecha)        



#Funcion main
def main():
    leer_datos()
    
main()