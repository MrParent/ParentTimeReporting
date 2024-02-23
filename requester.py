import requests
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