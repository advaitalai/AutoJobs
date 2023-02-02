''' Defines a class that can parse any job posting and create an Applicator object with standard apply functions
'''

import requests
import pprint
import typing
import bs4
from bs4 import BeautifulSoup, Tag
from utils.html import show_response_in_browser

# Import selenium to apply to jobs as well as load dynamic content
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Get Job Form object
from enum import Enum

# Input data structure
# XPATH_ID --> [WebElement, BeautifulSoup, InputName, InputType, Options]

class JobApplicator:
    
    # Enum for input name
    InputName = Enum('InputName', ['FIRST_NAME', 'LAST_NAME', 'FULL_NAME', 'EMAIL', 'PHONE', 'RESUME', 'COVER', 'PREFERRED_LOCATION', 'LINKEDIN', 'PORTFOLIO', 'UNKNOWN'])
    InputType = Enum('InputType', ['TEXT', 'FILE', 'RADIO', 'CHECK'])
    
    def __init__(self, url) -> None:
        self.url = url 
        
        # raw are WIP inputs, clean inputs have the final selenium elements.
        self.raw_inputs = []
        self.clean_inputs = []
        
        # XPATH_ID --> [InputName, InputType, Options]
        self.input_feed = {}
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(options=options)
        
    def get_soup(self) -> BeautifulSoup:
        ''' Handles dynamically loaded webpages and returns soup that appears only after the submit button is loaded '''
        
        self.browser.get(self.url)
        wait = WebDriverWait(self.browser, 10)
        submit_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@type='submit']")))
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        self.browser.quit()
        return soup
     
    def parse_input_name(tag: Tag):
        ''' Infers from element attributes or surrounding siblings what the input is for '''
        # first look at placeholder attributes
        # then look at siblings
        # if everything fails, return unknown
        pass
    
    def is_mandatory(tag) -> bool:
        ''' Returns True if the element is a mandatory input '''
        return False
    
    def is_visible(tag) -> bool:
        ''' Returns True if a selenium element is visible or not '''
        
    def get_input_candidates(self, soup) -> None:
        ''' Sets the initial list of candidate input elements (emails, files, textareas etc.) '''
        input_candidates = []
        try: 
            input_candidates = soup.find_all('input')
            for ta in soup.find_all('textarea'):
                input_candidates.append(ta)
            self.raw_inputs = input_candidates
        except:
            print("An error occurred while accessing the URL.")
        
        return input_candidates
    
    def set_random_inputs(self):
        pass
    
    def initialise_input_feed(self):
        # extract soup xpaths
        pass
    
    def xpath_soup(self, element: typing.Union[bs4.element.Tag, bs4.element.NavigableString]) -> str:
        # type: (typing.Union[bs4.element.Tag, bs4.element.NavigableString]) -> str
        """
        Generate xpath from BeautifulSoup4 element.
        :param element: BeautifulSoup4 element.
        :type element: bs4.element.Tag or bs4.element.NavigableString
        :return: xpath as string
        :rtype: str
        Usage
        -----
        >>> import bs4
        >>> html = (
        ...     '<html><head><title>title</title></head>'
        ...     '<body><p>p <i>1</i></p><p>p <i>2</i></p></body></html>'
        ...     )
        >>> soup = bs4.BeautifulSoup(html, 'html.parser')
        >>> xpath_soup(soup.html.body.p.i)
        '/html/body/p[1]/i'
        >>> import bs4
        >>> xml = '<doc><elm/><elm/></doc>'
        >>> soup = bs4.BeautifulSoup(xml, 'lxml-xml')
        >>> xpath_soup(soup.doc.elm.next_sibling)
        '/doc/elm[2]'
        """
        components = []
        
        child = element if element.name else element.parent
        for parent in child.parents:  # type: bs4.element.Tag
            siblings = parent.find_all(child.name, recursive=False)
            components.append(
                child.name if 1 == len(siblings) else '%s[%d]' % (
                    child.name,
                    next(i for i, s in enumerate(siblings, 1) if s is child)
                    )
                )
            child = parent
        components.reverse()
        return '/%s' % '/'.join(components)


if __name__ == '__main__':
    test_url = 'https://bolt.eu/en/careers/positions/5960750002/'
    ja = JobApplicator(test_url)
    soup = ja.get_soup()
    
    for i in ja.get_input_candidates(soup):
        print(ja.xpath_soup(i))

    
    