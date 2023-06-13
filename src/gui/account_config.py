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
        # self.inputs.append(frame_title_label)

        if self.fields is not None:
            for row_index, (field) in enumerate(self.fields):
                if type(field) == tuple:
                    row_index = row_index + 1
                    self.add_field(field, row_index)
                elif type(field) == list:
                    row_index = row_index + 1
                    self.add_nested_fields(field, row_index)

            # for i, (label, field_type, field_key) in enumerate(self.fields):
            #     # frame title is on row 0, add 1 to row
            #     i = i + 1
            #     if field_type == 'entry':
            #         self.create_entry(self, i, label, field_key)
            #     elif field_type == 'checkbox':
            #         self.create_checkbox(self, i, label, field_key)

    def add_nested_fields(self, fields, row_index):
        nested_fields_title = customtkinter.CTkLabel(self, text=fields[0])
        nested_fields_title.grid(row=row_index, column=0, sticky="w", pady=(10, 0))
        nested_fields_title.configure(
            font=("Roboto", 30)
            )

        for field in fields:
            row_index = row_index + 1
            parent_field = fields[0]
            self.add_nested_field(field, row_index, parent_field)

    def add_nested_field(self, field, row_index, parent_field):
        label = field[0]
        field_type = field[1]
        field_key = [parent_field, field[2]]

        if field_type == 'entry':
            self.create_entry(self, row_index, label, field_key)
        elif field_type == 'checkbox':
            self.create_checkbox(self, row_index, label, field_key)

    def add_field(self, field, row_index):
        label = field[0]
        field_type = field[1]
        field_key = field[2]

        if field_type == 'entry':
            self.create_entry(self, row_index, label, field_key)
        elif field_type == 'checkbox':
            self.create_checkbox(self, row_index, label, field_key)
        elif field_type == 'textarea':
            self.create_textarea(row_index, label, field_key)

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

    def create_textarea(self, row, label, field_key):
        textarea_label = customtkinter.CTkLabel(self, text=label)
        textarea_label.grid(row=row, column=0, padx=10, pady=(10, 0), sticky='w')

        textarea = customtkinter.CTkTextbox(self, height=5, width=30)
        textarea.grid(row=row, column=1, padx=10, pady=(10, 0), sticky='ew')
        self.inputs.append([field_key, textarea])


    def get(self):
        input_data = {}

        if self.fields is not None:
            field_idx = 0
            while field_idx < len(self.fields):
                field = self.fields[field_idx]
                if isinstance(field, tuple):
                    value = self.inputs[field_idx][1].get() if field[1] != 'textarea' else self.inputs[field_idx][1].get('1.0', 'end')
                    if field[1] == 'checkbox':
                        value = True if value == '1' else False
                    elif field[1] == 'entry':
                        value = int(value) if value.isdigit() else value
                    elif field[1] == 'textarea':
                        value = [line.strip() for line in value.split('\n') if line.strip()]
                    input_data[field[2]] = value
                    field_idx += 1
                elif isinstance(field, list):
                    nested_fields = field[1:]
                    nested_data = {}
                    for nested_field in nested_fields:
                        value = self.inputs[field_idx][1].get() if nested_field[1] != 'textarea' else self.inputs[field_idx][1].get('1.0', 'end')
                        if nested_field[1] == 'checkbox':
                            value = True if value == '1' else False
                        elif nested_field[1] == 'entry':
                            value = int(value) if value.isdigit() else value
                        elif nested_field[1] == 'textarea':
                            value = [line.strip() for line in value.split('\n') if line.strip()]
                        nested_data[nested_field[2]] = value
                        field_idx += 1
                    input_data[field[0]] = nested_data

        return input_data
