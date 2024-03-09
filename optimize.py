from datetime import datetime, timezone
import time_log
from PyQt5.QtWidgets import QFileDialog

# open file dialog.
def open_file_dialog():
    #open file dialog with txt file filter
    dialog = QFileDialog(filter="Text files (*.txt)")
    filename, _ = dialog.getOpenFileName()
    
    if filename:
        print(f"Selected file: {filename}")
        return filename
    else:
        print("No file selected.")
        return None
    
# optimize file dialog callback.
def open_and_parse_optimize_file(start_time, end_time):
    filename = open_file_dialog()
    if filename:
        time_entries = parse_file(start_time, end_time, filename)
        return time_entries
    else:
        print("No file selected. Bail out.")
        return None

# parse optimize txt file to get the time entries.
def parse_file(start_time, end_time, filename):
    start = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S%z')
    end = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
    time_entries = []
    with open(filename) as file:
        for line in file:
            first_part, second_part = line.strip().split('HasEnded=true ', 1)
            start_str = first_part.strip()
            stop_date, stop_time, description = second_part.strip().split(' ', 2)
            stop_str = f"{stop_date} {stop_time}"

            start_entry = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
            stop_entry = datetime.strptime(stop_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)

            if start_entry < start or stop_entry > end:
                continue

            duration = int((stop_entry - start_entry).total_seconds())
            print(duration)

            client_name, project_name, task = description.split(';')
            
            start_entry_str = start_entry.strftime('%Y-%m-%dT%H:%M:%S%z')
            stop_entry_str = stop_entry.strftime('%Y-%m-%dT%H:%M:%S%z')
            
            time_entry = time_log.TimeLog(start_entry_str, stop_entry_str, duration, task, client_name, project_name)
            time_entries.append(time_entry)
    return time_entries