import dash
import collections
import dataframe as datos
import plotly.express as px
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import numpy as np
from dash.dependencies import Input, Output,State
from datetime import datetime as dt
from time import time


app = dash.Dash(
    __name__,meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
#server = app.server
app.title = 'Datos Recientes - Plataforma de Monitoreo Salud Estructural'

server = app.server
# Contiene la estructuracion completa de la pagina 
app.layout = html.Div([
                
                #Div que contiene el titulo de la pagina
                html.Div([
                    html.Div(
                        id='retorno-reportes', 
                        style={'display': 'none'}
                    ),
                    html.Div([
                        html.Img(
                            src=app.get_asset_url("SHM-logo.bmp"),
                            id="SHM-imagen",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],className="one-third column",
                    ),
                    html.Div([
                        html.H3(
                            "Datos Recientes",
                            style={'color': 'Black','font-weight': 'bold',"margin-bottom": "0px"},
                        ),
                        html.H5(
                            "Plataforma Monitoreo Salud Estructural", 
                            style={"margin-top": "0px"}
                        ),
                    ],
                    className="one-half column",
                    id="title",
                    ),
                    html.Div([
                        dcc.Loading(
                            id="carga-reportes",
                            children=[
                                html.A(
                                    html.Button(
                                        "Generar Reporte", 
                                        id="boton-generar-reporte",
                                        n_clicks = 0,
                                        style={'color': 'Black', 'backgroundColor':'lavender','font-size':'17px'}
                                    ),
                                )
                            ]
                        )
                    ],
                    className="one-third column",
                    id="button",
                    ),
                ],
                id="header",
                className="row flex-display",
                style={"margin-bottom": "25px"},
        ),
        html.Div([
            html.Div([
                #Esta seccion contiene todo lo que se muestra en la pestaña "Datos Sensores" del menu de opciones
                dcc.Tabs([
                    dcc.Tab(
                        label='Datos Sensores', 
                        children=[
                            html.P(
                                "Seleccione Tipo de Sensor",
                                className="control_label",
                                style={'textAlign': 'center','font-size':'20px'}
                            ),
                            html.Div([
                                dcc.Loading(
                                    id="carga-elegir-tipo-sen", 
                                    children=[
                                        dcc.Dropdown(
                                            id="elegir-tipo-sensor", 
                                            multi=False, 
                                            options=[{"label": value , "value": key}for key,value in datos.tipos_sensores().items()],
                                            value=str(list(datos.tipos_sensores().keys())[0]),
                                        ),
                                    ],type="default"
                                )
                            ]),
                            html.Br(),
                            html.P(
                                "Seleccione Sensor",
                                className="control_label",
                                style={'textAlign': 'center','font-size':'20px'}
                            ),
                            html.Div([
                                dcc.Loading(
                                    id="carga-elegir-sen", 
                                    children=[
                                        dcc.Dropdown(
                                            id="elegir-sensor", 
                                            multi=False, 
                                            options=[{"label": value , "value": key}for key,value in datos.nombres_ace().items()],
                                            value=str(list(datos.nombres_ace().keys())[0]),
                                        ),
                                    ],type="default"
                                )
                            ],id='sensor-uni'),
                            html.Div([
                                dcc.Loading(
                                    id="carga-elegir-sen-multi", 
                                    children=[
                                        dcc.Dropdown(
                                            id="elegir-sensor-multi", 
                                            multi=True, 
                                            options=[{"label": value , "value": key}for key,value in datos.nombres_ace().items()],
                                            value=str(list(datos.nombres_ace().keys())[0]),
                                        ),
                                    ],type="default"
                                )
                            ],style={'display':'none'},id='sensor-multi'),
                            html.Br(),
                            html.P(
                                "Seleccione Fecha Inicial: ",
                                className="control_label",
                                style={'textAlign': 'center','font-size':'20px'}
                            ),
                            html.Div([
                                dcc.Loading(
                                    id="carga-elegir-fecha", 
                                    children=[
                                        dcc.DatePickerSingle(
                                            id='elegir-fecha',
                                            display_format='DD/MM/YYYY',
                                            min_date_allowed=datos.fecha_inicial('Acelerómetro'),
                                            max_date_allowed=datos.fecha_final('Acelerómetro'),
                                            initial_visible_month=datos.fecha_inicial('Acelerómetro'),
                                            date = datos.fecha_inicial('Acelerómetro')
                                        ),
                                    ],type="default"
                                )
                            ],style={'textAlign': 'center'}),
                            html.Br(),
                            html.P(
                                "Seleccione Ventana de Tiempo", 
                                className="control_label",
                                style={'textAlign': 'center','font-size':'20px'}
                            ),
                            html.Div([
                                dcc.Loading(
                                    id="carga-ventana-tiempo", 
                                    children=[
                                        dcc.RadioItems(
                                            id="ventana-tiempo",
                                            options=[{"label": key , "value": value}for key,value in datos.ventana_tiempo(3).items()],
                                            value=str(list(datos.ventana_tiempo(3).values())[0]),
                                            labelStyle={"display": "inline-block"},
                                            className="dcc_control",
                                        ),
                                    ],type="default"
                                )  
                            ],style={'textAlign': 'center'}),
                            html.Br(),
                            html.Div([
                                html.P(
                                    "Deslice para Seleccionar Hora", 
                                    className="control_label",
                                    style={'textAlign': 'center','font-size':'20px'}
                                ),
                                html.Div([
                                    dcc.Loading(
                                        id="carga-horas-disponibles", 
                                        children=[
                                            dcc.Slider(
                                                id='horas-disponibles',
                                                min=0,
                                                max=23,
                                                value=0,
                                                step=None,
                                                dots=True,
                                                updatemode='drag',
                                                included=False
                                            ),
                                        ],type="default"
                                    )
                                ]),  
                                html.P(
                                    "Hora Seleccionada: ---",
                                    id='hora-disponible-seleccionada', 
                                    className="control_label",
                                    style={'textAlign': 'center','font-size':'18px'}
                                )    
                            ],id='contenedor-horas-disponibles'),
                            html.Br(),
                            html.Div([
                                html.Button(
                                    "Actualizar Gráficos",
                                    id='boton-aceptar',
                                    n_clicks = 0,
                                    style={'color': 'Black', 'backgroundColor':'lavender','font-size':'17px'}
                                ),
                            ],style={'textAlign': 'center'}),
                        ]),
                        # Esta seccion contiene todo lo que se muestra en la pestaña "Propiedades de los graficos"
                    dcc.Tab(
                            label='Propiedades de los Gráficos', 
                            children=[
                                html.Br(),
                                html.Br(),
                                html.P(
                                    "Cantidad de Sensores a Visualizar por Gráficas", 
                                    className="control_label",
                                    style={'textAlign': 'center','font-size':'20px'}
                                ),
                                html.Br(),
                                html.Div([
                                    dcc.RadioItems(
                                        id='cantidad-sensores',
                                        options=[
                                            {'label': '1 Sensor', 'value': '1-sensor'},
                                            {'label': 'Varios Sensores', 'value': 'varios-sensores'},
                                        ],
                                        value='1-sensor',
                                        labelStyle={'display': 'inline-block'}
                                    ), 
                                ],style={'textAlign': 'center'}), 
                                html.Br(),
                                html.Br(),
                                html.P(
                                    "Linea de control Superior", 
                                    className="control_label",
                                    style={'textAlign': 'center','font-size':'20px'}
                                ),
                                html.Br(),
                                html.Div([
                                    dcc.Input(
                                        id='linea-control-sup', 
                                        type="number", 
                                        placeholder="Solo valores positivos",
                                        min=0, 
                                        max=1000, 
                                        step=0.001,
                                        style={"width": "35%",'font-size':'15px'}
                                    ),
                                ],style={'textAlign': 'center'}),
                                html.Br(),
                                html.Div([
                                    html.Button(
                                        'Agregar / Actualizar',
                                        id='boton-linea-sup',
                                        n_clicks = 0,
                                        style={'color': 'Black', 'backgroundColor':'lavender','font-size':'15px'}
                                    ),
                                    html.Button(
                                        'Quitar',
                                        id='boton-quitar-linea-sup',
                                        n_clicks = 0,
                                        style={'color': 'Black', 'backgroundColor':'tomato','font-size':'15px'}
                                    ),
                                ],style={'textAlign': 'center'}),
                                html.Br(),
                                html.Br(),
                                html.P(
                                    "Linea de control Inferior", 
                                    className="control_label",
                                    style={'textAlign': 'center','font-size':'20px'}
                                ),
                                html.Br(),
                                html.Div([
                                    dcc.Input(
                                        id='linea-control-inf', 
                                        type="number", 
                                        placeholder="Solo valores negativos",
                                        value =None,
                                        min=-1000, 
                                        max=0, 
                                        step=0.001,
                                        style={"width": "35%",'font-size':'15px'}
                                    ),
                                ],style={'textAlign': 'center'}),
                                html.Br(),
                                html.Div([
                                    html.Button(
                                        'Agregar / Actualizar',
                                        id='boton-linea-inf',
                                        n_clicks = 0,
                                        style={'color': 'Black', 'backgroundColor':'lavender','font-size':'15px'}
                                    ),
                                    html.Button(
                                        'Quitar',
                                        id='boton-quitar-linea-inf',
                                        n_clicks = 0,
                                        style={'color': 'Black', 'backgroundColor':'tomato','font-size':'15px'}
                                    ),
                                ],style={'textAlign': 'center'})
                            ])
                    ])
                ],className="pretty_container four columns",id="cross-filter-options",
            ),
            # En esta seccion se tiene todo lo relacionado con los indicadores, promedio, maximo valor , minimo valor y las lineas de control
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Loading(
                            id="carga-promedio", 
                            children=[
                                html.Br(),
                                html.Br(),  
                                html.P("Valor Promedio",style={'color': 'Black','font-weight': 'bold'}),
                                html.H4('---',id="valor-promedio"),
                                html.P("(Datos de los indicadores pertencientes al ultimo sensor seleccionado)", id="indicador-multi",style={'display': 'none'}),
                                ],type="default"        
                            )
                            ],id="promedio",className="mini_container",
                        ),
                    html.Div([
                        dcc.Loading(
                            id="carga-val-max", 
                            children=[
                                html.P("Valor Máximo",style={'color': 'Black','font-weight': 'bold'}),
                                html.H4('---',id="valor-max"),
                                html.P("N° Veces: ---",id='num-valor-max'),
                                html.P("Última Repetición:"),
                                html.P("---",id='fecha-valor-max'),
                                ],type="default"
                            ),
                            ],id="max",className="mini_container",
                        ),
                    html.Div([
                        dcc.Loading(
                            id="carga-val-min", 
                            children=[
                                html.P("Valor Mínimo",style={'color': 'Black','font-weight': 'bold'}),
                                html.H4('---',id="valor-min"),
                                html.P("N° Veces: ---",id='num-valor-min'),
                                html.P("Última Repetición:"),
                                html.P("---",id='fecha-valor-min'),
                                ],type="default"
                            ),
                            ],id="min",className="mini_container",
                        ),
                    html.Div([
                        dcc.Loading(
                            id="carga-aler-sup", 
                            children=[
                                html.P("N° Alertas",style={'color': 'Black','font-weight': 'bold'}),
                                html.P("Línea de Control",style={'color': 'Black','font-weight': 'bold'}),
                                html.P("Superior",style={'color': 'Black','font-weight': 'bold'}),
                                html.H4('---',id="alert-sup"),
                                html.P("Última Alerta:"),
                                html.P("---",id='fecha-alert-sup'),
                                ],type="default"
                            ),
                            ],id="alertmax",className="mini_container",
                        ),
                    html.Div([
                        dcc.Loading(
                            id="carga-aler-inf",
                            children=[
                                html.P("N° Alertas",style={'color': 'Black','font-weight': 'bold'}),
                                html.P("Línea de Control",style={'color': 'Black','font-weight': 'bold'}),
                                html.P("Inferior",style={'color': 'Black','font-weight': 'bold'}),
                                html.H4('---',id="alert-inf"),
                                html.P("Última Alerta:"),
                                html.P("---",id='fecha-alert-inf'),
                                ],type="default"
                            ),
                            ],id="alertmin",className="mini_container",
                        ),
                    ],id="info-container",className="row container-display",
                ),
                # En esta seccion se tienen todos los graficos a mostrar en la ventana
                html.Div([
                    dcc.Loading(
                        id="carga-grafico-principal",
                        children=[
                            dcc.Graph(
                                id="grafico-principal"
                                )
                            ],type="default"
                        ),
                    ],id='cuadro-grafico-principal',className="pretty_container",
                    ),
                ],id="right-column",className="eight columns",
            ),
            ],className="row flex-display",
        ),
        #Esta seccion contiene todas las graficas
        html.Div([
            html.Div([
                dcc.Loading(
                    id="carga-grafico-1",
                    children=[
                        dcc.Graph(
                            id='grafico-1'
                            )
                        ],type="default"
                    ),
                ],id='cuadro-grafico-1',className="pretty_container seven columns",
            ),
            html.Div([
                dcc.Loading(
                    id="carga-grafico-2",
                    children=[
                        dcc.Graph(
                            id='grafico-2'
                            )
                        ],type="default"
                    ),
                ],id='cuadro-grafico-2',className="pretty_container five columns",
            ),
            ],className="row flex-display",
        ),
    ],id="mainContainer",style={"display": "flex", "flex-direction": "column"},
)

#Si se desean agregar mas graficas se puede copiar esta plantilla despues de la grafica 2
'''
        html.Div([
                html.Div([
                    dcc.Graph(
                        figure=datos-grafico(),
                        id="grafico-3"
                    )],
                    className="pretty_container five columns", #El largo la grilla es 12 y esta plantilla tiene tamaño 5 (five)
                ),
            ],id='cuadro-grafico-3',className="row flex-display",
        ),
'''

@app.callback(Output('indicador-multi','style'),
              [Input('boton-aceptar', 'n_clicks')],[State('cantidad-sensores','value')])

def update_info(clicks,cantidad_sensores):
    if clicks >= 0:
        if cantidad_sensores == '1-sensor':
            return {'display':'none'}
        else:
            return {'display':'inline'}

# Esta funcion cambia segun el tipo de sensor, los sensores disponibles y ademas si en las propiedades se selecciona tener mas de 1 sensor por grafica cambia el dropdown a multiple
@app.callback([Output('elegir-sensor', 'value'),Output('elegir-sensor', 'options'),Output('elegir-sensor-multi', 'value'),Output('elegir-sensor-multi', 'options'),Output('sensor-multi', 'style'),Output('sensor-uni','style')],
              [Input('cantidad-sensores','value'),Input('elegir-tipo-sensor','value')])

def lista_sensores(cantidad_sensores,tipo_sensor):
    if cantidad_sensores == '1-sensor':
        if tipo_sensor == 'acelerometro':
            return str(list(datos.nombres_ace().keys())[0]),[{"label": value , "value": key}for key,value in datos.nombres_ace().items()],'',[{"label":'',"value":''}],{'display':'none'},{'display':'inline'}
        elif tipo_sensor == 'lvdt':
            return str(list(datos.nombres_lvdt().keys())[0]),[{"label": value , "value": key}for key,value in datos.nombres_lvdt().items()],'',[{"label":'',"value":''}],{'display':'none'},{'display':'inline'}
        elif tipo_sensor == 'weather-station':
            return str(list(datos.nombres_ws().keys())[0]),[{"label": value , "value": key}for key,value in datos.nombres_ws().items()],'',[{"label":'',"value":''}],{'display':'none'},{'display':'inline'}
        elif tipo_sensor == 'strain-gauge':
            return str(list(datos.nombres_sg().keys())[0]),[{"label": value , "value": key}for key,value in datos.nombres_sg().items()],'',[{"label":'',"value":''}],{'display':'none'},{'display':'inline'}
        elif tipo_sensor == 'inclinometro':
            return str(list(datos.nombres_in().keys())[0]),[{"label": value , "value": key}for key,value in datos.nombres_in().items()],'',[{"label":'',"value":''}],{'display':'none'},{'display':'inline'}
    elif cantidad_sensores == 'varios-sensores':
        if tipo_sensor == 'acelerometro':
            return '',[{"label":'',"value":''}],[str(list(datos.nombres_ace().keys())[0])],[{"label": value , "value": key}for key,value in datos.nombres_ace().items()],{'display':'inline'},{'display':'none'}
        elif tipo_sensor == 'lvdt':
            return '',[{"label":'',"value":''}],[str(list(datos.nombres_lvdt().keys())[0])],[{"label": value , "value": key}for key,value in datos.nombres_lvdt().items()],{'display':'inline'},{'display':'none'}
        elif tipo_sensor == 'weather-station':
            return '',[{"label":'',"value":''}],[str(list(datos.nombres_ws().keys())[0])],[{"label": value , "value": key}for key,value in datos.nombres_ws().items()],{'display':'inline'},{'display':'none'}
        elif tipo_sensor == 'strain-gauge':
            return '',[{"label":'',"value":''}],[str(list(datos.nombres_sg().keys())[0])],[{"label": value , "value": key}for key,value in datos.nombres_sg().items()],{'display':'inline'},{'display':'none'}
        elif tipo_sensor == 'inclinometro':
            return '',[{"label":'',"value":''}],[str(list(datos.nombres_in().keys())[0])],[{"label": value , "value": key}for key,value in datos.nombres_in().items()],{'display':'inline'},{'display':'none'}

#Esta funcion cambia las fechas del selector de fechas deacuerdo a las disponibles en cada sensor
@app.callback([Output('elegir-fecha','min_date_allowed'),Output('elegir-fecha','max_date_allowed'),Output('elegir-fecha','initial_visible_month'),Output('elegir-fecha','date')],
              [Input('elegir-tipo-sensor','value')])

def update_fecha(tipo_sensor):
    ini = datos.fecha_inicial(tipo_sensor)
    fin = datos.fecha_final(tipo_sensor)
    return ini,fin,ini,ini

# Esta funcion muestra el rangeslider de horas, siempre que este seleccionado la opcion de "1 hora" 
@app.callback(Output('contenedor-horas-disponibles', 'style'),
              [Input('ventana-tiempo','value')])

def update_seleccion_horas(opciones):
    if opciones == '12S':
        return {'display':'inline'}
    else:
        return {'display':'none'}

#Muestra las horas disponibles segun el sensor en el rangeslider
@app.callback([Output('horas-disponibles','value'),Output('horas-disponibles','min'),Output('horas-disponibles','max'),Output('horas-disponibles','marks')],
              [Input('elegir-sensor','value'),Input('elegir-sensor-multi','value'),Input('elegir-fecha','date'),Input('cantidad-sensores','value')])

def horas_disponibles_sensor(sensor,sensor_multi,fecha_ini,cantidad_sensores):
    if fecha_ini == None:
        fecha_ini = str(dt(2008,1,1)).split(sep=' ')[0]
    fecha_str = str(fecha_ini).split(sep='T')[0]
    fecha = dt.strptime(fecha_str, '%Y-%m-%d')
    if cantidad_sensores == '1-sensor':
        if sensor == '':
            horas,min,max = [0,1],0,1
        else:
            horas,min,max = datos.horas_del_dia(sensor,fecha)
        marks = {}
        for i in horas:
            if i == 0:
                marks[i]= {'label': '00:00','style': {'color': 'black'}}
            elif i == 6:
                marks[i]= {'label': '06:00','style': {'color': 'black'}}
            elif i == 12:
                marks[i]= {'label': '12:00','style': {'color': 'black'}}
            elif i == 18:
                marks[i]= {'label': '18:00','style': {'color': 'black'}}
            elif i == 23:
                marks[i]= {'label': '23:00','style': {'color': 'black'}}
            else:
                marks[i]= {'label': ' '}        
        return min,min,max,marks
    else:
        if str(type(sensor_multi)) == "<class 'str'>":
            horas,min,max = [0,1],0,1
        else:
            horas,min,max = datos.horas_del_dia(sensor_multi[0],fecha)
        marks = {}
        for i in horas:
            if i == 0:
                marks[i]= {'label': '00:00','style': {'color': 'black'}}
            elif i == 6:
                marks[i]= {'label': '06:00','style': {'color': 'black'}}
            elif i == 12:
                marks[i]= {'label': '12:00','style': {'color': 'black'}}
            elif i == 18:
                marks[i]= {'label': '18:00','style': {'color': 'black'}}
            elif i == 23:
                marks[i]= {'label': '23:00','style': {'color': 'black'}}
            else:
                marks[i]= {'label': ' '} 
        return min,min,max,marks

# Esta funcion actualiza el texto bajo el rangeslider de horas, con la hora que se selecciona en el rangeslider
@app.callback(Output('hora-disponible-seleccionada','children'),
             [Input('horas-disponibles', 'value')])

def update_hora_seleccionada(hora):
    hora_sel = 'Hora Seleccionada: ---'
    for i in range(24):
        if hora == i and hora < 10:
            hora_sel = 'Hora Seleccionada: 0'+str(i)+':00'
        elif hora == i and hora > 9:
            hora_sel = 'Hora Seleccionada: '+str(i)+':00'
    return hora_sel

# Esta funcion cambia las opciones que se muestran en el radioitem cantidad de sensores a visualizar
@app.callback(Output('cantidad-sensores','options'),
             [Input('elegir-tipo-sensor','value')])

def change_cantidad_sensores(tipo_sensor):
    return [{"label": key , "value": value}for key,value in datos.cantidad_sensores_visualizar(tipo_sensor).items()]

#funcion que desabilita el dropdown de tipos de sensores cuando se selecciona la opcion de multiples sensores
@app.callback(Output('elegir-tipo-sensor','disabled'),
             [Input('cantidad-sensores','value')])

def disable_tipo_sensores(cantidad_sensores):
    if cantidad_sensores == '1-sensor':
        return False
    else:
        return True

# Esta funcion cambia las opciones que se muestran en el radioitem ventana de tiempo, dependiendo de lo que se encuentre en la base de datos
@app.callback([Output('ventana-tiempo','options'),Output('ventana-tiempo','value')],
             [Input('elegir-fecha', 'date'),Input('elegir-tipo-sensor','value')])

def change_ventana_tiempo(fecha_ini,tipo_sensor):
    fecha_fin = dt(2008,1,2,0,0,0)
    if fecha_ini == None and fecha_fin == None:
        fecha_ini = dt(2008,1,1,0,0,0)
        fecha_fin = dt(2008,1,2,0,0,0)
    elif fecha_ini == None:
        fecha_ini = dt(2008,1,1,0,0,0)
    elif fecha_fin == None:
        fecha_fin = dt(2008,1,2,0,0,0)
    fecha_ini = str(fecha_ini)
    fecha_ini = dt.strptime(str(dt(int(fecha_ini[0:4]),int(fecha_ini[5:7]),int(fecha_ini[8:10]),0,0,0)),'%Y-%m-%d %H:%M:%S')
    fecha_fin = datos.fecha_final(tipo_sensor)
    rango = datos.dias_entre_fechas(fecha_ini,fecha_fin)
    if rango > 13:
        return [{"label": key , "value": value}for key,value in datos.ventana_tiempo(3).items()],str(list(datos.ventana_tiempo(3).values())[0])
    elif rango > 6 and rango < 14:
        return [{"label": key , "value": value}for key,value in datos.ventana_tiempo(2).items()],str(list(datos.ventana_tiempo(3).values())[0])
    elif rango > 0 and rango < 7:
        return [{"label": key , "value": value}for key,value in datos.ventana_tiempo(1).items()],str(list(datos.ventana_tiempo(3).values())[0])
    elif rango == 0:
        return [{"label": key , "value": value}for key,value in datos.ventana_tiempo(0).items()],str(list(datos.ventana_tiempo(3).values())[0])

# Esta funcion actualiza el numero de clicks del boton agregar linea de control inferior, cuando se presiona el boton quitar linea 
@app.callback(Output('boton-linea-inf', 'n_clicks'),
              [Input('boton-quitar-linea-inf', 'n_clicks')])

def update_boton_inf(click_quitar_inf):
    if click_quitar_inf > 0:
        return 0
    else:
        return 1

# Esta funcion actualiza el numero de clicks del boton agregar linea de control superior, cuando se presiona el boton quitar linea
@app.callback(Output('boton-linea-sup', 'n_clicks'),
              [Input('boton-quitar-linea-sup', 'n_clicks')])

def update_boton_sup(click_quitar_sup):
    if click_quitar_sup > 0:
        return 0
    else:
        return 1

# Esta funcion actualiza el texto que aparece en el cuadro para indicar el valor de la linea de control inferior, una vez que se presiona el boton de quitar linea
@app.callback(Output('linea-control-inf','value'),
             [Input('boton-quitar-linea-inf','n_clicks')])

def update_text_input_inf(clicks_inf):
    if clicks_inf >= 0 :
        return None

# Esta funcion actualiza el texto que aparece en el cuadro para indicar el valor de la linea de control superior, una vez que se presiona el boton de quitar linea
@app.callback(Output('linea-control-sup','value'),
             [Input('boton-quitar-linea-sup','n_clicks')])

def update_text_input_sup(clicks_sup):
    if clicks_sup >= 0 :
        return None


@app.callback([Output('valor-promedio', 'children'),Output('valor-max', 'children'),Output('valor-min', 'children'),Output('fecha-valor-max','children'),
               Output('fecha-valor-min','children'),Output('num-valor-max','children'),Output('num-valor-min','children'),Output('alert-sup','children'),
               Output('alert-inf','children'),Output('fecha-alert-sup','children'),Output('fecha-alert-inf','children'),Output('grafico-principal','figure')],
              [Input('boton-aceptar', 'n_clicks'),Input('boton-linea-sup', 'n_clicks'),Input('boton-linea-inf', 'n_clicks')],
              [State('cantidad-sensores','value'),State('horas-disponibles', 'value'),State('elegir-tipo-sensor','value'),State('elegir-sensor','value'),State('elegir-sensor-multi','value'),State('elegir-fecha','date'),State('ventana-tiempo','value'),
               State('linea-control-sup','value'),State('linea-control-inf','value')])

def update_grafico_principal(n_clicks,click_linea_sup,click_linea_inf,cantidad_sensores,hora,tipo_sensor,sensor,sensor_multi,fecha,ventana_tiempo,linea_control_sup,linea_control_inf):
    if fecha != None:
        if str(str(fecha).split(sep='T')[0]) == str(str(datos.fecha_inicial(tipo_sensor)).split(sep=' ')[0]):
            #fecha = dt.strptime(str(str(fecha).split(sep='T')[0]) + ' ' + str(str(datos.fecha_inicial()).split(sep=' ')[1]),'%Y-%m-%d %H:%M:%S')
            fecha = dt.strptime(str(str(fecha).split(sep='T')[0])+' '+datos.crear_hora(hora),'%Y-%m-%d %H:%M:%S')
        else:
            fecha = dt.strptime(str(str(fecha).split(sep='T')[0])+' '+datos.crear_hora(hora),'%Y-%m-%d %H:%M:%S')
    else:
        fecha = dt(2008,1,1,0,0,0)
    #Se inicializan variables
    df = pd.DataFrame()
    fig_principal = go.Figure()
    alert_inf, alert_sup, fecha_peak_sup, fecha_peak_inf = '---','---','---','---'
    promedio,maximo,minimo,count_max,count_min,fecha_ultimo_max,fecha_ultimo_min = '---','---','---','---','---','---','---'
    #Listas que conteneran cada trace generado por cada dataframe creado para poder visualizarlos en una grafica
    trace_principal = []
    if n_clicks >= 0:
        fecha_ini_titulo,fecha_fin_titulo = datos.fecha_titulo(fecha,ventana_tiempo) 
        #Dependiendo del tipo de sensor se crean visualizaciones distintas
        if tipo_sensor == 'acelerometro':
            if cantidad_sensores == '1-sensor':
                # La variable df contiene el dataframe que se utiliza para generar los graficos OHLC e histograma
                start_time = time()
                df = datos.datos_ace(fecha,ventana_tiempo,sensor)
                elapsed_time = time() - start_time
                print("Tiempo Transcurrido crear DF: %0.1f seconds." % elapsed_time)
                # Aqui se crea el grafico OHLC
                start_time = time()
                trace_principal.append(go.Ohlc(x=df['fecha'],
                    open=df['open'],
                    high=df['max'],
                    low=df['min'],
                    close=df['close'],
                    increasing_line_color= 'green', 
                    decreasing_line_color= 'red',
                    name=sensor,
                    showlegend=False))

                fig_principal = go.Figure(data=trace_principal)
                #Aqui se agregan las lineas de control
                if (click_linea_inf > 0 and linea_control_inf != None) and (click_linea_sup > 0 and linea_control_sup != None):
                    trace_linea_inf,alert_inf,fecha_peak_inf = datos.lineas_control('inf',df,linea_control_inf,0)
                    trace_linea_sup,alert_sup,fecha_peak_sup = datos.lineas_control('sup',df,0,linea_control_sup)
                    trace_linea_inf.extend(trace_linea_sup)
                    trace_principal.extend(trace_linea_inf)
                    fig_principal = go.Figure(data=trace_principal)

                #Linea de control inferior
                elif click_linea_inf > 0 and linea_control_inf != None:
                    trace_linea_inf,alert_inf,fecha_peak_inf = datos.lineas_control('inf',df,linea_control_inf,0)
                    trace_principal.extend(trace_linea_inf)
                    fig_principal = go.Figure(data=trace_principal)
                #Linea de control superior       
                elif click_linea_sup > 0 and linea_control_sup != None:
                    trace_linea_sup,alert_sup,fecha_peak_sup = datos.lineas_control('sup',df,0,linea_control_sup)
                    trace_principal.extend(trace_linea_sup)
                    fig_principal = go.Figure(data=trace_principal)
                
                fig_principal.update(layout_xaxis_rangeslider_visible=False)
                titulo_OHLC = datos.titulo_OHLC(ventana_tiempo)
                fig_principal.update_layout(title={'text':"Datos cada "+str(datos.titulo_freq_datos(ventana_tiempo))+" del "+str(datos.nombres_ace()[sensor])+" durante "+str(titulo_OHLC)+"<br>("+fecha_ini_titulo+" - "+fecha_fin_titulo+")"},yaxis={"title": "Aceleración (cm/s²)"})

                elapsed_time = time() - start_time
                print("Tiempo Transcurrido crear OHLC: %0.1f seconds." % elapsed_time)

                #Variables que contienen los datos a mostrar en los indicadores de promedio, minimo y maximo
                promedio,maximo,minimo,count_max,count_min,fecha_ultimo_max,fecha_ultimo_min = datos.datos_mini_container(df,sensor)
            else:
                
                #colores para las graficas
                colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']
                count = 0
                new_count_de = 0
                new_count_in = 1
                new_df = pd.DataFrame()
                new_sensor = ''
                list_df = []

                #por cada sensor seleccionado se crean df 
                for sen in sensor_multi:
                    df = datos.datos_ace(fecha,ventana_tiempo,sen)
                    
                    #trace para el grafico OHLC
                    trace_principal.append(
                        go.Ohlc(
                            x=df['fecha'],
                            open=df['open'],
                            high=df['max'],
                            low=df['min'],
                            close=df['close'],
                            increasing_line_color= colors[new_count_in], 
                            decreasing_line_color= colors[new_count_de],
                            showlegend=True,
                            name= sen
                            )
                        )

                    count = count + 1
                    new_count_in = new_count_in + 2
                    new_count_de = new_count_de + 2

                    new_df = df
                    new_sensor = sen
                    #lista de dataframe para generar los indicadores resumen
                    list_df.append(df)

                #Variables que contienen los datos a mostrar en los indicadores de promedio, minimo y maximo
                promedio,maximo,minimo,count_max,count_min,fecha_ultimo_max,fecha_ultimo_min = datos.datos_mini_container(new_df,new_sensor)
                
                df = pd.concat(list_df, axis=0,ignore_index=True)
                fig_principal = go.Figure(data=trace_principal)
                #Aqui se agregan las lineas de control
                if (click_linea_inf > 0 and linea_control_inf != None) and (click_linea_sup > 0 and linea_control_sup != None):
                    trace_linea_inf,alert_inf,fecha_peak_inf = datos.lineas_control('inf',df,linea_control_inf,0)
                    trace_linea_sup,alert_sup,fecha_peak_sup = datos.lineas_control('sup',df,0,linea_control_sup)
                    trace_linea_inf.extend(trace_linea_sup)
                    trace_principal.extend(trace_linea_inf)
                    fig_principal = go.Figure(data=trace_principal)

                #Linea de control inferior
                elif click_linea_inf > 0 and linea_control_inf != None:
                    trace_linea_inf,alert_inf,fecha_peak_inf = datos.lineas_control('inf',df,linea_control_inf,0)
                    trace_principal.extend(trace_linea_inf)
                    fig_principal = go.Figure(data=trace_principal)
                #Linea de control superior       
                elif click_linea_sup > 0 and linea_control_sup != None:
                    trace_linea_sup,alert_sup,fecha_peak_sup = datos.lineas_control('sup',df,0,linea_control_sup)
                    trace_principal.extend(trace_linea_sup)
                    fig_principal = go.Figure(data=trace_principal)
    
                fig_principal.update(layout_xaxis_rangeslider_visible=False)
                titulo_OHLC = datos.titulo_OHLC(ventana_tiempo)
            
                fig_principal.update_layout(title={'text':"Datos cada "+str(datos.titulo_freq_datos(ventana_tiempo))+", durante "+str(titulo_OHLC)+"<br>("+fecha_ini_titulo+" - "+fecha_fin_titulo+")"},yaxis={"title": "Aceleración (cm/s²)"})

                

            
        elif tipo_sensor == 'weather-station':
            # La variable df y dff contiene el dataframe que se utiliza para generar el graficos OHLC
            df = datos.datos_ace(fecha,ventana_tiempo,'temperatura')

            # Aqui se crea el grafico OHLC para la temperatura
            trace_principal.append(
                go.Ohlc(
                    x=df['fecha'],
                    open=df['open'],
                    high=df['max'],
                    low=df['min'],
                    close=df['close'],
                    increasing_line_color= 'green', 
                    decreasing_line_color= 'red',
                    showlegend=True,
                    name= 'Temperatura'
                    )
                )

            fig_principal = go.Figure(data=trace_principal)
            #Aqui se agregan las lineas de control
            if (click_linea_inf > 0 and linea_control_inf != None) and (click_linea_sup > 0 and linea_control_sup != None):
                trace_linea_inf,alert_inf,fecha_peak_inf = datos.lineas_control('inf',df,linea_control_inf,0)
                trace_linea_sup,alert_sup,fecha_peak_sup = datos.lineas_control('sup',df,0,linea_control_sup)
                trace_linea_inf.extend(trace_linea_sup)
                trace_principal.extend(trace_linea_inf)
                fig_principal = go.Figure(data=trace_principal)

            #Linea de control inferior
            elif click_linea_inf > 0 and linea_control_inf != None:
                trace_linea_inf,alert_inf,fecha_peak_inf = datos.lineas_control('inf',df,linea_control_inf,0)
                trace_principal.extend(trace_linea_inf)
                fig_principal = go.Figure(data=trace_principal)
            #Linea de control superior       
            elif click_linea_sup > 0 and linea_control_sup != None:
                trace_linea_sup,alert_sup,fecha_peak_sup = datos.lineas_control('sup',df,0,linea_control_sup)
                trace_principal.extend(trace_linea_sup)
                fig_principal = go.Figure(data=trace_principal)

            fig_principal.update(layout_xaxis_rangeslider_visible=False)
            titulo_OHLC = datos.titulo_OHLC(ventana_tiempo)
            #titulos para ambos graficos OHLC
            fig_principal.update_layout(title={'text':"Datos cada "+str(datos.titulo_freq_datos(ventana_tiempo))+" de la Temperatura durante "+str(titulo_OHLC)+"<br>("+fecha_ini_titulo+" - "+fecha_fin_titulo+")"},yaxis={"title": "Temperatura (°C)"})

            #Se obtienen los datos de los indicadores resumen, en este caso pertenecientes a los datos de temperatura
            promedio,maximo,minimo,count_max,count_min,fecha_ultimo_max,fecha_ultimo_min = datos.datos_mini_container(df,'temperatura')
            
            
        return promedio,maximo,minimo,fecha_ultimo_max,fecha_ultimo_min,count_max,count_min,alert_sup,alert_inf,fecha_peak_sup,fecha_peak_inf,fig_principal

    #else:
    #    return '---','---','---','---','---','---','---','---','---','---','---',{}

@app.callback(Output('grafico-1','figure'),
              [Input('boton-aceptar', 'n_clicks')],
              [State('cantidad-sensores','value'),State('horas-disponibles', 'value'),State('elegir-tipo-sensor','value'),State('elegir-sensor','value'),
               State('elegir-sensor-multi','value'),State('elegir-fecha','date'),State('ventana-tiempo','value')])

def update_grafico_1(n_clicks,cantidad_sensores,hora,tipo_sensor,sensor,sensor_multi,fecha,ventana_tiempo):
    if fecha != None:
        if str(str(fecha).split(sep='T')[0]) == str(str(datos.fecha_inicial(tipo_sensor)).split(sep=' ')[0]):
            #fecha = dt.strptime(str(str(fecha).split(sep='T')[0]) + ' ' + str(str(datos.fecha_inicial()).split(sep=' ')[1]),'%Y-%m-%d %H:%M:%S')
            fecha = dt.strptime(str(str(fecha).split(sep='T')[0])+' '+datos.crear_hora(hora),'%Y-%m-%d %H:%M:%S')
        else:
            fecha = dt.strptime(str(str(fecha).split(sep='T')[0])+' '+datos.crear_hora(hora),'%Y-%m-%d %H:%M:%S')
    else:
        fecha = dt(2008,1,1,0,0,0)
    #Se inicializan variables
    df = pd.DataFrame()
    fig_1 = go.Figure()
    if n_clicks >= 0:
        fecha_ini_titulo,fecha_fin_titulo = datos.fecha_titulo(fecha,ventana_tiempo) 
        #Dependiendo del tipo de sensor se crean visualizaciones distintas
        if tipo_sensor == 'acelerometro':
            if cantidad_sensores == '1-sensor':
                # La variable df contiene el dataframe que se utiliza para generar los graficos OHLC e histograma
                start_time = time()
                df = datos.datos_ace(fecha,ventana_tiempo,sensor)
                elapsed_time = time() - start_time
                print("Tiempo Transcurrido crear DF: %0.1f seconds." % elapsed_time)

                #Aqui se crea el grafico boxplot
                start_time = time()
                repeat = 12
                #Cuando la ventana de tiempo es de 1 hora o 1 dia se obtinen 12 box en cambio si es de 7 dias o 14 se obtienen 14 por eso cambia el valor de repeat
                if ventana_tiempo == '12S' or ventana_tiempo == '288S':
                    repeat = 12
                else:
                    repeat = 14
                # bucle que genera cada box 
                for i in range(repeat):
                    if i == 0: 
                        vars()['df'+str(i)],vars()['ultimo'+str(i)] = datos.datos_box(fecha,ventana_tiempo,sensor)
                        fig_1.add_trace(go.Box(y=vars()['df'+str(i)][vars()['ultimo'+str(i)]], name=str(vars()['ultimo'+str(i)]),boxpoints='suspectedoutliers',showlegend=False))
                    else:
                        vars()['df'+str(i)],vars()['ultimo'+str(i)] = datos.datos_box(vars()['ultimo'+str(i-1)],ventana_tiempo,sensor)
                        fig_1.add_trace(go.Box(y=vars()['df'+str(i)][vars()['ultimo'+str(i)]], name=str(vars()['ultimo'+str(i)]),boxpoints='suspectedoutliers',showlegend=False))
        
                elapsed_time = time() - start_time
                print("Tiempo Transcurrido crear BOX: %0.1f seconds." % elapsed_time)

                # Titulos para el grafico OHLC y Boxplot
                titulo_box = datos.titulo_box(ventana_tiempo)
                titulo_OHLC = datos.titulo_OHLC(ventana_tiempo)
   
                fig_1.update_layout(title="Promedio de datos cada "+str(titulo_box)+" del "+str(datos.nombres_ace()[sensor])+" durante "+str(titulo_OHLC)+"<br>("+fecha_ini_titulo+" - "+fecha_fin_titulo+")",yaxis={"title": "Aceleración (cm/s²)"})
                
            else:
                #Listas que conteneran cada trace generado por cada dataframe creado para poder visualizarlos en una grafica
                trace_sec1 = []
                
                #Para el grafico boxplot
                repeat = 12
                #Cuando la ventana de tiempo es de 1 hora o 1 dia se obtinen 12 box en cambio si es de 7 dias o 14 se obtienen 14 por eso cambia el valor de repeat
                if ventana_tiempo == '12S' or ventana_tiempo == '288S':
                    repeat = 12
                else:
                    repeat = 14
                #colores para las graficas
                colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']
                count = 0

                #por cada sensor seleccionado se crean df 
                for sen in sensor_multi:
                    # bucle que genera cada box para guardarlo en el trace
                    for i in range(repeat):
                        if i == 0: 
                            vars()['df'+str(i)],vars()['ultimo'+str(i)] = datos.datos_box(fecha,ventana_tiempo,sen)
                            trace_sec1.append(
                                go.Box(
                                    y=vars()['df'+str(i)][vars()['ultimo'+str(i)]], 
                                    name=str(vars()['ultimo'+str(i)]),
                                    boxpoints='suspectedoutliers',
                                    showlegend=False,
                                    marker_color = colors[count]
                                )
                            )
                        else:
                            vars()['df'+str(i)],vars()['ultimo'+str(i)] = datos.datos_box(vars()['ultimo'+str(i-1)],ventana_tiempo,sen)
                            trace_sec1.append(
                                go.Box(
                                    y=vars()['df'+str(i)][vars()['ultimo'+str(i)]], 
                                    name=str(vars()['ultimo'+str(i)]),
                                    boxpoints='suspectedoutliers',
                                    showlegend=False,
                                    marker_color = colors[count]
                                )
                            )

                    count = count + 1

                fig_1 = go.Figure(data=trace_sec1)
                
                titulo_OHLC = datos.titulo_OHLC(ventana_tiempo)

                titulo_box = datos.titulo_box(ventana_tiempo)
            
   
                fig_1.update_layout(title="Promedio de datos cada "+str(titulo_box)+", durante "+str(titulo_OHLC)+"<br>("+fecha_ini_titulo+" - "+fecha_fin_titulo+")",yaxis={"title": "Aceleración (cm/s²)"})
        elif tipo_sensor == 'weather-station':
            # La variable df contiene el dataframe que se utiliza para generar el graficos OHLC
            df = datos.datos_ace(dt(2008,4,1,0,38,3),ventana_tiempo,'humedad')

            # Aqui se crea el grafico OHLC para la humedad
            fig_1.add_trace(
                go.Ohlc(
                    x=df['fecha'],
                    open=df['open'],
                    high=df['max'],
                    low=df['min'],
                    close=df['close'],
                    increasing_line_color= 'blue', 
                    decreasing_line_color= 'red',
                    showlegend=True,
                    name= 'Humedad'
                    )
                )
 
            fig_1.update(layout_xaxis_rangeslider_visible=False)
            titulo_OHLC = datos.titulo_OHLC(ventana_tiempo)
            #titulos para ambos graficos OHLC

            fig_1.update_layout(title={'text':"Datos cada "+str(datos.titulo_freq_datos(ventana_tiempo))+" de la Humedad durante "+str(titulo_OHLC)+"<br>("+fecha_ini_titulo+" - "+fecha_fin_titulo+")"},yaxis={"title": "Humedad"})

        return fig_1

    #else:
    #    return {}

@app.callback(Output('grafico-2','figure'),
              [Input('boton-aceptar', 'n_clicks')],
              [State('cantidad-sensores','value'),State('horas-disponibles', 'value'),State('elegir-tipo-sensor','value'),State('elegir-sensor','value'),
               State('elegir-sensor-multi','value'),State('elegir-fecha','date'),State('ventana-tiempo','value')])

def update_grafico_2(n_clicks,cantidad_sensores,hora,tipo_sensor,sensor,sensor_multi,fecha,ventana_tiempo):
    if fecha != None:
        if str(str(fecha).split(sep='T')[0]) == str(str(datos.fecha_inicial(tipo_sensor)).split(sep=' ')[0]):
            #fecha = dt.strptime(str(str(fecha).split(sep='T')[0]) + ' ' + str(str(datos.fecha_inicial()).split(sep=' ')[1]),'%Y-%m-%d %H:%M:%S')
            fecha = dt.strptime(str(str(fecha).split(sep='T')[0])+' '+datos.crear_hora(hora),'%Y-%m-%d %H:%M:%S')
        else:
            fecha = dt.strptime(str(str(fecha).split(sep='T')[0])+' '+datos.crear_hora(hora),'%Y-%m-%d %H:%M:%S')
    else:
        fecha = dt(2008,1,1,0,0,0)
    #Se inicializan variables
    df = pd.DataFrame()
    fig_2 = go.Figure()
    if n_clicks >= 0:
        fecha_ini_titulo,fecha_fin_titulo = datos.fecha_titulo(fecha,ventana_tiempo) 
        #Dependiendo del tipo de sensor se crean visualizaciones distintas
        if tipo_sensor == 'weather-station':
            
            #Aqui se crea el histograma circular que contine datos de la direccion y velocidad del viento
            dir = datos.datos_ace(dt(2008,4,1,0,38,3),ventana_tiempo,'dir_viento')['dir_viento'].tolist()
            vel = datos.datos_ace(dt(2008,4,1,0,38,3),ventana_tiempo,'vel_viento')['vel_viento'].tolist()

            tmp1 = collections.Counter(dir)
            ini,fin = datos.rangos(tmp1)

            rr,tt = datos.datos_por_rango(pd.DataFrame({'dir_viento': dir,'vel_viento':vel}),ini,fin)
            dff = pd.DataFrame({'Dirección': tt,'Velocidad (m/s)':rr})
            fig_2 = px.bar_polar(dff, r="Velocidad (m/s)", theta="Dirección",color_discrete_sequence= px.colors.sequential.Plasma_r)
            titulo_OHLC = datos.titulo_OHLC(ventana_tiempo)

            fig_2.update_layout(title={'text':"Dirección y Velocidad (m/s) del viento durante "+str(titulo_OHLC)+" "})
        elif tipo_sensor == 'acelerometro':
            if cantidad_sensores == '1-sensor':
                # La variable df contiene el dataframe que se utiliza para generar el histograma
                # Aqui se crea el histograma
                start_time = time()
                df = datos.datos_ace(fecha,ventana_tiempo,sensor)
                
                start_time = time()

                fig_2 = go.Figure(data=[go.Histogram(x=df[sensor],showlegend=False)])

                elapsed_time = time() - start_time
                print("Tiempo Transcurrido crear Histograma: %0.1f seconds." % elapsed_time)
                titulo_OHLC = datos.titulo_OHLC(ventana_tiempo)

                fig_2.update_layout(title="Frecuencia de datos cada "+str(datos.titulo_freq_datos(ventana_tiempo))+" del "+str(datos.nombres_ace()[sensor])+"<br>durante "+str(titulo_OHLC)+"<br>("+fecha_ini_titulo+" - "+fecha_fin_titulo+")",yaxis={"title": "Frecuencia (N° de Datos)"}, xaxis={"title": "Aceleración (cm/s²)"},bargap=0.1,)
            else:
                #Listas que conteneran cada trace generado por cada dataframe creado para poder visualizarlos en una grafica
                trace_sec2 = []
                
                
                #colores para las graficas
                colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']
                count = 0

                #por cada sensor seleccionado se crean df 
                for sen in sensor_multi:
                    df = datos.datos_ace(fecha,ventana_tiempo,sen)

                    # Aqui se crea el histograma
                    trace_sec2.append(
                        go.Histogram(
                            x=df[sen],
                            showlegend=True,
                            marker_color = colors[count],
                            name=sen
                        )
                    )
                    count = count + 1
                
                fig_2 = go.Figure(data=trace_sec2)
                
                titulo_OHLC = datos.titulo_OHLC(ventana_tiempo)
            
                fig_2.update_layout(title="Frecuencia de datos cada "+str(datos.titulo_freq_datos(ventana_tiempo))+"<br>durante "+str(titulo_OHLC)+"<br>("+fecha_ini_titulo+" - "+fecha_fin_titulo+")",yaxis={"title": "Frecuencia (N° de Datos)"}, xaxis={"title": "Aceleración (cm/s²)"},bargap=0.1,)

        return fig_2

    #else:
    #    return {}


'''
# Funcion principal que actualiza los graficos, ademas de agregar o quitar las lineas de control al grafico principal
# y agregar los valores a los indicadores
@app.callback([Output('valor-promedio', 'children'),Output('valor-max', 'children'),Output('valor-min', 'children'),Output('fecha-valor-max','children'),
               Output('fecha-valor-min','children'),Output('num-valor-max','children'),Output('num-valor-min','children'),Output('alert-sup','children'),
               Output('alert-inf','children'),Output('fecha-alert-sup','children'),Output('fecha-alert-inf','children'),Output('grafico-2','figure'),
               Output('grafico-principal','figure'),Output('grafico-1','figure')],
              [Input('boton-aceptar', 'n_clicks'),Input('boton-linea-sup', 'n_clicks'),Input('boton-linea-inf', 'n_clicks')],
              [State('cantidad-sensores','value'),State('horas-disponibles', 'value'),State('elegir-tipo-sensor','value'),State('elegir-sensor','value'),State('elegir-sensor-multi','value'),State('elegir-fecha','date'),State('ventana-tiempo','value'),
               State('linea-control-sup','value'),State('linea-control-inf','value')])

def update_graficos(n_clicks,click_linea_sup,click_linea_inf,cantidad_sensores,hora,tipo_sensor,sensor,sensor_multi,fecha,ventana_tiempo,linea_control_sup,linea_control_inf):
    if fecha != None:
        if str(str(fecha).split(sep='T')[0]) == str(str(datos.fecha_inicial(tipo_sensor)).split(sep=' ')[0]):
            #fecha = dt.strptime(str(str(fecha).split(sep='T')[0]) + ' ' + str(str(datos.fecha_inicial()).split(sep=' ')[1]),'%Y-%m-%d %H:%M:%S')
            fecha = dt.strptime(str(str(fecha).split(sep='T')[0])+' '+datos.crear_hora(hora),'%Y-%m-%d %H:%M:%S')
        else:
            fecha = dt.strptime(str(str(fecha).split(sep='T')[0])+' '+datos.crear_hora(hora),'%Y-%m-%d %H:%M:%S')
    else:
        fecha = dt(2008,1,1,0,0,0)
    #Se inicializan variables
    df = pd.DataFrame()
    fig_principal,fig_1,fig_2 = go.Figure(),go.Figure(),go.Figure()
    alert_inf, alert_sup, fecha_peak_sup, fecha_peak_inf = '---','---','---','---'
    promedio,maximo,minimo,count_max,count_min,fecha_ultimo_max,fecha_ultimo_min = '---','---','---','---','---','---','---'
    if n_clicks >= 0:
        fecha_ini_titulo,fecha_fin_titulo = datos.fecha_titulo(fecha,ventana_tiempo) 
        #Dependiendo del tipo de sensor se crean visualizaciones distintas
        if tipo_sensor == 'acelerometro':
            
            if cantidad_sensores == '1-sensor':
                # La variable df contiene el dataframe que se utiliza para generar los graficos OHLC e histograma
                start_time = time()
                df = datos.datos_ace(fecha,ventana_tiempo,sensor)
                elapsed_time = time() - start_time
                print("Tiempo Transcurrido crear DF: %0.1f seconds." % elapsed_time)
                # Aqui se crea el grafico OHLC
                start_time = time()
                fig_principal = go.Figure(data=go.Ohlc(x=df['fecha'],
                    open=df['open'],
                    high=df['max'],
                    low=df['min'],
                    close=df['close'],
                    increasing_line_color= 'green', 
                    decreasing_line_color= 'red',
                    showlegend=False))
                fig_principal.update(layout_xaxis_rangeslider_visible=False)
                titulo_OHLC = datos.titulo_OHLC(ventana_tiempo)
                fig_principal.update_layout(title={'text':"Datos cada "+str(datos.titulo_freq_datos(ventana_tiempo))+" del "+str(datos.nombres_ace()[sensor])+" durante "+str(titulo_OHLC)+"<br>("+fecha_ini_titulo+" - "+fecha_fin_titulo+")"},yaxis={"title": "Aceleración (cm/s²)"})

                elapsed_time = time() - start_time
                print("Tiempo Transcurrido crear OHLC: %0.1f seconds." % elapsed_time)

                #Aqui se crea el grafico boxplot
                start_time = time()
                repeat = 12
                #Cuando la ventana de tiempo es de 1 hora o 1 dia se obtinen 12 box en cambio si es de 7 dias o 14 se obtienen 14 por eso cambia el valor de repeat
                if ventana_tiempo == '12S' or ventana_tiempo == '288S':
                    repeat = 12
                else:
                    repeat = 14
                # bucle que genera cada box 
                for i in range(repeat):
                    if i == 0: 
                        vars()['df'+str(i)],vars()['ultimo'+str(i)] = datos.datos_box(fecha,ventana_tiempo,sensor)
                        fig_1.add_trace(go.Box(y=vars()['df'+str(i)][vars()['ultimo'+str(i)]], name=str(vars()['ultimo'+str(i)]),boxpoints='suspectedoutliers',showlegend=False))
                    else:
                        vars()['df'+str(i)],vars()['ultimo'+str(i)] = datos.datos_box(vars()['ultimo'+str(i-1)],ventana_tiempo,sensor)
                        fig_1.add_trace(go.Box(y=vars()['df'+str(i)][vars()['ultimo'+str(i)]], name=str(vars()['ultimo'+str(i)]),boxpoints='suspectedoutliers',showlegend=False))
        
                elapsed_time = time() - start_time
                print("Tiempo Transcurrido crear BOX: %0.1f seconds." % elapsed_time)

                # Aqui se crea el histograma
                start_time = time()

                fig_2 = go.Figure(data=[go.Histogram(x=df[sensor],showlegend=False)])

                elapsed_time = time() - start_time
                print("Tiempo Transcurrido crear Histograma: %0.1f seconds." % elapsed_time)

                # Titulos para el grafico OHLC y Boxplot
                titulo_box = datos.titulo_box(ventana_tiempo)
            
   
                fig_1.update_layout(title="Promedio de datos cada "+str(titulo_box)+" del "+str(datos.nombres_ace()[sensor])+" durante "+str(titulo_OHLC)+"<br>("+fecha_ini_titulo+" - "+fecha_fin_titulo+")",yaxis={"title": "Aceleración (cm/s²)"})
                fig_2.update_layout(title="Frecuencia de datos cada "+str(datos.titulo_freq_datos(ventana_tiempo))+" del "+str(datos.nombres_ace()[sensor])+"<br>durante "+str(titulo_OHLC)+"<br>("+fecha_ini_titulo+" - "+fecha_fin_titulo+")",yaxis={"title": "Frecuencia (N° de Datos)"}, xaxis={"title": "Aceleración (cm/s²)"},bargap=0.1,)

                #Variables que contienen los datos a mostrar en los indicadores de promedio, minimo y maximo
                promedio,maximo,minimo,count_max,count_min,fecha_ultimo_max,fecha_ultimo_min = datos.datos_mini_container(df,sensor)

            else:

                #Listas que conteneran cada trace generado por cada dataframe creado para poder visualizarlos en una grafica
                trace_principal = []
                trace_sec1 = []
                trace_sec2 = []
                
                #Para el grafico boxplot
                repeat = 12
                #Cuando la ventana de tiempo es de 1 hora o 1 dia se obtinen 12 box en cambio si es de 7 dias o 14 se obtienen 14 por eso cambia el valor de repeat
                if ventana_tiempo == '12S' or ventana_tiempo == '288S':
                    repeat = 12
                else:
                    repeat = 14
                #colores para las graficas
                colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']
                count = 0
                new_count_de = 0
                new_count_in = 1
                new_df = pd.DataFrame()
                new_sensor = ''
                list_df = []

                #por cada sensor seleccionado se crean df 
                for sen in sensor_multi:
                    df = datos.datos_ace(fecha,ventana_tiempo,sen)
                    
                    #trace para el grafico OHLC
                    trace_principal.append(
                        go.Ohlc(
                            x=df['fecha'],
                            open=df['open'],
                            high=df['max'],
                            low=df['min'],
                            close=df['close'],
                            increasing_line_color= colors[new_count_in], 
                            decreasing_line_color= colors[new_count_de],
                            showlegend=True,
                            name= sen
                            )
                        )

                    # bucle que genera cada box para guardarlo en el trace
                    for i in range(repeat):
                        if i == 0: 
                            vars()['df'+str(i)],vars()['ultimo'+str(i)] = datos.datos_box(fecha,ventana_tiempo,sen)
                            trace_sec1.append(
                                go.Box(
                                    y=vars()['df'+str(i)][vars()['ultimo'+str(i)]], 
                                    name=str(vars()['ultimo'+str(i)]),
                                    boxpoints='suspectedoutliers',
                                    showlegend=False,
                                    marker_color = colors[count]
                                )
                            )
                        else:
                            vars()['df'+str(i)],vars()['ultimo'+str(i)] = datos.datos_box(vars()['ultimo'+str(i-1)],ventana_tiempo,sen)
                            trace_sec1.append(
                                go.Box(
                                    y=vars()['df'+str(i)][vars()['ultimo'+str(i)]], 
                                    name=str(vars()['ultimo'+str(i)]),
                                    boxpoints='suspectedoutliers',
                                    showlegend=False,
                                    marker_color = colors[count]
                                )
                            )

                    # Aqui se crea el histograma
                    trace_sec2.append(
                        go.Histogram(
                            x=df[sen],
                            showlegend=True,
                            marker_color = colors[count],
                            name=sen
                        )
                    )
                    count = count + 1
                    new_count_in = new_count_in + 2
                    new_count_de = new_count_de + 2

                    new_df = df
                    new_sensor = sen
                    #lista de dataframe para generar los indicadores resumen
                    list_df.append(df)

                

                #Variables que contienen los datos a mostrar en los indicadores de promedio, minimo y maximo
                promedio,maximo,minimo,count_max,count_min,fecha_ultimo_max,fecha_ultimo_min = datos.datos_mini_container(new_df,new_sensor)

                fig_principal = go.Figure(data=trace_principal)
                fig_1 = go.Figure(data=trace_sec1)
                fig_2 = go.Figure(data=trace_sec2)
                fig_principal.update(layout_xaxis_rangeslider_visible=False)
                titulo_OHLC = datos.titulo_OHLC(ventana_tiempo)

                # Titulos para el grafico OHLC y Boxplot
                titulo_box = datos.titulo_box(ventana_tiempo)
            
   
                fig_1.update_layout(title="Promedio de datos cada "+str(titulo_box)+", durante "+str(titulo_OHLC)+"<br>("+fecha_ini_titulo+" - "+fecha_fin_titulo+")",yaxis={"title": "Aceleración (cm/s²)"})
                fig_2.update_layout(title="Frecuencia de datos cada "+str(datos.titulo_freq_datos(ventana_tiempo))+"<br>durante "+str(titulo_OHLC)+"<br>("+fecha_ini_titulo+" - "+fecha_fin_titulo+")",yaxis={"title": "Frecuencia (N° de Datos)"}, xaxis={"title": "Aceleración (cm/s²)"},bargap=0.1,)

                fig_principal.update_layout(title={'text':"Datos cada "+str(datos.titulo_freq_datos(ventana_tiempo))+", durante "+str(titulo_OHLC)+"<br>("+fecha_ini_titulo+" - "+fecha_fin_titulo+")"},yaxis={"title": "Aceleración (cm/s²)"})

                df = pd.concat(list_df, axis=0,ignore_index=True)
            
            

            #Aqui se agregan las lineas de control
            #Linea de control inferior
            if click_linea_inf > 0 and linea_control_inf != None:
                y = []

                #Bucle que agrega una linea recta en el valor ingresado 
                for i in range(len(df["fecha"])):
                    y.append(float(linea_control_inf))
                fig_principal.add_trace(go.Scattergl(x=df["fecha"], y=y, mode='lines',line=dict(color='purple'),name='Linea Inferior',showlegend=False))
                # Calculo de peaks
                if(float(linea_control_inf) < 0):
                    peak = []
                    columnas = ['min','max','open','close']
                    # se calculan los peaks para cada tipo de dato que contine el grafico OHLC
                    peaks_inf = datos.peak(-(df['min']),-(linea_control_inf))
                    peaks_sup = datos.peak(-(df['max']),-(linea_control_inf))
                    peaks_ini = datos.peak(-(df['open']),-(linea_control_inf))
                    peaks_fin = datos.peak(-(df['close']),-(linea_control_inf))

                    peak.append(peaks_inf)
                    peak.append(peaks_sup)
                    peak.append(peaks_ini)
                    peak.append(peaks_fin)    

                    alert_inf = len(peaks_inf) + len(peaks_sup) + len(peaks_ini) + len(peaks_fin)
                    alert_inf = str(alert_inf) + " peaks"
                    #Obtine la fecha del ultimo peak detectado
                    fecha_peak_inf = datos.obtener_fecha_alerta(df,peaks_inf,peaks_sup,peaks_ini,peaks_fin)
                
                    #Se marcan en el grafico OHLC los peaks detectados
                    for peak,col in zip(peak,columnas):
                        fig_principal.add_trace(go.Scatter(
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
            #Linea de control superior       
            if click_linea_sup > 0 and linea_control_sup != None:
                y = []

                #Bucle que agrega una linea recta en el valor ingresado 
                for i in range(len(df["fecha"])):
                    y.append(float(linea_control_sup))
                fig_principal.add_trace(go.Scattergl(x=df["fecha"], y=y, mode='lines',line=dict(color='purple'),name='Linea Superior',showlegend=False))

                # Calculo de peaks
                if(float(linea_control_sup) > 0):
                    peak = []
                    columnas = ['min','max','open','close']

                    # se calculan los peaks para cada tipo de dato que contine el grafico OHLC
                    peaks_inf = datos.peak(df['min'],linea_control_sup)
                    peaks_sup = datos.peak(df['max'],linea_control_sup)
                    peaks_ini = datos.peak(df['open'],linea_control_sup)
                    peaks_fin = datos.peak(df['close'],linea_control_sup)

                    peak.append(peaks_inf)
                    peak.append(peaks_sup)
                    peak.append(peaks_ini)
                    peak.append(peaks_fin)    

                    alert_sup = len(peaks_inf) + len(peaks_sup) + len(peaks_ini) + len(peaks_fin)
                    alert_sup = str(alert_sup) + " peaks"
                    #Obtine la fecha del ultimo peak detectado
                    fecha_peak_sup = datos.obtener_fecha_alerta(df,peaks_inf,peaks_sup,peaks_ini,peaks_fin)

                    #Se marcan en el grafico OHLC los peaks detectados
                    for peak,col in zip(peak,columnas):
                        fig_principal.add_trace(go.Scatter(
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

        elif tipo_sensor == 'weather-station':
            # La variable df y dff contiene el dataframe que se utiliza para generar el graficos OHLC
            df = datos.datos_ace(fecha,ventana_tiempo,'temperatura')
            dff = datos.datos_ace(fecha,ventana_tiempo,'humedad')

            # Aqui se crea el grafico OHLC para la temperatura
            fig_principal.add_trace(
                go.Ohlc(
                    x=df['fecha'],
                    open=df['open'],
                    high=df['max'],
                    low=df['min'],
                    close=df['close'],
                    increasing_line_color= 'green', 
                    decreasing_line_color= 'red',
                    showlegend=True,
                    name= 'Temperatura'
                    )
                )
            # Aqui se crea el grafico OHLC para la humedad
            fig_1.add_trace(
                go.Ohlc(
                    x=dff['fecha'],
                    open=dff['open'],
                    high=dff['max'],
                    low=dff['min'],
                    close=dff['close'],
                    increasing_line_color= 'blue', 
                    decreasing_line_color= 'red',
                    showlegend=True,
                    name= 'Humedad'
                    )
                )

            fig_principal.update(layout_xaxis_rangeslider_visible=False)
            fig_1.update(layout_xaxis_rangeslider_visible=False)
            titulo_OHLC = datos.titulo_OHLC(ventana_tiempo)
            #titulos para ambos graficos OHLC
            fig_principal.update_layout(title={'text':"Datos cada "+str(datos.titulo_freq_datos(ventana_tiempo))+" de la Temperatura durante "+str(titulo_OHLC)+"<br>("+fecha_ini_titulo+" - "+fecha_fin_titulo+")"},yaxis={"title": "Temperatura (°C)"})
            fig_1.update_layout(title={'text':"Datos cada "+str(datos.titulo_freq_datos(ventana_tiempo))+" de la Humedad durante "+str(titulo_OHLC)+"<br>("+fecha_ini_titulo+" - "+fecha_fin_titulo+")"},yaxis={"title": "Humedad"})

            #Aqui se crea el histograma circular que contine datos de la direccion y velocidad del viento
            dir = datos.datos_ace(fecha,ventana_tiempo,'dir_viento')['dir_viento'].tolist()
            vel = datos.datos_ace(fecha,ventana_tiempo,'vel_viento')['vel_viento'].tolist()

            tmp1 = collections.Counter(dir)
            ini,fin = datos.rangos(tmp1)

            rr,tt = datos.datos_por_rango(pd.DataFrame({'dir_viento': dir,'vel_viento':vel}),ini,fin)
            dff = pd.DataFrame({'Dirección': tt,'Velocidad (m/s)':rr})
            fig_2 = px.bar_polar(dff, r="Velocidad (m/s)", theta="Dirección",color_discrete_sequence= px.colors.sequential.Plasma_r)

            fig_2.update_layout(title={'text':"Dirección y Velocidad (m/s) del viento durante "+str(titulo_OHLC)+" "})

            #Se obtienen los datos de los indicadores resumen, en este caso pertenecientes a los datos de temperatura
            promedio,maximo,minimo,count_max,count_min,fecha_ultimo_max,fecha_ultimo_min = datos.datos_mini_container(df,'temperatura')
            
            #Aqui se agregan las lineas de control
            #Linea de control inferior
            if click_linea_inf > 0 and linea_control_inf != None:
                y = []

                #Bucle que agrega una linea recta en el valor ingresado 
                for i in range(len(df["fecha"])):
                    y.append(float(linea_control_inf))
                fig_principal.add_trace(go.Scattergl(x=df["fecha"], y=y, mode='lines',line=dict(color='purple'),name='Linea Inferior',showlegend=False))
                # Calculo de peaks
                if(float(linea_control_inf) < 0):
                    peak = []
                    columnas = ['min','max','open','close']
                    # se calculan los peaks para cada tipo de dato que contine el grafico OHLC
                    peaks_inf = datos.peak(-(df['min']),-(linea_control_inf))
                    peaks_sup = datos.peak(-(df['max']),-(linea_control_inf))
                    peaks_ini = datos.peak(-(df['open']),-(linea_control_inf))
                    peaks_fin = datos.peak(-(df['close']),-(linea_control_inf))

                    peak.append(peaks_inf)
                    peak.append(peaks_sup)
                    peak.append(peaks_ini)
                    peak.append(peaks_fin)    

                    alert_inf = len(peaks_inf) + len(peaks_sup) + len(peaks_ini) + len(peaks_fin)
                    alert_inf = str(alert_inf) + " peaks"
                    #Obtine la fecha del ultimo peak detectado
                    fecha_peak_inf = datos.obtener_fecha_alerta(df,peaks_inf,peaks_sup,peaks_ini,peaks_fin)
                
                    #Se marcan en el grafico OHLC los peaks detectados
                    for peak,col in zip(peak,columnas):
                        fig_principal.add_trace(go.Scatter(
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
            #Linea de control superior       
            if click_linea_sup > 0 and linea_control_sup != None:
                y = []

                #Bucle que agrega una linea recta en el valor ingresado 
                for i in range(len(df["fecha"])):
                    y.append(float(linea_control_sup))
                fig_principal.add_trace(go.Scattergl(x=df["fecha"], y=y, mode='lines',line=dict(color='purple'),name='Linea Superior',showlegend=False))

                # Calculo de peaks
                if(float(linea_control_sup) > 0):
                    peak = []
                    columnas = ['min','max','open','close']

                    # se calculan los peaks para cada tipo de dato que contine el grafico OHLC
                    peaks_inf = datos.peak(df['min'],linea_control_sup)
                    peaks_sup = datos.peak(df['max'],linea_control_sup)
                    peaks_ini = datos.peak(df['open'],linea_control_sup)
                    peaks_fin = datos.peak(df['close'],linea_control_sup)

                    peak.append(peaks_inf)
                    peak.append(peaks_sup)
                    peak.append(peaks_ini)
                    peak.append(peaks_fin)    

                    alert_sup = len(peaks_inf) + len(peaks_sup) + len(peaks_ini) + len(peaks_fin)
                    alert_sup = str(alert_sup) + " peaks"
                    #Obtine la fecha del ultimo peak detectado
                    fecha_peak_sup = datos.obtener_fecha_alerta(df,peaks_inf,peaks_sup,peaks_ini,peaks_fin)

                    #Se marcan en el grafico OHLC los peaks detectados
                    for peak,col in zip(peak,columnas):
                        fig_principal.add_trace(go.Scatter(
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


        #elif tipo_sensor == 'strain-gauge':
        #    fig_principal,fig_1,fig_2 = {},{},{}
        #    alert_inf, alert_sup, fecha_peak_sup, fecha_peak_inf = '---','---','---','---'
        #elif tipo_sensor == 'inclinometro':
        #    fig_principal,fig_1,fig_2 = {},{},{}
        #    alert_inf, alert_sup, fecha_peak_sup, fecha_peak_inf = '---','---','---','---'
        #elif tipo_sensor == 'lvdt':
        #    fig_principal,fig_1,fig_2 = {},{},{}
        #    alert_inf, alert_sup, fecha_peak_sup, fecha_peak_inf = '---','---','---','---'

        
        return promedio,maximo,minimo,fecha_ultimo_max,fecha_ultimo_min,count_max,count_min,alert_sup,alert_inf,fecha_peak_sup,fecha_peak_inf,fig_2,fig_principal,fig_1

    else:
        return '---','---','---','---','---','---','---','---','---','---','---',{},{},{}
'''

#Funcion para crear los reportes
@app.callback(Output('retorno-reportes','children'),
             [Input('boton-generar-reporte','n_clicks')],[State('grafico-principal','figure'),State('grafico-1','figure'),State('grafico-2','figure'),
              State('valor-promedio', 'children'),State('valor-max', 'children'),State('valor-min', 'children'),State('fecha-valor-max','children'),
              State('fecha-valor-min','children'),State('num-valor-max','children'),State('num-valor-min','children'),State('alert-sup','children'),
              State('alert-inf','children'),State('fecha-alert-sup','children'),State('fecha-alert-inf','children'),State('elegir-sensor','value'),
              State('elegir-sensor-multi','value'),State('elegir-fecha','date'),State('ventana-tiempo','value'),State('linea-control-sup','value'),
              State('linea-control-inf','value'),State('horas-disponibles', 'value'),State('cantidad-sensores','value')])

def crear_reporte(clicks, fig_principal,fig_sec1,fig_sec2,valor_promedio,valor_max,valor_min,fecha_valor_max,fecha_valor_min,num_valor_max,num_valor_min,alert_sup,alert_inf,fecha_alert_sup,fecha_alert_inf,sensor,sensor_multi,fecha,ventana_tiempo,valor_linea_control_sup,valor_linea_control_inf,hora,cantidad_sensores):
    
    if clicks > 0:
        datos.generar_reportes(go.Figure(fig_principal),go.Figure(fig_sec1),go.Figure(fig_sec2),valor_promedio,valor_max,valor_min,fecha_valor_max,fecha_valor_min,num_valor_max,num_valor_min,alert_sup,alert_inf,fecha_alert_sup,fecha_alert_inf,sensor,sensor_multi,fecha,ventana_tiempo,valor_linea_control_sup,valor_linea_control_inf,hora,cantidad_sensores)
    return 'uno'


# Main
if __name__ == "__main__":
    #PORT = 8000
    #ADDRESS = '11.11.11.11'
    #app.run_server(port=PORT,host=ADDRESS,debug=False, dev_tools_ui=False, dev_tools_props_check=False)
    #app.run_server(debug=False, dev_tools_ui=False, dev_tools_props_check=False)
    #app.run_server(debug=True,dev_tools_ui=False, dev_tools_props_check=False)
    app.run_server(debug=True)