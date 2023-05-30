import customtkinter as ctk
from Recursos.style import Estilo
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import pandas as pd
import configparser
import matplotlib.pyplot as plt

class visual(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		estilo = Estilo()
		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(1, weight=1)
		self.grid(sticky= 'nswe')

		self.graphic_menu_label = ctk.CTkLabel(self, text="Tipo de gráfica", compound="left")
		self.graphic_menu_label.grid(row=0, column=0, padx=20, pady=20, sticky="e")
		self.graphic_menu = ctk.CTkOptionMenu(self, values=[ "Barras", "Pastel"], command=self.generate_graphic)
		self.graphic_menu.grid(row=0, column=1, padx=20, pady=20, sticky="e")

		self.graphicFrame = ctk.CTkFrame(self, fg_color='white')
		self.graphicFrame.grid(row = 1, column = 0,sticky= 'nswe', columnspan=2)
		#generate_graphic(self, 'Barras')

	def generate_graphic(self, graphic_option):
		#dataframe = pd.read_csv(path=None, sep=',|;', engine="python", on_bad_lines='skip')

		if 'fig' in locals():
			self.frame.destroy()
		# the figure that will contain the plot
		fig = plt.subplots(figsize = (12, 5))

		path = configparser.ConfigParser()
		path.read('config.ini')
		dataframe = pd.read_csv(str(path.get('SETTINGS', 'dataframe_path')))

		plot1 = fig.add_subplot(111)
		plot1.plot(dataframe.plot(x = "NombreServicio", y = "Adultos", kind="bar"))

		# creating the Tkinter canvas
		# containing the Matplotlib figure
		canvas = FigureCanvasTkAgg(fig, master = self.graphicFrame)  
		canvas.draw()

		# placing the canvas on the Tkinter window
		canvas.get_tk_widget().pack()

		# creating the Matplotlib toolbar
		toolbar = NavigationToolbar2Tk(canvas, self.graphicFrame)
		toolbar.update()

		# placing the toolbar on the Tkinter window
		canvas.get_tk_widget().pack()