import customtkinter as ctk
import configparser
import os

from PIL import Image

class lateralmenu(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.configure()
		self.grid_rowconfigure(5, weight=1)
		self.grid_columnconfigure(0, weight=1)

		settings = self.read_config_file()
		
		image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'Archivos')
		menu_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, 'dark_menu.png')),
													dark_image=Image.open(os.path.join(image_path, 'light_menu.png')), size=(20, 20))
		upload_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, 'dark_upload.png')),
													dark_image=Image.open(os.path.join(image_path, 'light_upload.png')), size=(20, 20))
		edit_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, 'dark_edit.png')),
													dark_image=Image.open(os.path.join(image_path, 'light_edit.png')), size=(20, 20))
		graph_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, 'dark_graph.png')),
													dark_image=Image.open(os.path.join(image_path, 'light_graph.png')), size=(20, 20))
		map_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, 'dark_map.png')),
														dark_image=Image.open(os.path.join(image_path, 'light_map.png')), size=(20, 20))

		self.menu_button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, image=menu_image, compound='left', text='Menú', font=ctk.CTkFont(size=15, weight='bold'), fg_color='transparent', text_color=('gray10', 'gray90'), hover_color=('gray70', 'gray30'), anchor='we', command=self.hide_menu)
		self.menu_button.grid(row=0, column=0, padx=20, pady=20)

		self.upload_menu_button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, image=upload_image, text='Cargar datos' if settings['SETTINGS']['language'] == 'Spanish' else 'Load data', fg_color='transparent', text_color=('gray10', 'gray90'), hover_color=('gray70', 'gray30'), anchor='w')
		self.upload_menu_button.grid(row=1, column=0, sticky='new')
		
		self.preprocess_menu_button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, image=edit_image, text='Prepocesar datos' if settings['SETTINGS']['language'] == 'Spanish' else 'Visualize data', fg_color='transparent', text_color=('gray10', 'gray90'), hover_color=('gray70', 'gray30'), anchor='w', state = 'disabled')
		self.preprocess_menu_button.grid(row=2, column=0, sticky='new')

		self.dashboard_menu_button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10,image=graph_image, text='Dashboards' if settings['SETTINGS']['language'] == 'Spanish' else 'Captures', fg_color='transparent', text_color=('gray10', 'gray90'), hover_color=('gray70', 'gray30'), anchor='w', state = 'disabled')
		self.dashboard_menu_button.grid(row=3, column=0, sticky='new')
		
		self.maps_menu_button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10,image=map_image, text='Mapas' if settings['SETTINGS']['language'] == 'Spanish' else 'Maps', fg_color='transparent', text_color=('gray10', 'gray90'), hover_color=('gray70', 'gray30'), anchor='w', state = 'disabled')
		self.maps_menu_button.grid(row=4, column=0, sticky='new')

		self.appearance_mode_menu = ctk.CTkOptionMenu(self, values=['System', 'Light', 'Dark'], command=self.change_appearance_mode_event)
		self.appearance_mode_menu.set(settings['SETTINGS']['theme'])
		self.appearance_mode_menu.grid(row=5, column=0, padx=20, pady=20, sticky='s')

		self.language_menu = ctk.CTkOptionMenu(self, values=['Spanish', 'English'], command=self.change_language_event)
		self.language_menu.set(settings['SETTINGS']['language'])
		self.language_menu.grid(row=6, column=0, padx=20, pady=20, sticky='s')

	def read_config_file(self):
		settings = configparser.ConfigParser()
		settings.read('config.ini')
		return settings
	
	def change_appearance_mode_event(self, new_appearance_mode):
		self.change_config_file('theme', new_appearance_mode)
		ctk.set_appearance_mode(new_appearance_mode)

	def change_language_event(self, new_language):
		self.change_config_file('language', new_language)

	def change_config_file(self, setting, value):
		settings = self.read_config_file()
		settings['SETTINGS'][setting] = value
		
		with open('config.ini', 'w') as configfile:
			settings.write(configfile)

	def show_menu(self):
		widgets = [(self.menu_button, {'text': 'Menú', 'command': self.hide_menu}),
			(self.upload_menu_button, {'text': 'Cargar datos'}), (self.preprocess_menu_button, {'text': 'Preprocesar datos'}),
			(self.dashboard_menu_button, {'text': 'Dashboards'}), (self.maps_menu_button, {'text': 'Mapas'})]
		
		for widget, config in widgets:
			widget.configure(**config)
			widget.grid(sticky = 'we')

			if widget is self.menu_button:
				widget.grid(sticky = 'we', padx = 20)

			if widget is self.maps_menu_button:
				widget.grid(sticky = 'nwe')

		self.appearance_mode_menu.grid()
		self.language_menu.grid()

	def hide_menu(self):
		widgets_to_hide = [self.menu_button, self.upload_menu_button, self.preprocess_menu_button, 
		    self.dashboard_menu_button, self.maps_menu_button]

		for widget in widgets_to_hide:
			widget.configure(text = '', width = 5)
			widget.grid(sticky = 'w')

			if widget is self.menu_button:
				widget.configure(text = '', command = self.show_menu, width = 5)
				widget.grid(sticky = 'w', padx = 0)

			if widget is self.maps_menu_button:
				widget.grid(sticky = 'nw')
		
		self.appearance_mode_menu.grid_remove()
		self.language_menu.grid_remove()