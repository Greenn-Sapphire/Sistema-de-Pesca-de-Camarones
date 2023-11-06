import customtkinter as ctk

class ScrollableCheckBoxFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, item_list, row_index, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.command = command
        self.checkbox_list = []
        self.row_index = row_index

        if len(item_list) > 50:
            min_num_items = len(item_list) // 4
            first_sublist = item_list[:min_num_items]  # Obtiene la primera sublista con el 25% de los elementos
            self.rest_sublists = [item_list[i:i + min_num_items] for i in range(min_num_items, len(item_list), min_num_items)]
            
            for item in first_sublist:
                self.add_item(item)
                
            self.row_index+=1
            self.show_more_button = ctk.CTkButton(self.master.master.master, text='Mostrar más', fg_color='transparent', border_color=None, command=self.show_more_filters)
            self.show_more_button.grid(row=self.row_index, column=0, sticky='w', padx=4)
            self.row_index+=1

        else:
            self.row_index+=1
            for item in item_list:
                self.add_item(item)

    def get_actual_row(self):
        return self.row_index
    
    def add_item(self, item):
        checkbox = ctk.CTkCheckBox(self, text=item)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10), sticky='w')
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget('text'):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def update_items(self, new_item_list):
        # Primero, eliminamos todos los checkboxes existentes
        for checkbox in self.checkbox_list:
            checkbox.destroy()

        # Luego, creamos los nuevos checkboxes basados en la lista de elementos proporcionada
        self.checkbox_list = []
        for item in new_item_list:
            self.add_item(item)

    def get_checked_items(self):
        return [checkbox.cget('text') for checkbox in self.checkbox_list if checkbox.get() == 1]

    def set_checked(self, item):
        # Marca el checkbox correspondiente al elemento proporcionado como seleccionado
        for checkbox in self.checkbox_list:
            if str(checkbox.cget('text')).strip().lower() == str(item).strip().lower():
                checkbox.select()

    def set_all_checked(self):
        # Marca el checkbox correspondiente al elemento proporcionado como seleccionado
        for checkbox in self.checkbox_list:
            checkbox.select()

    def show_more_filters(self):
        for item in self.rest_sublists[0]:
            self.add_item(item)
        del self.rest_sublists[0]

        if not self.rest_sublists:
            self.show_more_button.destroy()