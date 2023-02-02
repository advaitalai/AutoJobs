import requests
from selenium import webdriver


def show_response_in_browser(response):
    browser = webdriver.Chrome()
    browser.get('data:text/html;charset=utf-8,' + response.text)
    
    input("Press Enter to close the browser window...")
    browser.quit()


    