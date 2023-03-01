import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from bokeh.io import export_png

from bokeh.io import output_file
# para visualizar el resultado
from bokeh.plotting import figure, show, gridplot
#from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool

directory="/home/charmeleon/Documents/INSIVUMEH/dataset/output/"  

df = pd.read_csv('database.csv', header=1,delimiter=',')
df['FECHA']=pd.to_datetime(df['FECHA'], format="%d/%m/%Y")
df = df.sort_values("FECHA")


ID={"CHAMPERICO FEGUA":"INS110701CV","COBAN":"INS160101CV","ESQUIPULAS":"INS200701CV","FLORES AEROPUERTO":"INS170101CV",\
    "LA AURORA":"INS010102CV"}
        
for k in ID:
    
    output_file(''+directory+''+k+'.html')
    
    gk=df.groupby(['VARIABLE'])
    data=gk.get_group('LLUVIA')
    variable=data[k]
    fecha=data['FECHA']
    
    TOOLS = "save,pan,box_zoom,reset,wheel_zoom"
    fig = figure(x_axis_type='datetime', title='',
                 plot_height=200, plot_width=800, toolbar_location='below',
                 y_axis_label="Precipitación (mm)", y_range=(-5, 90), background_fill_color='white', background_fill_alpha=0.6, tools=TOOLS)
    line = fig.line(fecha,variable,
                    line_color="deepskyblue", line_width=1, legend_label=k)
    #circle = fig.circle(data['FECHA'], data['LA AURORA'],
     #                   fill_color="blue", line_color="blue", size=2)
    fig.add_tools(HoverTool(tooltips=[
                  ("Fecha", "@x{%d-%m-%Y}"), ("Valor", "$y{y.f}")], formatters={'@x': 'datetime', 'y': 'printf'}))
    fig.legend.location = 'top_left'
    fig.title.text_font_size = '15pt'
    fig.yaxis.axis_label_text_font_size = "15pt"

    p = gridplot([[fig]])

    show(p)
