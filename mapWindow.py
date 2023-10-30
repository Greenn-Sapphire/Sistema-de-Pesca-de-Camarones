import customtkinter as ctk
import tkintermapview
import pandas as pd

from Widgets.filterpanel import FilterPanel
from CTkMessagebox import CTkMessagebox

class maps(ctk.CTkFrame):
	def __init__(self, master, dataframe):
		super().__init__(master)
		self.grid_remove()
		self.grid_columnconfigure(1, weight = 1) #Darle todo el espacio restante a la Tabla
		self.grid_rowconfigure(0, weight = 1) #Darle todo el espacio restante al ScrollableFrame
		self.grid_configure()
		self.dataframe = dataframe
		self.marker_list = []
		
		nonfilterlist = ['LAT_INI', 'LONG_INI', 'LAT_FIN', 'LONG_FIN', 'LAT_INI', 'Hr_INI', 'Hr_FIN',
				   'Nºind/Tot', 'Nºind/mes', 'Nºind/est', 
				   'LONG_TOT', 'LONG_PAT', 'DIAME_DISCO', 'PESO', 'WA', 'SEXO', 'EDO_MAD',
				   'CLAV_GRUP', 'CLA_ORDEN', 'CLAVE_FAM', 'CODIGOSPP', 'CLAVE_SP', 'OBSERV']

		self.filterFrame = FilterPanel(self, self.dataframe, nonfilterlist, width = 150)
		self.filterFrame.configure(corner_radius = 5)
		self.filterFrame.grid(row = 0, column = 0, sticky = 'nwse', padx = 8, pady = 8)
		self.filterFrame.grid_rowconfigure(8, weight = 1)
		self.filterFrame.grid_columnconfigure(0, weight = 1)

		self.Button = ctk.CTkButton(self, text = 'Aplicar filtros', command = self.Filter_callbck)
		self.Button.grid(row = 1, column = 0, sticky = 'ew', padx = 8, pady = (2, 8))

		self.container = ctk.CTkFrame(self)
		self.container.grid(row = 0, column = 1, rowspan = 2, sticky = 'nswe', padx = 8, pady = 8)
		self.container.grid_columnconfigure(0, weight = 1)
		self.container.grid_rowconfigure(1, weight = 1)

		self.region_selector = ctk.CTkOptionMenu(self.container, values = ['Baja California Sur', 'Golfo de Tehuantepec', 'Islas Contoy'], width = 180, command=self.change_region_event)
		self.region_selector.grid(row = 0, column = 0, sticky = 'e', padx = 8, pady = (8, 0))

		self.map_widget = tkintermapview.TkinterMapView(self.container, corner_radius = 5)
		self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
		self.map_widget.grid(row = 1, column = 0, sticky = 'nswe', padx = 8, pady = (2, 8))

		self.map_widget.set_position(15.8083695, -94.1006715)  # Golfo Tehuantepec
		self.map_widget.set_zoom(9)
		
		unique_coordinates_df = pd.concat([self.dataframe[['LAT_INI', 'LONG_INI', 'LAT_FIN', 'LONG_FIN', 'FECHA', 'BARCO', 'AREA', 'REGION', 'Hr_INI', 'Hr_FIN', 'DIA/NOCHE', 'PROF/m', 'PLATAF', 'ESTRATO PROF.', 'T °C', 'SALIN (0/00)', 'Camaron/kg', 'FAC/kg']]]).drop_duplicates()
		unique_coordinates_df.reset_index(drop=True, inplace=True)
		
		unique_coordinates_df['LAT_INI'] = self.dms_to_dd(unique_coordinates_df['LAT_INI'])
		unique_coordinates_df['LAT_FIN'] = self.dms_to_dd(unique_coordinates_df['LAT_FIN'])
		unique_coordinates_df['LONG_INI'] = self.dms_to_dd(unique_coordinates_df['LONG_INI'])*-1
		unique_coordinates_df['LONG_FIN'] = self.dms_to_dd(unique_coordinates_df['LONG_FIN'])*-1
		self.create_markers(unique_coordinates_df)

	def change_region_event(self, region):
		if region == 'Golfo de Tehuantepec':
			self.map_widget.set_position(16.004032949759438, -94.99997078781678)
		elif region == 'Islas Contoy':
			self.map_widget.set_position(21.49335742259156, -86.80067298449022)
		elif region == 'Baja California Sur':
			self.map_widget.set_position(25.9420633164181, -112.8625387474789)

	def dms_to_dd(self, coordenada):
			#Si es Norte y Este se suma, de lo contrario se resta
			grades = coordenada // 10000
			minutes = (coordenada % 10000) // 100
			seconds = coordenada % 100
			coord = round(grades + (minutes/60) + (seconds/3600), 4)

			return coord

	def create_markers(self, coordinates_df):
		for _, row in coordinates_df.iterrows():
			lat_ini, long_ini, lat_fin, long_fin = row['LAT_INI'], row['LONG_INI'], row['LAT_FIN'], row['LONG_FIN']
			
			textini = f"Latitud: {row['LAT_INI']}\nLongitud: {row['LONG_INI']}\n"
			textfin = f"Latitud: {row['LAT_FIN']}\nLongitud: {row['LONG_FIN']}\n"
			text = f"Fecha: {row['FECHA']}\nBarco: {row['BARCO']}\nÁrea: {row['AREA']}\nRegión: {row['REGION']}\nDía/Noche: {row['DIA/NOCHE']}\nProfundidad (m): {row['PROF/m']}\nEstrato profundo: {row['ESTRATO PROF.']}\nTemperatura (°C): {row['T °C']}\nSalinidad (0/00): {row['SALIN (0/00)']}\nKg camarón: {row['Camaron/kg']}\nKg FAC: {row['FAC/kg']}"
			
			#marker_ini = self.map_widget.set_marker(lat_ini, long_ini, marker_color_circle='black', marker_color_outside='cornflowerblue', text='', data=textini+text, text_color='black', command=on_click_ini)
			marker_fin = self.map_widget.set_marker(lat_fin, long_fin, marker_color_circle='black', marker_color_outside='firebrick', text='', data=textfin+text, text_color='black', command=on_click_fin)
			#path = self.map_widget.set_path([marker_ini.position, marker_fin.position], color='darkgrey')
			#self.marker_list.append(marker_ini)
			self.marker_list.append(marker_fin)
			#self.marker_list.append(path)


#self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")  # OpenStreetMap (default)
#self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal

	def Filter_callbck(self):
		try:
			for marker in self.marker_list:
				marker.delete()
			
			df_list = self.filterFrame.apply_filter_graphs()
			coordinates_df = pd.concat([df_list[['LAT_INI', 'LONG_INI', 'LAT_FIN', 'LONG_FIN', 'FECHA', 'BARCO', 'AREA', 'REGION', 'Hr_INI', 'Hr_FIN', 'DIA/NOCHE', 'PROF/m', 'PLATAF', 'ESTRATO PROF.', 'T °C', 'SALIN (0/00)', 'Camaron/kg', 'FAC/kg']]]).drop_duplicates()
			coordinates_df.reset_index(drop=True, inplace=True)
		
			coordinates_df['LAT_INI'] = self.dms_to_dd(coordinates_df['LAT_INI'])
			coordinates_df['LAT_FIN'] = self.dms_to_dd(coordinates_df['LAT_FIN'])
			coordinates_df['LONG_INI'] = self.dms_to_dd(coordinates_df['LONG_INI'])*-1
			coordinates_df['LONG_FIN'] = self.dms_to_dd(coordinates_df['LONG_FIN'])*-1
			self.create_markers(coordinates_df)
		except Exception as e:
			CTkMessagebox(title = 'Error', message = f'Error inesperado: {str(e)}', icon = 'warning')
			return

def on_click_ini(marker):
	if marker.text is None or marker.text == '':
		marker.set_text(marker.data)
	else:
		marker.set_text('')

def on_click_fin(marker):
	if marker.text is None or marker.text == '':
		marker.set_text(marker.data)
	else:
		marker.set_text('')