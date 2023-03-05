from bokeh.models import Range1d, LinearAxis
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure, output_file
import pandas as pd
from bokeh.io import save, export_png


#directory = "/home/charmeleon/Documents/INSIVUMEH/dataset/output/"
directory="output/"
directory2="img/"
df = pd.read_csv('database.csv', header=1, delimiter=',')

# convertir la columna FECHA a formato datetime y ordenar el dataframe
df['FECHA'] = pd.to_datetime(df['FECHA'], format="%d/%m/%Y")
df = df.sort_values("FECHA")

#
# Obtener la fecha más reciente en el dataframe
latest_date = df['FECHA'].max()

# Obtener el primer día del último mes
first_day_of_last_month = latest_date.replace(day=1) - pd.DateOffset(months=1)

# Filtrar los datos para que solo incluyan los del último mes
last_month_data = df[df['FECHA'] >= first_day_of_last_month]


ID={"AMATITLAN":"INS011401AT",
"ANTIGUA GUATEMALA":"INS030101AT",
"CONCEPCION":"INS050101AT",
"IXCHIGUAN":"INS122301AT",
"JALAPA":"INS210101AT",
"LA REFORMA":"INS122101AT",
"LO DE COY":"INS010801AT",
"MARISCOS":"INS180501AT",
"MORALES MET":"INS180401AT",
"PACHUTÉ":"INS090401AT",
"PLAYA GRANDE IXCAN":"INS142201AT",
"SAN JOSE PINULA":"INS010301AT",
"SAN PEDRO AYAMPUC":"INS010701AT",
"SANTA CRUZ DEL QUICHE":"INS140101AT",
"SANTA MARGARITA":"INS040801AT",
"TOTONICAPAN":"INS080101AT",
"ALAMEDA ICTA":"INS040101CV",
"ASUNCION MITA":"INS220501CV",
"CAMOTAN":"INS200501CV",
"CATARINA":"INS121601CV",
"CHAMPERICO FEGUA":"INS110701CV",
"CHINIQUE":"INS140301CV",
"CHIXOY PCH":"INS141901CV",
"COBAN":"INS160101CV",
"CUBULCO":"INS150401CV",
"EL CAPITAN":"INS071301CV",
"EL TABLON":"INS070101CV",
"ESQUIPULAS":"INS200701CV",
"FLORES AEROPUERTO":"INS170101CV",
"HUEHUETENANGO":"INS130101CV",
"INSIVUMEH":"INS010101CV",
"LA AURORA":"INS010102CV",
"LA FRAGUA":"INS190201CV",
"LA UNION":"INS190901CV",
"LABOR OVALLE":"INS090301CV",
"LAS VEGAS PHC":"INS180201CV",
"LOS ALBORES":"INS020301CV",
"LOS ALTOS":"INS090101CV",
"LOS ESCLAVOS":"INS060101CV",
"MAZATENANGO":"INS100101CV",
"MONTUFAR":"INS221401CV",
"NEBAJ":"INS141301CV",
"PANZÓS PHC ALTAVERAPAZ":"INS160701CV",
"PASABIEN":"INS190301CV",
"POTRERO CARRILLO":"INS210101CV",
"PUERTO BARRIOS PHC":"INS180101CV",
"QUEZADA":"INS221701CV",
"RETALHULEU AEROPUERTO":"INS110101CV",
"SABANA GRANDE":"INS050101CV",
"SACAPULAS":"INS141601CV",
"SAN AGUSTIN ACASAGUASTLAN":"INS020302CV",
"SAN JERONIMO":"INS150701CV",
"SAN MARCOS PHC":"INS120101CV",
"SAN MARTIN JILOTEPEQUE":"INS040301CV",
"SAN PEDRO NECTA":"INS130601CV",
"SANTA CRUZ BALANYÁ":"INS041001CV",
"SANTA MARIA CAHABON":"INS161201CV",
"SANTIAGO ATITLAN":"INS071901CV",
"SUIZA CONTENTA":"INS030801CV",
"TECUN UMAN":"INS121701CV",
"TODOS SANTOS":"INS131501CV",
"POPTUN":"INS171201CV",
"SAN JOSE AEROPUERTO":"INS050901CV"}


for k in ID:
    # filtrar los datos por la estación (k)
    gk = last_month_data.groupby(['VARIABLE'])
    precip = gk.get_group('LLUVIA')[k]
    temp = gk.get_group('TMED')[k]
    tempmin = gk.get_group('TMIN')[k]
    tempmax = gk.get_group('TMAX')[k]
    fecha = gk.get_group('LLUVIA')['FECHA']
    
    fig = figure(x_axis_type='datetime', title=k, plot_height=300, plot_width=800, toolbar_location='below',
                 y_axis_label="Precipitación (mm)", y_range=(-5, 90), background_fill_color='white', 
                 background_fill_alpha=0.6, tools="save,pan,box_zoom,reset,wheel_zoom")
    
    fig.yaxis.axis_label_text_font_size = "5pt"
    fig.title.text_font_size = '5pt'
    fig.left[0].formatter.use_scientific = False
    
    # agregar el segundo eje para la temperatura
    fig.extra_y_ranges = {"temp_range": Range1d(start=5, end=40)}
    fig.add_layout(LinearAxis(y_range_name="temp_range", axis_label="Temperatura (°C)"), 'right')
    

    # agregar las líneas y los círculos
    fig.line(fecha, precip, line_color='navy', line_width=1, legend_label='Precipitación',
             name='precip')
    
    fig.line(fecha, temp, line_color='seagreen', line_width=1, line_dash='dashed', legend_label='Temperatura media', 
             name='temp',y_range_name='temp_range')
    fig.circle(fecha, tempmin, fill_color='deepskyblue', line_color='blue', size=2,
               legend_label='Temperatura min', name='tempmin',y_range_name='temp_range')
    fig.circle(fecha, tempmax, fill_color='firebrick', line_color='red', size=2,
               legend_label='Temperatura max', name='tempmax',y_range_name='temp_range')

    fig.legend.location = 'top_left'
    fig.title.text_font_size = '9pt'
    fig.yaxis.axis_label_text_font_size = "9pt"
    
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

    fig.legend.background_fill_alpha = 0.5
    fig.legend.label_text_font_size = "7pt"
    fig.legend.spacing = 5
    save(fig)
    export_png(fig, filename=f"{directory2}{k}.png")


