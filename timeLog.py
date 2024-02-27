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
        return f"Time: {self.get_duration():<8} Desc: {self.description:<80} Client: {self.client_name:<12} Project: {self.project_name:<12}"
    
    def short_str(self):
        return f"{self.get_duration():<8} {self.description:<15} {self.start.split('T')[0]:<8}"

    def get_duration(self):
        hours, minutes, seconds = convert_seconds(self.duration)
        return f"{hours:02}:{minutes:02}"
    
    def get_duration_minutes(self):
        minutes = convert_to_minutes(self.duration)
        return str(minutes)
    
    def get_jira_start_time(self):
        return format_time(self.start, 1)
    
    def get_jira_duration(self):
        hours, minutes, seconds = convert_seconds(self.duration)
        return f"{hours}h {minutes}m"
    
    def get_start_date(self):
        return self.start.split('T')[0]

# Check if a string is a valid Jira issue description
def is_valid_description(description):
    # The regex pattern
    pattern = r'^[A-Z]+-\d+$'
    
    # Use the match function to check if the description matches the pattern
    match = re.match(pattern, description)
    
    # If the match function returns a match object, the description is valid
    return match is not None

# Check if a TimeLog entry is valid for Maconomy. FIXME: Check against mapping for valid Maconomy entries
def is_valid_maconomy_entry(entry):
    if(entry.description and entry.duration and entry.start and entry.project_name and entry.client_name):
        return True
    else:
        return False

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

def merge_time_logs(time_logs):
    # Create a dictionary to group the time logs
    grouped_time_logs = {}

    for time_log in time_logs:
        # Create a key for the day, description, client_name, and project_name
        key = (time_log.get_start_date(), time_log.description, time_log.client_name, time_log.project_name)

        # If the key is not in the dictionary, add the time log to the dictionary
        if key not in grouped_time_logs:
            grouped_time_logs[key] = time_log
        else:
            # If the key is in the dictionary, merge the time logs
            existing_time_log = grouped_time_logs[key]
            existing_time_log.duration += time_log.duration
            existing_time_log.stop = max(existing_time_log.stop, time_log.stop)
            existing_time_log.start = min(existing_time_log.start, time_log.start)

    # Return the merged time logs
    return list(grouped_time_logs.values())