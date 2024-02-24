from PyQt5.QtWidgets import QApplication, QAbstractItemView, QDateEdit, QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidgetItem, QLabel
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from popup import PopupWindow
import timeLog
import requester
import sys

# Create a QFont object for a monospace font
monospace_font = QFont("Courier")

# Function to push the selected items to Jira worklog
def push_selected_items_jira():
    checked_items = []
    for index in range(listbox.count()):
        item = listbox.item(index)
        if item.checkState() == Qt.Checked:
            checked_items.append(item)
    
    timeEntries_to_push = []

    for item in checked_items:
        timeEntry = item.data(Qt.UserRole)
        if timeLog.is_valid_description(timeEntry.description):
            timeEntries_to_push.append(timeEntry)

    #formatted_time = timeLog.format_time('2024-02-24T13:30:00+00:00', 1)
    #response = requester.make_jira_request('NOBIA-7036', '30m', formatted_time)
    #print(response.text)
    popupWindow = PopupWindow(timeEntries_to_push)
    popupWindow.exec_()

# Function to add items to a QListWidget as checkboxes
def add_items_as_checkboxes(listbox, timeEntries):
    listbox.clear()
    
    for entry in timeEntries:
        item = QListWidgetItem(str(entry))
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item.setCheckState(Qt.CheckState.Checked)
        item.setFont(monospace_font)
        item.setData(Qt.UserRole, entry)
        listbox.addItem(item)

# Function to get the Toggl entries
def get_toggl_entries():
    response = requester.make_toggl_request(start_date_edit.dateTime(), end_date_edit.dateTime())
    timeEntries = []
    
    for entry in response:
        #safe get entry start
        start = entry.get('start', "None")
        stop = entry.get('stop', "None")
        duration = entry.get('duration', "None")
        description = entry.get('description', "None")
        client_name = entry.get('client_name', "None")
        project_name = entry.get('project_name', "None")
        timeEntry = timeLog.TimeLog(start, stop, duration, description, client_name, project_name)
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
jira_button.clicked.connect(push_selected_items_jira)

hbox3 = QHBoxLayout()

# Create a button to trigger the selection
maconomy_button = QPushButton("Push to Maconomy")
maconomy_button.setFixedSize(200, 30)
#maconomy_button.clicked.connect(push_selected_items_maconomy)

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