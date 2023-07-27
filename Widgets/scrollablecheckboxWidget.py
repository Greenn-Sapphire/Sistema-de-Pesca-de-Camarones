import customtkinter as ctk

class ScrollableCheckBoxFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

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
            if checkbox.cget('text') == item:
                checkbox.select()