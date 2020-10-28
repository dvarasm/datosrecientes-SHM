import psycopg2
from time import time
from sqlalchemy import create_engine
from scipy.io import loadmat
import pandas as pd

engine = create_engine('postgresql+psycopg2://qlhalplmkayixb:08c3ce3637d78695ab14e09427d7392181c78e92061de836782c1f966b4e3c6d@ec2-3-234-169-147.compute-1.amazonaws.com:5432/d2kgv5span6j91')
#engine = create_engine('postgresql+psycopg2://postgres:ferrari1@localhost:5432/shm_puentes')
def cargar_archivo_clima(nombre):
    pdata = pd.read_csv(nombre,sep="\t",skiprows=19)

    t = pdata.iloc[:,0].tolist()

    #Tiempo
    tiempo_com = []
    for i in range(len(t)):
        tiempo_com.append(str(t[i])[:4]+'-'+str(t[i])[4:6]+'-'+str(t[i])[6:8]+' '+str(t[i])[8:10]+':'+str(t[i])[10:12]+':'+str(t[i])[12:14])

    datos = pd.DataFrame({'tiempo_medicion': tiempo_com,
                          'vel_viento': pdata.iloc[:,1].tolist(),
                          'dir_viento': pdata.iloc[:,3].tolist(),
                          'temperatura': pdata.iloc[:,5].tolist(),
                          'humedad': pdata.iloc[:,7].tolist()})
    return datos
sensor = ['Velocidad del viento','Dirección del viento','Temperatura','Humedad']
tabla = ['vel_viento','dir_viento','temperatura','humedad']

for i in range(0,24):
    start_time = time()
    print(' hora: '+str(i))
    if(i < 10):
        if(i < 5):
            df = cargar_archivo_clima("/home/dvarasm/Datos Puente Chino/0401/en(0"+str(i)+"3803).txt")
            for k,j in zip(sensor,tabla):
                medicion = df[j].tolist()
                tiempo_medicion = df['tiempo_medicion'].tolist()
                new_df = pd.DataFrame({
                    'tiempo_medicion' : tiempo_medicion,
                    'medicion' : medicion
                })
                new_dff = new_df.groupby("tiempo_medicion").mean()
                fecha = []
                lectura = []
                for index, row in new_dff.iterrows():
                    #print(index, row['medicion'])
                    fecha.append(index)
                    lectura.append(row['medicion'])
                print(new_dff)
                print(new_dff.keys())
                dff = pd.DataFrame({
                    'nombre_sensor' : k,
                    'fecha' : fecha,
                    'lectura' : lectura
                })
                print(dff)
                dff.to_csv (r''+str(j)+'_'+str(i)+'.csv', index = False, header=True)
                #new_df.to_sql(j, engine, if_exists='append', index = False)
        else:
            df = cargar_archivo_clima("/home/dvarasm/Datos Puente Chino/0401/en(0"+str(i)+"3804).txt")
            for k,j in zip(sensor,tabla):
                medicion = df[j].tolist()
                tiempo_medicion = df['tiempo_medicion'].tolist()
                new_df = pd.DataFrame({
                    'nombre_sensor' : k,
                    'tiempo_medicion' : tiempo_medicion,
                    'medicion' : medicion
                })
                new_dff = new_df.groupby("tiempo_medicion").mean()
                fecha = []
                lectura = []
                for index, row in new_dff.iterrows():
                    #print(index, row['medicion'])
                    fecha.append(index)
                    lectura.append(row['medicion'])
                print(new_dff)
                print(new_dff.keys())
                dff = pd.DataFrame({
                    'nombre_sensor' : k,
                    'fecha' : fecha,
                    'lectura' : lectura
                })
                print(dff)
                dff.to_csv (r''+str(j)+'_'+str(i)+'.csv', index = False, header=True)
                #new_df.to_sql(j, engine, if_exists='append', index = False)
    else:
        if(i < 14):
            df = cargar_archivo_clima("/home/dvarasm/Datos Puente Chino/0401/en("+str(i)+"3804).txt")
            for k,j in zip(sensor,tabla):
                medicion = df[j].tolist()
                tiempo_medicion = df['tiempo_medicion'].tolist()
                new_df = pd.DataFrame({
                    'nombre_sensor' : k,
                    'tiempo_medicion' : tiempo_medicion,
                    'medicion' : medicion
                })
                new_dff = new_df.groupby("tiempo_medicion").mean()
                fecha = []
                lectura = []
                for index, row in new_dff.iterrows():
                    #print(index, row['medicion'])
                    fecha.append(index)
                    lectura.append(row['medicion'])
                print(new_dff)
                print(new_dff.keys())
                dff = pd.DataFrame({
                    'nombre_sensor' : k,
                    'fecha' : fecha,
                    'lectura' : lectura
                })
                print(dff)
                dff.to_csv (r''+str(j)+'_'+str(i)+'.csv', index = False, header=True)
                #new_df.to_sql(j, engine, if_exists='append', index = False)
        else:
            df = cargar_archivo_clima("/home/dvarasm/Datos Puente Chino/0401/en("+str(i)+"3806).txt")
            for k,j in zip(sensor,tabla):
                medicion = df[j].tolist()
                tiempo_medicion = df['tiempo_medicion'].tolist()
                new_df = pd.DataFrame({
                    'nombre_sensor' : k,
                    'tiempo_medicion' : tiempo_medicion,
                    'medicion' : medicion
                })
                new_dff = new_df.groupby("tiempo_medicion").mean()
                fecha = []
                lectura = []
                for index, row in new_dff.iterrows():
                    #print(index, row['medicion'])
                    fecha.append(index)
                    lectura.append(row['medicion'])
                print(new_dff)
                print(new_dff.keys())
                dff = pd.DataFrame({
                    'nombre_sensor' : k,
                    'fecha' : fecha,
                    'lectura' : lectura
                })
                print(dff)
                dff.to_csv (r''+str(j)+'_'+str(i)+'.csv', index = False, header=True)
                #new_df.to_sql(j, engine, if_exists='append', index = False)

        elapsed_time = time() - start_time
        print("Tiempo Transcurrido: %0.1f seconds." % elapsed_time)
        print ("Hora insertada en DB")