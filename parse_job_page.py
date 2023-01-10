from bs4 import BeautifulSoup
from utils import html

class Job:   
    def __init__(self, url) -> None:
        self.soup = BeautifulSoup(html.get_source(url), 'html.parser')
    
    def get_title(self):
        print(self.soup.title)
        
if __name__ == '__main__':
    url = 'https://miro.com/careers/vacancy/6502537002/'
    job = Job(url)
    job.get_title()