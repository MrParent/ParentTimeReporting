import requests
from requests.auth import HTTPBasicAuth
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from base64 import b64encode
import json
from logger_config import logger
import maconomy_row
import json
import options

# The toggl web request function.
def make_toggl_request(start_time, end_time):
    toggl_api_key = options.toggl_api_key

    if not toggl_api_key and not options.toggl_logged_in:
        logger.info("Toggl API key is not set and not logged in")
        TogglLoginWindow().exec_()
        if not options.toggl_username or not options.toggl_password:
            logger.info("Toggl login is aborted")
            return

    start_time = start_time.toString("yyyy-MM-ddT00:00:00+00:00")
    end_time = end_time.toString("yyyy-MM-ddT23:59:00+00:00")
    
    auth_string =""
    if(not toggl_api_key):
        auth_string = b64encode(f"{options.toggl_username}:{options.toggl_password}".encode()).decode()
    else:
        auth_string = b64encode(f"{toggl_api_key}:api_token".encode()).decode()

    headers = {
        'content-type': 'application/json',
        'Authorization' : f'Basic {auth_string}'
    }

    params = {
        'meta' : 'true',
        'start_date': start_time,
        'end_date': end_time
    }

    response = requests.get('https://api.track.toggl.com/api/v9/me/time_entries', headers=headers, params=params)
    if response.status_code != 200:
        logger.info("Toggl login failed. Please check the login information (and api key if used) and try again.")
        show_login_failed_message()
        logger.info("Toggl Response = ")
        logger.info(response)
        return
    else:
        options.toggl_logged_in = True
    response = response.json()
    logger.info("Toggl Response = ")
    logger.info(response)
    return response

# The jira web request function.
def make_jira_request(ticket, duration, start_time):
    #get the api key from the environment variable
    jira_api_key = options.jira_api_key
    jira_user_name = options.jira_user_name

    if not jira_api_key or not jira_user_name:
        logger.info("Jira API key or username is not set")
        show_jira_login_failed_message()
        return

    auth = HTTPBasicAuth(jira_user_name, jira_api_key)

    url = f"https://{options.company}.atlassian.net/rest/internal/3/issue/{ticket}/worklog"
    params = { 'adjustEstimate': 'auto' }

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }

    body = {
        'timeSpent' : duration,
        'comment':{'type':'doc','version':1,'content':[]},
        'started': start_time
    }

    response = requests.post(url, headers=headers, json=body, params=params, auth=auth)
    logger.info("Jira Response = ")
    logger.info(response)
    return response

# The maconomy login request function.
def make_maconomy_login_request(username, password):
    basic_header = b64encode(f"{username}:{password}".encode()).decode()
    url = f"https://{options.maconomy_prod}-webclient.deltekfirst.com/maconomy-api/auth/{options.maconomy_prod}"

    payload = {}
    headers = {
    'Maconomy-Authentication': 'X-Disable-Negotiate,X-Force-Maconomy-Credentials,X-Force-Maconomy-Credentials,X-Basic,X-Reconnect,X-Cookie',
    'Maconomy-Client': 'iAccess',
    'Maconomy-Format': 'date-format="yyyy-MM-dd";time-format="HH:mm";thousand-separator=",";decimal-separator=".";number-of-decimals=2',
    'Authorization': f'Basic {basic_header}',
    'Connection': 'keep-alive'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    logger.info("Maconomy Login Response = ")
    logger.info(response)
    maconomy_row.maconomy_cookie = response.headers.get('Maconomy-Cookie')
    maconomy_row.cookie_jar = response.cookies
    return response

# The maconomy request function to get the employee number.
def make_maconomy_request_get_employee_number():
    url = f"https://{options.maconomy_prod}-webclient.deltekfirst.com/maconomy-api/environment/{options.maconomy_prod}?variables=user.info.employeenumber"
    payload = {}
    headers = {
    'Maconomy-Authentication': 'X-Disable-Negotiate,X-Force-Maconomy-Credentials,X-Force-Maconomy-Credentials,X-Basic,X-Reconnect,X-Cookie',
    'Maconomy-Client': 'iAccess',
    'Maconomy-Format': 'date-format="yyyy-MM-dd";time-format="HH:mm";thousand-separator=",";decimal-separator=".";number-of-decimals=2',
    'Authorization': f'X-Cookie {maconomy_row.maconomy_cookie}',
    'Connection': 'keep-alive',
    'Accept': 'application/vnd.deltek.maconomy.environment+json; version=1.0'
    }
    
    response = requests.request("GET", url, headers=headers, data=payload, cookies=maconomy_row.cookie_jar)
    
    logger.info("Maconomy Employee Number Response = ")
    logger.info(response)
    maconomy_row.employee_number = response.json().get('user').get('info').get('employeenumber').get('string').get('value')
    return response

# The maconomy request function to create and get the instance id.
def make_maconomy_request_instance():
    url = f"https://{options.maconomy_prod}-webclient.deltekfirst.com/maconomy-api/containers/{options.maconomy_prod}/timeregistration/instances"
    
    with open('instance_setup.json') as f:
        payload = json.load(f)
    payload = json.dumps(payload)
    content_length = len(payload)

    headers = {
    'Maconomy-Authentication': 'X-Disable-Negotiate,X-Force-Maconomy-Credentials,X-Force-Maconomy-Credentials,X-Basic,X-Reconnect,X-Cookie',
    'Maconomy-Client': 'iAccess',
    'Maconomy-Format': 'date-format="yyyy-MM-dd";time-format="HH:mm";thousand-separator=",";decimal-separator=".";number-of-decimals=2',
    'Authorization': f'X-Cookie {maconomy_row.maconomy_cookie}',
    'Accept': 'application/vnd.deltek.maconomy.containers+json; version=5.0',
    'Content-Type': 'application/vnd.deltek.maconomy.containers+json; version=5.0',
    'Content-Length': f'{content_length}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, cookies=maconomy_row.cookie_jar)

    maconomy_row.concurrency_token = response.headers.get('Maconomy-Concurrency-Control')
    response_json = response.json()
    maconomy_row.instance_id = response_json.get('meta').get('containerInstanceId')
    logger.info("Maconomy Instance Response = ")
    logger.info(response)
    return response

# The maconomy request function to call the instance data once (initialize?).
def make_maconomy_request_instance_data():
    url = f"https://{options.maconomy_prod}-webclient.deltekfirst.com/maconomy-api/containers/{options.maconomy_prod}/timeregistration/instances/{maconomy_row.instance_id}/data;any"
    
    payload = {}
    
    headers = {
    'Maconomy-Authentication': 'X-Disable-Negotiate,X-Force-Maconomy-Credentials,X-Force-Maconomy-Credentials,X-Basic,X-Reconnect,X-Cookie',
    'Maconomy-Client': 'iAccess',
    'Maconomy-Format': 'date-format="yyyy-MM-dd";time-format="HH:mm";thousand-separator=",";decimal-separator=".";number-of-decimals=2',
    'Authorization': f'X-Cookie {maconomy_row.maconomy_cookie}',
    'Accept': 'application/vnd.deltek.maconomy.containers+json; version=5.0',
    'Connection': 'keep-alive',
    'Maconomy-Concurrency-Control': f'{maconomy_row.concurrency_token}',
    'Content-Length': '0',
    'Host': f'{options.maconomy_prod}-webclient.deltekfirst.com'
    }

    response = requests.request("POST", url, headers=headers, data=payload, cookies=maconomy_row.cookie_jar)
    
    logger.info("Maconomy Instance Data Response = ")
    logger.info(response)
    print(response.json())
    maconomy_row.concurrency_token = response.headers.get('Maconomy-Concurrency-Control')
    return response

# The maconomy request function to update the card to the right week.
def make_maconomy_request_update_card(entry):
    url = f"https://{options.maconomy_prod}-webclient.deltekfirst.com/maconomy-api/containers/{options.maconomy_prod}/timeregistration/instances/{maconomy_row.instance_id}/data/panes/card/0"
    data = {
        "data": {
            "datevar": f"{entry.date}"
        }
    }
    payload = json.dumps(data)
    content_length = len(payload)

    headers = {
    'Maconomy-Authentication': 'X-Disable-Negotiate,X-Force-Maconomy-Credentials,X-Force-Maconomy-Credentials,X-Basic,X-Reconnect,X-Cookie',
    'Maconomy-Client': 'iAccess',
    'Maconomy-Format': 'date-format="yyyy-MM-dd";time-format="HH:mm";thousand-separator=",";decimal-separator=".";number-of-decimals=2',
    'Authorization': f'X-Cookie {maconomy_row.maconomy_cookie}',
    'Accept': 'application/vnd.deltek.maconomy.containers+json; version=5.0',
    'Connection': 'keep-alive',
    'Maconomy-Concurrency-Control': f'{maconomy_row.concurrency_token}',
    'Content-Type': 'application/vnd.deltek.maconomy.containers+json; version=5.0',
    'Content-Length': f'{content_length}',
    'Host': f'{options.maconomy_prod}-webclient.deltekfirst.com'
    }

    response = requests.request("POST", url, headers=headers, data=payload, cookies=maconomy_row.cookie_jar)
    logger.info("Maconomy Update Card Response = ")
    logger.info(response)
    print(response.json())
    maconomy_row.concurrency_token = response.headers.get('Maconomy-Concurrency-Control')
    return response

# The maconomy request function to insert a row in the timesheet.
def make_maconomy_request_insert_row(entry):
    url = f"https://{options.maconomy_prod}-webclient.deltekfirst.com/maconomy-api/containers/{options.maconomy_prod}/timeregistration/instances/{maconomy_row.instance_id}/data/panes/table?row=end"

    day_of_week = entry.get_weekday() + 1
    data = {
        "data": {
            "jobnumber": entry.job_nr,
            f"numberday{day_of_week}": entry.duration,
            "taskname": entry.task,
            f"descriptionday{day_of_week}": entry.description,
            "specification3name": entry.spec3
        }
    }

    payload = json.dumps(data)
    content_length = len(payload)

    headers = {
    'Maconomy-Authentication': 'X-Disable-Negotiate,X-Force-Maconomy-Credentials,X-Force-Maconomy-Credentials,X-Basic,X-Reconnect,X-Cookie',
    'Maconomy-Client': 'iAccess',
    'Maconomy-Format': 'date-format="yyyy-MM-dd";time-format="HH:mm";thousand-separator=",";decimal-separator=".";number-of-decimals=2',
    'Authorization': f'X-Cookie {maconomy_row.maconomy_cookie}',
    'Accept': 'application/vnd.deltek.maconomy.containers+json; version=5.0',
    'Content-Type': 'application/vnd.deltek.maconomy.containers+json; version=5.0',
    'Connection': 'keep-alive',
    'Maconomy-Concurrency-Control': f'{maconomy_row.concurrency_token}',
    'Content-Length': f'{content_length}',
    'Host': f'{options.maconomy_prod}-webclient.deltekfirst.com',
    'Referer': f'https://{options.maconomy_prod}-webclient.deltekfirst.com/workspace/weeklytimesheets;date={entry.date};employeenumber={maconomy_row.employee_number}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, cookies=maconomy_row.cookie_jar)
    logger.info("Maconomy Insert Row Response = ")
    logger.info(response)
    print(response.json())
    maconomy_row.concurrency_token = response.headers.get('Maconomy-Concurrency-Control')
    return response

# The maconomy request function to insert a merged row in the timesheet.
def make_maconomy_request_insert_row_merged(job_nr, task, description, spec3, durations):
    url = f"https://{options.maconomy_prod}-webclient.deltekfirst.com/maconomy-api/containers/{options.maconomy_prod}/timeregistration/instances/{maconomy_row.instance_id}/data/panes/table?row=end"

    data = {
        "data": {
            "jobnumber": job_nr,
            "taskname": task,
            "specification3name": spec3
        }
    }

    for day_of_week, duration in durations.items():
        data["data"][f"numberday{day_of_week}"] = duration
        data["data"][f"descriptionday{day_of_week}"] = description

    payload = json.dumps(data)
    content_length = len(payload)

    headers = {
    'Maconomy-Authentication': 'X-Disable-Negotiate,X-Force-Maconomy-Credentials,X-Force-Maconomy-Credentials,X-Basic,X-Reconnect,X-Cookie',
    'Maconomy-Client': 'iAccess',
    'Maconomy-Format': 'date-format="yyyy-MM-dd";time-format="HH:mm";thousand-separator=",";decimal-separator=".";number-of-decimals=2',
    'Authorization': f'X-Cookie {maconomy_row.maconomy_cookie}',
    'Accept': 'application/vnd.deltek.maconomy.containers+json; version=5.0',
    'Content-Type': 'application/vnd.deltek.maconomy.containers+json; version=5.0',
    'Connection': 'keep-alive',
    'Maconomy-Concurrency-Control': f'{maconomy_row.concurrency_token}',
    'Content-Length': f'{content_length}',
    'Host': f'{options.maconomy_prod}-webclient.deltekfirst.com'
    }

    response = requests.request("POST", url, headers=headers, data=payload, cookies=maconomy_row.cookie_jar)
    logger.info("Maconomy Insert Row Response = ")
    logger.info(response)
    print(response.json())
    maconomy_row.concurrency_token = response.headers.get('Maconomy-Concurrency-Control')
    return response

# Show login failed message.
def show_login_failed_message():
    msg = QMessageBox()
    msg.setWindowTitle("Login failed")
    msg.setText("Login failed. Please try again")
    msg.setIcon(QMessageBox.Information)
    msg.exec_()

# Show jira login failed message.
def show_jira_login_failed_message():
    msg = QMessageBox()
    msg.setWindowTitle("Login with api key failed")
    msg.setText("Login with API key and username failed. Please check the api key and username environment variables and try again")
    msg.setIcon(QMessageBox.Information)
    msg.exec_()

# The Toggl login window.
class TogglLoginWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        options.toggl_username = None
        options.toggl_password = None

        self.setWindowTitle("Toggl Login")

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
        self.confirm_button.clicked.connect(self.on_confirm_toggl_login)
        self.layout.addWidget(self.confirm_button)

        self.abort_button = QPushButton("Abort")
        self.abort_button.clicked.connect(self.on_abort)
        self.layout.addWidget(self.abort_button)

        self.setGeometry(100, 100, 260, 100)

        self.setLayout(self.layout)

    # The confirm button action.
    def on_confirm_toggl_login(self):
        options.toggl_username = self.username_field.text()
        options.toggl_password = self.password_field.text()
        self.close()

    # The abort button action.
    def on_abort(self):
        # Handle abort action here
        print("Login to Toggl aborted")
        self.close()