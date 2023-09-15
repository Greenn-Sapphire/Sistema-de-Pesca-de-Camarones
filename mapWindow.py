import customtkinter as ctk
import tkintermapview
from Archivos import *
from dataframe import Data
import pandas as pd

class maps(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.grid_remove()
		self.grid_columnconfigure(0, weight = 1) #Darle todo el espacio restante a la Tabla
		self.grid_rowconfigure(0, weight = 1) #Darle todo el espacio restante al ScrollableFrame

		map_widget = tkintermapview.TkinterMapView(self, corner_radius = 5)
		map_widget.grid(row = 0, column = 0, sticky = 'nswe')

		map_widget.set_position(15.8083695, -94.1006715)  # Golfo Tehuantepec
		map_widget.set_zoom(9)
		
		unique_coordinates_df = pd.concat([Data.dataframe[['LAT_INI', 'LONG_INI', 'LAT_FIN', 'LONG_FIN']]]).drop_duplicates()
		unique_coordinates_df.reset_index(drop=True, inplace=True)

		# Función para convertir coordenadas a grados decimales.
		def dms_to_dd_lat(coordinate):
				grades = coordinate // 10000
				rest = coordinate % 10000
				minutes = rest // 100
				seconds = rest % 100
				lat = grades + (minutes/60) + (seconds/3600)
				return lat
		
		def dms_to_dd_lon(coordinate):
				grades = coordinate // 10000
				rest = coordinate % 10000
				minutes = rest // 100
				seconds = rest % 100
				lon = -grades - (minutes/60) - (seconds/3600)
				return lon
		
		unique_coordinates_df['LAT_INI'] = dms_to_dd_lat(unique_coordinates_df['LAT_INI'])
		unique_coordinates_df['LAT_FIN'] = dms_to_dd_lat(unique_coordinates_df['LAT_FIN'])
		unique_coordinates_df['LONG_INI'] = dms_to_dd_lon(unique_coordinates_df['LONG_INI'])
		unique_coordinates_df['LONG_FIN'] = dms_to_dd_lon(unique_coordinates_df['LONG_FIN'])

		for _, row in unique_coordinates_df.iterrows():
			lat_ini, long_ini, lat_fin, long_fin = row['LAT_INI'], row['LONG_INI'], row['LAT_FIN'], row['LONG_FIN']
			marker_ini = map_widget.set_marker(lat_ini, long_ini, marker_color_circle='black', marker_color_outside='cornflowerblue', text='')
			marker_fin = map_widget.set_marker(lat_fin, long_fin, marker_color_circle='black', marker_color_outside='firebrick', text='')
			path = map_widget.set_path([marker_ini.position, marker_fin.position], color='darkgrey')

#self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")  # OpenStreetMap (default)
#self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal