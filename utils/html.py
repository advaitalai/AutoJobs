import requests

def get_source(url):
    response = requests.get(url)
    return response.text