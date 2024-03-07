from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

# Edit row dialog. FIXME: The format of the fields are now in toggle format. 
# - It should be in readable format and when saved, should convert back to the formats that's handled.
class EditRowDialog(QDialog):
    def __init__(self, item, parent=None):
        super().__init__()

        self.item = item

        self.setWindowTitle("Edit Row")
        self.setGeometry(800, 300, 400, 300)

        self.layout = QVBoxLayout()

        self.start_field = QLineEdit(self.item.start)
        self.layout.addWidget(QLabel("Start"))
        self.layout.addWidget(self.start_field)

        self.stop_field = QLineEdit(self.item.stop)
        self.layout.addWidget(QLabel("Stop"))
        self.layout.addWidget(self.stop_field)

        self.duration_field = QLineEdit(str(self.item.duration))
        self.layout.addWidget(QLabel("Duration"))
        self.layout.addWidget(self.duration_field)

        self.description_field = QLineEdit(self.item.description)
        self.layout.addWidget(QLabel("Description"))
        self.layout.addWidget(self.description_field)

        self.client_name_field = QLineEdit(self.item.client_name)
        self.layout.addWidget(QLabel("Client Name"))
        self.layout.addWidget(self.client_name_field)

        self.project_name_field = QLineEdit(self.item.project_name)
        self.layout.addWidget(QLabel("Project Name"))
        self.layout.addWidget(self.project_name_field)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_changes)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)
        self.show()
    
    # Save the changes.
    def save_changes(self):
        self.item.start = self.start_field.text()
        self.item.stop = self.stop_field.text()
        self.item.duration = int(self.duration_field.text())
        self.item.description = self.description_field.text()
        self.item.client_name = self.client_name_field.text()
        self.item.project_name = self.project_name_field.text()
        self.accept()
