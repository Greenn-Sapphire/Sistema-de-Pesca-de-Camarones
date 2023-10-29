import customtkinter as ctk

from Widgets.scrollablecheckboxWidget import ScrollableCheckBoxFrame

class FilterPanel(ctk.CTkScrollableFrame):
    def __init__(self, master, dataframe, nofilterlist, **kwargs):
        super().__init__(master, **kwargs)
        self.dataframe = dataframe
        self.nonfilter = nofilterlist
        self.master = master
        self.scroll_checkboxs = {}
        self.filterLabel = ctk.CTkLabel(self, text = 'Filtros', font = ctk.CTkFont(size = 15, weight = 'bold'))
        self.filterLabel.grid(row = 0, column = 0, padx = 20, pady = 20)

        row_index = 1
        for colname in self.dataframe.columns:
            if colname not in self.nonfilter:
                label = ctk.CTkLabel(self, text=colname, font=ctk.CTkFont(size=12, weight='bold'))
                label.grid(row=row_index, column=0, sticky='w', padx=4)

                frame = ScrollableCheckBoxFrame(self, width=200, item_list=self.dataframe[colname].unique().tolist(), command=self.updateScrollBox)
                frame.grid(row=row_index + 1, column=0, padx=2, pady=2, sticky='ns')

                self.scroll_checkboxs[colname] = {'colname': colname, 'frame': frame}
                row_index += 2

    def updateScrollBox(self):
        filtered_df = self.dataframe.copy()

        for column_name, data in self.scroll_checkboxs.items():
            items = data['frame'].get_checked_items()
            if items:
                filtered_df = filtered_df[filtered_df[column_name].isin(items)]

        for column_name, data in self.scroll_checkboxs.items():
            unique_items = filtered_df[column_name].unique().tolist()
            current_items = data['frame'].get_checked_items()
            data['frame'].update_items(unique_items)
            for item in current_items:
                data['frame'].set_checked(item)

    def apply_filter(self):
        try:
            filtered_df = self.master.frame.config_window.getdataframe()
        except:
            filtered_df = self.dataframe

        for column_name, data in self.scroll_checkboxs.items():
            items = data['frame'].get_checked_items()
            if items:
                filtered_df = filtered_df[filtered_df[column_name].isin(items)]

        df_list = filtered_df.values.tolist()
        column_names = filtered_df.columns.tolist()
        df_list.insert(0, column_names)
        return df_list
        
    def apply_filter_graphs(self):
        filtered_df = self.dataframe

        for column_name, data in self.scroll_checkboxs.items():
            items = data['frame'].get_checked_items()
            if items:
                filtered_df = filtered_df[filtered_df[column_name].isin(items)]

        return filtered_df