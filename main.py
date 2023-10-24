import sys
import folium
import pandas as pd
from sqlalchemy import create_engine
from folium.plugins import MiniMap

# Conectarse a la base de datos usando SQLAlchemy
engine = create_engine("mysql+mysqlconnector://root:wtRykrEX9As8wN@localhost/geomotica")
id_analisis = sys.argv[1]
tabla = sys.argv[2]

# Consulta SQL para obtener datos
query = f"""SELECT LONGITUD, LATITUD, CULTIVO, NOMBRE_FINCA, ACTIVIDAD, 
            FECHA_INICIO, HORA_INICIO, HORA_FINAL 
            FROM {tabla} WHERE ID_ANALISIS = {id_analisis};"""

df = pd.read_sql(query, engine, params={"id_analisis": id_analisis})

# Crear mapa centrado en la primera coordenada con opción de satélite
tiles_option = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
attribution = "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community"

m = folium.Map(location=[df['LATITUD'].iloc[0], df['LONGITUD'].iloc[0]], zoom_start=15, tiles=tiles_option, attr=attribution)

# Añadir trazado de puntos
locations = df[['LATITUD', 'LONGITUD']].values
folium.PolyLine(locations, color="blue", weight=2.5).add_to(m)

# Añadir popup a cada punto con información relevante
for _, row in df.iterrows():
    popup_content = f"""
    <strong>Cultivo:</strong> {row['CULTIVO']}<br>
    <strong>Finca:</strong> {row['NOMBRE_FINCA']}<br>
    <strong>Actividad:</strong> {row['ACTIVIDAD']}<br>
    <strong>Fecha:</strong> {row['FECHA_INICIO']}<br>
    <strong>Horario:</strong> {row['HORA_INICIO']} - {row['HORA_FINAL']}
    """
    folium.CircleMarker((row['LATITUD'], row['LONGITUD']), radius=5, color="blue").add_child(folium.Popup(popup_content)).add_to(m)

# Añadir controles de capas
folium.LayerControl().add_to(m)

# Añadir minimapa
minimap = MiniMap()
m.add_child(minimap)

# Guardar el mapa en un archivo HTML
m.save("mapa.html")
