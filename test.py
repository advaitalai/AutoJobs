from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('headless')

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(chrome_options=options)

# Go to the Google home page
driver.get('https://jobs.accel.com/#srch_jobsTab')

wait = WebDriverWait(driver, 30)
wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(),'Loading')]")))

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.response:
        print(
            request.url,
            request.response.status_code,
            request.response.headers['Content-Type']
        )