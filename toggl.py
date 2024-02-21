class TimeEntry :
    def __init__(self, start, stop, duration, description, client_name, project_name):
        self.start = start
        self.stop = stop
        self.duration = duration
        self.description = description
        self.client_name = client_name
        self.project_name = project_name
    
    def __str__(self):
        return f"Time: {self.get_duration():<12} Desc: {self.description:<80} Client: {self.client_name:<12} Project: {self.project_name:<12} StartTime: {self.start.split('T')[1]:<8}"
        #return f"Start: {self.start}, Stop: {self.stop}, Duration: {self.duration}, Description: {self.description}, Client Name: {self.client_name}, Project Name: {self.project_name}"
    
    def convert_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return hours, minutes, seconds
    
    def get_duration(self):
        hours, minutes, seconds = self.convert_seconds(int(self.duration))
        return f"{hours:02}:{minutes:02}:{seconds:02}"
