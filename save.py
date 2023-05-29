import customtkinter as ctk
from Recursos.style import Estilo
from Archivos import *

class save(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		estilo = Estilo()

		self.button = ctk.CTkButton(self, text="Save", command=self.button_callbck)
		self.button.grid(row = 2, column = 1,sticky= 'n')

	def button_callbck(self):
		print("Botón ventana 1")