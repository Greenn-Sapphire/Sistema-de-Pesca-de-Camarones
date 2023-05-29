import customtkinter as ctk
from Recursos.style import Estilo
from visual import visual
from upload import upload
from save import save
import configparser
import os
from PIL import Image
from Archivos import *

class App(ctk.CTk):
	def __init__(self):
		super().__init__()	
		estilo = Estilo()
		settings = configparser.ConfigParser()
		settings.read('config.ini')

		image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
		self.home_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
													dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
		self.chat_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
													dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
		self.add_user_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
														dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

		ctk.set_appearance_mode(settings['SETTINGS']['theme'])
		self.title("Sistema de Pesca de Camarones")
		self.iconbitmap('Archivos/shrimp_1.ico')
		width, height = self.winfo_screenwidth(), self.winfo_screenheight()
		self.geometry("%dx%d+0+0" % (width, height))
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)

		self.home_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
													dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
		self.chat_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
													dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
		self.add_user_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
														dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

		#Barra de navegación
		self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
		self.navigation_frame.grid(row=0, column=0, sticky="ns")
		self.navigation_frame.grid_rowconfigure(3, weight=1)
		self.navigation_frame.grid_columnconfigure(0, weight=1)

		self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="Opciones", compound="left", font=ctk.CTkFont(size=15, weight="bold"))
		self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

		self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, image=self.home_image, text="Cargar datos" if settings['SETTINGS']['language'] == "Spanish" else "Load data", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.home_button_event)
		self.home_button.grid(row=1, column=0, sticky="new")
		self.frame_2_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, image=self.chat_image, text="Visualizar datos" if settings['SETTINGS']['language'] == "Spanish" else "Visualize data", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.frame_2_button_event)
		self.frame_2_button.grid(row=2, column=0, sticky="new")
		self.frame_3_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,image=self.add_user_image, text="Guardar visualizaciones" if settings['SETTINGS']['language'] == "Spanish" else "Save visualizations", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.frame_3_button_event)
		self.frame_3_button.grid(row=3, column=0, sticky="new")

		self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=[ "System", "Light", "Dark"], command=self.change_appearance_mode_event)
		self.appearance_mode_menu.set(settings['SETTINGS']['theme'])
		self.appearance_mode_menu.grid(row=4, column=0, padx=20, pady=20, sticky="s")

		self.language_menu = ctk.CTkOptionMenu(self.navigation_frame, values=[ "Spanish", "English"], command=self.change_language_event)
		self.language_menu.set(settings['SETTINGS']['language'])
		self.language_menu.grid(row=5, column=0, padx=20, pady=20, sticky="s")

		#Frame interactuable
		self.interactFrame = ctk.CTkFrame(self, fg_color='transparent')
		self.interactFrame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
		self.interactFrame.grid_rowconfigure(0, weight=1)
		self.interactFrame.grid_columnconfigure(0, weight=1)

		self.uploadFrame = upload(self.interactFrame)

		self.visualFrame = visual(self.interactFrame)

		self.saveFrame = save(self.interactFrame)

		self.select_frame_by_name("upload")

	def change_appearance_mode_event(self, new_appearance_mode):
		settings = configparser.ConfigParser()
		settings.read('config.ini')
		if(new_appearance_mode == 'System'):
			settings['SETTINGS']['theme'] = 'System'
		elif(new_appearance_mode == 'Light'):
			settings['SETTINGS']['theme'] = 'Light'
		elif(new_appearance_mode == 'Dark'):
			settings['SETTINGS']['theme'] = 'Dark'
		ctk.set_appearance_mode(new_appearance_mode)

		with open('config.ini', 'w') as configfile:
			settings.write(configfile)

	def change_language_event(self, new_language):
		settings = configparser.ConfigParser()
		settings.read('config.ini')
		if(new_language == 'Spanish'):
			settings['SETTINGS']['language'] = 'Spanish'
		else:
			settings['SETTINGS']['language'] = 'English'

		with open('config.ini', 'w') as configfile:
			settings.write(configfile)

	def select_frame_by_name(self, name):
		self.home_button.configure(fg_color=("gray75", "gray25") if name == "upload" else "transparent")
		self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "visual" else "transparent")
		self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "save" else "transparent")

		# show selected frame
		if name == "upload":
			self.uploadFrame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
		else:
			self.uploadFrame.grid_forget()
		if name == "visual":
			self.visualFrame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
		else:
			self.visualFrame.grid_forget()
		if name == "save":
			self.saveFrame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
		else:
			self.saveFrame.grid_forget()

	def home_button_event(self):
		self.select_frame_by_name("upload")

	def frame_2_button_event(self):
		self.select_frame_by_name("visual")

	def frame_3_button_event(self):
		self.select_frame_by_name("save")

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()