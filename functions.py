from tkinter.filedialog import askopenfilename
from CTkMessagebox import CTkMessagebox
import pandas as pd
import configparser

from Recursos.widgets import Table

def readDataframe(self):
    try:
        filename = askopenfilename(initialdir = 'C://', filetypes = [("CSV", "*.csv"), ("Excel", "*.xlsx")])
        dataframe = pd.read_csv(filename, sep = ',|;', engine = 'python', on_bad_lines = 'skip')
    except:
        CTkMessagebox(title = 'Error', message = 'No se ha seleccionado ninguna archivo', icon = 'cancel')
        return
    
    Table(self, dataframe)

def readConfig():
    settings = configparser.ConfigParser()
    settings.read('config.ini')
    return settings

def changeConfig(setting, value):
    settings = readConfig()
    settings['SETTINGS'][setting] = value
    
    with open('config.ini', 'w') as configfile:
        settings.write(configfile)

def select_frame_by_name(self, name):
    self.home_button.configure(fg_color=("gray75", "gray25") if name == "upload" else "transparent")
    self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "visual" else "transparent")
    self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "save" else "transparent")

    # show selected frame
    if name == "upload":
        self.uploadFrame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
    else:
        self.uploadFrame.grid_forget()
    if name == "visual":
        self.visualFrame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
    else:
        self.visualFrame.grid_forget()
    if name == "save":
        self.saveFrame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
    else:
        self.saveFrame.grid_forget()