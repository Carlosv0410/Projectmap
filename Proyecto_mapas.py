#LIBRERIAS IMPORTADAS
import streamlit as st 
import altair as alt
import pandas as pd 
import json 
from geopy.geocoders import Nominatim 
import folium 
from streamlit_folium import folium_static 
import os

#CARGA DE DATA EN EXCEL Y PROCESAMIENTO DE DATAFRAME
data_analitics = pd.read_excel('Data_analitics.xlsx',sheet_name='Q11')
df_data_analitics = pd.DataFrame(data_analitics)

#SELECTORES DE OPCIONES Y FILTROS 

filtro1_q11 = st.sidebar.multiselect('select answer', df_data_analitics['Experience working with radioactivity'].unique())
filtro2_q11 = st.sidebar.multiselect('select province', df_data_analitics['Location'].unique())
filtro_radio = st.sidebar.slider('radius around Bruce [km]', 0,1600 , 20 , step=10)

#TITULOS Y SUBTITULOS DE LA APLICACION 
st.title('Q11: Do you have personal experience working in a job that involves the use of radioactivity')
st.title('Data frame - Q11')

st.subheader('DataFrame - original')
st.write(df_data_analitics)

grafico1 = alt.Chart(data_analitics).mark_bar().encode(
	x= 'Age:N',
	y= 'count(Location):Q',
	column= alt.Column('Gender'),
	shape='Gender',
	color='Experience working with radioactivity:N',
	tooltip=['count(Experience working with radioactivity):Q','Location:N']   
).interactive().properties( title = 'Q11: Do you have personal experience working in a job that involves the use of radioactivity', width=150, height=160)
st.altair_chart(grafico1)

df_data_analitics_filtro1 =df_data_analitics[df_data_analitics['Experience working with radioactivity'].isin(filtro1_q11)]
df_data_analitics_filtro2 =df_data_analitics_filtro1[df_data_analitics_filtro1 ['Location'].isin(filtro2_q11)]
df_data_analitics_filtro3 = df_data_analitics_filtro2.loc[df_data_analitics_filtro2['Distance Bruce'] <= filtro_radio]
st.subheader('DataFrame - filtered')
st.write(df_data_analitics_filtro3)


grafico2 = alt.Chart(df_data_analitics_filtro3).mark_bar().encode(
	x= 'Age:N',
	y= 'count(Location):Q',
	column= alt.Column('Gender'),
	shape='Gender',
	color='Experience working with radioactivity:N',
	tooltip=['count(Experience working with radioactivity):Q','Location:N']   
).interactive().properties( title = 'Q11: Do you have personal experience working in a job that involves the use of radioactivity', width=150, height=160)
st.altair_chart(grafico2)


filtro3_q11 = st.sidebar.multiselect('select answer 2', df_data_analitics['Experience working with radioactivity'].unique())
filtro4_q11 = st.sidebar.multiselect('select province 2', df_data_analitics['Location'].unique())
filtro_radio2 = st.sidebar.slider('radius around Bruce[km] 2', 0,1600 , 20 , step=10)

df_data_analitics_filtro4 =df_data_analitics[df_data_analitics['Experience working with radioactivity'].isin(filtro3_q11)]
df_data_analitics_filtro5 =df_data_analitics_filtro4[df_data_analitics_filtro4 ['Location'].isin(filtro4_q11)]
df_data_analitics_filtro6 = df_data_analitics_filtro5.loc[df_data_analitics_filtro5['Distance Bruce'] <= filtro_radio2]
#st.subheader('DataFrame - filtered')
#st.write(df_data_analitics_filtro6)

grafico3 = alt.Chart(df_data_analitics_filtro6).mark_bar().encode(
	x= 'Age:N',
	y= 'count(Location):Q',
	column= alt.Column('Gender'),
	shape='Gender',
	color='Experience working with radioactivity:N',
	tooltip=['count(Experience working with radioactivity):Q','Location:N']   
).interactive().properties( title = 'Q11: Do you have personal experience working in a job that involves the use of radioactivity', width=150, height=160)
st.altair_chart(grafico3)

#Título de la app
st.title('Map of Canada')
# Selectbox para cambiar el tipo de mapa que se presentará
add_select = st.sidebar.selectbox("What data do you want to see?",("OpenStreetMap", "Stamen Terrain","Stamen Toner","Stamen Watercolor","CartoDB dark_matter","Mapbox Bright"))
# Se define la ubicacion  central de origen del mapa
mapa_canada = folium.Map(tiles=add_select, location=[56.130366 , -106.346771], zoom_start=3)
#Importar el archivo Json que contiene los datos geográficos de Canada
canada_provincias = os.path.join('canada_provincias.json')
# Importar el Excel que contiene la columnas de resultados entre provincias y convertir a una Data Frame 
canada_data = pd.read_excel('canada_data.xlsx',sheet_name='Hoja1')

#Leemos el archivo de datos  
st.write(canada_data)
#Genera un mapa coropleticos que indica la data anterior la cual se conecta con el archivo de georeferenciación para su visualización
choropleth= folium.Choropleth(
 geo_data=canada_provincias,
 name='Resultados por provincias',
 data = canada_data,
 columns=['Provincia', 'Resultado'],
 key_on='feature.properties.name',
 nan_fill_color='blue',
 fill_color='YlOrRd',
 nan_fill_opacity=0.2, 
 fill_opacity=0.3,
 line_opacity=0.5,
 smooth_factor =1.2,
 legend_name='Provincia',
 highlight=True,
 control = True,
 overlay=True,
 show = True).add_to(mapa_canada)
choropleth.geojson.add_child(folium.features.GeoJsonTooltip(
		fields=['name'],
		aliases = ['Provincia'],
		style=('background-color: grey; color: white;'),
		labels=False)
)

#radio = st.slider('Radio [km]', 1,1500 , 10 , step=20)

filtro_radio_map = st.slider('radius around station [km]', 0,1600 , 20 , step=10)
folium.Circle([44.327231, -81.586447], filtro_radio_map*1000, fill=True, color='red').add_child(folium.Popup('Station Bruce')).add_to(mapa_canada)
folium.Circle([43.870029, -78.724924], filtro_radio_map*1000, fill=True, color='yellow').add_child(folium.Popup('Station Darlington')).add_to(mapa_canada)
folium.Circle([43.811667, -79.06583], filtro_radio_map*1000, fill=True, color='green').add_child(folium.Popup('Station Pickering')).add_to(mapa_canada)

folium.LayerControl().add_to(mapa_canada)
folium_static(mapa_canada)