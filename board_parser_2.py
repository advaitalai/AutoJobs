''' This class accepts board leads from upstream board hunters & extracts Job objects from them.
    It is able to interpret different types of lead pages -- static or dynamic and accordingly fetch a 
    list of jobs '''
    

from enum import Enum
from job import Job
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
import json
from pprint import pprint

# To get fetched / dynamic content, go directly to API
from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BoardParser:

    BoardType = Enum('BoardType', ['STATIC', 'DYNAMIC'])
    FetchFormat = Enum('FetchFormat', ['JSON'])    
    
    def __init__(self, url) -> None:
        self.url = url
        self.job_dict = {} # This is a dict representation of JSON board data
        
        # self.is_paginated = False
        # self.fetch_format = FetchFormat.JSON
        # self.set_board_type(url)
    
    def get_page_links(self) -> list:
        ''' Get all a href links in the scraped page to search for potential job postings '''
        
        # Send a GET request to the URL
        response = requests.get(self.url)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all 'a' tags
        links = soup.find_all("a")

        # Extract the href attribute from each link
        href_links = [link.get("href") for link in links]
        
        return href_links
    
    def is_job_post(self, job_link: str) -> bool:
        ''' Check if a link is likely a job post having a unique ID '''
        
        if job_link is None:
            return False
        
        # Define the regex pattern to match typical job post URLs
        pattern = r"(job|jobs|career|careers).*\d{5,}"

        # Search for a match in the URL
        match = re.search(pattern, job_link)

        # Return True if a match is found, False otherwise
        return match is not None
    
    def get_fetched_data(self) -> list:
        ''' Intercept and return backend API calls to fetch dynamic data.
            Return a link which is a likely board JSON link '''
        
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        # Create a new instance of the Chrome driver
        driver = webdriver.Chrome(chrome_options=options)

        # Go to the Google home page
        driver.get(self.url)

        # Need to incorporate code for lazy load content
        # wait = WebDriverWait(driver, 30)
        # wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(),'Loading')]")))

        legit_links = []

        # Access requests via the `requests` attribute
        for request in driver.requests:
            if request.response:
                legit_links.append(request)
                print(
                    request.url,
                    request.response.status_code,
                    request.response.headers['Content-Type']
                )
                
        return legit_links
    
    def get_likely_board(self, fetched_data: list) -> str:
        ''' Takes a list of selenium requests and returns the like board JSON URL '''
        
        target_board = ''
        
        # Access requests via the `requests` attribute
        for request in fetched_data:
            
            if request.response.headers['Content-Type'] == 'application/json' and self.is_likely_board(request.url):
                target_board = request.url
                print("Found likely board API: %s" %(target_board))
                
        return target_board
    
    def is_likely_board(self, url: str) -> bool:
        ''' Checks a request URL whether it is a likely job board JSON via regex expressions
            Anything of the form *greenhouse*open-positions *company-name*jobs 
            Need to re-write for regex matching '''
        
        # list1 = ['greenhouse', 'miro', 'phonepe']
        # list2 = ['job', 'board', 'jobs', 'open-positions']
        
        return url in ['https://miro.com/careers/_next/data/dOmq7u_mjR9v5tqnFL7qR/open-positions.json',
                       'https://boards-api.greenhouse.io/v1/boards/phonepe/jobs']
        
    
    def parse_json(self, url:str) -> None:
        ''' Sets the board_dict for later loading to Job objects '''
        
        response = requests.get(url)
        
        if response.status_code != 200:
            raise ValueError(f"Failed to load {url} with status code {response.status_code}")
        json_data = json.loads(response.text)
        self.job_dict = json_data
        
        return self.job_dict
        
        
# Test first with company careers pages
if __name__ == '__main__':
    bp = BoardParser('https://miro.com/careers/open-positions/')
    
    links = bp.get_fetched_data()
    target = bp.get_likely_board(links)
    pprint(bp.parse_json(target))
    
    


