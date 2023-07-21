from Widgets.scrollablecheckboxWidget import ScrollableCheckBoxFrame
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from CTkTable import *
from CTkXYFrame import *
import pandas as pd

class Table(ctk.CTkFrame):
    def __init__(self, master, dataframe, window):
        super().__init__(master)
        try:
            self.frame.destroy()
            self.frameInfo.destroy()
        except:
            pass
        finally:
            self.frame = CTkXYFrame(master)
            self.frame.grid(row = 0, column = 1, rowspan = 4, sticky = 'nswe', padx = 2, pady = 8)

            df_list = dataframe.values.tolist()
            column_names = dataframe.columns.tolist()
            df_list.insert(0, column_names)

            if window == 'upload':
                self.table = CTkTable(self.frame, row = 30, hover_color = '#778899', values = df_list)
                self.table.grid(row = 0, column = 0)
                
                self.DataCol = ctk.CTkLabel(master.infoFrame, text = len(dataframe.columns))
                self.DataRegis = ctk.CTkLabel(master.infoFrame, text = len(dataframe.index))
                self.DataRepeat = ctk.CTkLabel(master.infoFrame, text = dataframe.duplicated().sum())
                self.DataEmpty = ctk.CTkLabel(master.infoFrame, text = dataframe.isnull().sum())
                self.DataCol.grid(row = 2, column = 0, sticky ='ew', pady = (0, 2))
                self.DataRegis.grid(row = 4, column = 0, sticky ='ew', pady = (0, 2))
                self.DataRepeat.grid(row = 6, column = 0, sticky ='ew', pady = (0, 2))
                self.DataEmpty.grid(row = 8, column = 0, sticky ='ew', pady = (0, 2))
            else:
                self.table = CTkTable(self.frame, row = 30, hover_color = '#778899', values = df_list, command = self.UpdateData)
                self.table.grid(row = 0, column = 0)

                self.Label_Project = ctk.CTkLabel(master.infoFrame, text = 'Proyecto:', font = ctk.CTkFont(size = 12, weight = 'bold'))
                self.Scroll_Check_Project = ScrollableCheckBoxFrame(master.infoFrame, width=200, item_list = dataframe['PROYECTO/SIP'].unique().tolist())
                self.Label_Project.grid(row = 1, column = 0, sticky = 'w', padx = 4)
                self.Scroll_Check_Project.grid(row=2, column=0, padx=2, pady=2, sticky="ns")

                self.Label_Year = ctk.CTkLabel(master.infoFrame, text = 'Año:', font = ctk.CTkFont(size = 12, weight = 'bold'))
                self.Scroll_Check_Year = ScrollableCheckBoxFrame(master.infoFrame, width=200, item_list = dataframe['AÑO'].unique().tolist())
                self.Label_Year.grid(row = 3, column = 0, sticky = 'w', padx = 4)
                self.Scroll_Check_Year.grid(row=4, column=0, padx=2, pady=2, sticky="ns")
		
                dataframe['FECHA'] = pd.to_datetime(dataframe['FECHA'], unit='s')
                fechas_formateadas = dataframe['FECHA'].dt.strftime('%d/%m/%Y').tolist()
                fechas_unicas = pd.Series(fechas_formateadas).unique().tolist()	
                self.Label_Date = ctk.CTkLabel(master.infoFrame, text = 'Fecha:', font = ctk.CTkFont(size = 12, weight = 'bold'))
                self.OptionMenu_Date = ScrollableCheckBoxFrame(master.infoFrame, width=200, item_list = fechas_unicas)
                self.Label_Date.grid(row = 5, column = 0, sticky = 'w', padx = 4)
                self.OptionMenu_Date.grid(row = 6, column = 0, padx = 2, pady = 2, sticky = 'ew')
                    
                self.Label_Area = ctk.CTkLabel(master.infoFrame, text = 'Área:', font = ctk.CTkFont(size = 12, weight = 'bold'))
                self.OptionMenu_Area = ScrollableCheckBoxFrame(master.infoFrame, width=200, item_list = dataframe['AREA'].unique().tolist())
                self.Label_Area.grid(row = 7, column = 0, sticky = 'w', padx = 4)
                self.OptionMenu_Area.grid(row = 8, column = 0, padx = 2, pady = 2, sticky = 'ew')
                    
                self.Label_Reg = ctk.CTkLabel(master.infoFrame, text = 'Región:', font = ctk.CTkFont(size = 12, weight = 'bold'))
                self.OptionMenu_Reg = ScrollableCheckBoxFrame(master.infoFrame, width=200, item_list = dataframe['REGION'].unique().tolist())
                self.Label_Reg.grid(row = 9, column = 0, sticky = 'w', padx = 4)
                self.OptionMenu_Reg.grid(row = 10, column = 0, padx = 2, pady = 2, sticky = 'ew')
                    
                self.Label_Reg = ctk.CTkLabel(master.infoFrame, text = 'Subzona:', font = ctk.CTkFont(size = 12, weight = 'bold'))
                self.OptionMenu_Reg = ScrollableCheckBoxFrame(master.infoFrame, width=200, item_list = dataframe['SUBZONA'].unique().tolist())
                self.Label_Reg.grid(row = 11, column = 0, sticky = 'w', padx = 4)
                self.OptionMenu_Reg.grid(row = 12, column = 0, padx = 2, pady = 2, sticky = 'ew')

            CTkMessagebox(title = 'Aviso', message = 'Tabla creada con éxito', icon = 'check')

    def UpdateData(self, data):
        msn = "Introduce un nuevo valor\n{}\n\nFila: {}\tColumna: {}".format(data['value'], data['row'], data['column'])
        dialog = ctk.CTkInputDialog(text = msn, title = "Modificar valor")
        self.table.insert(data['row'], data['column'], dialog.get_input())