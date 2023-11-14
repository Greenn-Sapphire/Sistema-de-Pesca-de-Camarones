import customtkinter as ctk
import numpy

from Widgets.scrollablecheckboxWidget import ScrollableCheckBoxFrame

class FilterPanel(ctk.CTkScrollableFrame):
    def __init__(self, master, dataframe, nofilterlist, **kwargs):
        super().__init__(master, **kwargs)
        self.dataframe = dataframe
        self.nonfilter = nofilterlist
        self.scroll_checkboxs = {}
        self.filterLabel = ctk.CTkLabel(self, text = 'Filtros', font = ctk.CTkFont(size = 15, weight = 'bold'))
        self.filterLabel.grid(row = 0, column = 0, padx = 20, pady = 20)

        row_index = 1
        for colname in self.dataframe.columns:
            if colname not in self.nonfilter:
                label = ctk.CTkLabel(self, text=colname, font=ctk.CTkFont(size=12, weight='bold'))
                label.grid(row=row_index, column=0, sticky='w', padx=4)
                row_index += 1
                
                if self.dataframe[colname].isnull().any():
                    item_list = sorted(self.dataframe[colname].dropna().unique().tolist())
                    item_list.insert(0, numpy.nan)
                else:
                    item_list = sorted(self.dataframe[colname].unique().tolist())
                
                row_index += 1
                scroll_checkbox_frame = ScrollableCheckBoxFrame(self, width=200, item_list=item_list, row_index=row_index, command=self.updateScrollBox)
                scroll_checkbox_frame.grid(row=row_index, column=0, padx=2, pady=2, sticky='ns')
                row_index = scroll_checkbox_frame.get_actual_row()

                self.scroll_checkboxs[colname] = {'colname': colname, 'scroll_checkbox_frame': scroll_checkbox_frame}

    def updateScrollBox(self):
        filtered_df = self.dataframe

        for column_name, data in self.scroll_checkboxs.items():
            items = data['scroll_checkbox_frame'].get_checked_items()
            if items:
                filtered_df = filtered_df[filtered_df[column_name].isin(items)]

            unique_items = filtered_df[column_name].unique().tolist()

            data['scroll_checkbox_frame'].update_items(unique_items)

            for item in items:
                data['scroll_checkbox_frame'].set_checked(item)

    def apply_filter(self):
        filtered_df = self.dataframe

        for column_name, data in self.scroll_checkboxs.items():
            items = data['scroll_checkbox_frame'].get_checked_items()
            if items:
                filtered_df = filtered_df[filtered_df[column_name].isin(items)]

        indexes_to_display = filtered_df.index.tolist()
        return indexes_to_display
        
    def apply_filter_graphs(self):
        filtered_df = self.dataframe

        for column_name, data in self.scroll_checkboxs.items():
            items = data['scroll_checkbox_frame'].get_checked_items()
            if items:
                filtered_df = filtered_df[filtered_df[column_name].isin(items)]

        return filtered_df