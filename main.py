import customtkinter as ctk
import pandas as pd
import configparser
import numpy

from Widgets.filterpanel import FilterPanel
from Widgets.lateralmenu import lateralmenu
from CTkMessagebox import CTkMessagebox
from preprocessWindow import preprocess
from dashboards import dashboards
from uploadWindow import upload
from mapWindow import maps
from Archivos import *

#<a href="https://www.flaticon.com/free-icons/align" title="align icons">Align icons created by Freepik - Flaticon</a>
#<a href="https://www.flaticon.com/free-icons/seo-full" title="seo full icons">Seo full icons created by Freepik - Flaticon</a>
#<a href="https://www.flaticon.com/free-icons/up-arrow" title="up arrow icons">Up arrow icons created by Freepik - Flaticon</a>
#<a href="https://www.flaticon.com/free-icons/spot" title="spot icons">Spot icons created by Freepik - Flaticon</a>
#<a href="https://www.flaticon.com/free-icons/write" title="write icons">Write icons created by Freepik - Flaticon</a>
class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		settings = self.read_config_file()
		ctk.set_appearance_mode(settings['SETTINGS']['theme'])
		self.title('Sistema de Pesca de Camarones')
		self.iconbitmap('Archivos/shrimp.ico')
		width, height = self.winfo_screenwidth(), self.winfo_screenheight()
		self.geometry('%dx%d+0+0' % (width, height))
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)

		self.lateral_menu = lateralmenu(self)
		self.lateral_menu.grid(row=0, column=0, sticky='ns')

		#Frame interactuable
		self.main_frame = ctk.CTkFrame(self, fg_color='transparent', corner_radius = 0)
		self.main_frame.grid(row=0, column=1, sticky='nswe')
		self.main_frame.grid_rowconfigure(0, weight=1)
		self.main_frame.grid_columnconfigure(1, weight=1)

		#Referenciar las 'ventanas' para mandarlas a llamarlas con la función select_frame_by_name
		self.upload_frame = upload(self.main_frame, corner_radius = 5)
		self.upload_frame.grid(row=0, column=0, sticky='ns', padx = 0)
		self.upload_frame.upload_button.configure(command = self.read_data)

		#Llamada a la ventana upload
		self.select_frame_by_name('upload')

	def read_config_file(self):
		settings = configparser.ConfigParser()
		settings.read('config.ini')
		return settings
	
	#Funcion para cambiar entre frames principales
	def select_frame_by_name(self, name):
		try:
			self.lateral_menu.upload_menu_button.configure(fg_color = ('gray75', 'gray25') if name == 'upload' else 'transparent')
			self.lateral_menu.preprocess_menu_button.configure(fg_color = ('gray75', 'gray25') if name == 'preprocess' else 'transparent')

			self.lateral_menu.dashboard_menu_button.configure(fg_color = ('gray75', 'gray25') if name == 'dashboard' else 'transparent')
			self.lateral_menu.maps_menu_button.configure(fg_color = ('gray75', 'gray25') if name == 'maps' else 'transparent')

			# show selected frame
			if name == 'upload':
				self.upload_frame.grid(row = 0, column = 0, sticky = 'nse', padx = 10, pady = 10)
				self.table_frame.grid(row=0, column=1, sticky='nswe', padx = 2, pady = 10)
			else:
				self.upload_frame.grid_forget()

			if name == 'preprocess':
				self.preprocess_frame.grid(row = 0, column = 0, sticky = 'nse', padx = 10, pady = 10)
				self.preprocess_frame.preprocess_button.grid(row = 3, column = 0, sticky = 'sew', padx = 8, pady = (2, 8))
				self.table_frame.grid(row=0, column=1, sticky='nswe', padx = 2, pady = 10)
			else:
				self.preprocess_frame.grid_forget()

			if name == 'dashboards':
				self.table_frame.grid_forget()
				self.preprocess_frame.grid(row = 0, column = 0, sticky = 'nse', padx = 10, pady = 10)
				self.preprocess_frame.preprocess_button.grid_forget()
				self.dashboard_frame.grid(row = 0, column = 1, sticky = 'nswe', padx = 2, pady = 10)
			else:
				self.dashboard_frame.grid_forget()

			if name == 'maps':
				self.table_frame.grid_forget()
				self.preprocess_frame.grid(row = 0, column = 0, sticky = 'nse', padx = 10, pady = 10)
				self.preprocess_frame.preprocess_button.grid_forget()
				self.maps_frame.grid(row = 0, column = 1, sticky = 'nswe', padx = 2, pady = 10)
			else:
				self.maps_frame.grid_forget()
		except Exception as e:
			pass

	def read_data(self):
		self.dataframe = self.upload_frame.readData()
		if not self.dataframe.empty:
			self.upload_frame.data_information_frame.showinfo(self.dataframe)
			self.table_frame = self.upload_frame.createTable(self.main_frame, self.dataframe)
			self.table_frame.grid(row=0, column=1, sticky='nswe', padx = 2, pady = 10)

			self.preprocess_frame = preprocess(self.main_frame, self.dataframe)
			self.preprocess_frame.filter_button.configure(command = self.filter_data)
			self.preprocess_frame.preprocess_button.configure(command = self.process_data)
			self.lateral_menu.upload_menu_button.configure(command = lambda: self.select_frame_by_name('upload'))
			self.lateral_menu.preprocess_menu_button.configure(command = lambda: self.select_frame_by_name('preprocess'))
			self.lateral_menu.preprocess_menu_button.configure(state = 'normal')

	def filter_data(self):
		if self.table_frame.winfo_viewable():
			try:
				indexes_to_display = self.preprocess_frame.data_filter_frame.apply_filter()
				
				self.table_frame.table.display_rows(rows = indexes_to_display, all_rows_displayed = False, redraw = True)
				CTkMessagebox(title = 'Aviso', message = 'Datos filtrados (temporalmente)', icon = 'check')
			except Exception as e:
				CTkMessagebox(title = 'Error', message = f'Error inesperado: {str(e)}', icon = 'warning')
				return
			
		elif self.dashboard_frame.winfo_viewable():
			df_list = self.preprocess_frame.data_filter_frame.apply_filter_graphs()
			self.dashboard_frame.filter_dashboard_data(df_list)
			CTkMessagebox(title = 'Aviso', message = 'Datos filtrados', icon = 'check')

		elif self.maps_frame.winfo_viewable():
			df_list = self.preprocess_frame.data_filter_frame.apply_filter_graphs()
			self.maps_frame.filter_map_data(df_list)
			CTkMessagebox(title = 'Aviso', message = 'Datos filtrados', icon = 'check')

	def process_data(self):
		modified_data_list = self.table_frame.table.get_sheet_data(get_header = True)
		modified_dataframe = pd.DataFrame(modified_data_list[1:], columns = modified_data_list[0])
		modified_dataframe = modified_dataframe.replace({'': numpy.nan, None: numpy.nan})

		if not self.dataframe.equals(modified_dataframe):
			self.dataframe = modified_dataframe
			try:
				self.preprocess_frame.preprocess_data(self.dataframe)
			except:
				return
			self.preprocess_frame.data_filter_frame.destroy()
			self.preprocess_frame.data_filter_frame = FilterPanel(self.preprocess_frame, self.dataframe, self.preprocess_frame.nonfilterlist, width = 150, corner_radius = 5)
			self.preprocess_frame.data_filter_frame.grid(row = 0, column = 0, sticky = 'nwse', padx = 8, pady = 8)
			self.preprocess_frame.data_filter_frame.grid_rowconfigure(8, weight = 1)
			self.preprocess_frame.data_filter_frame.grid_columnconfigure(0, weight = 1)
		else:
			try:
				self.preprocess_frame.preprocess_data(self.dataframe)
			except:
				return

		self.dashboard_frame = dashboards(self.main_frame, self.dataframe)
		self.lateral_menu.dashboard_menu_button.configure(command = lambda: self.select_frame_by_name('dashboards'))
		self.lateral_menu.dashboard_menu_button.configure(state = 'normal')
		self.maps_frame = maps(self.main_frame, self.dataframe)
		self.lateral_menu.maps_menu_button.configure(command = lambda: self.select_frame_by_name('maps'))
		self.lateral_menu.maps_menu_button.configure(state = 'normal')
		CTkMessagebox(title = 'Aviso', message = 'Datos procesados con éxito', icon = 'check')

if __name__ == '__main__':
    app = App()
    app.protocol('WM_DELETE_WINDOW', app.quit)
    app.mainloop()