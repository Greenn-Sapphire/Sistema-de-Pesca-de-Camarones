import customtkinter as ctk
from Recursos.style import Estilo

class visual(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		estilo = Estilo()

		self.button = ctk.CTkButton(self, text="Botón", command=self.button_callbck)
		self.button.grid(row = 2, column = 1,sticky= 'n')

	def button_callbck(self):
		print("Botón ventana 1")