import customtkinter as ctk

from Widgets.scrollablecheckboxWidget import ScrollableCheckBoxFrame
from Widgets.spinbox import SpinBoxWidget
from CTkMessagebox import CTkMessagebox
from CTkTable import *

class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, master, dataframe, **kwargs):
        super().__init__(master, **kwargs)
        self.title('Configuración de la tabla')
        self.geometry("340x360")
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.dataframe = dataframe
        self.orginialdataframe = dataframe

        self.mainframe = ctk.CTkFrame(self)
        self.mainframe.grid(column = 0, row = 0, sticky = 'nswe', padx = 5, pady = 5)
        self.mainframe.columnconfigure(0, weight = 1)

        self.label = ctk.CTkLabel(self.mainframe, text = 'Número de registros a mostrar', font = ctk.CTkFont(size = 12, weight = 'bold'))
        self.label.grid(column = 0, row = 1, sticky = 'we')

        self.spinbox = SpinBoxWidget(self.mainframe, width = 100, height = 32)
        self.spinbox.grid(column = 0, row = 2, sticky = 'we', padx = 5, pady = (2, 5))

        self.label = ctk.CTkLabel(self.mainframe, text = 'Columnas a mostrar', font = ctk.CTkFont(size = 12, weight = 'bold'))
        self.label.grid(column = 0, row = 3, sticky = 'we')

        self.checkbox = ScrollableCheckBoxFrame(self.mainframe,  item_list = self.dataframe.keys())
        self.checkbox.grid(column = 0, row = 4, sticky = 'we', padx = 5, pady = (2, 5))

        self.button = ctk.CTkButton(self.mainframe, text = 'Aplicar', command = self.apply_config)
        self.button.grid(column = 0, row = 5, sticky = 'we', padx = 5, pady = 2)

    def apply_config(self):
        rowsnum = self.spinbox.get()
        if rowsnum < 1 or rowsnum > len(self.dataframe.index):
            CTkMessagebox(title = 'Error', message = f'El número introducido está fuera de rango.', icon = 'cancel')
            return
        rowsnum += 1
        checkcolumns = self.checkbox.get_checked_items()

        if checkcolumns:
            self.dataframe = self.orginialdataframe[checkcolumns]
        else:
            self.dataframe = self.orginialdataframe

        df_list = self.dataframe.values.tolist()
        column_names = self.dataframe.columns.tolist()
        df_list.insert(0, column_names)

        self.master.table.grid_forget()
        self.master.table.destroy()
        self.master.table = CTkTable(self.master.scrollFrame, row = rowsnum, hover_color = '#778899', values = df_list, command = self.master.UpdateData)
        self.master.table.grid(row = 0, column = 0)
    
    def getdataframe(self):
        return self.dataframe