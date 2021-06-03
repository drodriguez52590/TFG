import pandas as pd
#import csv

ies_input = open ("meteo2020_09_02.txt","rt")
ies_output = open ("tmeteo2020_09_02.txt","wt")

for line in ies_input:
    ies_output.write(line.replace('\t',';'))
 
ies_output = open ("tmeteo2020_09_02.txt","r")
list_of_lines = ies_output.readlines()
#Establecemos cabezera (variables)
list_of_lines[0]= "fecha;Temp.Ai1;Bn;Gh;Dh;CelulaTop;CelulaMid;CelulaBot;TopCal;MidCal;BotCal;Presion;V.Vien.1;D.Vien.1;Elev.Sol1;Orient.Sol1;Temp.Ai2;Hum.Rel;Bn2;G(41);Gn;Pirgeo;TemPirgeo;Auxil;V.Vient.2;D.Vient.2;Lluvia;Limpieza;Elev.Sol2;Orient.Sol2\n"
ies_output = open ("tmeteo2020_09_02.txt","w")
ies_output.writelines(list_of_lines)


ies_input.close()
ies_output.close()

#txt to csv
dataframe1 = pd.read_csv("tmeteo2020_09_02.txt")
  
# storing this dataframe in a csv file
dataframe1.to_csv('tmeteo2020_09_03.csv', 
                  index = None)
