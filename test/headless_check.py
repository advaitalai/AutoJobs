import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://arh.antoinevastel.com/bots/areyouheadless'

# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')

# specify the path to the webdriver binary
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(options=options)

# navigate to the website
driver.get(url)

# take a screenshot
driver.save_screenshot('screenshot.png')

# close the browser
driver.quit()