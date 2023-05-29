import customtkinter as ctk
from tkinter import ttk
import pandas as pd
from Recursos.style import Estilo
from tkinter.filedialog import askopenfilename
from CTkTable import *
from Archivos import *

class upload(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		estilo = Estilo()
		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(1, weight=1)
		self.grid(sticky= 'nswe')

		self.uploadbutton = ctk.CTkButton(self, text="Cargar archivo", command=self.button_callbck)
		self.uploadbutton.grid(row = 0, column = 0, sticky= 'w')
		self.connectbutton = ctk.CTkButton(self, text="Conectar a una base de datos", command=self.button_callbck)
		self.connectbutton.grid(row = 0, column = 1, sticky= 'e')
		#self.filterbutton = ctk.CTkButton(self, text="Conectar a una base de datos", command=self.button_callbck)
		#self.filterbutton.grid(row = 0, column = 1, sticky= 'e')

		

	def button_callbck(self):
		filename = askopenfilename(initialdir="C://")
		dataframe = pd.read_csv(filename, sep=',|;', engine="python", on_bad_lines='skip')

		if 'table' in locals():
			self.frame.destroy()

		self.frame = ctk.CTkScrollableFrame(self, orientation='horizontal', fg_color='transparent')
		self.frame.grid(row = 1, column = 0, sticky = 'nswe', columnspan=2, padx=10, pady=10)
		table = CTkTable(self.frame, column_names=[dataframe.columns.to_numpy().tolist()] ,values=dataframe.to_numpy().tolist())
		table.grid(row= dataframe.shape[0], column= dataframe.shape[1])

		"""
		tableframe = ttk.Treeview(self.frame, columns = dataframe.columns, show = "headings")
		for column in dataframe.columns:
			tableframe.heading(column, text=column)
		tableframe.grid(row=1, column=0, columnspan=2)

		for i, (name, score) in enumerate(dataframe, start=1):
			tableframe.insert("", "end", values=(i, name, score))
		
		#Codigo de tabla que funciona
		self._widgets = []
		for row in range(dataframe.shape[0]):
			current_row = []
			for column in range(dataframe.shape[1]):
				if row == 0:
					label = ctk.CTkLabel(self.frame, text=dataframe.columns[column], width=10)
					label.grid(row=row, column=column, sticky="we", padx=1, pady=1)

				label = ctk.CTkLabel(self.frame, text=dataframe.iloc[row, column], width=10)
				label.grid(row=row+1, column=column, sticky="we", padx=1, pady=1)
				current_row.append(label)
			self._widgets.append(current_row)

		for column in range(dataframe.shape[1]):
			self.grid_columnconfigure(column, weight=1)
		"""
