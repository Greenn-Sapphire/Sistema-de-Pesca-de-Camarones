import customtkinter as ctk

class InformationPanel(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.infoLabel = ctk.CTkLabel(self, text = 'Información', font = ctk.CTkFont(size = 18, weight = 'bold'))
        self.infoLabel.grid(row = 0, column = 0, sticky = 'ew', pady = (20, 10))

        self.Label_ColNum = ctk.CTkLabel(self, text = 'Número de columnas', font = ctk.CTkFont(size = 12, weight = 'bold'))
        self.Label_ColNum.grid(row = 1, column = 0, sticky = 'ew', pady = (1, 0))
        self.Label_Regis = ctk.CTkLabel(self, text = 'Número de registros', font = ctk.CTkFont(size = 12, weight = 'bold'))
        self.Label_Regis.grid(row = 3, column = 0, sticky = 'ew', pady = (1, 0))
        self.Label_Repeat = ctk.CTkLabel(self, text = 'Registros repetidos', font = ctk.CTkFont(size = 12, weight = 'bold'))
        self.Label_Repeat.grid(row = 5, column = 0, sticky = 'ew', pady = (1, 0))
        self.Label_Empty = ctk.CTkLabel(self, text = 'Registros vacios', font = ctk.CTkFont(size = 12, weight = 'bold'))
        self.Label_Empty.grid(row = 7, column = 0, sticky = 'ew', pady = (1, 0))
        self.Label_Type = ctk.CTkLabel(self, text = 'Tipo de dato', font = ctk.CTkFont(size = 12, weight = 'bold'))
        self.Label_Type.grid(row = 9, column = 0, sticky = 'ew', pady = (2, 0))
    
    def showinfo(self, dataframe):
        self.DataCol = ctk.CTkLabel(self, text = len(dataframe.columns))
        self.DataCol.grid(row = 2, column = 0, sticky ='ew', pady = (0, 2))
        self.DataRegis = ctk.CTkLabel(self, text = len(dataframe.index))
        self.DataRegis.grid(row = 4, column = 0, sticky ='ew', pady = (0, 2))
        self.DataRepeat = ctk.CTkLabel(self, text = dataframe.duplicated().sum())
        self.DataRepeat.grid(row = 6, column = 0, sticky ='ew', pady = (0, 2))
        self.DataEmpty = ctk.CTkLabel(self, text = dataframe.isnull().sum())
        self.DataEmpty.grid(row = 8, column = 0, sticky ='ew', pady = (0, 2))
        self.DataType = ctk.CTkLabel(self, text = dataframe.dtypes)
        self.DataType.grid(row = 10, column = 0, sticky ='ew', pady = (0, 2))