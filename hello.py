from bs4 import BeautifulSoup
import requests

# function to extract html document from given url
def getHTMLdocument(url):
      
    # request for HTML document of given url
    response = requests.get(url)
      
    # response will be provided in JSON format
    return response.text

soup = BeautifulSoup(getHTMLdocument('https://miro.com/careers/vacancy/6502537002/'), 'html.parser')