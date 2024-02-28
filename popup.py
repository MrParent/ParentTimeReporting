from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt
import requester
import maconomyRow

monospace_font = QFont("Courier")

class PopupWindow(QDialog):
    def __init__(self, entries, whoToPushTo, parent=None):
        super(PopupWindow, self).__init__(parent)

        self.setWindowTitle("Push to Jira worklogs" if whoToPushTo == "Jira" else "Push to Maconomy time sheet")
        
        self.layout = QVBoxLayout()
        self.listbox = QListWidget()
        last_date = None
        for entry in entries:
        # If the start date of the entry is different from the last date, add a date item
            if entry.get_start_date() != last_date:
                last_date = entry.get_start_date()
                date_item = QListWidgetItem(last_date)
                date_item.setFlags(Qt.NoItemFlags)  # Make the item non-selectable and non-checkable
                date_item.setFont(QFont('Arial', 10, QFont.Bold))  # Make the item bold
                self.listbox.addItem(date_item)

            if whoToPushTo == "Maconomy":
                maconomyEntry = maconomyRow.get_maconomy_configured_entry(maconomyRow.maconomy_config, entry)
                entryText = maconomyEntry.short_str()
                item = QListWidgetItem(entryText)
                item.setData(Qt.UserRole, maconomyEntry)
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                item.setCheckState(Qt.CheckState.Checked)
                item.setFont(monospace_font)
                self.listbox.addItem(item)
            else:
                entryText = entry.short_str()
                item = QListWidgetItem(entryText)
                item.setData(Qt.UserRole, entry)
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                item.setCheckState(Qt.CheckState.Checked)
                item.setFont(monospace_font)
                self.listbox.addItem(item)

        self.confirm_button = QPushButton("Confirm")
        
        if whoToPushTo == "Jira":
            self.confirm_button.clicked.connect(self.on_confirm_jira)
        else:
            self.confirm_button.clicked.connect(self.on_confirm_maconomy)
        
        self.abort_button = QPushButton("Abort")
        self.abort_button.clicked.connect(self.on_abort)

        self.layout.addWidget(self.listbox)
        self.layout.addWidget(self.confirm_button)
        self.layout.addWidget(self.abort_button)

        if whoToPushTo == "Jira":
            self.setGeometry(800, 300, 400, 300)
        else:
            self.setGeometry(100, 100, 1500, 600)

        self.setLayout(self.layout)

    # FIXME: Add progress functionality
    def on_confirm_jira(self):
        print("Push to Jira started")
        # Handle confirm action here
        for index in range(self.listbox.count()):
            item = self.listbox.item(index)
            if item.checkState() == Qt.Checked:
                entry = item.data(Qt.UserRole)
                if entry.description and entry.get_jira_duration() and entry.get_jira_start_time():
                    print(entry.short_str() + " is Valid. Trying to update Jira ticket worklog...")
                    response = requester.make_jira_request(entry.description, entry.get_jira_duration(), entry.get_jira_start_time())
                    print("Done. Response: " + response.text)
                else:
                    print("Entry is not valid: " + entry.short_str())
        print("Push to Jira finished")
        self.close()

    def on_confirm_maconomy(self):
        print("Push to Maconomy started")
        for index in range(self.listbox.count()):
            item = self.listbox.item(index)
            if item.checkState() == Qt.Checked:
                entry = item.data(Qt.UserRole)
                print(entry)
        # Handle confirm action here
        print("Push to Maconomy finished")
        self.close()

    def on_abort(self):
        # Handle abort action here
        print("Push to Jira aborted")
        self.close()