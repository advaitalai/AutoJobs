''' Defines a class that can parse any job posting and create an Applicator object with standard apply functions
    Stages of data processing pipline are as follows:
    1. Get the dynamically loaded full soup. 
    2. Get a list of candidate input elements - inputs & textareas
    3. Initialise dictionary with xpath keys, WebElements & Tags
    4. Identify and discard optional inputs (TBD)
    5. Infer InputName, InputType, Options
    6. Deliver candidate selenium action (e.g. click, submit, sendkeys)
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

# Element data structure
# XPATH_ID --> {WebElement, Tag, InputName, InputType, Options}
# WebElement is needed to check visibility
# Tag is needed to access tree - siblings, parents etc

class JobApplicator:
    
    # Enum for input name
    InputName = Enum('InputName', ['FIRST_NAME', 'LAST_NAME', 'FULL_NAME', 'EMAIL', 'PHONE', 'RESUME', 'COVER', 'CURRENT_LOCATION', 'PREFERRED_LOCATION', 'LINKEDIN', 'UNKNOWN'])
    InputType = Enum('InputType', ['TEXT', 'FILE', 'RADIO', 'CHECK', 'UNKNOWN'])
    
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
        self.soup = None
        
    def initialise_input_feed(self) -> None:
        ''' Handles dynamically loaded webpages and returns soup that appears only after the submit button is loaded '''
        
        self.browser.get(self.url)
        wait = WebDriverWait(self.browser, 10)
        submit_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@type='submit']")))
        self.soup = BeautifulSoup(self.browser.page_source, "html.parser")
        
        for tag in self.get_input_candidates():
            xpath = self.xpath_soup(tag)
            self.input_feed[xpath] = {}
            self.input_feed[xpath]['WebElement'] = self.browser.find_element(By.XPATH, xpath)
            self.input_feed[xpath]['Tag'] = tag
            
            # Initialise InputTypes
            self.input_feed[xpath]['InputType'] = self.infer_input_type(xpath)
            
            # Initialise InputNames
            # self.input_feed[xpath]['InputName'] = self.infer_input_name(xpath)
            
        # Close the browser session
        self.browser.quit()
    
    def is_mandatory(xpath) -> bool:
        ''' Returns True if the element is a mandatory input '''
        return False
    
    def is_visible(tag) -> bool:
        ''' Returns True if a selenium element is visible or not '''
        
    def get_input_candidates(self):
        ''' Helper function. Gets the initial list of candidate input elements (emails, files, textareas etc.) '''
        input_candidates = []
        try: 
            input_candidates = self.soup.find_all('input')
            for ta in self.soup.find_all('textarea'):
                input_candidates.append(ta)
            self.raw_inputs = input_candidates
        except Exception as e:
            print("An error occurred while accessing the URL: ", e)
        
        return input_candidates
        
    def print_input_feed(self):
        # extract soup xpaths
        pprint.pprint(self.input_feed)
        
    def infer_input_type(self, xpath) -> InputType:
        ''' Infers the input type (name, email etc.) given an xpath '''
        # First look at 'type' attribute or the element name (e.g. textarea)
        # Then look at 'placeholder' attribute
        # Then look at sibling contents (probably navigable strings?)
        # Else return unknown
        
        tag: Tag = self.input_feed[xpath]['Tag']
        input_type = None

        if tag.name == 'textarea':
            input_type = self.InputType.TEXT
        
        # It is an 'input' type
        elif tag.name == 'input':
            if tag.has_attr('type'):
                type_value = tag['type']
                if type_value == 'radio':
                    input_type = self.InputType.RADIO
                elif type_value == 'checkbox':
                    input_type = self.InputType.CHECK
                elif type_value == 'file':
                    input_type = self.InputType.FILE
                elif type_value == 'text':
                    input_type = self.InputType.TEXT
                else:
                    input_type = self.InputType.UNKNOWN
            
            # Element doesn't have a 'type' attribute
            else:
                input_type = None
    
        # Unrecognised tag name
        else:
            input_type = self.InputType.UNKNOWN
        
        return input_type
    
    def infer_input_name(self, xpath) -> str:
        ''' Gets the input intent like name, email, phone number etc. '''
        # Algo is as follows
        # First check the placeholder which is a human readable hint
        # If no placeholder, check the sibling inner HTMLs for potential hints
        # Initially returns a string and then refines it into a structured InputName
        
        tag: Tag = self.input_feed[xpath]['Tag']
        input_name = None
        
        if tag.has_attr('placeholder'):
            placeholder = tag['placeholder']
            input_name = placeholder
        
        # Else check out the siblings leaves or sibling string children
        else:
            input_name = self.find_first_sibling_text(tag)
        return input_name
    
    def find_first_sibling_text(self, tag: Tag) -> str:
        for sibling in tag.previous_siblings:
            if sibling.string:
                return sibling.string
            else:
                for child in sibling.children:
                    if child.string:
                        return child.string
        for sibling in tag.next_siblings:
            if sibling.string:
                return sibling.string
            else:
                for child in sibling.children:
                    if child.string:
                        return child.string
        return None
    
    def traverse_post_order(self, tag: Tag) -> None:
        
        # First traverse the children
        for child in tag.children:
            self.traverse_post_order(child)
        
        # Finally print the root node string
        print(tag.string)
    
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
    ja.initialise_input_feed()
    #ja.print_input_feed()
    
    # Print first post order traversal
    input_feed: typing.Dict = ja.input_feed
    first_xpath = list(input_feed.keys())[0]
    print(first_xpath)
    first_tag = input_feed[first_xpath]['Tag']
    print(first_tag)
    ja.traverse_post_order(first_tag)
    
    