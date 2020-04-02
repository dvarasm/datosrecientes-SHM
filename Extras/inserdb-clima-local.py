import psycopg2
import crearcsv as datos
from time import time

try:
    connection = psycopg2.connect(user="postgres",
                                  password="postgres",
                                  host="localhost",
                                  port="5432",
                                  database="puentes")
    cursor = connection.cursor()
    query = """ INSERT INTO public.clima(tipo_sensor, tiempo_medicion, vel_viento, dir_viento, 
            temperatura, humedad) VALUES (%s,%s,%s,%s,%s,%s)"""
    for i in range(0,24):
        start_time = time()
        print(' hora: '+str(i))
        if(i < 10):
            if(i < 5):
                df = datos.cargar_archivo_clima("/home/dvarasm/Datos Puente Chino/0401/en(0"+str(i)+"3803).txt")
                for k in range(len(df['Marca de Tiempo'])):
                    insert = ('Weather Station',df['Marca de Tiempo'][k],df['Velocidad del viento'][k],df['Direccion del viento'][k],df['Temperatura'][k],
                                    df['Humedad'][k])
                    cursor.execute(query, insert)
                    connection.commit()
            else:
                df = datos.cargar_archivo_clima("/home/dvarasm/Datos Puente Chino/0401/en(0"+str(i)+"3804).txt")
                for k in range(len(df['Marca de Tiempo'])):
                    insert = ('Weather Station',df['Marca de Tiempo'][k],df['Velocidad del viento'][k],df['Direccion del viento'][k],df['Temperatura'][k],
                                    df['Humedad'][k])
                    cursor.execute(query, insert)
                    connection.commit()
        else:
            if(i < 14):
                df = datos.cargar_archivo_clima("/home/dvarasm/Datos Puente Chino/0401/en("+str(i)+"3804).txt")
                for k in range(len(df['Marca de Tiempo'])):
                    insert = ('Weather Station',df['Marca de Tiempo'][k],df['Velocidad del viento'][k],df['Direccion del viento'][k],df['Temperatura'][k],
                                    df['Humedad'][k])
                    cursor.execute(query, insert)
                    connection.commit()
            else:
                df = datos.cargar_archivo_clima("/home/dvarasm/Datos Puente Chino/0401/en("+str(i)+"3806).txt")
                for k in range(len(df['Marca de Tiempo'])):
                    insert = ('Weather Station',df['Marca de Tiempo'][k],df['Velocidad del viento'][k],df['Direccion del viento'][k],df['Temperatura'][k],
                                    df['Humedad'][k])
                    cursor.execute(query, insert)
                    connection.commit()

        elapsed_time = time() - start_time
        print("Tiempo Transcurrido: %0.1f seconds." % elapsed_time)
        print ("Hora insertada en DB")
    

except (Exception, psycopg2.Error) as error :
    if(connection):
        print("Failed to insert record into mobile table", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")