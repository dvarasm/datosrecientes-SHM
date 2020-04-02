import psycopg2
import pandas as pd
from time import time
from sqlalchemy import create_engine
from scipy.io import loadmat


engine = create_engine('postgresql+psycopg2://qlhalplmkayixb:08c3ce3637d78695ab14e09427d7392181c78e92061de836782c1f966b4e3c6d@ec2-3-234-169-147.compute-1.amazonaws.com:5432/d2kgv5span6j91')

def cargar_archivo_acelerometro(nombre):

    mat = loadmat(nombre) # carga del archivo
    mdata = mat['Data']
    columnas = [hora for hora in range(len(mdata[0]))] #indices de columnas 
    pdata = pd.DataFrame(mdata,columns=columnas) #transforma a dataframe de pandas
    t = pdata[0].tolist()
    timestamp = []

    for hora in range(len(t)):
        timestamp.append(str(t[hora])[:4]+'-'+str(t[hora])[4:6]+'-'+str(t[hora])[6:8]+' '+str(t[hora])[8:10]+':'+str(t[hora])[10:12]+':'+str(t[hora])[12:14])

    datos = pd.DataFrame({
                      'tiempo_medicion': timestamp,
                      'acelerometro_1': pdata[1].tolist(),
                      'acelerometro_2': pdata[2].tolist(),
                      'acelerometro_3': pdata[3].tolist(),
                      'acelerometro_4': pdata[4].tolist(),
                      'acelerometro_5': pdata[5].tolist(),
                      'acelerometro_6': pdata[6].tolist(),
                      'acelerometro_7': pdata[7].tolist(),
                      'acelerometro_8': pdata[8].tolist(),
                      'acelerometro_9': pdata[9].tolist(),
                      'acelerometro_10': pdata[10].tolist(),
                      'acelerometro_11': pdata[11].tolist(),
                      'acelerometro_12': pdata[12].tolist(),
                      'acelerometro_13': pdata[13].tolist(),
                      'acelerometro_14': pdata[14].tolist(),
                      'acelerometro_bi_1': pdata[15].tolist(),
                      'acelerometro_bi_2': pdata[16].tolist()})
    datos['tiempo_medicion']  =  pd.to_datetime(datos['tiempo_medicion'])
    return datos

mes = ['01']#,'02','03']
dias_ene = list(range(1,2))#dia 15 hora 2 se alcanzo a insertar
dias_feb = list(range(1,5)) #4 9hr
dias_mar = list(range(18,32))
hora_fin = 0
hora_ini = 1

for mes in mes:
    print('mes: '+str(mes))
    if(mes == '01'):
        mesmes = dias_ene
    elif(mes == '02'):
        mesmes = dias_feb
    elif(mes == '03'):
        mesmes = dias_mar
    for dia in mesmes:
        print('dia: '+str(dia))
        if (dia == 13 and mes == '01'):
            hora_fin = 22
        elif (dia == 26 and mes == '03'):
            hora_fin = 22
        elif (int(dia) == 3 and str(mes) == '01'): 
            hora_fin = 24
        elif (dia ==14 and mes == '01'):
            hora_fin = 24
        elif (dia == 16 and mes == '01'):
            hora_fin = 24
        elif (dia == 3 and mes == '02'):
            hora_fin = 24
        elif (dia==27 and mes == '03'):
            hora_fin = 24
        elif (dia==29 and mes == '03'):
            hora_fin = 24
        elif(dia == 20 and mes == '01'):
            hora_fin = 17
        elif(dia == 29 and mes == '01'):
            hora_fin = 23
        elif(dia == 4 and mes == '02'):
            hora_fin = 10
        elif(dia == 18 and mes == '03'):
            hora_fin = 11
        elif(dia == 15 and mes == '01'):
            hora_ini = 3
            hora_fin = 25
        else:
            hora_fin = 25
        
        for hora in range(hora_ini,hora_fin):
            start_time = time()
            print('hora: '+str(hora))
            if(int(dia) < 10):
                print("/home/dvarasm/Datos Puente Chino/2008"+str(mes)+"/"+str(mes)+str(dia)+"/d_08_"+str(int(mes))+"_"+str(dia)+"_"+str(hora)+".mat")
                df = cargar_archivo_acelerometro("/home/dvarasm/Datos Puente Chino/2008"+str(mes)+"/"+str(mes)+"0"+str(dia)+"/d_08_"+str(int(mes))+"_"+str(dia)+"_"+str(hora)+".mat")
            else:
                print("/home/dvarasm/Datos Puente Chino/2008"+str(mes)+"/"+str(mes)+str(dia)+"/d_08_"+str(int(mes))+"_"+str(dia)+"_"+str(hora)+".mat")
                df = cargar_archivo_acelerometro("/home/dvarasm/Datos Puente Chino/2008"+str(mes)+"/"+str(mes)+str(dia)+"/d_08_"+str(int(mes))+"_"+str(dia)+"_"+str(hora)+".mat")
            
            tiempo_medicion = df['tiempo_medicion'].tolist()
            print('df creado')
            if dia == 15 and hora == 3:
                inicio = 5
            else:
                inicio = 1

            for i in range(inicio,3):
                nombre = 'Acelerómetro '+str(i)
                ace = 'acelerometro_'+str(i)
                medicion = df[ace].tolist()
                new_df = pd.DataFrame({
                    'tiempo_medicion' : tiempo_medicion,
                    'medicion' : medicion
                })
                #print(new_df)
                print('insertando en db')
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
                    'nombre_sensor' : nombre,
                    'fecha' : fecha,
                    'lectura' : lectura
                })
                print(dff)
                dff.to_csv (r''+str(ace)+'_'+str(hora)+'.csv', index = False, header=True)
                #new_df.to_sql(ace, engine, if_exists='append', index = False)
                print('datos insertados en db')
            elapsed_time = time() - start_time
            print("Tiempo Transcurrido: %0.1f seconds." % elapsed_time)
            print ("Hora insertada en DB")