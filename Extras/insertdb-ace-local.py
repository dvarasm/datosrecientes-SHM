import psycopg2
import pandas as pd
from time import time
from sqlalchemy import create_engine
from scipy.io import loadmat


engine = create_engine('postgresql+psycopg2://postgres:ferrari1@localhost:5432/puentes')

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
                      'tipo_sensor': 'Acelerómetro',
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
dias_ene = list(range(1,17))
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
            df.to_sql('acelerometros', engine, if_exists='append', index = False)
            elapsed_time = time() - start_time
            print("Tiempo Transcurrido: %0.1f seconds." % elapsed_time)
            print ("Hora insertada en DB")