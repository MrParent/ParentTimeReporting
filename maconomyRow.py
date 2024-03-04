import json
from datetime import datetime 

maconomy_cookie = None
concurrency_token = None
instance_id = None
cookie_jar = None
employee_number = None

class MaconomyRow:
    def __init__(self, job_nr, task, description, date, duration, spec3):
        self.job_nr = job_nr
        self.task = task
        self.description = description
        self.date = date
        self.duration = duration
        self.spec3 = spec3
    
    def __str__(self):
        return f"job_nr: {self.job_nr:<10} Task: {self.task:<24} Description: {self.description:<70} Date: {self.date:<12} Duration: {self.duration:<4} Spec3: {self.spec3:<12}"
    
    def short_str(self):
        return f"job_nr: {self.job_nr:<10} Task: {self.task:<24} Description: {self.description:<70} Duration: {self.duration:<4} Spec3: {self.spec3:<12}"
    
    def get_weekday(self):
        date_in_datetime = datetime.strptime(self.date, '%Y-%m-%d')
        return date_in_datetime.weekday()

def get_maconomy_configured_entry(data, entry):
    for definition in data.get('definitions'):
        print(definition.get('local-job'))
        print(entry.client_name)
        if definition.get('local-job') == entry.client_name:
            for task in definition.get('tasks'):
                print(definition.get('local-task')) 
                print(entry.project_name)
                if task.get('local-task') == entry.project_name:
                    spec3 = definition.get('spec3')
                    if not spec3:
                        spec3 = data.get('defaults').get('spec3')
                    maconomy_job = definition.get('remote-job')
                    maconomy_task = task.get('remote-task')
                    return MaconomyRow(maconomy_job, maconomy_task, entry.description, entry.get_start_date(), entry.get_duration_hours(), spec3)
    return MaconomyRow("None", "None", "None", "None", "None", "None")

with open('config.json', 'r', encoding='utf-8') as f:
    maconomy_config = json.load(f)