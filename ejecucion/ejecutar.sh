#!/bin/bash
for i in 1 2 3 4 5 6 7 8 9
do
  python3.8 ./control.py meteo2021_08_0$i.txt
done

for i in 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
do
  python3.8 ./control.py meteo2021_08_$i.txt
done
for i in 1 2 3 4 5 6 7 8 9
do
  python3.8 ./control.py meteo2021_01_0$i.txt
done

for i in 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31
do
  python3.8 ./control.py meteo2021_01_$i.txt
done




