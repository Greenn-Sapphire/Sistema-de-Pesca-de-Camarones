from tkinter.filedialog import askopenfilename
from CTkMessagebox import CTkMessagebox
import pandas as pd
import configparser
import os

from Widgets.tableWidget import Table
from preprocessWindow import preprocess

from dataframe import Data as data

#Clase que usara como un tipo diccionario donde estara el dataframe
#from functions import Data | Como importar la Clase
#df = Data.dataframe | Como hacer uso del dataframe de la clase


#Funcion que leera un archivos .csv o .xlsx y lo convertira en un dataframe de pandas
def readDataframe(self, master):
    try:
        file = askopenfilename(initialdir = 'C://', filetypes = [('Excel', '*.xlsx'), ('CSV', '*.csv')])
        path, extension = os.path.splitext(file)
        match extension:
            case '.csv':
                data.dataframe = pd.read_csv(file, sep = ',|;', engine = 'python', on_bad_lines = 'skip')
            case '.xlsx':
                data.dataframe = pd.read_excel(file)
    except:
        CTkMessagebox(title = 'Error', message = 'No se ha seleccionado ningún archivo', icon = 'cancel')
        return
    
    Table(self, data.dataframe, 'upload')

    master.master.preprocessFrame = preprocess(master)
    master.master.preprocessFrame.grid_forget()
    master.master.uploadFrame.grid(row = 0, column = 0, sticky = 'nswe', padx = 10, pady = 10)
    
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
    try:
        self.upload_button.configure(fg_color = ('gray75', 'gray25') if name == 'upload' else 'transparent')
        self.preprocess_button.configure(fg_color = ('gray75', 'gray25') if name == 'visual' else 'transparent')

        self.captures_menu_button.configure(fg_color = ('gray75', 'gray25') if name == 'captures' else 'transparent')
        self.species_menu_button.configure(fg_color = ('gray75', 'gray25') if name == 'species' else 'transparent')
        self.maps_menu_button.configure(fg_color = ('gray75', 'gray25') if name == 'maps' else 'transparent')

        # show selected frame
        if name == 'upload':
            self.uploadFrame.grid(row = 0, column = 0, sticky = 'nswe', padx = 10, pady = 10)
        else:
            self.uploadFrame.grid_forget()
        if name == 'preprocess':
            self.preprocessFrame.grid(row = 0, column = 0, sticky = 'nswe', padx = 10, pady = 10)
        else:
            self.preprocessFrame.grid_forget()
        if name == 'captures':
            self.capturesFrame.grid(row = 0, column = 0, sticky = 'nswe', padx = 10, pady = 10)
        else:
            self.capturesFrame.grid_forget()
        if name == 'species':
            self.speciesFrame.grid(row = 0, column = 0, sticky = 'nswe', padx = 10, pady = 10)
        else:
            self.speciesFrame.grid_forget()
        if name == 'maps':
            self.mapsFrame.grid(row = 0, column = 0, sticky = 'nswe', padx = 10, pady = 10)
        else:
            self.mapsFrame.grid_forget()
    except:
        pass