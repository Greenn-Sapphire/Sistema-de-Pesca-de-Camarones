import customtkinter as ctk

from Widgets.scrollablecheckboxWidget import ScrollableCheckBoxFrame

class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, master, dataframe, checks, **kwargs):
        super().__init__(master, **kwargs)
        self.title('Configuración de la tabla')
        self.geometry("340x360")
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.dataframe = dataframe
        self.orginialdataframe = dataframe
        self.checks = checks

        self.mainframe = ctk.CTkFrame(self)
        self.mainframe.grid(column = 0, row = 0, sticky = 'nswe', padx = 5, pady = 5)
        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.rowconfigure(1, weight = 1)

        self.label = ctk.CTkLabel(self.mainframe, text = 'Columnas a mostrar', font = ctk.CTkFont(size = 12, weight = 'bold'))
        self.label.grid(column = 0, row = 0, sticky = 'we')

        self.checkbox = ScrollableCheckBoxFrame(self.mainframe, item_list = self.dataframe.keys())
        self.checkbox.grid(column = 0, row = 1, sticky = 'nswe', padx = 5, pady = 2)
        self.checkbox.columnconfigure(0, weight = 1)
        self.checkbox.rowconfigure(0, weight = 1)
        for item in self.checks:
            self.checkbox.set_checked(item)

        self.button = ctk.CTkButton(self.mainframe, text = 'Aplicar', command = self.apply_config)
        self.button.grid(column = 0, row = 2, sticky = 'we', padx = 5, pady = 2)

    def apply_config(self):
        try:
            items = self.checkbox.item_list.tolist()
            self.checks = self.checkbox.get_unchecked_items()
            headers_to_hide_index = [items.index(item) for item in self.checks]
            self.checks = self.checkbox.get_checked_items()
            headers_to_show_index = [items.index(item) for item in self.checks]
            self.master.checks = self.checks

            if self.checks:
                self.dataframe = self.orginialdataframe[self.checks]
            else:
                self.dataframe = self.orginialdataframe

            df_list = self.dataframe.values.tolist()
            column_names = self.dataframe.columns.tolist()
            df_list.insert(0, column_names)

            self.master.table.hide_columns(columns = headers_to_hide_index, redraw = True, deselect_all = True)
            self.master.table.display_columns(columns = headers_to_show_index, redraw = True, deselect_all = True)
            self.master.table.set_all_column_widths(width = None, only_set_if_too_small = False, redraw = True)
        except Exception as e:
            print(e)