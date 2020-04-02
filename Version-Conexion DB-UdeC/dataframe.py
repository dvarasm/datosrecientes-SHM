import pandas as pd
import numpy as np
import psycopg2
import time
import pdfkit
import webbrowser
import base64
import collections
import unicodedata
import plotly
import plotly.graph_objects as go
from datetime import datetime as dt
from datetime import timedelta as td

# Contiene las credenciales para realizar la conección con postgresql
#coneccion = psycopg2.connect(user="postgres",password="ferrari1",host="localhost",port="5432",database="shm_puentes")

coneccion = psycopg2.connect(user="clandero",password="219UNIx2",host="152.74.52.187",port="5432",database="prototipo_shm")
esquema = ['public.','inventario_puentes.','llacolen.']

#Funcion para crear el dataframe a utilizar en el grafico OHLC, ademas el valor de la columna avg se utiliza para para el histograma
#La funcion requiere de una fecha inicial, para calcular a partir de esta los rangos de fechas
#La frecuencia, la cual corresponde al intervalo para generar el rango de fechas (12seg,288seg,2016seg y 4032seg)
#Y por ultimo requiere del nombre del sensor
def datos_ace(fecha_inicio,freq,sensor):
    if (str(fecha_inicio).split(sep=' ')[0]== '2008-01-01') and (str(fecha_inicio).split(sep=' ')[1] == '00:00:00'):
        new_fecha = pd.read_sql_query("SELECT fecha FROM "+str(esquema[2])+str(sensor)+" ORDER BY fecha ASC LIMIT 1",coneccion)['fecha'][0]
        new_hora = str(new_fecha).split(sep=' ')[1]
        fecha_inicio = dt.strptime(str(str(fecha_inicio).split(sep=' ')[0]+' '+new_hora),'%Y-%m-%d %H:%M:%S')
    periodo = 301 #Cantidad de fechas a generar, es 301 porque se necesitan tuplas de fechas para calcular los valores
    avg_,min_,max_,open_,close_ = [],[],[],[],[]
    rango_horas = list(pd.date_range(fecha_inicio, periods=periodo, freq=freq).strftime('%Y-%m-%d %H:%M:%S'))
    for i in range(len(rango_horas)-1):
        #consultas a la base de datos
        #La query1 entrega el avg,min y max de un rango de tiempo
        query1 = ("SELECT avg(lectura) as "+str(sensor)+", min(lectura) as min, max(lectura) as max "
             "FROM "+str(esquema[2])+str(sensor)+" "
             "Where fecha between '"+str(rango_horas[i])+"' and '"+str(rango_horas[i+1])+"' ;")
        #La query2 entrega el primer elemento de la base de datos al inicio del rango de tiempo y el ultimo elemento al final del rango de tiempo
        query2 = ("(SELECT lectura as open "
             "FROM "+str(esquema[2])+str(sensor)+" "
             "Where fecha ='"+str(rango_horas[i])+"' "
             "Order BY fecha ASC LIMIT 1)"
             "UNION ALL"
             "(SELECT lectura as close "
             "FROM "+str(esquema[2])+str(sensor)+" "
             "Where fecha ='"+str(rango_horas[i+1])+"' "
             "Order BY fecha DESC LIMIT 1)")
        tmp = pd.read_sql_query(query1,coneccion)
        tmp1 = pd.read_sql_query(query2,coneccion)
        #comprobaciones si por algun motivo en la fecha en que se busca un valor no existe, este reemplaza por 0
        if (tmp.empty):
            avg_.append(0)
            min_.append(0)
            max_.append(0)
        elif (tmp1.empty):
            open_.append(0)
            close_.append(0)
        elif(len(tmp1['open']) < 2):
            close_.append(0)
            open_.append(tmp1['open'][0])
        else:
            avg_.append(tmp[sensor][0])
            min_.append(tmp['min'][0])
            max_.append(tmp['max'][0])
            open_.append(tmp1['open'][0])
            close_.append(tmp1['open'][1])        
    rango_horas.pop(0) # Se elimina la fecha sobrante ya que se deja solo 300 fechas, las cuales corresponde al inicio de cada rango
    #Se crea el dataframe con todos los valores extraidos
    new_df = pd.DataFrame(list(zip(list(rango_horas), avg_,min_,max_,open_,close_)),columns =['fecha', sensor,'min','max','open','close'])
    return new_df

# Funcion que calcula la fecha del ultimo peak detectado 
def obtener_fecha_alerta(df,peaks_inf,peaks_sup,peaks_ini,peaks_fin):
    list_df = df['fecha'].tolist()
    tmp = []
    for i in peaks_inf:
        tmp.append(list_df[i])
    for j in peaks_sup:
        tmp.append(list_df[j])
    for k in peaks_ini:
        tmp.append(list_df[k])
    for l in peaks_fin:
        tmp.append(list_df[l])
    tmp.sort(reverse = True)
    if len(tmp) == 0:
        return 'N/A'
    else:
        return str(tmp[0])

# Funcion que calcula todos los peaks, que se encuentran sobre una linea de control, ya sea inferior o superior
def peak_(df,linea_control):
    lista = df.tolist()
    peaks = []
    for i in range(len(lista)):
        if(float(lista[i]) >= float(linea_control)):
            peaks.append(i)
    return peaks

def lineas_control(tipo,df,linea_control_inf,linea_control_sup):
     
    if tipo == 'inf':
        trace_linea_inf = []
        y = []
        #Bucle que agrega una linea recta en el valor ingresado 
        for i in range(len(df["fecha"])):
            y.append(float(linea_control_inf))
        trace_linea_inf.append(go.Scattergl(x=df["fecha"], y=y, mode='lines',line=dict(color='purple'),name='Línea Inferior',showlegend=False))
        # Calculo de peaks
        if(float(linea_control_inf) < 0):
            
            peak = []
            columnas = ['min','max','open','close']
            # se calculan los peaks para cada tipo de dato que contine el grafico OHLC
            peaks_inf = peak_(-(df['min']),-(linea_control_inf))
            peaks_sup = peak_(-(df['max']),-(linea_control_inf))
            peaks_ini = peak_(-(df['open']),-(linea_control_inf))
            peaks_fin = peak_(-(df['close']),-(linea_control_inf))

            peak.append(peaks_inf)
            peak.append(peaks_sup)
            peak.append(peaks_ini)
            peak.append(peaks_fin)    

            alert_inf = len(peaks_inf) + len(peaks_sup) + len(peaks_ini) + len(peaks_fin)
            alert_inf = str(alert_inf) + " peaks"
            #Obtine la fecha del ultimo peak detectado
            fecha_peak_inf = obtener_fecha_alerta(df,peaks_inf,peaks_sup,peaks_ini,peaks_fin)
                
            #Se marcan en el grafico OHLC los peaks detectados
            for peak,col in zip(peak,columnas):
                trace_linea_inf.append(go.Scatter(
                    x=[df["fecha"][j]for j in list(peak)],
                    y=[df[col][j]for j in list(peak)],
                    mode='markers',
                    name= 'Peak',
                    marker=dict(
                        size=8,
                        color='red',
                        symbol='cross'
                    ),
                    showlegend=False
                ))
        return trace_linea_inf,alert_inf,fecha_peak_inf

    elif tipo == 'sup':
        trace_linea_sup = []
        y = []
        #Bucle que agrega una linea recta en el valor ingresado 
        for i in range(len(df["fecha"])):
            y.append(float(linea_control_sup))
        trace_linea_sup.append(go.Scattergl(x=df["fecha"], y=y, mode='lines',line=dict(color='purple'),name='Línea Superior',showlegend=False))
        # Calculo de peaks
        if(float(linea_control_sup) > 0):
            
            peak = []
            columnas = ['min','max','open','close']
            # se calculan los peaks para cada tipo de dato que contine el grafico OHLC
            peaks_inf = peak_(df['min'],linea_control_sup)
            peaks_sup = peak_(df['max'],linea_control_sup)
            peaks_ini = peak_(df['open'],linea_control_sup)
            peaks_fin = peak_(df['close'],linea_control_sup)

            peak.append(peaks_inf)
            peak.append(peaks_sup)
            peak.append(peaks_ini)
            peak.append(peaks_fin)    

            alert_sup = len(peaks_inf) + len(peaks_sup) + len(peaks_ini) + len(peaks_fin)
            alert_sup = str(alert_sup) + " peaks"
            #Obtine la fecha del ultimo peak detectado
            fecha_peak_sup = obtener_fecha_alerta(df,peaks_inf,peaks_sup,peaks_ini,peaks_fin)
                
            #Se marcan en el grafico OHLC los peaks detectados
            for peak,col in zip(peak,columnas):
                trace_linea_sup.append(go.Scatter(
                    x=[df["fecha"][j]for j in list(peak)],
                    y=[df[col][j]for j in list(peak)],
                    mode='markers',
                    name= 'Peak',
                    marker=dict(
                        size=8,
                        color='red',
                        symbol='cross'
                    ),
                    showlegend=False
                ))
        return trace_linea_sup,alert_sup,fecha_peak_sup


#Funcion para generar rangos de datos para el histograma circular
def rangos (tmp1):
	valores = list(tmp1.keys())
	f,inicial,final = [],[],[]
	for i in range(8):
		if (i < 4):
			f.append(min(valores)+((-1)*(min(valores)/4)*i))
		else:
			f.append(max(valores)-((max(valores)/4)*(i-4)))
	f = sorted(f)
	for i in range(7):
		if((i+1)%2==0):
			inicial.append(f[i])
			final.append(f[i+1])
		else:
			inicial.append(f[i])
			final.append(f[i+1])
	return inicial,final

#funcion para definir los datos en cada rango para el histograma circular
def datos_por_rango(df,inicial,final):
	rr,tt,v,c = [],[],[],[]
	count,value,media = 0,0,0
	for ini,end in zip(inicial,final):
		for i, row in df.iterrows():
			if (row['dir_viento'] >= float(ini) and row['dir_viento']<=float(end)):
				value = value + row['vel_viento']
				count = count + 1
		v.append(value)
		c.append(count)
		value = 0
		count = 0
	for i in range(0,len(c)):
		if(c[i] != 0):
			media = v[i]/c[i]
		rr.append(media)
		media = 0
	for ini,end in zip(inicial,final):
		media = (ini + end) / 2
		tt.append(media)
	return rr,tt

#Dependiendo de los sensores disponibles, se muestra la alternativa de cambiar el tipo de visualizacion de 1-sensor o varios-sensores
def cantidad_sensores_visualizar(tipo_sensor):
    if tipo_sensor == 'acelerometro':
        if len(nombres_ace().keys()) > 1:
            cantidad_sensores = {"1 Sensor":"1-sensor","Varios Sensores":"varios-sensores"}
        else:
            cantidad_sensores = {"1 Sensor":"1-sensor"}
    else:
        cantidad_sensores = {"1 Sensor":"1-sensor"}
    return dict(cantidad_sensores)

# Funcion que retorna dependiendo de la cantidad de dias disponibles en la base de datos, las opciones a seleccionar en el RadioItem
def ventana_tiempo(tipo):
    if tipo == 0:
        ventana_tiempo = {"1 Hora":"12S"}
    elif tipo == 1:
        ventana_tiempo = {"1 Hora":"12S","1 Día":"288S"}
    elif tipo == 2:
        ventana_tiempo = {"1 Hora":"12S","1 Día":"288S","7 Días":"2016S"}
    elif tipo == 3:
        ventana_tiempo = {"1 Hora":"12S","1 Día":"288S","7 Días":"2016S","14 Días":"4032S"}
    return dict(ventana_tiempo)

# Funcion que sirve para generar las opciones de horas disponibles que se muestran en el RangeSlider
def crear_hora(hora):
    hora_new = '00:00:00'
    if hora == 24:
        hora_new = '00:00:00'
    else:
        for i in range(24):
            if hora == i and hora < 10:
                hora_new = '0'+str(i)+':00:00'
            elif hora == i and hora > 9:
                hora_new = str(i)+':00:00'
    return hora_new

# Funcion que retorna los nombres de los acelerometros disponibles a seleccionar en el Dropdown
def nombres_ace():
    df = pd.read_sql_query("SELECT DISTINCT nombre_tabla FROM "+str(esquema[1])+"sensores_instalados WHERE nombre_tabla like '%.acelerometro%';",coneccion)
    nombres = df['nombre_tabla'].tolist()
    nombres = sorted(nombres, key=lambda x: int("".join([i for i in x if i.isdigit()])))
    nombres_sensores = {}
    for nom in nombres:
        nombres_sensores[nom.split('.')[1]] = str(nom.split('.')[1])
    return dict(nombres_sensores)

# Funcion que retorna los nombres de las weather station disponibles a seleccionar en el Dropdown
def nombres_ws():
    nombres_ws = {"weather-station_1": "Weather Station 1"}
    return dict(nombres_ws)

# Funcion que retorna los nombres de los strain gauge disponibles a seleccionar en el Dropdown
def nombres_sg():
    nombres_sg = {"strain-gauge_1": "Strain Gauge 1"}
    return dict(nombres_sg)

# Funcion que retorna los nombres de los inclinometros disponibles a seleccionar en el Dropdown
def nombres_in():
    nombres_in = {"inclinometro_1": "Inclinómetro 1"}
    return dict(nombres_in)

# Funcion que retorna los nombres de los LVDT disponibles a seleccionar en el Dropdown
def nombres_lvdt():
    nombres_lvdt = {"lvdt_1": "LVDT 1"}
    return dict(nombres_lvdt)

#Funcion que elimina tildes
def elimina_tildes(cadena):
    sin = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
    return sin

# Funcion que retorna los nombres de los tipos de sensores disponibles a seleccionar en el Dropdown
def tipos_sensores():
    df = pd.read_sql_query("SELECT DISTINCT nombre FROM "+str(esquema[1])+"tipos_de_sensor;",coneccion)
    tipos = df['nombre'].tolist()
    tipos.sort(reverse=False)
    tipos_sensores = {}
    #for tipo in tipos:
    #    tipos_sensores[str(elimina_tildes(tipo)).lower().replace(' ', '-') ] = str(tipo)
    tipos_sensores[str(elimina_tildes(tipos[0])).lower().replace(' ', '-') ] = str(tipos[0])
    return dict(tipos_sensores)

# Funcion que retorna la minima fecha que existe en la base de datos
def fecha_inicial(tipo_sensor):
    if tipo_sensor == 'acelerometro':
        return pd.read_sql_query("SELECT fecha FROM "+str(esquema[2])+"acelerometro_5493257 ORDER BY fecha ASC LIMIT 1 ",coneccion)['fecha'][0]
    elif tipo_sensor == 'weather-station':
        return pd.read_sql_query("SELECT fecha FROM "+str(esquema[0])+"temperatura ORDER BY id_lectura ASC LIMIT 1 ",coneccion)['fecha'][0]

# Funcion que retorna la ultima fecha que existe en la base de datos
def fecha_final(tipo_sensor):
    if tipo_sensor == 'acelerometro':
        fecha =  pd.read_sql_query("SELECT fecha FROM "+str(esquema[2])+"acelerometro_5493257 ORDER BY fecha DESC LIMIT 1 ",coneccion)['fecha'][0]
        if fecha == None:
            fecha = dt (2008,1,16,23,18,28)
        return fecha
    elif tipo_sensor == 'weather-station':
        fecha = pd.read_sql_query("SELECT fecha FROM "+str(esquema[0])+"temperatura ORDER BY id_lectura DESC LIMIT 1 ",coneccion)['fecha'][0]
        if fecha == None:
            fecha = dt (2008,4,1,0,38,36)
        return fecha

#Funcion que cuenta la cantidad de dias entre 2 fechas
def dias_entre_fechas(fecha_ini,fecha_fin):
    return abs(fecha_fin - fecha_ini).days

#funcion que revisa las horas disponibles en la base de datos
def horas_del_dia(sensor,fecha_inicial):
    fecha_final = fecha_inicial + td(days=1)
    if sensor == 'weather-station_1':
        horas =  pd.read_sql_query("select distinct extract(hour from  fecha) as horas "
                                   "from "+str(esquema[0])+"temperatura "
                                   "where fecha between '"+str(fecha_inicial)+"' and '"+str(fecha_final)+"';",coneccion)
    else:
        horas =  pd.read_sql_query("select distinct extract(hour from  fecha) as horas "
                                   "from "+str(esquema[2])+str(sensor)+" "
                                   "where fecha between '"+str(fecha_inicial)+"' and '"+str(fecha_final)+"';",coneccion)
    horas = list(map(int, horas['horas'].tolist()))
    horas.sort()
    cant_horas = len(horas)
    if not horas:
        min_ = 0
        max_ = 0
    else:
        min_ = horas[0]
        max_ = horas[cant_horas-1]
    return horas,min_,max_

# Funcion que dado un dataframe y un sensor especifico, calcula el promedio, maximo, minimo, cuantas repeticiones de maximos, cuantas repeticiones de minimos
# y entrega las fechas de la ultima repeticon de maximo y minimo de todo el dataframe que se le entrega
# estos datos son visualizados sobre el grafico OHLC 
def datos_mini_container(df,sensor):
    max_ = np.amax(df['max'].tolist())
    min_ = np.amin(df['min'].tolist())
    avg_ = np.average(df[sensor].tolist())

    promedio = round(avg_,3)
    maximo = round(max_,3)
    minimo = round(min_,3)
    
    count_max = 'N° Veces: '+str(df['max'].tolist().count(max_))
    count_min = 'N° Veces: '+str(df['min'].tolist().count(min_))
    df_max = df.loc[df.loc[:, 'max'] == max_].reset_index().sort_values(by=['fecha'],ascending=True)
    df_min = df.loc[df.loc[:, 'min'] == min_].reset_index().sort_values(by=['fecha'],ascending=True)
    fecha_ultimo_max = str(df_max['fecha'][len(df_max['fecha'])-1])
    fecha_ultimo_min = str(df_min['fecha'][len(df_min['fecha'])-1])

    return promedio,maximo,minimo,count_max,count_min,fecha_ultimo_max,fecha_ultimo_min

# Funcion que crea el dataframe para una cajita del grafico boxplot, ya que por cada una de ellas se seleccionan 300 datos que son el 
# promedio de un rango de tiempo, este rango de tiempo depende de la frecuencia que puede ser 12seg, 288seg, 2016seg y 4032seg
# la obtencion de estos datos se realiza de la misma forma que para el grafico OHLC
def datos_box(fecha_inicio,freq,sensor):
    if freq == '12S':
        freq = '1S'
    elif freq == '288S':
        freq = '24S'
    elif freq == '2016S':
        freq = '144S'
    elif freq == '4032S':
        freq = '288S'
    periodo = 301
    tmp = []
    rango_horas = list(pd.date_range(fecha_inicio, periods=periodo, freq=freq).strftime('%Y-%m-%d %H:%M:%S'))
    for i in range(len(rango_horas)-1):
        query1 = ("SELECT avg(lectura) as "+str(sensor)+" "
                  "FROM "+str(esquema[2])+str(sensor)+" "
                  "Where fecha between '"+str(rango_horas[i])+"' and '"+str(rango_horas[i+1])+"' ;")
        df = pd.read_sql_query(query1,coneccion)[sensor]
        for j in range(1):
            tmp.append(df[j])
    rango_horas.pop(0)
    ultimo = rango_horas[-1]
    new_df = pd.DataFrame(list(zip(list(rango_horas), tmp)),columns =['fecha', str(ultimo)])
    return new_df,ultimo

#Funcion que retorna dependiendo de la frecuencia seleccionada su equivalente para incluirlo en la descripcion del grafico boxplot
def titulo_box(freq):
    if freq == '12S':
        freq = '5 min'
    elif freq == '288S':
        freq = '2 horas'
    elif freq == '2016S':
        freq = '12 horas'
    elif freq == '4032S':
        freq = '24 horas'
    return freq

#Funcion que retorna dependiendo de la frecuencia seleccionada su equivalente para incluirlo en la descripcion del grafico OHLC
def titulo_OHLC(freq):
    if freq == '12S':
        freq = '1 hora'
    elif freq == '288S':
        freq = '1 dia'
    elif freq == '2016S':
        freq = '7 dias'
    elif freq == '4032S':
        freq = '14 dias'
    return freq

#Funcion que retorna dependiendo de la frecuencia seleccionada su equivalente para incluirlo en la descripcion del grafico histograma
def titulo_freq_datos(freq):
    if freq == '12S':
        freq = '12 seg'
    elif freq == '288S':
        freq = '4 min y 48 seg'
    elif freq == '2016S':
        freq = '33 min y 36 seg'
    elif freq == '4032S':
        freq = '1 hr, 7 min y 12 seg'
    return freq

#Funcion que retorna el rango de fecha para incluirlo en el titulo de los graficos
def fecha_titulo(fecha_inicial,freq):
    if freq == '12S':
        sum_fecha = td(hours=1)
    elif freq == '288S':
        sum_fecha = td(days=1)
    elif freq == '2016S':
        sum_fecha = td(days=7)
    elif freq == '4032S':
        sum_fecha = td(days=14)
    fecha_final = str(fecha_inicial + sum_fecha)
    fecha_inicial = str(fecha_inicial)
    return fecha_inicial,fecha_final

#Funcion para generar los reportes, se tiene una plantilla en html, la cual se transforma en pdf
def generar_reportes(fig_principal,fig_sec1,fig_sec2,valor_promedio,valor_max,valor_min,fecha_valor_max,fecha_valor_min,num_valor_max,num_valor_min,alert_sup,alert_inf,fecha_alert_sup,fecha_alert_inf,sensor,sensor_multi,fecha,ventana_tiempo,valor_linea_control_sup,valor_linea_control_inf,hora,cantidad_sensores):
    
    #Transforma las figuras (graficos generados) en uri, para poder ser visualizados en html 
    #Escritorio
    def fig_to_uri(fig):
        return base64.b64encode(fig.to_image(format="png")).decode('utf-8')

    #Transforma el logo en uri, para poder ser visualizados en html
    with open("./assets/SHM-logo2.bmp", "rb") as imageFile:
        logo = base64.b64encode(imageFile.read()).decode('utf-8')
    
    # se guardan los garficos en formato uri en una lista
    #escritorio
    graficos = [fig_to_uri(fig_principal),fig_to_uri(fig_sec1),fig_to_uri(fig_sec2)]

    #heroku
    #graficos = [fig_principal.to_html(config={"displayModeBar": False}),fig_sec1.to_html(config={"displayModeBar": False}),fig_sec2.to_html(config={"displayModeBar": False})]

    # si es mas de 1 sensor en la visualizacion, se guardan los nombres en un string
    sensores_multi = ''
    if cantidad_sensores != '1-sensor':
        for sen in sensor_multi: 
            sensores_multi += str(sen) + ','

    meses = ['','Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    fecha_datos = str(fecha).split(sep='T')[0]
    fecha_max = str(fecha_valor_max).split(sep=' ')[0]
    fecha_min = str(fecha_valor_min).split(sep=' ')[0]
    dia_datos = str(fecha_datos).split(sep='-')[2]
    dia_max = str(fecha_max).split(sep='-')[2]
    dia_min = str(fecha_min).split(sep='-')[2]
    mes_datos = str(meses[int(str(fecha_datos).split(sep='-')[1])])
    mes_max = str(meses[int(str(fecha_max).split(sep='-')[1])])
    mes_min = str(meses[int(str(fecha_min).split(sep='-')[1])])
    ano_datos = str(fecha_datos).split(sep='-')[0]
    ano_max = str(fecha_max).split(sep='-')[0]
    ano_min = str(fecha_min).split(sep='-')[0]

    if valor_linea_control_sup != None and valor_linea_control_inf != None:
        fecha_inf = str(fecha_alert_inf).split(sep=' ')[0]
        fecha_sup = str(fecha_alert_sup).split(sep=' ')[0]
        dia_inf = str(fecha_inf).split(sep='-')[2]
        dia_sup = str(fecha_sup).split(sep='-')[2]
        mes_inf = str(meses[int(str(fecha_inf).split(sep='-')[1])])
        mes_sup = str(meses[int(str(fecha_sup).split(sep='-')[1])])
        ano_inf = str(fecha_inf).split(sep='-')[0]
        ano_sup = str(fecha_sup).split(sep='-')[0]
    elif valor_linea_control_inf != None:
        fecha_inf = str(fecha_alert_inf).split(sep=' ')[0]
        dia_inf = str(fecha_inf).split(sep='-')[2]
        mes_inf = str(meses[int(str(fecha_inf).split(sep='-')[1])])
        ano_inf = str(fecha_inf).split(sep='-')[0]
    elif valor_linea_control_sup != None:
        fecha_sup = str(fecha_alert_sup).split(sep=' ')[0]
        dia_sup = str(fecha_sup).split(sep='-')[2]
        mes_sup = str(meses[int(str(fecha_sup).split(sep='-')[1])])
        ano_sup = str(fecha_sup).split(sep='-')[0]
    
    
    ##Plantilla html
    encabezado_multi = (
        '<html lang="es">'
        '<head>'
            '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">'
            '<style>body{ margin:0 100; background:whitesmoke; }</style>'
        '</head>'
        '<body style="margin:60">'
        '<h1 style="text-align: center;"><img style="font-size: 14px; text-align: justify; float: left;" src="data:image/png;base64,'+logo+'" alt="Logo SHM" width="102" height="73" margin= "5px"/></h1>'
        '<h1 style="text-align: left;"><span style="font-family:arial,helvetica,sans-serif;"><strong>  Datos Recientes</strong></h1>'
        '<h2> <span style="font-family:arial,helvetica,sans-serif;">Plataforma Monitoreo Salud Estructural</h2>'
        '<p>&nbsp;</p>'
        '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Datos obtenidos de los sensores <strong>"'+str(sensores_multi)+'"</strong>, la ventana de tiempo seleccionada para las visualizaciones es de <strong>"'+str(titulo_OHLC(ventana_tiempo))+'"</strong>, el dia '+str(dia_datos)+' de '+str(mes_datos)+' de '+str(ano_datos)+' desde las '+str(crear_hora(int(hora)))+' a las '+str(crear_hora(int(hora) + 1))+' .</p>'
        '<p>&nbsp;</p>'
    )

    #heroku
    '''
    img = (''
        '<p><div style="display: block; margin-left: auto; margin-right: auto; height:400; width:850;"> {image} </div></p>'
        '')

    img2 = (''
        '<p><div style="display: block; margin-left: auto; margin-right: auto; height:400; width:600;"> {image} </div></p>'
        '')
	'''
    #Escritorio
    
    img = (''
        '<p><img style="display: block; margin-left: auto; margin-right: auto;" src="data:image/png;base64,{image}" alt="Gr&aacute;fico Principal" width="850" height="400" /></p>'
        '')
    img2 = (''
        '<p><img style="display: block; margin-left: auto; margin-right: auto;" src="data:image/png;base64,{image}" alt="Gr&aacute;fico Principal" width="600" height="400" /></p>'
        '')
    
    encabezado = (
        '<html lang="es">'
        '<head>'
            '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
            '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">'
            '<style>body{ margin:0 100; background:whitesmoke; }</style>'
        '</head>'
        '<body style="margin:60">'
        '<h1 style="text-align: center;"><img style="font-size: 14px; text-align: justify; float: left;" src="data:image/png;base64,'+logo+'" alt="Logo SHM" width="102" height="73" margin= "5px"/></h1>'
        '<h1 style="text-align: left;"><span style="font-family:arial,helvetica,sans-serif;"><strong>  Datos Recientes</strong></h1>'
        '<h2> <span style="font-family:arial,helvetica,sans-serif;">Plataforma Monitoreo Salud Estructural</h2>'
        '<p>&nbsp;</p>'
        '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Datos obtenidos del sensor <strong>"'+str(sensor)+'"</strong> la ventana de tiempo seleccionada para las visualizaciones es de <strong>"'+str(titulo_OHLC(ventana_tiempo))+'"</strong>, el dia '+str(dia_datos)+' de '+str(mes_datos)+' de '+str(ano_datos)+' desde las '+str(crear_hora(int(hora)))+' a las '+str(crear_hora(int(hora) + 1))+' .</p>'
        '<p>&nbsp;</p>'
    )

    resumen = (
        '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;"><strong>Resumen de Indicadores</strong></p>'
        '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Valor promedio: <strong>'+str(valor_promedio)+'</strong></p>'  
        '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Valor m&aacute;ximo: <strong>'+str(valor_max)+'</strong>,   Repeticiones: <strong>'+str(num_valor_max)[10:len(str(num_valor_max))]+'</strong>,   Fecha de &uacute;ltima repetici&oacute;n: <strong>'+str(dia_max)+'-'+str(mes_max)+'-'+str(ano_max)+' '+str(fecha_valor_max).split(sep=' ')[1]+'</strong></p>'
        '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Valor m&iacute;nimo: <strong>'+str(valor_min)+'</strong>,   Repeticiones: <strong>'+str(num_valor_min)[10:len(str(num_valor_min))]+'</strong>,   Fecha de &uacute;ltima repetici&oacute;n: <strong>'+str(dia_min)+'-'+str(mes_min)+'-'+str(ano_min)+' '+str(fecha_valor_min).split(sep=' ')[1]+'</strong></p>'
        '<p>&nbsp;</p>'
    )
    resumen_multi = (
        '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;"><strong>Resumen de Indicadores</strong></p>'
        '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">(Datos del &uacute;ltimo sensor seleccionado)</p>'
        '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Valor promedio: <strong>'+str(valor_promedio)+'</strong></p>'  
        '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Valor m&aacute;ximo: <strong>'+str(valor_max)+'</strong>,   Repeticiones: <strong>'+str(num_valor_max)[10:len(str(num_valor_max))]+'</strong>,   Fecha de &uacute;ltima repetici&oacute;n: <strong>'+str(dia_max)+'-'+str(mes_max)+'-'+str(ano_max)+' '+str(fecha_valor_max).split(sep=' ')[1]+'</strong></p>'
        '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Valor m&iacute;nimo: <strong>'+str(valor_min)+'</strong>,   Repeticiones: <strong>'+str(num_valor_min)[10:len(str(num_valor_min))]+'</strong>,   Fecha de &uacute;ltima repetici&oacute;n: <strong>'+str(dia_min)+'-'+str(mes_min)+'-'+str(ano_min)+' '+str(fecha_valor_min).split(sep=' ')[1]+'</strong></p>'
        '<p>&nbsp;</p>'
    )
    
    #version con indicadores descritos en parrafos
    '''
    resumen = (
        '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;"><strong>Resumen de Indicadores</strong></p>'
        '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Los datos seleccionados tienen un valor promedio de '+str(valor_promedio)+', adem&aacute;s de un valor m&aacute;ximo de '+str(valor_max)+', que se repite '+str(num_valor_max)[10:len(str(num_valor_max))]+' vez y su &uacute;ltima repetici&oacute;n fue el '+str(dia_max)+' de '+str(mes_max)+' de '+str(ano_max)+' a las '+str(fecha_valor_max).split(sep=' ')[1]+' y por &uacute;ltimo un valor m&iacute;nimo de '+str(valor_min)+' que se repite '+str(num_valor_min)[10:len(str(num_valor_min))]+' vez y su &uacute;ltima repetici&oacute;n fue el '+str(dia_min)+' de '+str(mes_min)+' de '+str(ano_min)+' a las '+str(fecha_valor_min).split(sep=' ')[1]+'.</p>'
        '<p>&nbsp;</p>'
    )
    resumen_multi = (
        '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;"><strong>Resumen de Indicadores</strong></p>'
        '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">(Datos del &uacute;ltimo sensor seleccionado)</p>'
        '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Los datos seleccionados tienen un valor promedio de '+str(valor_promedio)+', adem&aacute;s de un valor m&aacute;ximo de '+str(valor_max)+', que se repite '+str(num_valor_max)[10:len(str(num_valor_max))]+' vez y su &uacute;ltima repetici&oacute;n fue el '+str(dia_max)+' de '+str(mes_max)+' de '+str(ano_max)+' a las '+str(fecha_valor_max).split(sep=' ')[1]+' y por &uacute;ltimo un valor m&iacute;nimo de '+str(valor_min)+' que se repite '+str(num_valor_min)[10:len(str(num_valor_min))]+' vez y su &uacute;ltima repetici&oacute;n fue el '+str(dia_min)+' de '+str(mes_min)+' de '+str(ano_min)+' a las '+str(fecha_valor_min).split(sep=' ')[1]+'.</p>'
        '<p>&nbsp;</p>'
    )
    '''
    linea = ('<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;"><strong>L&iacute;neas de control </strong></p>')
    linea_multi = (
        '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;"><strong>L&iacute;neas de control </strong></p>'
        '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">(Datos de todos los sensores seleccionados)</p>'
        )
    if valor_linea_control_sup != None and valor_linea_control_inf != None:
        linea_sup = (
            '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Valor de l&iacute;nea de control superior: <strong>'+str(valor_linea_control_sup)+'</strong></p>'
            '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Peaks superiores: <strong>'+str(alert_sup)+'</strong></p>' 
            '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Fecha &uacute;ltimo peak superior detectado: <strong>'+str(dia_sup)+'-'+str(mes_sup)+'-'+str(ano_sup)+' '+str(fecha_alert_sup).split(sep=' ')[1]+'</strong></p>'
            )
        linea_inf = (
            '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Valor de l&iacute;nea de control inferior: <strong>'+str(valor_linea_control_inf)+'</strong></p>'
            '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Peaks inferiores: <strong>'+str(alert_inf)+'</strong></p>' 
            '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Fecha &uacute;ltimo peak inferior detectado: <strong>'+str(dia_inf)+'-'+str(mes_inf)+'-'+str(ano_inf)+' '+str(fecha_alert_inf).split(sep=' ')[1]+'</strong></p>'
            )
        #version con lineas de control descritos en parrafos
        '''
        linea_sup = ('<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">L&iacute;nea de control superior ubicada en el valor '+str(valor_linea_control_sup)+', existen '+str(alert_sup)+' que superan este umbral y el &uacute;ltimo peak detectado fue el '+str(dia_sup)+' de '+str(mes_sup)+' de '+str(ano_sup)+' a las '+str(fecha_alert_sup).split(sep=' ')[1]+'.')
        linea_inf = ('<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">L&iacute;nea de control inferior ubicada en el valor '+str(valor_linea_control_inf)+', existen '+str(alert_inf)+' que superan este umbral y el &uacute;ltimo peak detectado fue el '+str(dia_inf)+' de '+str(mes_inf)+' de '+str(ano_inf)+' a las '+str(fecha_alert_inf).split(sep=' ')[1]+'.')
        '''
    elif valor_linea_control_sup != None:
        linea_sup = (
            '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Valor de l&iacute;nea de control superior: <strong>'+str(valor_linea_control_sup)+'</strong></p>'
            '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Peaks superiores: <strong>'+str(alert_sup)+'</strong></p>' 
            '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Fecha &uacute;ltimo peak superior detectado: <strong>'+str(dia_sup)+'-'+str(mes_sup)+'-'+str(ano_sup)+' '+str(fecha_alert_sup).split(sep=' ')[1]+'</strong></p>'
            )
        #version con lineas de control descritos en parrafos
        #linea_sup = ('<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">L&iacute;nea de control superior ubicada en el valor '+str(valor_linea_control_sup)+', existen '+str(alert_sup)+' que superan este umbral y el &uacute;ltimo peak detectado fue el '+str(dia_sup)+' de '+str(mes_sup)+' de '+str(ano_sup)+' a las '+str(fecha_alert_sup).split(sep=' ')[1]+'.')
    elif valor_linea_control_inf != None:
        linea_inf = (
            '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Valor de l&iacute;nea de control inferior: <strong>'+str(valor_linea_control_inf)+'</strong></p>'
            '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Peaks inferiores: <strong>'+str(alert_inf)+'</strong></p>' 
            '<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">Fecha &uacute;ltimo peak inferior detectado: <strong>'+str(dia_inf)+'-'+str(mes_inf)+'-'+str(ano_inf)+' '+str(fecha_alert_inf).split(sep=' ')[1]+'</strong></p>'
            )
        #version con lineas de control descritos en parrafos
        #linea_inf = ('<p style="text-align: justify;"><span style="font-family:arial,helvetica,sans-serif;">L&iacute;nea de control inferior ubicada en el valor '+str(valor_linea_control_inf)+', existen '+str(alert_inf)+' que superan este umbral y el &uacute;ltimo peak detectado fue el '+str(dia_inf)+' de '+str(mes_inf)+' de '+str(ano_inf)+' a las '+str(fecha_alert_inf).split(sep=' ')[1]+'.')

    #heroku
    '''
    fecha = (
        '<p style="text-align: justify; padding-left: 30px; padding-right: 30px;"><span style="font-family:arial,helvetica,sans-serif;">Reporte del obtenido el '+str(time.strftime("%d/%m/%y"))+' a las&nbsp;'+str(time.strftime("%H:%M:%S"))+'</p>'
        '<a style="text-align: center;" href="#" onclick="window.print();return false;" title="Click para guardar o imprimir reporte"><strong>Guardar/Imprimir Reporte</strong></a>'
        '</body>'
        '</html>')
    '''
    #escritorio
    
    fecha = (
        '<p style="text-align: justify; padding-left: 30px; padding-right: 30px;"><span style="font-family:arial,helvetica,sans-serif;">Reporte del obtenido el '+str(time.strftime("%d/%m/%y"))+' a las&nbsp;'+str(time.strftime("%H:%M:%S"))+'</p>'
        '</body>'
        '</html>')
       

    #Se agregan las imagenes a la plantilla html
    imagenes = ''
    tmp = 1
    for image in graficos:
        if tmp == 3:
            _ = img2
        else: 
            _ = img
        _ = _.format(image=image)
        imagenes += _
        tmp += 1

    
    #Dependiendo de la situacion se modifica la plantilla html, tanto como para agregar contenido o para quitarlo 
    if cantidad_sensores != '1-sensor':
        reporte = encabezado_multi + resumen_multi + imagenes + fecha
        if valor_linea_control_sup != None and valor_linea_control_inf != None:
            reporte = encabezado_multi + resumen_multi + linea_multi + linea_sup + linea_inf + imagenes + fecha
        elif valor_linea_control_inf != None:
            reporte = encabezado_multi + resumen_multi + linea_multi + linea_inf + imagenes + fecha
        elif valor_linea_control_sup != None:
            reporte = encabezado_multi + resumen_multi + linea_multi + linea_sup + imagenes + fecha
    
    else:
        reporte = encabezado + resumen + imagenes + fecha

        if valor_linea_control_sup != None and valor_linea_control_inf != None:
            reporte = encabezado + resumen + linea + linea_sup + linea_inf + imagenes + fecha
        elif valor_linea_control_inf != None:
            reporte = encabezado + resumen + linea + linea_inf + imagenes + fecha
        elif valor_linea_control_sup != None:
            reporte = encabezado + resumen + linea + linea_sup + imagenes + fecha

    #Funcion que transforma el html en pdf para la version de escritorio o servidor con linux (necesita instalar dependencias extra no compatibles con heroku)
    pdfkit.from_string(reporte,'reporte.pdf')

    #Forma de generar el reporte para la version del subsistema montado en heroku
    #text_file = open("reporte.html", "w")
    #n = text_file.write(reporte)
    #text_file.close()

    #Funcion que abre el pdf recien creado
    
    #en chrome
    #webbrowser.get('google-chrome').open_new_tab('reporte.html') #heroku
    #webbrowser.get('google-chrome').open_new_tab('reporte.pdf') #escritorio
    
    #en navegador o lector de pdf por defecto
    #webbrowser.open_new_tab('reporte.html')#heroku
    webbrowser.open_new_tab('reporte.pdf')#escritorio