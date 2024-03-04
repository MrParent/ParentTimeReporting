import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
import json

toggl_api_key = os.getenv('TOGGL_API_KEY')
jira_api_key = os.getenv('JIRA_API_KEY')
jira_user_name = os.getenv('JIRA_USER_NAME')
company = ""
maconomy_prod = ""

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        self.layout = QVBoxLayout()

        #import the options from the config file
        with open('options.json') as f:
            optionsJson = json.load(f)
        self.company = optionsJson.get('company')
        self.maconomy_prod = optionsJson.get('maconomy_prod')

        self.company_label = QLabel("Company:")
        self.layout.addWidget(self.company_label)

        self.company_field = QLineEdit()
        self.company_field.setText(self.company)
        self.layout.addWidget(self.company_field)

        self.maconomy_prod_label = QLabel("Maconomy Prod:")
        self.layout.addWidget(self.maconomy_prod_label)

        self.maconomy_prod_field = QLineEdit()
        self.maconomy_prod_field.setText(self.maconomy_prod)
        self.layout.addWidget(self.maconomy_prod_field)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_options)
        self.layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_options)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)

    def save_options(self):
        #set global company value in module
        global company
        global maconomy_prod
        company = self.company_field.text()
        maconomy_prod = self.maconomy_prod_field.text()
        with open('options.json', 'w') as f:
            json.dump({'company': company, 'maconomy_prod': maconomy_prod}, f)
        self.close()

    def cancel_options(self):
        self.close()


def showSettingsWindow():
    settingsWindow = SettingsWindow()
    settingsWindow.exec_()

def getOptions():
    with open('options.json') as f:
        optionsJson = json.load(f)
    company = optionsJson.get('company')
    maconomy_prod = optionsJson.get('maconomy_prod')
    return company, maconomy_prod