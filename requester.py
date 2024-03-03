import requests
from requests.auth import HTTPBasicAuth
from base64 import b64encode
import os
import json
from logger_config import logger
import maconomyRow
import json


def make_toggl_request(startTime, endTime):
    #get the api key from the environment variable
    toggl_api_key = os.getenv('TOGGL_API_KEY') 
    startTime = startTime.toString("yyyy-MM-ddT00:00:00+00:00")
    endTime = endTime.toString("yyyy-MM-ddT23:59:00+00:00")
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
    logger.info("Toggl Response = ")
    logger.info(response)
    return response

def make_jira_request(ticket, duration, startTime):
    #get the api key from the environment variable
    jira_api_key = os.getenv('JIRA_API_KEY')
    jira_user_name = os.getenv('JIRA_USER_NAME')

    auth = HTTPBasicAuth(jira_user_name, jira_api_key)

    url = f"https://configura.atlassian.net/rest/internal/3/issue/{ticket}/worklog"
    params = { 'adjustEstimate': 'auto' }

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }

    body = {
        'timeSpent' : duration,
        'comment':{'type':'doc','version':1,'content':[]},
        'started': startTime
    }

    response = requests.post(url, headers=headers, json=body, params=params, auth=auth)
    logger.info("Jira Response = ")
    logger.info(response)
    return response

def make_maconomy_login_request(username, password):
    basicHeader = b64encode(f"{username}:{password}".encode()).decode()
    url = "https://me96763-webclient.deltekfirst.com/maconomy-api/auth/me96763"

    payload = {}
    headers = {
    'Maconomy-Authentication': 'X-Disable-Negotiate,X-Force-Maconomy-Credentials,X-Force-Maconomy-Credentials,X-Basic,X-Reconnect,X-Cookie',
    'Maconomy-Client': 'iAccess',
    'Maconomy-Format': 'date-format="yyyy-MM-dd";time-format="HH:mm";thousand-separator=",";decimal-separator=".";number-of-decimals=2',
    'Authorization': f'Basic {basicHeader}',
    'Connection': 'keep-alive'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    logger.info("Maconomy Login Response = ")
    logger.info(response)
    maconomyRow.maconomyCookie = response.headers.get('Maconomy-Cookie')
    maconomyRow.cookieJar = response.cookies
    return response

def make_maconomy_request_get_employee_number():
    url = "https://me96763-webclient.deltekfirst.com/maconomy-api/environment/me96763?variables=user.info.employeenumber"
    payload = {}
    headers = {
    'Maconomy-Authentication': 'X-Disable-Negotiate,X-Force-Maconomy-Credentials,X-Force-Maconomy-Credentials,X-Basic,X-Reconnect,X-Cookie',
    'Maconomy-Client': 'iAccess',
    'Maconomy-Format': 'date-format="yyyy-MM-dd";time-format="HH:mm";thousand-separator=",";decimal-separator=".";number-of-decimals=2',
    'Authorization': f'X-Cookie {maconomyRow.maconomyCookie}',
    'Connection': 'keep-alive',
    'Accept': 'application/vnd.deltek.maconomy.environment+json; version=1.0'
    }
    
    response = requests.request("GET", url, headers=headers, data=payload, cookies=maconomyRow.cookieJar)
    
    logger.info("Maconomy Employee Number Response = ")
    logger.info(response)
    maconomyRow.employeeNumber = response.json().get('user').get('info').get('employeenumber').get('string').get('value')
    return response

def make_maconomy_request_instance():
    url = "https://me96763-webclient.deltekfirst.com/maconomy-api/containers/me96763/timeregistration/instances"
    
    with open('instanceSetup.json') as f:
        payload = json.load(f)
    payload = json.dumps(payload)
    contentLength = len(payload)

    headers = {
    'Maconomy-Authentication': 'X-Disable-Negotiate,X-Force-Maconomy-Credentials,X-Force-Maconomy-Credentials,X-Basic,X-Reconnect,X-Cookie',
    'Maconomy-Client': 'iAccess',
    'Maconomy-Format': 'date-format="yyyy-MM-dd";time-format="HH:mm";thousand-separator=",";decimal-separator=".";number-of-decimals=2',
    'Authorization': f'X-Cookie {maconomyRow.maconomyCookie}',
    'Accept': 'application/vnd.deltek.maconomy.containers+json; version=5.0',
    'Content-Type': 'application/vnd.deltek.maconomy.containers+json; version=5.0',
    'Content-Length': f'{contentLength}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, cookies=maconomyRow.cookieJar)

    maconomyRow.concurrencyToken = response.headers.get('Maconomy-Concurrency-Control')
    responseJson = response.json()
    maconomyRow.containerInstanceId = responseJson.get('meta').get('containerInstanceId')
    logger.info("Maconomy Instance Response = ")
    logger.info(response)
    return response

def make_maconomy_request_instance_data():
    url = f"https://me96763-webclient.deltekfirst.com/maconomy-api/containers/me96763/timeregistration/instances/{maconomyRow.containerInstanceId}/data;any"
    
    payload = {}
    
    headers = {
    'Maconomy-Authentication': 'X-Disable-Negotiate,X-Force-Maconomy-Credentials,X-Force-Maconomy-Credentials,X-Basic,X-Reconnect,X-Cookie',
    'Maconomy-Client': 'iAccess',
    'Maconomy-Format': 'date-format="yyyy-MM-dd";time-format="HH:mm";thousand-separator=",";decimal-separator=".";number-of-decimals=2',
    'Authorization': f'X-Cookie {maconomyRow.maconomyCookie}',
    'Accept': 'application/vnd.deltek.maconomy.containers+json; version=5.0',
    'Connection': 'keep-alive',
    'Maconomy-Concurrency-Control': f'{maconomyRow.concurrencyToken}',
    'Content-Length': '0',
    'Host': 'me96763-webclient.deltekfirst.com'
    }

    response = requests.request("POST", url, headers=headers, data=payload, cookies=maconomyRow.cookieJar)
    
    logger.info("Maconomy Instance Data Response = ")
    logger.info(response)
    print(response.json())
    maconomyRow.concurrencyToken = response.headers.get('Maconomy-Concurrency-Control')
    return response

def make_maconomy_request_update_card(entry):
    url = f"https://me96763-webclient.deltekfirst.com/maconomy-api/containers/me96763/timeregistration/instances/{maconomyRow.containerInstanceId}/data/panes/card/0"
    data = {
        "data": {
            "datevar": f"{entry.date}"
        }
    }
    payload = json.dumps(data)
    contentLength = len(payload)

    headers = {
    'Maconomy-Authentication': 'X-Disable-Negotiate,X-Force-Maconomy-Credentials,X-Force-Maconomy-Credentials,X-Basic,X-Reconnect,X-Cookie',
    'Maconomy-Client': 'iAccess',
    'Maconomy-Format': 'date-format="yyyy-MM-dd";time-format="HH:mm";thousand-separator=",";decimal-separator=".";number-of-decimals=2',
    'Authorization': f'X-Cookie {maconomyRow.maconomyCookie}',
    'Accept': 'application/vnd.deltek.maconomy.containers+json; version=5.0',
    'Connection': 'keep-alive',
    'Maconomy-Concurrency-Control': f'{maconomyRow.concurrencyToken}',
    'Content-Type': 'application/vnd.deltek.maconomy.containers+json; version=5.0',
    'Content-Length': f'{contentLength}',
    'Host': 'me96763-webclient.deltekfirst.com'
    }

    response = requests.request("POST", url, headers=headers, data=payload, cookies=maconomyRow.cookieJar)
    logger.info("Maconomy Update Card Response = ")
    logger.info(response)
    print(response.json())
    maconomyRow.concurrencyToken = response.headers.get('Maconomy-Concurrency-Control')
    return response

def make_maconomy_request_insert_row(entry):
    url = f"https://me96763-webclient.deltekfirst.com/maconomy-api/containers/me96763/timeregistration/instances/{maconomyRow.containerInstanceId}/data/panes/table?row=end"

    dayOfWeek = entry.get_weekday() + 1
    data = {
        "data": {
            "jobnumber": entry.jobNr,
            f"numberday{dayOfWeek}": entry.duration,
            "taskname": entry.task,
            f"descriptionday{dayOfWeek}": entry.description,
            "specification3name": entry.spec3
        }
    }

    payload = json.dumps(data)
    contentLength = len(payload)

    headers = {
    'Maconomy-Authentication': 'X-Disable-Negotiate,X-Force-Maconomy-Credentials,X-Force-Maconomy-Credentials,X-Basic,X-Reconnect,X-Cookie',
    'Maconomy-Client': 'iAccess',
    'Maconomy-Format': 'date-format="yyyy-MM-dd";time-format="HH:mm";thousand-separator=",";decimal-separator=".";number-of-decimals=2',
    'Authorization': f'X-Cookie {maconomyRow.maconomyCookie}',
    'Accept': 'application/vnd.deltek.maconomy.containers+json; version=5.0',
    'Content-Type': 'application/vnd.deltek.maconomy.containers+json; version=5.0',
    'Connection': 'keep-alive',
    'Maconomy-Concurrency-Control': f'{maconomyRow.concurrencyToken}',
    'Content-Length': f'{contentLength}',
    'Host': 'me96763-webclient.deltekfirst.com',
    'Referer': f'https://me96763-webclient.deltekfirst.com/workspace/weeklytimesheets;date={entry.date};EmployeeNumber={maconomyRow.employeeNumber}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, cookies=maconomyRow.cookieJar)
    logger.info("Maconomy Insert Row Response = ")
    logger.info(response)
    print(response.json())
    maconomyRow.concurrencyToken = response.headers.get('Maconomy-Concurrency-Control')
    return response