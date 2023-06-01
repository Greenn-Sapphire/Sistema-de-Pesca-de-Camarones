from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from CTkTable import *

class Table(ctk.CTkFrame):
    def __init__(self, master, dataframe):
        super().__init__(master)
        try:
            self.frame.destroy()
            self.frameInfo.destroy()
        except:
            print("Table does not exist")
        finally:
            self.frame = ctk.CTkScrollableFrame(master, orientation='horizontal', fg_color='transparent')
            self.frame.grid(row = 1, column = 1, sticky = 'nswe', padx=10, pady=5)
                
            table = CTkTable(self.frame, row = 20, column_names=[dataframe.columns.to_numpy().tolist()] ,values=dataframe.to_numpy().tolist())
            table.grid(row= dataframe.shape[0], column= dataframe.shape[1])

            self.frameInfo = ctk.CTkLabel(master.infoFrame, text = len(dataframe.columns))
            self.frameInfo.grid(row=2, column = 0, sticky='n')

            self.frameInfo = ctk.CTkLabel(master.infoFrame, text = len(dataframe.index))
            self.frameInfo.grid(row=4, column = 0, sticky='n')

            self.frameInfo = ctk.CTkLabel(master.infoFrame, text = dataframe.duplicated().sum())
            self.frameInfo.grid(row=6, column = 0, sticky='n')

            self.frameInfo = ctk.CTkLabel(master.infoFrame, text = dataframe.isnull().sum())
            self.frameInfo.grid(row=8, column = 0, sticky='n')

            CTkMessagebox(title = 'Aviso', message = 'Tabla creada con éxito', icon = 'check')

class Options_Widget(ctk.CTkFrame):
    def __init__(self, master, actualrow, actualcolumn, numofcolumns, numofrows):
        super().__init__(master)
        self.Optionswidget = ctk.CTkFrame(master, corner_radius = 5)
        self.Optionswidget.grid(row = actualrow, column = actualcolumn, rowspan = 2, sticky= 'nwse', padx=8, pady=8)
        self.Optionswidget.grid_columnconfigure(numofcolumns, weight=1)
        self.Optionswidget.grid_rowconfigure(numofrows, weight=1)