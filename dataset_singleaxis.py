from bokeh.models.tools import HoverTool
from bokeh.plotting import figure, output_file
import pandas as pd
from bokeh.io import save

directory = "/home/charmeleon/Documents/INSIVUMEH/dataset/output/"
df = pd.read_csv('database.csv', header=1, delimiter=',')

# convertir la columna FECHA a formato datetime y ordenar el dataframe
df['FECHA'] = pd.to_datetime(df['FECHA'], format="%d/%m/%Y")
df = df.sort_values("FECHA")

# Obtener la fecha más reciente en el dataframe
latest_date = df['FECHA'].max()

# Obtener el primer día del último mes
first_day_of_last_month = latest_date.replace(day=1) - pd.DateOffset(months=1)

# Filtrar los datos para que solo incluyan los del último mes
last_month_data = df[df['FECHA'] >= first_day_of_last_month]

#Estaciones
ID = {"CHAMPERICO FEGUA": "INS110701CV", "COBAN": "INS160101CV", "ESQUIPULAS": "INS200701CV", 
      "FLORES AEROPUERTO": "INS170101CV", "LA AURORA": "INS010102CV"}

# ...

for k in ID:
    # filtrar los datos por la estación (k)
    gk = last_month_data.groupby(['VARIABLE'])
    precip = gk.get_group('LLUVIA')[k]
    temp = gk.get_group('TMED')[k]
    tempmin = gk.get_group('TMIN')[k]
    tempmax = gk.get_group('TMAX')[k]
    fecha = gk.get_group('LLUVIA')['FECHA']
    
    # configurar la figura
    fig = figure(x_axis_type='datetime', title=k, plot_height=400, plot_width=900, toolbar_location='below',
                 y_axis_label="Valor", y_range=(-5, 90), background_fill_color='white', background_fill_alpha=0.6,
                 tools="save,pan,box_zoom,reset,wheel_zoom")

    # agregar las líneas y los círculos de temperatura
    fig.line(fecha, precip, line_color='navy', line_width=1, legend_label='Precipitación (mm)',
             name='precip')
    
    fig.line(fecha, temp, line_color='seagreen', line_width=1, line_dash='dashed', legend_label='Temperatura media C', 
             name='temp')
    fig.circle(fecha, tempmin, fill_color='deepskyblue', line_color='blue', size=2,
               legend_label='Temperatura min C', name='tempmin')
    fig.circle(fecha, tempmax, fill_color='firebrick', line_color='red', size=2,
               legend_label='Temperatura max C', name='tempmax')

    fig.legend.location = 'top_left'
    fig.title.text_font_size = '15pt'
    fig.yaxis.axis_label_text_font_size = "15pt"
    
    # agregar etiquetas a las líneas y los círculos
    tooltips = [
        ("Valor", "@y"),
        ("Fecha", "@x{%F}")
    ]
    formatters = {
        '@x': 'datetime'
    }
    hover = HoverTool(names=['precip', 'temp', 'tempmin', 'tempmax'], tooltips=tooltips, formatters=formatters
                      )
    fig.add_tools(hover)

    # generar el archivo html y mostrar la gráfica
    output_file(f'{directory}{k}.html')
    save(fig)
