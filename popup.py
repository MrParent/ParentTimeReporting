from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt
import requester
import maconomyRow
from logger_config import logger

monospace_font = QFont("Courier")

class JiraPopupWindow(QDialog):
    def __init__(self, entries, parent=None):
        super(JiraPopupWindow, self).__init__(parent)

        self.setWindowTitle("Push to Jira worklogs")
        
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

            entry_text = entry.short_str()
            item = QListWidgetItem(entry_text)
            item.setData(Qt.UserRole, entry)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Checked)
            item.setFont(monospace_font)
            self.listbox.addItem(item)

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.on_confirm_jira)
        
        self.abort_button = QPushButton("Abort")
        self.abort_button.clicked.connect(self.on_abort)

        self.layout.addWidget(self.listbox)
        self.layout.addWidget(self.confirm_button)
        self.layout.addWidget(self.abort_button)

        self.setGeometry(800, 300, 400, 300)
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

    def on_abort(self):
        # Handle abort action here
        print("Push to Jira aborted")
        self.close()


class MaconomyPopupWindow(QDialog):
    def __init__(self, entries, parent=None):
        super(MaconomyPopupWindow, self).__init__(parent)

        self.setWindowTitle("Push to Maconomy time sheet")
        
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

            maconomy_entry = maconomyRow.get_maconomy_configured_entry(maconomyRow.maconomy_config, entry)
            entry_text = maconomy_entry.short_str()
            item = QListWidgetItem(entry_text)
            item.setData(Qt.UserRole, maconomy_entry)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Checked)
            item.setFont(monospace_font)
            self.listbox.addItem(item)

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.on_confirm_maconomy)
        
        self.abort_button = QPushButton("Abort")
        self.abort_button.clicked.connect(self.on_abort)

        self.layout.addWidget(self.listbox)
        self.layout.addWidget(self.confirm_button)
        self.layout.addWidget(self.abort_button)

        self.setGeometry(100, 100, 1500, 600)
        self.setLayout(self.layout)

    def on_confirm_maconomy(self):
        if not maconomyRow.maconomy_cookie:
            MaconomyLoginWindow().exec_()
        else:
            print("Push to Maconomy started")
            update_card = False
            for index in range(self.listbox.count()):
                item = self.listbox.item(index)
                if item.checkState() == Qt.Checked:
                    entry = item.data(Qt.UserRole)
                    logger.info(entry)
                    if not update_card:
                        logger.info("Updating card")
                        response = requester.make_maconomy_request_update_card(entry)
                        update_card = True
                        logger.info(response)
                    response = requester.make_maconomy_request_insert_row(entry)
                    logger.info(response)
            # Handle confirm action here
            print("Push to Maconomy finished")
            self.close()

    def on_abort(self):
        # Handle abort action here
        print("Push to Maconomy aborted")
        self.close()


class MaconomyLoginWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Maconomy Login")

        self.layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.layout.addWidget(self.username_label)

        self.username_field = QLineEdit()
        self.layout.addWidget(self.username_field)

        self.password_label = QLabel("Password:")
        self.layout.addWidget(self.password_label)

        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_field)

        self.layout.addSpacing(10)  # Add spacing between the fields and buttons

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.on_confirm_maconomy_login)
        self.layout.addWidget(self.confirm_button)

        self.abort_button = QPushButton("Abort")
        self.layout.addWidget(self.abort_button)

        self.setGeometry(100, 100, 260, 100)

        self.setLayout(self.layout)

    def on_confirm_maconomy_login(self):
        username = self.username_field.text()
        password = self.password_field.text()
        response = requester.make_maconomy_login_request(username, password)

        print("Login response: " + response.text)
        logger.info("Login response: " + response.text)

        if response.status_code != 200:
            requester.show_login_failed_message()
            return

        print("Done. Response: " + response.text)

        maconomyRow.maconomy_cookie = response.headers.get('Maconomy-Cookie')
        print("Maconomy-Cookie: " + str(maconomyRow.maconomy_cookie))

        response = requester.make_maconomy_request_get_employee_number()
        print("Done. Response: " + response.text)
        
        response = requester.make_maconomy_request_instance()
        print("Done. Response: " + response.text)

        response = requester.make_maconomy_request_instance_data()
        print("Done. Response: " + response.text)

        self.close()

    def on_abort(self):
        # Handle abort action here
        print("Login to Maconomy aborted")
        self.close()