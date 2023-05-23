import customtkinter

class AccountConfigFrame(customtkinter.CTkFrame):
    def __init__(self, master, frame_title, fields=None):
        super().__init__(master)
        self.frame_title = frame_title
        self.fields = fields

        self.inputs = []

        # Append frame title to inputs list
        frame_title_label = customtkinter.CTkLabel(self, text=self.frame_title)
        frame_title_label.grid(row=0, column=0, sticky="ew")
        self.inputs.append(frame_title_label)

        if self.fields is not None:
            for i, (key, field_type) in enumerate(self.fields.items()):
                # frame title is on row 0, add 1 to row
                i = i + 1
                if field_type == 'entry':
                    entry_label = customtkinter.CTkLabel(self, text=key)
                    entry_label.grid(row=i, column=0, sticky='w')

                    entry = customtkinter.CTkEntry(self)
                    entry.grid(row=i, column=1, sticky='w')
                    self.inputs.append(entry)
                elif field_type == 'checkbox':
                    checkbox_label = customtkinter.CTkLabel(self, text=key)
                    checkbox_label.grid(row=i, column=0, sticky='w')
                    checkbox = customtkinter.CTkCheckBox(self, text="")
                    checkbox.grid(row=i, column=1, sticky='w')
                    self.inputs.append(checkbox)

    def get(self):
        input_data = []

        if self.fields is not None:
            for i, (key, field_type) in enumerate(self.fields.items()):
                # frame title is on row 0, add 1 to row
                i = i + 1
                input_data.append([key, self.inputs[i].get()])

        return input_data
