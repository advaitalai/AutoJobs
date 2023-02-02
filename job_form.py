''' Class to handle application forms for Job objects '''

from enum import Enum

class JobForm:
    InputType = Enum('InputType', ['FIRST_NAME', 'LAST_NAME', 'EMAIL', 'PHONE', 'RESUME', 'COVER', 'PREFERRED_LOCATION', 'LINKEDIN', 'PORTFOLIO'])
    
    def _init__(self):
        pass
    
    