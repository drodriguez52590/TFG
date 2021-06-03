import psycopg2

conn = psycopg2.connect("host=172.17.0.1 port=5432 dbname=meteo user=danirr password=52590")
cur = conn.cursor()
cur.execute("""
    CREATE TABLE meteoprueba(
    fecha timestamp PRIMARY KEY,
    TempAi1 numeric,
    Bn numeric,
    Gh numeric,
    Dh numeric,
    CelulaTop numeric,
    CelulaMid numeric,
    CelulaBot numeric,
    TopCal numeric,
    MidCal numeric,
    BotCal numeric,
    Presion numeric,
    VVien1 numeric,
    DVien1 numeric,
    ElevSol1 numeric,
    OrientSol1 numeric,
    TempAi2 numeric,
    HumRel numeric,
    Bn2 numeric,
    G41 numeric,
    Gn numeric,
    Pirgeo numeric,
    TemPirgeo numeric,
    Auxil numeric,
    VVien2 numeric,
    DVien2 numeric,
    Lluvia numeric,
    Limpieza numeric,
    ElevSol2 numeric,
    OrientSol2 numeric,
""")
conn.commit()
