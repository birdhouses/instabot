import customtkinter

class AccountConfigFrame(customtkinter.CTkFrame):
    def __init__(self, master, frame_title, fields=None):
        super().__init__(master)
        self.frame_title = frame_title
        self.fields = fields

        self.inputs = []

        # Append frame title to inputs list
        frame_title_label = customtkinter.CTkLabel(self, text=self.frame_title)
        frame_title_label.grid(row=0, column=0, sticky="w", pady=(10, 0))
        frame_title_label.configure(
            font=("Roboto", 50)
            )
        self.inputs.append(frame_title_label)

        if self.fields is not None:
            for i, (label, field_type, field_key) in enumerate(self.fields):
                # frame title is on row 0, add 1 to row
                i = i + 1
                if field_type == 'entry':
                    self.create_entry(self, i, label, field_key)
                elif field_type == 'checkbox':
                    self.create_checkbox(self, i, label, field_key)

    def create_entry(self, sus, row, label, field_key):
        entry_label = customtkinter.CTkLabel(self, text=label)
        entry_label.grid(row=row, column=0, padx=10, pady=(10, 0), sticky='w')

        entry = customtkinter.CTkEntry(self)
        entry.grid(row=row, column=1, padx=10, pady=(10, 0), sticky='ew')
        self.inputs.append([field_key, entry])

    def create_checkbox(self, sus, row, label, field_key):
        checkbox_label = customtkinter.CTkLabel(self, text=label)
        checkbox_label.grid(row=row, column=0, padx=10, pady=(10, 0), sticky='w')

        checkbox = customtkinter.CTkCheckBox(self, text="")
        checkbox.grid(row=row, column=1, padx=10, pady=(10, 0), sticky='w')
        self.inputs.append([field_key, checkbox])

    def get(self):
        input_data = []

        if self.fields is not None:
            for i, (key) in enumerate(self.fields):
                # frame title is on row 0, add 1 to row
                i = i + 1
                input_data.append([key[2], self.inputs[i][1].get()])

        return input_data
