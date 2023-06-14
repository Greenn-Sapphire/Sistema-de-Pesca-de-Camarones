from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import customtkinter as ctk
import matplotlib
import pandas as pd
matplotlib.use('TkAgg')

from Widgets.scrollableinfoframeWidget import ScrollableInfoFrame
from Widgets.graphicWidget import GraphicFrame
from Widgets.style import Estilo
from functions import Data

class visual(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		estilo = Estilo()
		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(1, weight=1)
		self.grid(sticky= 'nswe')

		self.infoFrame = ScrollableInfoFrame(self)
		#self.infoFrame.configure(corner_radius = 5, scrollbar_button_hover_color = self._fg_color, scrollbar_button_color = self._fg_color)
		self.infoFrame.grid(row = 0, column = 0, rowspan = 2, sticky = 'nwse', padx = 8, pady = 8)
		self.infoFrame.grid_columnconfigure(0, weight = 1)
		self.infoFrame.grid_rowconfigure(8, weight = 1)
	
		self.infoFrameLabel = ctk.CTkLabel(self.infoFrame, text = 'Filtros', compound = 'left', font = ctk.CTkFont(size = 15, weight = 'bold'))
		self.infoFrameLabel.grid(row = 0, column = 0, padx = 20, pady = 20)

		self.filterName = ctk.CTkLabel(self.infoFrame, text = 'Filtrar')
		self.filterName.grid(row = 1, column = 0, padx = 20)
		self.filterFrame = ctk.CTkOptionMenu(self.infoFrame, values = ['Mayor que', 'Menor que'], command = self.generate_graphic)
		self.filterFrame.grid(row = 1, column = 0, padx = 20, pady = 20)
		self.filterFrame = ctk.CTkOptionMenu(self.infoFrame, values = ['Mayor que', 'Menor que'], command = self.generate_graphic)
		self.filterFrame.grid(row = 1, column = 0, padx = 20, pady = 20)
		self.filterFrame = ctk.CTkOptionMenu(self.infoFrame, values = ['Mayor que', 'Menor que'], command = self.generate_graphic)
		self.filterFrame.grid(row = 1, column = 0, padx = 20, pady = 20)

		self.graphic_menu_label = ctk.CTkLabel(self, text = 'Tipo de gráfica', compound = 'left')
		self.graphic_menu_label.grid(row = 0, column = 1, padx = 20, sticky = 'e')
		self.graphic_menu = ctk.CTkOptionMenu(self, values = ['Barras', 'Cajas', 'Histograma', 'Dispersion', 'Pastel'], command = self.generate_graphic)
		self.graphic_menu.grid(row = 0, column = 1, pady = 8, sticky = 'e')

	def generate_graphic(self, graphictype):
		match graphictype:
			case 'Barras':
				graphictype = 'bar'
			case 'Cajas':
				graphictype = 'boxplot'
			case 'Histograma':
				graphictype = 'hist'
			case 'Pastel':
				graphictype = 'pie'
			case 'Dispersion':
				graphictype = 'scatter'

		self.graphicFrame = GraphicFrame(self, Data.dataframe, 'NombreServicio', 'Precio', graphictype)
		self.graphicFrame.grid(row = 1, column = 1, sticky = 'nswe', padx = 10, pady = 5)