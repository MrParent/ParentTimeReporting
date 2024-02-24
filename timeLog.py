import re
from datetime import datetime, timedelta, timezone

class TimeLog :
    def __init__(self, start, stop, duration, description, client_name, project_name):
        self.start = start
        self.stop = stop
        self.duration = duration
        self.description = description
        self.client_name = client_name
        self.project_name = project_name
    
    def __str__(self):
        return f"Time: {self.get_duration():<8} Desc: {self.description:<80} Client: {self.client_name:<12} Project: {self.project_name:<12} StartTime: {self.start.split('T')[0]:<8}"
    
    def short_str(self):
        return f"{self.get_duration():<8} {self.description:<15} {self.start.split('T')[0]:<8}"

    def get_duration(self):
        hours, minutes, seconds = convert_seconds(int(self.duration))
        return f"{hours:02}:{minutes:02}"
    
    def get_duration_minutes(self):
        minutes = convert_to_minutes(self.duration)
        return str(minutes)

# Check if a string is a valid Jira issue description
def is_valid_description(description):
    # The regex pattern
    pattern = r'^[A-Z]+-\d+$'
    
    # Use the match function to check if the description matches the pattern
    match = re.match(pattern, description)
    
    # If the match function returns a match object, the description is valid
    return match is not None

def convert_seconds(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds

def convert_to_minutes(seconds):
    minutes, remainder = divmod(seconds, 60)
    return minutes

def format_time(input_time, timezone_offset):
    # Parse the time from the input format
    dt = datetime.strptime(input_time, '%Y-%m-%dT%H:%M:%S%z')

    # Convert to the desired timezone
    dt = dt.astimezone(timezone(timedelta(hours=timezone_offset)))

    # Format the time into the desired format
    formatted_time = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + dt.strftime('%z')

    return formatted_time