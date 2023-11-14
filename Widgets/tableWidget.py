import customtkinter as ctk
import openpyxl
import os

from tkinter.filedialog import asksaveasfilename
from Widgets.configWindow import ToplevelWindow
from CTkMessagebox import CTkMessagebox
from tksheet import Sheet
from Archivos import *
from PIL import Image

class TableWidget(ctk.CTkFrame):
    def __init__(self, master, df_list, dataframe, **kwargs):
        super().__init__(master, **kwargs)
        self.dataframe = dataframe
        self.checks = self.dataframe.keys()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'Archivos')
        config_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, 'light_settings.png')),
                                                    dark_image=Image.open(os.path.join(image_path, 'dark_settings.png')), size=(20, 20))
        save_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, 'light_save.png')),
                                                    dark_image=Image.open(os.path.join(image_path, 'dark_save.png')), size=(20, 20))

        self.table_save_button = ctk.CTkButton(self, text = 'Guardar tabla', image=save_image, width = 20, height = 20, command = self.save_table)
        self.table_save_button.grid(row = 0, column = 0, sticky = 'e', padx = (0, 185), pady = (8, 0))
        self.table_config_button = ctk.CTkButton(self, text = 'Configuración de tabla', image=config_image, width = 20, height = 20, command = self.open_config)
        self.table_config_button.grid(row = 0, column = 0, sticky = 'e', padx = (185, 8), pady = (8, 0))
        self.config_window = None

        self.table = Sheet(self)
        self.table.headers(df_list[0])
        self.table.set_sheet_data(df_list[1:])
        self.table.enable_bindings()
        self.table.disable_bindings('column_drag_and_drop', 'row_drag_and_drop', 'edit_header', 'edit_index', 'rc_delete_column')
        self.table.set_all_column_widths(width = None, only_set_if_too_small = False, redraw = True)
        self.table.grid(row = 1, column = 0, sticky = 'nswe', pady = (2, 0))

    def open_config(self):
        if self.config_window is None or not self.config_window.winfo_exists():
            self.config_window = ToplevelWindow(self, self.dataframe, self.checks)  # create window if its None or destroyed
        else:
            self.config_window.focus()  # if window exists focus it

    def save_table(self):
        try:
            file_path = asksaveasfilename(initialdir = 'C://', defaultextension='.xlsx', filetypes = [('Excel', '*.xlsx'), ('CSV', '*.csv')])
            if file_path:
                workbook = openpyxl.Workbook()
                sheet = workbook.active

                headers = self.table.headers()
                sheet.append(headers)
                sheet_data = self.table.get_sheet_data()
                for row_data in sheet_data:
                    sheet.append(row_data)

                workbook.save(file_path)
                CTkMessagebox(title = 'Aviso', message = 'Archivo guardado en: ' + file_path, icon = 'check')
        except Exception as e:
            print(e)