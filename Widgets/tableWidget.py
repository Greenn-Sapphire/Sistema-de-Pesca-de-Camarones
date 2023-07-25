from datetime import datetime
from Widgets.scrollablecheckboxWidget import ScrollableCheckBoxFrame
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from CTkTable import *
from CTkXYFrame import *
import pandas as pd

from dataframe import Data

class Table(ctk.CTkFrame):
    def __init__(self, master, dataframe, window):
        super().__init__(master)
        try:
            self.frame.destroy()
        except:
            pass
        finally:
            self.frame = CTkXYFrame(master)
            self.frame.grid(row = 0, column = 1, rowspan = 4, sticky = 'nswe', padx = 2, pady = 8)

            try:
                df_list = dataframe.values.tolist()
                column_names = dataframe.columns.tolist()
                df_list.insert(0, column_names)
            except Exception as e:
                print(e)
            
            self.table = CTkTable(self.frame, row = 30, hover_color = '#778899', values = df_list, command = self.UpdateData)
            self.table.grid(row = 0, column = 0)

            if window == 'preprocess':
                self.table.configure(command = self.UpdateData)

    def UpdateData(self, data):
        msn = "Introduce un nuevo valor\n{}\n\nFila: {}\tColumna: {}".format(data['value'], data['row'], data['column'])
        dialog = ctk.CTkInputDialog(text = msn, title = "Modificar valor")

        new_value = dialog.get_input()
        try:
            new_value = new_value.strip()
        except:
            pass

        if new_value is not None and new_value != '':
            self.table.insert(data['row'], data['column'], new_value)

            col_name = self.table.get_column(data['column'])
            col_name = col_name[0]

            if col_name in ['Hr_INI', 'Hr_FIN']:
                new_value = datetime.strptime(new_value, '%H:%M:%S').time()
            else:
                match Data.dataframe[col_name].dtype:
                    case 'int64':
                        new_value = int(new_value)
                    case 'int32':
                        new_value = int(new_value)
                    case 'float32':
                        new_value = float(new_value)
                    case 'float64':
                        new_value = float(new_value)
                    case 'object':
                        new_value = str(new_value)
                    case 'datetime64[ns]':
                        new_value = pd.to_datetime(new_value)
                    case _:
                        print("Tipo de dato no reconocido: ", Data.dataframe[col_name].dtype)

            if not Data.dataframe[col_name].isin([new_value]).any():
                Data.dataframe.iat[data['row'], data['column']] = new_value
                
                match col_name:
                    case 'PROYECTO/SIP':
                        self.destroywidgets(self.Scroll_Check_Project, col_name, 2)
                    case 'AÑO':
                        self.destroywidgets(self.Scroll_Check_Year, col_name, 4)
                    case 'FECHA':
                        self.destroywidgets(self.Scroll_Check_Date, col_name, 6)
                    case 'AREA':
                        self.destroywidgets(self.Scroll_Check_Area, col_name, 8)
                    case 'REGION':
                        self.destroywidgets(self.Scroll_Check_Reg, col_name, 10)
                    case 'SUBZONA':
                        self.destroywidgets(self.Scroll_Check_Sub, col_name, 12)
    
    def destroywidgets(self, widget, col_name, irow):
        widget.grid_forget()
        widget.destroy()
        widget = ScrollableCheckBoxFrame(self.master.infoFrame, width=200, item_list = Data.dataframe[col_name].unique().tolist())
        widget.grid(row = irow, column = 0, padx = 2, pady = 2, sticky = 'ew')