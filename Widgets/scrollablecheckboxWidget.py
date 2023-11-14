import customtkinter as ctk

class ScrollableCheckBoxFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, item_list, row_index = 0, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.command = command
        self.checkbox_list = []
        self.row_index = row_index
        self.item_list = item_list

        self.row_index+=1
        for item in item_list:
            self.add_item(item)

    def get_actual_row(self):
        return self.row_index
    
    def add_item(self, item):
        checkbox = ctk.CTkCheckBox(self, text=item)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(pady=(0, 10), sticky='w')
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
            if checkbox.cget('text') not in new_item_list:
                checkbox.grid_forget()
            else:
                checkbox.grid(pady=(0, 10), sticky='w')

    def get_checked_items(self):
        return [checkbox.cget('text') for checkbox in self.checkbox_list if checkbox.get() == 1]

    def get_unchecked_items(self):
        return [checkbox.cget('text') for checkbox in self.checkbox_list if checkbox.get() == 0]

    def set_checked(self, item):
        # Marca el checkbox correspondiente al elemento proporcionado como seleccionado
        for checkbox in self.checkbox_list:
            if str(checkbox.cget('text')).strip().lower() == str(item).strip().lower():
                checkbox.select()

    def set_all_checked(self):
        # Marca el checkbox correspondiente al elemento proporcionado como seleccionado
        for checkbox in self.checkbox_list:
            checkbox.select()