# Defines a job class. Make this after the board parser.

from bs4 import BeautifulSoup
from utils import html

class Job:   
    def __init__(self) -> None:
        self.title = ''
        self.location = ''
        self.salary = ''
        self.domain = 'product'
        self.team = ''
        self.role = ''
        self.basic_quals = ''
        self.pref_quals = ''
        self.benefits = ''
        self.company = ''
        self.about_company = ''
    
    def parse_post(url:str):
        pass
    
    def get_title(self):
        print(self.soup.title)