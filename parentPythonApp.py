from PyQt5.QtWidgets import QApplication, QAbstractItemView, QDateEdit, QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidgetItem, QLabel
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from toggl import TimeEntry
from base64 import b64encode
import requests
import sys
import os

# Create a QFont object for a monospace font
monospace_font = QFont("Courier")

# Function to handle the selection
def select_strings():
    checked_strings = []
    for index in range(listbox.count()):
        item = listbox.item(index)
        if item.checkState() == Qt.Checked:
            checked_strings.append(item.text())
    print("Checked strings:", checked_strings)

# Function to add items to a QListWidget as checkboxes
def add_items_as_checkboxes(listbox, timeEntries):
    listbox.clear()
    for entry in timeEntries:
        item = QListWidgetItem(entry.__str__())
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item.setCheckState(Qt.CheckState.Checked)
        item.setFont(monospace_font)
        listbox.addItem(item)

# Function to get the Toggl entries
def get_toggl_entries():
    #get the api key from the environment variable
    toggl_api_key = os.getenv('TOGGL_API_KEY') 
    startTime = start_date_edit.dateTime().toString("yyyy-MM-ddT00:00:00+00:00")
    endTime = end_date_edit.dateTime().toString("yyyy-MM-ddT23:59:00+00:00")
    auth_string = b64encode(f"{toggl_api_key}:api_token".encode()).decode()

    headers = {
        'content-type': 'application/json',
        'Authorization' : f'Basic {auth_string}'
    }

    params = {
        'meta' : 'true',
        'start_date': startTime,
        'end_date': endTime
    }

    response = requests.get('https://api.track.toggl.com/api/v9/me/time_entries', headers=headers, params=params).json()
    timeEntries = []
    
    for entry in response:
        #safe get entry start
        start = entry.get('start', "None")
        stop = entry.get('stop', "None")
        duration = entry.get('duration', "None")
        description = entry.get('description', "None")
        client_name = entry.get('client_name', "None")
        project_name = entry.get('project_name', "None")
        timeEntry = TimeEntry(start, stop, duration, description, client_name, project_name)
        timeEntries.append(timeEntry)
    add_items_as_checkboxes(listbox, timeEntries)

# Create the main application
app = QApplication([])

# Create the main window
window = QWidget()

# Create a layout
layout = QVBoxLayout()

#align the widgets in a row
hbox = QHBoxLayout()
hbox2 = QHBoxLayout()

# Create a date edit widget and label
start_date_label = QLabel("Start Date")
start_date_label.setFixedSize(80, 20)
start_date_label.setFont(monospace_font)
hbox.addWidget(start_date_label)
start_date_edit = QDateEdit(calendarPopup=True)
start_date_edit.setDate(QDate.currentDate())  # Set the current date
start_date_edit.setDisplayFormat("yyyy-MM-dd")  # Set the display format
start_date_edit.setFixedSize(200, 20)
hbox.addWidget(start_date_edit) 
hbox.addStretch(1)
layout.addLayout(hbox)

# Create a date edit widget and label
end_date_label = QLabel("End Date")
end_date_label.setFixedSize(80, 20)
end_date_label.setFont(monospace_font)
hbox2.addWidget(end_date_label)
end_date_edit = QDateEdit(calendarPopup=True)
end_date_edit.setDate(QDate.currentDate())  # Set the current date
end_date_edit.setDisplayFormat("yyyy-MM-dd")  # Set the display format
end_date_edit.setFixedSize(200, 20)
hbox2.addWidget(end_date_edit)
hbox2.addStretch(1)
layout.addLayout(hbox2)

toggl_entries_button = QPushButton("Get Toggl Entries (with api key)")
toggl_entries_button.setFixedSize(400, 30)
toggl_entries_button.clicked.connect(get_toggl_entries)
layout.addWidget(toggl_entries_button)

# Create a QListWidget and add the strings to it as checkboxes
listbox = QListWidget()

# Set the selection mode
listbox.setSelectionMode(QListWidget.MultiSelection)

listbox.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

#listbox.setWordWrap(True)

# Create a button to trigger the selection
jira_button = QPushButton("Push to Jira")
jira_button.setFixedSize(200, 30)
jira_button.clicked.connect(select_strings)

hbox3 = QHBoxLayout()

# Create a button to trigger the selection
maconomy_button = QPushButton("Push to Maconomy")
maconomy_button.setFixedSize(200, 30)
maconomy_button.clicked.connect(select_strings)

# Create a layout and add the QListWidget and button to it
layout.addWidget(listbox)

# Create a hbox and add the buttons to it
hbox3.addWidget(jira_button)
hbox3.addWidget(maconomy_button)
hbox3.addStretch(1)
layout.addLayout(hbox3)

# Set the layout on the window
window.setLayout(layout)

# Set the window title and geometry
window.setWindowTitle("Toggl Time Entries")
window.setGeometry(100, 100, 1500, 600)

# Show the window
window.show()

# Start the main loop
sys.exit(app.exec_())