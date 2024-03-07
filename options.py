import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import json
#import requests

# Global variables.
toggl_api_key = os.getenv('TOGGL_API_KEY')
jira_api_key = os.getenv('JIRA_API_KEY')
jira_user_name = os.getenv('JIRA_USER_NAME')
toggl_username = ""
toggl_password = ""
toggl_logged_in = False
company = ""
maconomy_prod = ""

# Class to create the settings window.
class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        self.setWindowTitle("Settings")

        self.layout = QVBoxLayout()

        #import the options from the config file
        with open('options.json') as f:
            options_json = json.load(f)
        self.company = options_json.get('company')
        self.maconomy_prod = options_json.get('maconomy_prod')

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

    # Function to save the options to the config file. FIXME: Fix bugs in url checks and evaluate if good to use.
    def save_options(self):
        # jira_url = "https://" + self.company_field.text().lower() + ".atlassian.net/jira/your-work"

        # if url_ok(jira_url) == False: 
        #     message_string = "Company is not valid."
        #     print(message_string)
        #     show_options_url_check_failed(message_string)
        #     return
        
        # maconomy_url = "https://" + self.maconomy_prod_field.text().lower() + "-webclient.deltekfirst.com"
        # print(maconomy_url)
        # print(url_ok(maconomy_url))
        # if url_ok(maconomy_url) == False:
        #     message_string = "Maconomy prod is not valid."
        #     print(message_string)
        #     show_options_url_check_failed(message_string)
        #     return

        global company
        global maconomy_prod
        company = self.company_field.text().lower()
        maconomy_prod = self.maconomy_prod_field.text().lower()
        with open('options.json', 'w') as f:
            json.dump({'company': company, 'maconomy_prod': maconomy_prod}, f)
        self.close()

    # Function to cancel and close the options window.
    def cancel_options(self):
        self.close()

# Function to show the settings window.
def showSettingsWindow():
    settingsWindow = SettingsWindow()
    settingsWindow.exec_()

# Function to get the options from the config file.
def getOptions():
    with open('options.json') as f:
        options_json = json.load(f)
    company = options_json.get('company')
    maconomy_prod = options_json.get('maconomy_prod')
    return company, maconomy_prod

# Function to check if the url is valid. FIXME: Fix bugs in url checks and evaluate if good to use.
# def url_ok(url):     
#     # exception block
#     try:
#         # pass the url into
#         # request.hear
#         response = requests.head(url) 
#         print(response.status_code)
#         if response.status_code == 200:
#             return True
#         else:
#             return False
#     except requests.ConnectionError as e:
#         return e

# def show_options_url_check_failed(message_string):
#     msg = QMessageBox()
#     msg.setWindowTitle("Url checks failed")
#     msg.setText(message_string + "Please check the options and try again.")
#     msg.setIcon(QMessageBox.Information)
#     msg.exec_()