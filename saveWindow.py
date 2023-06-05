import customtkinter as ctk
from Widgets.style import Estilo
from Archivos import *
from Widgets.scrollablecheckboxWidget import ScrollableCheckBoxFrame
from functions import Data

class save(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		estilo = Estilo()