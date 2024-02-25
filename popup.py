from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt
import requester

monospace_font = QFont("Courier")

class PopupWindow(QDialog):
    def __init__(self, entries, parent=None):
        super(PopupWindow, self).__init__(parent)

        self.setWindowTitle("Push to Jira worklogs")

        self.layout = QVBoxLayout()

        self.listbox = QListWidget()
        for entry in entries:
            item = QListWidgetItem(entry.short_str())
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Checked)
            item.setFont(monospace_font)
            item.setData(Qt.UserRole, entry)
            self.listbox.addItem(item)

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.on_confirm)

        self.abort_button = QPushButton("Abort")
        self.abort_button.clicked.connect(self.on_abort)

        self.layout.addWidget(self.listbox)
        self.layout.addWidget(self.confirm_button)
        self.layout.addWidget(self.abort_button)

        self.setGeometry(800, 300, 400, 300)

        self.setLayout(self.layout)

    def on_confirm(self):
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

    def on_abort(self):
        # Handle abort action here
        print("Push to Jira aborted")
        self.close()