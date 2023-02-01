''' Gets form elements using beautiful soup and controls a stealth node js function to submit application '''

from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_elements(url):
    # Make a request to the webpage
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    text_elements = soup.find_all('input', type='text')
    button_elements = soup.find_all('button')
    checkbox_elements = soup.find_all('input', type='checkbox')

    # Print the text, buttons, and checkboxes
    print('Text Inputs:')
    for element in text_elements:
        print(element.strip())
    print('\nButtons:')
    for element in button_elements:
        print(element)
    print('\nCheckboxes:')
    for element in checkbox_elements:
        print(element)
        
def get_form(url):
    driver = webdriver.Chrome()
    
    driver.get(url)

    # Wait for the iframe to be loaded
    wait = WebDriverWait(driver, 5)
    iframe = wait.until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))
    
    dynamic_form = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'form')))
    
    # Do something with the form element
    print(dynamic_form.get_attribute('innerHTML'))
    

#get_elements('https://miro.com/careers/vacancy/6502537002/')
get_form('https://miro.com/careers/vacancy/6502537002/')
