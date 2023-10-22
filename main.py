import customtkinter as ctk
import configparser
import os

from uploadWindow import upload
from Archivos import *
from PIL import Image

#<a href="https://www.flaticon.com/free-icons/align" title="align icons">Align icons created by Freepik - Flaticon</a>
#<a href="https://www.flaticon.com/free-icons/seo-full" title="seo full icons">Seo full icons created by Freepik - Flaticon</a>
#<a href="https://www.flaticon.com/free-icons/up-arrow" title="up arrow icons">Up arrow icons created by Freepik - Flaticon</a>
#<a href="https://www.flaticon.com/free-icons/spot" title="spot icons">Spot icons created by Freepik - Flaticon</a>
#<a href="https://www.flaticon.com/free-icons/write" title="write icons">Write icons created by Freepik - Flaticon</a>
class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		settings = self.readConfig()

		image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Archivos')
		self.menu_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, 'dark_menu.png')),
													dark_image=Image.open(os.path.join(image_path, 'light_menu.png')), size=(20, 20))
		self.upload_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, 'dark_upload.png')),
													dark_image=Image.open(os.path.join(image_path, 'light_upload.png')), size=(20, 20))
		self.edit_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, 'dark_edit.png')),
													dark_image=Image.open(os.path.join(image_path, 'light_edit.png')), size=(20, 20))
		self.graph_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, 'dark_graph.png')),
													dark_image=Image.open(os.path.join(image_path, 'light_graph.png')), size=(20, 20))
		self.map_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, 'dark_map.png')),
														dark_image=Image.open(os.path.join(image_path, 'light_map.png')), size=(20, 20))

		ctk.set_appearance_mode(settings['SETTINGS']['theme'])
		self.title('Sistema de Pesca de Camarones')
		self.iconbitmap('Archivos/shrimp.ico')
		width, height = self.winfo_screenwidth(), self.winfo_screenheight()
		self.geometry('%dx%d+0+0' % (width, height))
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)

		#Barra de navegación
		self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
		#Posicionar elemento sobre el elemento padre en la fila 0 y columna 0
		#"sticky" indica de lado debe pegarse el objeto y como distribuir el espacio adicional que no ocupe el objeto
		#en este caso se pegará norte a sur 'ns', para este a oeste es 'ew'
		#https://www.pythontutorial.net/tkinter/tkinter-grid/
		self.navigation_frame.grid(row=0, column=0, sticky='ns')
		#Ya entendí como funciona, aquí se define el espacio que ocupara la fila 5, no el definir el número de columnas
		self.navigation_frame.grid_rowconfigure(5, weight=1)
		#Lo mismo aquí se define la cantidad de espacio que ocupara la columna 0
		self.navigation_frame.grid_columnconfigure(0, weight=1)

		self.navigation_frame_label = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, image=self.menu_image, compound='left', text='Menú', font=ctk.CTkFont(size=15, weight='bold'), fg_color='transparent', text_color=('gray10', 'gray90'), hover_color=('gray70', 'gray30'), anchor='we', command=self.hide_menu)
		self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

		self.upload_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, image=self.upload_image, text='Cargar datos' if settings['SETTINGS']['language'] == 'Spanish' else 'Load data', fg_color='transparent', text_color=('gray10', 'gray90'), hover_color=('gray70', 'gray30'), anchor='w')
		self.upload_button.grid(row=1, column=0, sticky='new')
		self.preprocess_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, image=self.edit_image, text='Prepocesar datos' if settings['SETTINGS']['language'] == 'Spanish' else 'Visualize data', fg_color='transparent', text_color=('gray10', 'gray90'), hover_color=('gray70', 'gray30'), anchor='w', state = 'disabled', command=lambda: self.select_frame_by_name('preprocess'))
		self.preprocess_button.grid(row=2, column=0, sticky='new')

		self.captures_menu_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,image=self.graph_image, text='Lances' if settings['SETTINGS']['language'] == 'Spanish' else 'Captures', fg_color='transparent', text_color=('gray10', 'gray90'), hover_color=('gray70', 'gray30'), anchor='w', state = 'disabled', command=lambda: self.select_frame_by_name('captures'))
		self.captures_menu_button.grid(row=3, column=0, sticky='new')
		self.species_menu_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,image=self.graph_image, text='Especies' if settings['SETTINGS']['language'] == 'Spanish' else 'Species', fg_color='transparent', text_color=('gray10', 'gray90'), hover_color=('gray70', 'gray30'), anchor='w', state = 'disabled', command=lambda: self.select_frame_by_name('species'))
		self.species_menu_button.grid(row=4, column=0, sticky='new')
		self.maps_menu_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,image=self.map_image, text='Mapas' if settings['SETTINGS']['language'] == 'Spanish' else 'Maps', fg_color='transparent', text_color=('gray10', 'gray90'), hover_color=('gray70', 'gray30'), anchor='w', state = 'disabled', command=lambda: self.select_frame_by_name('maps'))
		self.maps_menu_button.grid(row=5, column=0, sticky='new')

		self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=['System', 'Light', 'Dark'], command=self.change_appearance_mode_event)
		self.appearance_mode_menu.set(settings['SETTINGS']['theme'])
		self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky='s')

		self.language_menu = ctk.CTkOptionMenu(self.navigation_frame, values=['Spanish', 'English'], command=self.change_language_event)
		self.language_menu.set(settings['SETTINGS']['language'])
		self.language_menu.grid(row=7, column=0, padx=20, pady=20, sticky='s')

		#Frame interactuable
		self.interactFrame = ctk.CTkFrame(self, fg_color='transparent')
		self.interactFrame.grid(row=0, column=1, sticky='nswe', padx=4, pady=4)
		self.interactFrame.grid_rowconfigure(0, weight=1)
		self.interactFrame.grid_columnconfigure(0, weight=1)

		#Referenciar las 'ventanas' para mandarlas a llamarlas con la función select_frame_by_name
		self.uploadFrame = upload(self.interactFrame)

		#Llamada a la ventana upload
		self.select_frame_by_name('upload')

	def show_menu(self):
		widgets = [(self.navigation_frame_label, {'text': 'Menú', 'command': self.hide_menu}),
			(self.upload_button, {'text': 'Cargar datos'}), (self.preprocess_button, {'text': 'Preprocesar datos'}),
			(self.captures_menu_button, {'text': 'Lances'}), (self.species_menu_button, {'text': 'Especies'}), 
			(self.maps_menu_button, {'text': 'Mapas'})]
		
		for widget, config in widgets:
			widget.configure(**config)
			widget.grid(sticky = 'we')

			if widget is self.navigation_frame_label:
				widget.grid(sticky = 'we', padx = 20)

			if widget is self.maps_menu_button:
				widget.grid(sticky = 'nwe')

		self.appearance_mode_menu.grid()
		self.language_menu.grid()

	def hide_menu(self):
		widgets_to_hide = [self.navigation_frame_label, self.upload_button, self.preprocess_button, 
		    self.captures_menu_button, self.species_menu_button, self.maps_menu_button]

		for widget in widgets_to_hide:
			widget.configure(text = '', width = 5)
			widget.grid(sticky = 'w')

			if widget is self.navigation_frame_label:
				widget.configure(text = '', command = self.show_menu, width = 5)
				widget.grid(sticky = 'w', padx = 0)

			if widget is self.maps_menu_button:
				widget.grid(sticky = 'nw')
		
		self.appearance_mode_menu.grid_remove()
		self.language_menu.grid_remove()

	#Cuando se usa el atributo commad desde un objeto CTkOptionMenu este siempre arrojara dos valores que son:
	#'self' - Que hace referencia al propio elemento del que viene la interracion
	#'value' o en este caso 'new_appearance_mode' que es uno de los posibles valores que definimos en el objeto
	def change_appearance_mode_event(self, new_appearance_mode):
		self.changeConfig('theme', new_appearance_mode)
		ctk.set_appearance_mode(new_appearance_mode)

	def change_language_event(self, new_language):
		self.changeConfig('language', new_language)

	#Funcion que leera el archivo config.ini
	def readConfig(self):
		settings = configparser.ConfigParser()
		settings.read('config.ini')
		return settings

	#Funcion para escribir sobre el archivo config.ini
	def changeConfig(self, setting, value):
		settings = self.readConfig()
		settings['SETTINGS'][setting] = value
		
		with open('config.ini', 'w') as configfile:
			settings.write(configfile)

	#Funcion para cambiar entre frames principales
	def select_frame_by_name(self, name):
		try:
			self.upload_button.configure(fg_color = ('gray75', 'gray25') if name == 'upload' else 'transparent')
			self.preprocess_button.configure(fg_color = ('gray75', 'gray25') if name == 'visual' else 'transparent')

			self.captures_menu_button.configure(fg_color = ('gray75', 'gray25') if name == 'captures' else 'transparent')
			self.species_menu_button.configure(fg_color = ('gray75', 'gray25') if name == 'species' else 'transparent')
			self.maps_menu_button.configure(fg_color = ('gray75', 'gray25') if name == 'maps' else 'transparent')

			# show selected frame
			if name == 'upload':
				self.uploadFrame.grid(row = 0, column = 0, sticky = 'nswe', padx = 10, pady = 10)
				self.uploadFrame.filterFrame.grid_forget()
				self.uploadFrame.filterbutton.grid_forget()
				self.uploadFrame.preprocessbutton.grid_forget()
				self.uploadFrame.infoWidget.grid(row = 0, column = 0, sticky = 'nwse', padx = 8, pady = 8)
				self.uploadFrame.uploadbutton.grid(row = 1, column = 0, sticky = 'sew', padx = 8, pady = (2, 8))
			else:
				if not self.uploadFrame.winfo_viewable():
					self.uploadFrame.grid_forget()
			if name == 'preprocess':
				self.uploadFrame.grid(row = 0, column = 0, sticky = 'nswe', padx = 10, pady = 10)
				self.uploadFrame.infoWidget.grid_forget()
				self.uploadFrame.uploadbutton.grid_forget()
				self.uploadFrame.filterFrame.grid(row = 0, column = 0, sticky = 'nwse', padx = 8, pady = 8)
				self.uploadFrame.filterbutton.grid(row = 2, column = 0, sticky = 'sew', padx = 8, pady = (2, 8))
				self.uploadFrame.preprocessbutton.grid(row = 3, column = 0, sticky = 'sew', padx = 8, pady = (2, 8))
				#self.preprocessFrame.grid(row = 0, column = 0, sticky = 'nswe', padx = 10, pady = 10)
			else:
				if not self.uploadFrame.winfo_viewable():
					self.uploadFrame.grid_forget()
			if name == 'captures':
				self.capturesFrame.grid(row = 0, column = 0, sticky = 'nswe', padx = 10, pady = 10)
			else:
				self.capturesFrame.grid_forget()
			if name == 'species':
				self.speciesFrame.grid(row = 0, column = 0, sticky = 'nswe', padx = 10, pady = 10)
			else:
				self.speciesFrame.grid_forget()
			if name == 'maps':
				self.mapsFrame.grid(row = 0, column = 0, sticky = 'nswe', padx = 10, pady = 10)
			else:
				self.mapsFrame.grid_forget()
		except:
			pass
    
if __name__ == '__main__':
    app = App()
    app.protocol('WM_DELETE_WINDOW', app.quit)
    app.mainloop()