import customtkinter as ctk
import tkintermapview
import pandas as pd

from CTkMessagebox import CTkMessagebox

class maps(ctk.CTkFrame):
	def __init__(self, master, dataframe):
		super().__init__(master)
		self.grid_columnconfigure(0, weight = 1) #Darle todo el espacio restante a la Tabla
		self.grid_rowconfigure(1, weight = 1) #Darle todo el espacio restante al ScrollableFrame
		self.dataframe = dataframe
		self.marker_list = []

		self.region_selector = ctk.CTkOptionMenu(self, values = ['Baja California Sur', 'Golfo de Tehuantepec', 'Islas Contoy'], width = 180, command=self.change_region_event)
		self.region_selector.grid(row = 0, column = 0, sticky = 'e', padx = 8, pady = (8, 0))

		self.map_widget = tkintermapview.TkinterMapView(self, corner_radius = 5)
		self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
		self.map_widget.grid(row = 1, column = 0, sticky = 'nswe', padx = 8, pady = (2, 8))

		self.map_widget.set_position(25.8617666, -112.7485556)
		self.map_widget.set_zoom(8)
		
		unique_coordinates_df = pd.concat([self.dataframe[['LAT_FIN', 'LONG_FIN', 'FECHA', 'BARCO', 'AREA', 'REGION', 'Hr_INI', 'Hr_FIN', 'DIA/NOCHE', 'PROF/m', 'PLATAF', 'ESTRATO PROF.', 'T °C', 'SALIN (0/00)', 'Camaron/kg', 'FAC/kg']]]).drop_duplicates()
		unique_coordinates_df.reset_index(drop=True, inplace=True)
		
		unique_coordinates_df['LAT_FIN'] = self.dms_to_dd(unique_coordinates_df['LAT_FIN'])
		unique_coordinates_df['LONG_FIN'] = self.dms_to_dd(unique_coordinates_df['LONG_FIN'])*-1
		self.create_markers(unique_coordinates_df)

	def change_region_event(self, region):
		if region == 'Baja California Sur':
			self.map_widget.set_position(25.8617666, -112.7485556)
			self.map_widget.set_zoom(8)

		elif region == 'Golfo de Tehuantepec':
			self.map_widget.set_position(15.7390152, -94.2082479)
			self.map_widget.set_zoom(9)
			
		elif region == 'Islas Contoy':
			self.map_widget.set_position(21.4955336, -86.8039131)
			self.map_widget.set_zoom(13)

	def dms_to_dd(self, coordenada):
			#Si es Norte y Este se suma, de lo contrario se resta
			grades = coordenada // 10000
			minutes = (coordenada % 10000) // 100
			seconds = coordenada % 100
			coord = round(grades + (minutes/60) + (seconds/3600), 4)
			return coord

	def create_markers(self, coordinates_df):
		for _, row in coordinates_df.iterrows():
			lat_fin, long_fin = row['LAT_FIN'], row['LONG_FIN']
			text = f"Latitud: {row['LAT_FIN']}\nLongitud: {row['LONG_FIN']}\nFecha: {row['FECHA']}\nBarco: {row['BARCO']}\nÁrea: {row['AREA']}\nRegión: {row['REGION']}\nDía/Noche: {row['DIA/NOCHE']}\nProfundidad (m): {row['PROF/m']}\nEstrato profundo: {row['ESTRATO PROF.']}\nTemperatura (°C): {row['T °C']}\nSalinidad (0/00): {row['SALIN (0/00)']}\nKg camarón: {row['Camaron/kg']}\nKg FAC: {row['FAC/kg']}"
			
			marker_fin = self.map_widget.set_marker(lat_fin, long_fin, marker_color_circle='black', marker_color_outside='firebrick', text='', data=text, text_color='black', command=on_click_fin)
			self.marker_list.append(marker_fin)
			
	def filter_map_data(self, df_list):
		try:
			for marker in self.marker_list:
				marker.delete()
			
			coordinates_df = pd.concat([df_list[['LAT_INI', 'LONG_INI', 'LAT_FIN', 'LONG_FIN', 'FECHA', 'BARCO', 'AREA', 'REGION', 'Hr_INI', 'Hr_FIN', 'DIA/NOCHE', 'PROF/m', 'PLATAF', 'ESTRATO PROF.', 'T °C', 'SALIN (0/00)', 'Camaron/kg', 'FAC/kg']]]).drop_duplicates()
			coordinates_df.reset_index(drop=True, inplace=True)
		
			coordinates_df['LAT_FIN'] = self.dms_to_dd(coordinates_df['LAT_FIN'])
			coordinates_df['LONG_FIN'] = self.dms_to_dd(coordinates_df['LONG_FIN'])*-1
			self.create_markers(coordinates_df)

		except Exception as e:
			CTkMessagebox(title = 'Error', message = f'Error inesperado: {str(e)}', icon = 'warning')
			return

def on_click_fin(marker):
	if marker.text is None or marker.text == '':
		marker.set_text(marker.data)
	else:
		marker.set_text('')