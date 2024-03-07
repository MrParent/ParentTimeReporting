from PyQt5.QtWidgets import QApplication, QAbstractItemView, QDateEdit, QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidgetItem, QLabel, QDialog
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from popup import JiraPopupWindow, MaconomyPopupWindow
import time_log
import requester
import sys
import options
import edit_row_dialog

# Create a QFont object for a monospace font
monospace_font = QFont("Courier")

# Function to push the selected items to Jira worklog
def push_selected_items_jira():
    checked_items = []
    for index in range(listbox.count()):
        item = listbox.item(index)
        if item.checkState() == Qt.Checked:
            checked_items.append(item)
    
    time_entries_to_push = []

    for item in checked_items:
        time_entry = item.data(Qt.UserRole)
        if time_log.is_valid_description(time_entry.description):
            time_entries_to_push.append(time_entry)

    popup_window = JiraPopupWindow(time_entries_to_push)
    popup_window.exec_()

    #FIXME: if no api key is found, show default login fields.

# Function to push the selected items to Maconomy
def push_selected_items_maconomy():
    checked_items = []
    for index in range(listbox.count()):
        item = listbox.item(index)
        if item.checkState() == Qt.Checked:
            checked_items.append(item)
    
    time_entries_to_push = []

    for item in checked_items:
        time_entry = item.data(Qt.UserRole)
        if time_log.is_valid_maconomy_entry(time_entry):
            time_entries_to_push.append(time_entry)

    time_entries_to_push = time_log.merge_time_logs(time_entries_to_push)
    popup_window = MaconomyPopupWindow(time_entries_to_push)
    popup_window.exec_()

    # FIXME: if no api key is found, show default login fields. 
    # merge time entries of the same day, client, project and description
    # present the merged time entries to the user in a popup dialog
    # in the dialog, being able to push to Maconomy or abort. Still checkable items.
    # log the result of the push to Maconomy in the console
    # log the result of the push to Maconomy in a file
    
# Function to add items to a QListWidget as checkboxes
def add_items_as_checkboxes(listbox, time_entries):
    listbox.clear()
    
    last_date = None
    for entry in time_entries:
        # If the start date of the entry is different from the last date, add a date item
        if entry.get_start_date() != last_date:
            last_date = entry.get_start_date()
            date_item = QListWidgetItem(last_date)
            date_item.setFlags(Qt.NoItemFlags)  # Make the item non-selectable and non-checkable
            date_item.setFont(QFont('Arial', 10, QFont.Bold))  # Make the item bold
            listbox.addItem(date_item)
        
        item = QListWidgetItem(str(entry))
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item.setCheckState(Qt.CheckState.Checked)
        item.setFont(monospace_font)
        item.setData(Qt.UserRole, entry)
        listbox.addItem(item)

# Function to get the Toggl entries
def get_toggl_entries():
    response = requester.make_toggl_request(start_date_edit.dateTime(), end_date_edit.dateTime())
    if not response:
        return
    
    time_entries = []
    for entry in response:
        #safe get entry start
        start = entry.get('start', "None")
        stop = entry.get('stop', "None")
        duration = entry.get('duration', "None")
        description = entry.get('description', "None")
        client_name = entry.get('client_name', "None")
        project_name = entry.get('project_name', "None")
        time_entry = time_log.TimeLog(start, stop, duration, description, client_name, project_name)
        time_entries.append(time_entry)
    
    add_items_as_checkboxes(listbox, time_entries)
    #FIXME: if no api key is found, show default login fields.

# Function to handle double click on an item in the listbox.
def on_item_double_clicked(item):
    print(item.text())
    edit_dialog = edit_row_dialog.EditRowDialog(item.data(Qt.UserRole))
    if edit_dialog.exec_() == QDialog.Accepted:
        # Update the text of the item after the dialog is closed
        item.setText(str(item.data(Qt.UserRole)))

# parent python app main module code
main_application = QApplication([])
options.company, options.maconomy_prod = options.getOptions()
window = QWidget()
layout = QVBoxLayout()
hbox = QHBoxLayout()
hbox2 = QHBoxLayout()

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

hbox_top_buttons = QHBoxLayout()
toggl_entries_button = QPushButton("Get Toggl Entries")
toggl_entries_button.setFixedSize(200, 30)
toggl_entries_button.clicked.connect(get_toggl_entries)

hbox_top_buttons.addWidget(toggl_entries_button, alignment=Qt.AlignLeft)
hbox_top_buttons.addStretch(1)
settings_button = QPushButton("Settings")
settings_button.setFixedSize(140, 30)
settings_button.clicked.connect(options.showSettingsWindow)
hbox_top_buttons.addWidget(settings_button, alignment=Qt.AlignRight)
layout.addLayout(hbox_top_buttons)

listbox = QListWidget()

listbox.setSelectionMode(QListWidget.MultiSelection)
listbox.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
listbox.itemDoubleClicked.connect(on_item_double_clicked)

jira_button = QPushButton("Push to Jira worklogs")
jira_button.setFixedSize(200, 30)
jira_button.clicked.connect(push_selected_items_jira)

hbox3 = QHBoxLayout()
maconomy_button = QPushButton("Push to Maconomy time sheet")
maconomy_button.setFixedSize(200, 30)
maconomy_button.clicked.connect(push_selected_items_maconomy)
layout.addWidget(listbox)

hbox3.addWidget(jira_button)
hbox3.addWidget(maconomy_button)
hbox3.addStretch(1)
layout.addLayout(hbox3)

window.setLayout(layout)
window.setWindowTitle("Parent time report tool")
window.setGeometry(100, 100, 1400, 600)

window.show()

# Start the main loop
sys.exit(main_application.exec_())