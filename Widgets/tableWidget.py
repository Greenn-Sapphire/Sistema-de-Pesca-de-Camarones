import customtkinter as ctk
import pandas as pd

from Widgets.scrollablecheckboxWidget import ScrollableCheckBoxFrame
from Widgets.configWindow import ToplevelWindow
from datetime import datetime
from CTkXYFrame import *
from CTkTable import *

class TableWidget(ctk.CTkFrame):
    def __init__(self, master, df_list, config_image, dataframe, **kwargs):
        super().__init__(master, **kwargs)
        self.originaldataframe = dataframe
        self.dataframe = dataframe
        self.numrow = 20
        self.checks = self.originaldataframe.keys()
        
        self.configButton = ctk.CTkButton(self, text = '', image=config_image, width = 20, height = 20, command = self.open_config)
        self.configButton.grid(row = 0, column = 0, sticky = 'e', padx = 8, pady = (8, 0))
        self.config_window = None
        self.scrollFrame = CTkXYFrame(self, fg_color = 'transparent')
        self.scrollFrame.grid(row = 1, column = 0, sticky = 'nswe', pady = (2, 0))

        self.table = CTkTable(self.scrollFrame, row = 21, hover_color = '#778899', values = df_list, command = self.UpdateData)
        self.table.grid(row = 0, column = 0)

    def open_config(self):
        if self.config_window is None or not self.config_window.winfo_exists():
            self.config_window = ToplevelWindow(self, self.dataframe, self.numrow, self.checks)  # create window if its None or destroyed
        else:
            self.config_window.focus()  # if window exists focus it

    def UpdateData(self, data):					
        msn = 'Introduce un nuevo valor\n{}\n\nFila: {}\tColumna: {}'.format(data['value'], data['row'], data['column'])
        dialog = ctk.CTkInputDialog(text = msn, title = 'Modificar valor')

        new_value = dialog.get_input()

        if new_value is not None and new_value != '':
            self.table.insert(data['row'], data['column'], new_value)

            col_name = self.table.get_column(data['column'])
            col_name = col_name[0]

            if col_name in ['Hr_INI', 'Hr_FIN']:
                new_value = datetime.strptime(new_value, '%H:%M:%S').time()
            else:
                match self.master.dataframe[col_name].dtype:
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
                        print('Tipo de dato no reconocido: ', self.master.dataframe[col_name].dtype)

            if not self.master.dataframe[col_name].isin([new_value]).any():
                self.master.dataframe.iat[data['row'], data['column']] = new_value
                
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
        widget = ScrollableCheckBoxFrame(self.filterFrame, width=200, item_list = self.dataframe[col_name].unique().tolist())
        widget.grid(row = irow, column = 0, padx = 2, pady = 2, sticky = 'ew')