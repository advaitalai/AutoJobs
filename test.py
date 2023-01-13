from bs4 import element
from bs4 import BeautifulSoup
import requests, re
import time
from selenium import webdriver
from requests_html import HTMLSession

url = 'https://jobs.accel.com/#srch_jobsTab'


# This is the vanilla requests route. Doesn't solve for javascript rendered pages.
# response = requests.get(url)

# Trying the requests_HTML route
session = HTMLSession()
r = session.get(url)

r.html.render(timeout=20)
soup = BeautifulSoup(r.html.html, 'lxml')

cnt = 1
for d in soup.descendants:
    if isinstance(d, element.NavigableString) and not isinstance(d, element.Comment) and not isinstance(d, element.Script) and not d.string.isspace():
        print('%d %s: %s' %(cnt, type(d), d.string))
        cnt += 1