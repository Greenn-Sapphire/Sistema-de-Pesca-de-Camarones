import customtkinter as ctk

class SpinBoxWidget(ctk.CTkFrame):
    def __init__(self, master, numrow, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(1, weight=1)
        self.command = command
        self.numrow = numrow

        self.subtract_button = ctk.CTkButton(self, text="-", width=48, height=26, command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3, sticky="w")

        self.entry = ctk.CTkEntry(self, height=26, border_width=0, justify='center')
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="we")

        self.add_button = ctk.CTkButton(self, text="+", width=48, height=26, command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3, sticky="e")

        self.entry.insert(0, "0")
        self.set(self.numrow)
    
    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get())
            if value < len(self.master.master.dataframe.index):
                value += 1
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
                self.numrow = value
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get())
            if value > 1:
                value -= 1
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
                self.numrow = value
        except ValueError:
            return

    def get(self):
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))