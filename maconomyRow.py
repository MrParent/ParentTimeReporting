import json

class MaconomyRow:
    def __init__(self, jobNr, task, description, date, duration, spec3):
        self.jobNr = jobNr
        self.task = task
        self.description = description
        self.date = date
        self.duration = duration
        self.spec3 = spec3
    
    def __str__(self):
        return f"JobNr: {self.jobNr:<10} Task: {self.task:<24} Description: {self.description:<70} Date: {self.date:<12} Duration: {self.duration:<4} Spec3: {self.spec3:<12}"
    
    def short_str(self):
        return f"JobNr: {self.jobNr:<10} Task: {self.task:<24} Description: {self.description:<70} Duration: {self.duration:<4} Spec3: {self.spec3:<12}"

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
                    maconomyJob = definition.get('remote-job')
                    maconomyTask = task.get('remote-task')
                    return MaconomyRow(maconomyJob, maconomyTask, entry.description, entry.get_start_date(), entry.get_duration_hours(), spec3)
    return MaconomyRow("None", "None", "None", "None", "None", "None")

with open('config.json', 'r', encoding='utf-8') as f:
    maconomy_config = json.load(f)