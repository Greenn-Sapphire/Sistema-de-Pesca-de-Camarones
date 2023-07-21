import customtkinter as ctk
import seaborn as sns

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Widgets.style import Estilo
import matplotlib.pyplot as plt
from dataframe import Data

class species(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		estilo = Estilo()
		self.grid(sticky= 'nswe')
		self.grid_columnconfigure(1, weight = 1)
		self.grid_rowconfigure(0, weight = 1)

		self.infoFrame = ctk.CTkScrollableFrame(self)
		self.infoFrame.configure(corner_radius = 5, scrollbar_button_hover_color = ('gray86', 'gray17'), scrollbar_button_color = ('gray81', 'gray20'))
		self.infoFrame.grid(row = 0, column = 0, sticky = 'nwse', padx = 8, pady = 8)
		self.infoFrame.grid_rowconfigure(6, weight = 1)
		self.infoFrame.grid_columnconfigure(0, weight = 1)
		
		self.infoLabel = ctk.CTkLabel(self.infoFrame, text = 'Filtros', font = ctk.CTkFont(size = 15, weight = 'bold'))
		self.infoLabel.grid(row = 0, column = 0, padx = 20, pady = 20)
		
		self.Label_Species = ctk.CTkLabel(self.infoFrame, text = 'Especie:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.OptionMenu_Species = ctk.CTkOptionMenu(self.infoFrame, values = sorted([str(valor) for valor in Data.dataframe['ESPECIE'].unique().tolist()]), dynamic_resizing = False)
		self.Label_Species.grid(row = 1, column = 0, sticky = 'w')
		self.OptionMenu_Species.grid(row = 2, column = 0, padx = 2, pady = 2, sticky = 'ew')

		self.Label_Fam = ctk.CTkLabel(self.infoFrame, text = 'Familia:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.OptionMenu_Fam = ctk.CTkOptionMenu(self.infoFrame, values = sorted([str(valor) for valor in Data.dataframe['FAMILIA'].unique().tolist()]), dynamic_resizing = False)
		self.Label_Fam.grid(row = 3, column = 0, sticky = 'w')
		self.OptionMenu_Fam.grid(row = 4, column = 0, padx = 2, pady = 2, sticky = 'ew')
			
		self.Label_Group = ctk.CTkLabel(self.infoFrame, text = 'Grupo:', font = ctk.CTkFont(size = 12, weight = 'bold'))
		self.OptionMenu_Group = ctk.CTkOptionMenu(self.infoFrame, values = sorted([str(valor) for valor in Data.dataframe['GRUPO'].unique().tolist()]), dynamic_resizing = False)
		self.Label_Group.grid(row = 5, column = 0, sticky = 'w')
		self.OptionMenu_Group.grid(row = 6, column = 0, padx = 2, pady = 2, sticky = 'ew')

		self.Button = ctk.CTkButton(self, text = 'Aplicar filtros')
		self.Button.grid(row = 1, column = 0, sticky = 'ew', padx = 8, pady = (2, 8))

		self.Dashboard_Frame = ctk.CTkFrame(self)
		self.Dashboard_Frame.grid(row = 0, column = 1, rowspan = 2, sticky = 'nsew', padx = 8, pady = 8)

		# Crear los datos y generar la gráfica usando Seaborn
		fig, axs = plt.subplots(2, 2, figsize=(12, 7), facecolor='none')
		plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.3)

		axs[0, 0].pie(Data.dataframe['DIA/NOCHE'].value_counts(), autopct='%1.1f%%', colors=['skyblue', 'lightcoral'])
		axs[0, 0].set_title('Porcentaje de Lances de Día y de Noche')
		
		sns.boxplot(x='LONG_TOT', data=Data.dataframe, ax = axs[0, 1])
		axs[0, 1].set_title('Distribución de Longitud de Especies')

		axs[1, 0].pie(Data.dataframe['SEXO'].value_counts(), autopct='%1.1f%%', colors=['skyblue', 'lightcoral', 'blueviolet'])
		axs[1, 0].set_title('Porcentaje Sexos')

		sns.boxplot(x='PESO', data=Data.dataframe, ax = axs[1, 1])
		axs[1, 1].set_title('Distribución de Peso de Especies')
		plt.tight_layout()

		# Crear el lienzo de la gráfica y agregarlo al marco
		canvas = FigureCanvasTkAgg(fig, master = self.Dashboard_Frame)
		canvas.draw()
		canvas.get_tk_widget().configure(bg = 'lightgray', highlightthickness = 0)
		canvas.get_tk_widget().pack()