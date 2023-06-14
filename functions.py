from tkinter.filedialog import askopenfilename
from CTkMessagebox import CTkMessagebox
import pandas as pd
import configparser
import os

from Widgets.tableWidget import Table

#Clase que usara como un tipo diccionario donde estara el dataframe
#from functions import Data | Como importar la Clase
#df = Data.dataframe | Como hacer uso del dataframe de la clase
class Data():
    pass
data = Data

#Funcion que leera un archivos .csv o .xlsx y lo convertira en un dataframe de pandas
def readDataframe(self):
    try:
        file = askopenfilename(initialdir = 'C://', filetypes = [('CSV', '*.csv'), ('Excel', '*.xlsx')])
        path, extension = os.path.splitext(file)
        match extension:
            case '.csv':
                data.dataframe = pd.read_csv(file, sep = ',|;', engine = 'python', on_bad_lines = 'skip')
            case '.xlsx':
                data.dataframe = pd.read_excel(file)
    except:
        CTkMessagebox(title = 'Error', message = 'No se ha seleccionado ningún archivo', icon = 'cancel')
        return
    
    Table(self, data.dataframe)

#Funcion que leera el archivo config.ini
def readConfig():
    settings = configparser.ConfigParser()
    settings.read('config.ini')
    return settings

#Funcion para escribir sobre el archivo config.ini
def changeConfig(setting, value):
    settings = readConfig()
    settings['SETTINGS'][setting] = value
    
    with open('config.ini', 'w') as configfile:
        settings.write(configfile)

#Funcion para cambiar entre frames principales
def select_frame_by_name(self, name):
    self.home_button.configure(fg_color = ('gray75', 'gray25') if name == 'upload' else 'transparent')
    self.frame_2_button.configure(fg_color = ('gray75', 'gray25') if name == 'visual' else 'transparent')
    self.frame_3_button.configure(fg_color = ('gray75', 'gray25') if name == 'save' else 'transparent')

    # show selected frame
    if name == 'upload':
        self.uploadFrame.grid(row = 0, column = 0, sticky = 'nswe', padx = 10, pady = 10)
    else:
        self.uploadFrame.grid_forget()
    if name == 'visual':
        self.visualFrame.grid(row = 0, column = 0, sticky = 'nswe', padx = 10, pady = 10)
    else:
        self.visualFrame.grid_forget()
    if name == 'save':
        self.saveFrame.grid(row = 0, column = 0, sticky = 'nswe', padx = 10, pady = 10)
    else:
        self.saveFrame.grid_forget()