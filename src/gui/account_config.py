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
            row_index = 0
            for field in self.fields:
                row_index += 1
                if type(field) == tuple:
                    self.add_field(field, row_index)
                elif type(field) == list:
                    row_index = self.add_nested_fields(field, row_index)

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

        return row_index

    def add_nested_field(self, field, row_index, parent_field):
        label = field[0]
        field_type = field[1]
        field_key = [parent_field, field[2]]
        default_value = field[3]

        if field_type == 'entry':
            self.create_entry(self, row_index, label, field_key, default_value)
        elif field_type == 'checkbox':
            self.create_checkbox(self, row_index, label, field_key, default_value)
        elif field_type == 'textarea':
            self.create_textarea(row_index, label, field_key, default_value)

    def add_field(self, field, row_index):
        label = field[0]
        field_type = field[1]
        field_key = field[2]
        default_value = field[3]

        if field_type == 'entry':
            self.create_entry(self, row_index, label, field_key, default_value)
        elif field_type == 'checkbox':
            self.create_checkbox(self, row_index, label, field_key, default_value)
        elif field_type == 'textarea':
            self.create_textarea(row_index, label, field_key, default_value)

    def create_entry(self, sus, row, label, field_key, default_value=None):
        entry_label = customtkinter.CTkLabel(self, text=label)
        entry_label.grid(row=row, column=0, padx=10, pady=(10, 0), sticky='w')

        entry = customtkinter.CTkEntry(self, width=400)
        entry.grid(row=row, column=1, padx=10, pady=(10, 0), sticky='ew')

        if default_value is not None:
            entry.insert(0, default_value)

        self.inputs.append([field_key, entry])

    def create_checkbox(self, sus, row, label, field_key, default_value=None):
        checkbox_label = customtkinter.CTkLabel(self, text=label)
        checkbox_label.grid(row=row, column=0, padx=10, pady=(10, 0), sticky='w')

        checkbox = customtkinter.CTkCheckBox(self, text="", width=400)
        checkbox.grid(row=row, column=1, padx=10, pady=(10, 0), sticky='w')

        if default_value is not None:
            if default_value:
                checkbox.select()
            else:
                checkbox.deselect()

        self.inputs.append([field_key, checkbox])

    def create_textarea(self, row, label, field_key, default_value=None):
        textarea_label = customtkinter.CTkLabel(self, text=label)
        textarea_label.grid(row=row, column=0, padx=10, pady=(10, 0), sticky='w')

        textarea = customtkinter.CTkTextbox(self, height=100, width=600)
        textarea.grid(row=row, column=1, padx=10, pady=(10, 0), sticky='ew')

        if default_value is not None:
            textarea.insert('1.0', default_value)

        self.inputs.append([field_key, textarea])


    def get(self, fields=None, start_idx=0):
        if fields is None:
            fields = self.fields

        input_data = {}
        field_idx = start_idx
        for field in fields:
            if isinstance(field, tuple):
                value = self.get_value(field_idx, field)
                input_data[field[2]] = value
                field_idx += 1
            elif isinstance(field, list):
                nested_fields = field[1:]
                nested_data, field_idx = self.get(nested_fields, field_idx)
                input_data[field[0]] = nested_data

        return input_data, field_idx

    def get_value(self, field_idx, field):
        value = self.inputs[field_idx][1].get() if field[1] != 'textarea' else self.inputs[field_idx][1].get('1.0', 'end')
        if field[1] == 'checkbox':
            value = True if value == 1 else False
        elif field[1] == 'entry':
            value = int(value) if value.isdigit() else value
        elif field[1] == 'textarea':
            value = [line.strip() for line in value.split('\n') if line.strip()]
        return value
