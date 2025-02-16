from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt
import requester
import maconomy_row
from logger_config import logger
from collections import defaultdict
import options

# Create a QFont object for a monospace font.
monospace_font = QFont("Courier")

# Class to create the Jira popup window.
class JiraPopupWindow(QDialog):
    def __init__(self, entries, parent=None):
        super(JiraPopupWindow, self).__init__(parent)

        self.setWindowTitle("Push to Jira worklogs")
        
        self.layout = QVBoxLayout()
        self.listbox = QListWidget()
        last_date = None
        for entry in entries:
            if entry.get_start_date() != last_date:
                last_date = entry.get_start_date()
                date_item = QListWidgetItem(last_date)
                date_item.setFlags(Qt.NoItemFlags)  # Make the item non-selectable and non-checkable
                date_item.setFont(QFont('Arial', 10, QFont.Bold))
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

    # Confirm jira push. FIXME: Add progress functionality.
    def on_confirm_jira(self):
        print("Check if Jira company is set")
        if not options.company:
            options.show_options_url_check_failed("Company is not set.")
            return
        
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

    # Abort jira push.
    def on_abort(self):
        print("Push to Jira aborted")
        self.close()

# Class to create the Maconomy popup window.
class MaconomyPopupWindow(QDialog):
    def __init__(self, entries, parent=None):
        super(MaconomyPopupWindow, self).__init__(parent)
        self.setWindowTitle("Push to Maconomy time sheet")
        
        self.layout = QVBoxLayout()
        self.listbox = QListWidget()
        last_date = None
        errors = []
        date_item = None
        for entry in entries:
            if entry.get_start_date() != last_date:
                last_date = entry.get_start_date()
                date_item = QListWidgetItem(last_date)
                date_item.setFlags(Qt.NoItemFlags)  # Make the item non-selectable and non-checkable
                date_item.setFont(QFont('Arial', 10, QFont.Bold))
                self.listbox.addItem(date_item)

            maconomy_entry = maconomy_row.get_maconomy_configured_entry(maconomy_row.maconomy_config, entry)
            if maconomy_entry.job_nr == "None":
                errors.append(entry)
                continue
            
            entry_text = maconomy_entry.short_str()
            item = QListWidgetItem(entry_text)
            item.setData(Qt.UserRole, maconomy_entry)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Checked)
            item.setFont(monospace_font)
            self.listbox.addItem(item)
        
        if errors:
            print("Please update the config file for the following rows:")
            logger.info("Please update the config file for the following rows:")
        for error in errors:
            print("Error: " + error.short_str())
            logger.info("Error: " + error.short_str())

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.on_confirm_maconomy)
        
        self.abort_button = QPushButton("Abort")
        self.abort_button.clicked.connect(self.on_abort)

        self.layout.addWidget(self.listbox)
        self.layout.addWidget(self.confirm_button)
        self.layout.addWidget(self.abort_button)

        self.setGeometry(100, 100, 1500, 600)
        self.setLayout(self.layout)

    # Confirm Maconomy push. FIXME: Add progress functionality.
    def on_confirm_maconomy(self):
        print("Check if Maconomy prod is set")
        if not options.maconomy_prod:
            options.show_options_url_check_failed("Maconomy prod is not set.")
            return
        MaconomyLoginWindow(self.listbox, self).exec_()

    # Abort Maconomy push.
    def on_abort(self):
        print("Push to Maconomy aborted")
        self.close()

# Class to create the Maconomy login window.
class MaconomyLoginWindow(QDialog):
    def __init__(self, listbox, parent=None):
        super().__init__(parent)
        self.listbox = listbox
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

        self.layout.addSpacing(10)

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.on_confirm_maconomy_login)
        self.layout.addWidget(self.confirm_button)

        self.abort_button = QPushButton("Abort")
        self.layout.addWidget(self.abort_button)

        self.setGeometry(100, 100, 260, 100)
        self.setLayout(self.layout)

    # Confirm Maconomy login.
    def on_confirm_maconomy_login(self):
        username = self.username_field.text()
        password = self.password_field.text()
        print("Login to Maconomy started")
        response = requester.make_maconomy_login_request(username, password)

        print("Login response: " + response.text)
        logger.info("Login response: " + response.text)

        if response.status_code != 200:
            requester.show_login_failed_message()
            return

        maconomy_row.maconomy_cookie = response.headers.get('Maconomy-Cookie')
        print("Maconomy-Cookie: " + str(maconomy_row.maconomy_cookie))

        print("Setup of maconomy started")
        response = requester.make_maconomy_request_get_employee_number()
        print("Done. Response: " + response.text)
        
        response = requester.make_maconomy_request_instance()
        print("Done. Response: " + response.text)

        response = requester.make_maconomy_request_instance_data()
        print("Done. Response: " + response.text)
        print("Setup of maconomy finished")

        print("Push of maconomy rows started")
        update_card = False
        # Create a dictionary with the key (job_nr, task, description) 
        # and the value a list of entries with the same key
        entries_dict = defaultdict(list)
        for index in range(self.listbox.count()):
            item = self.listbox.item(index)
            if item.checkState() == Qt.Checked:
                entry = item.data(Qt.UserRole)
                key = (entry.job_nr, entry.task, entry.description)
                entries_dict[key].append(entry)
        # Combine the entries for each key
        combined_entries = []
        for key, entries in entries_dict.items():
            combined_entries.append(self.combine_entries(entries))

        for job_nr, task, description, spec3, durations in combined_entries:
            if not update_card:
                logger.info("Updating card")
                response = requester.make_maconomy_request_update_card(entry)
                update_card = True
                logger.info(response)
            response = requester.make_maconomy_request_insert_row_merged(job_nr, task, description, spec3, durations)
            logger.info(response)

        print("Push to Maconomy finished")
        self.close()
        self.parent().close()
        # for index in range(self.listbox.count()):
        #     item = self.listbox.item(index)
        #     if item.checkState() == Qt.Checked:
        #         entry = item.data(Qt.UserRole)
        #         logger.info(entry)
        #         if not update_card:
        #             logger.info("Updating card")
        #             response = requester.make_maconomy_request_update_card(entry)
        #             update_card = True
        #             logger.info(response)
        #         response = requester.make_maconomy_request_insert_row(entry)
        #         logger.info(response)
        #print("Push to Maconomy finished")
        #self.close()
        #self.parent().close()

    # Combine the entries for the same key
    def combine_entries(self, entries):
    # Combine the entries by summing the durations for each day of the week
        durations = defaultdict(int)
        for entry in entries:
            day_of_week = entry.get_weekday() + 1
            durations[day_of_week] += entry.duration

        job_nr, task, description, spec3 = entries[0].job_nr, entries[0].task, entries[0].description, entries[0].spec3
        return job_nr, task, description, spec3, durations

    # Abort Maconomy login.
    def on_abort(self):
        print("Login to Maconomy aborted")
        self.close()