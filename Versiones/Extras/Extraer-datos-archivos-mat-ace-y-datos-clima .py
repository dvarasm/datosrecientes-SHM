from scipy.io import loadmat
import pandas as pd

def cargar_archivo_acelerometro(nombre):

    mat = loadmat(nombre) # carga del archivo
    mdata = mat['Data']
    columnas = [i for i in range(len(mdata[0]))] #indices de columnas 
    pdata = pd.DataFrame(mdata,columns=columnas) #transforma a dataframe de pandas

    t = pdata[0].tolist()

#Tiempo
    timestamp = []

    for i in range(len(t)):
        timestamp.append(str(t[i])[:4]+'-'+str(t[i])[4:6]+'-'+str(t[i])[6:8]+' '+str(t[i])[8:10]+':'+str(t[i])[10:12]+':'+str(t[i])[12:14])

    datos = pd.DataFrame({
                      'tipo_sensor': 'Acelerómetro',
                      'Marca de Tiempo': timestamp,
                      'Acelerometro 1': pdata[1].tolist(),
                      'Acelerometro 2': pdata[2].tolist(),
                      'Acelerometro 3': pdata[3].tolist(),
                      'Acelerometro 4': pdata[4].tolist(),
                      'Acelerometro 5': pdata[5].tolist(),
                      'Acelerometro 6': pdata[6].tolist(),
                      'Acelerometro 7': pdata[7].tolist(),
                      'Acelerometro 8': pdata[8].tolist(),
                      'Acelerometro 9': pdata[9].tolist(),
                      'Acelerometro 10': pdata[10].tolist(),
                      'Acelerometro 11': pdata[11].tolist(),
                      'Acelerometro 12': pdata[12].tolist(),
                      'Acelerometro 13': pdata[13].tolist(),
                      'Acelerometro 14': pdata[14].tolist(),
                      'Acelerometro biaxial 1': pdata[15].tolist(),
                      'Acelerometro biaxial 2': pdata[16].tolist()})
    return datos

def cargar_archivo_clima(nombre):
    pdata = pd.read_csv(nombre,sep="\t",skiprows=19)

    t = pdata.iloc[:,0].tolist()

    #Tiempo
    tiempo_com = []
    for i in range(len(t)):
        tiempo_com.append(str(t[i])[:4]+'-'+str(t[i])[4:6]+'-'+str(t[i])[6:8]+' '+str(t[i])[8:10]+':'+str(t[i])[10:12]+':'+str(t[i])[12:14])

    datos = pd.DataFrame({'Marca de Tiempo': tiempo_com,
                          'Velocidad del viento': pdata.iloc[:,1].tolist(),
                          'Direccion del viento': pdata.iloc[:,3].tolist(),
                          'Temperatura': pdata.iloc[:,5].tolist(),
                          'Humedad': pdata.iloc[:,7].tolist()})
    return datos
'''
for i in range(1,4): #por 6 horas
    df = cargar_archivo_acelerometro("d:/Datos Puente Chino/200803/03"+str(j)+"/d_08_3_"+str(j)+"_"+str(i)+".mat")
    df.drop_duplicates('Marca de Tiempo', keep="last", inplace=True)
    if (i == 1):
        df.to_csv("03"+str(j)+".csv", mode='w', header=True, index=False)
    else:
        df.to_csv("03"+str(j)+".csv", mode='a', header=False, index=False)


for j in range(19,32): #14 dias
    for i in range(1,25): #por 6 horas
        df = cargar_archivo_acelerometro("d:/Datos Puente Chino/200803/03"+str(j)+"/d_08_3_"+str(j)+"_"+str(i)+".mat")
        #df.drop_duplicates('Marca de Tiempo', keep="last", inplace=True)
        if (i == 1):
            df.to_csv("03"+str(j)+".csv", mode='w', header=True, index=False)
        else:
            df.to_csv("03"+str(j)+".csv", mode='a', header=False, index=False)
'''