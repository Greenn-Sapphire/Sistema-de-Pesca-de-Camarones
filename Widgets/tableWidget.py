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
            pass
        finally:
            self.frame = ctk.CTkScrollableFrame(master, orientation = 'horizontal', fg_color = 'transparent')
            self.frame.grid(row = 0, column = 1, rowspan = 4, sticky = 'nswe', padx = 10, pady = 5)
                
            table = CTkTable(self.frame, row = 21, column_names = [dataframe.columns.to_numpy().tolist()], values = dataframe.to_numpy().tolist())
            table.grid(row = 0, column = 0)

            self.frameInfo = ctk.CTkLabel(master.infoFrame, text = len(dataframe.columns))
            self.frameInfo.grid(row = 2, column = 0, sticky ='ew')

            self.frameInfo = ctk.CTkLabel(master.infoFrame, text = len(dataframe.index))
            self.frameInfo.grid(row = 4, column = 0, sticky ='ew')

            self.frameInfo = ctk.CTkLabel(master.infoFrame, text = dataframe.duplicated().sum())
            self.frameInfo.grid(row = 6, column = 0, sticky ='ew')

            self.frameInfo = ctk.CTkLabel(master.infoFrame, text = dataframe.isnull().sum())
            self.frameInfo.grid(row = 8, column = 0, sticky ='ew')

            CTkMessagebox(title = 'Aviso', message = 'Tabla creada con éxito', icon = 'check')