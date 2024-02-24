import requests
from requests.auth import HTTPBasicAuth
from base64 import b64encode
import os

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

    return response