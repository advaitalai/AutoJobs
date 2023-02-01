Data structures / Artifacts:
Post: URL containing a job post with a unique ID (e.g. Miro Sr. PM job)
Board: List of job posts (e.g. accel jobs, careers page)
Job: A cleaned object containing jost post information
Attribute: Job attribute such as location, title, salary

Personas:
Candidate
Employer
Recruiter
HiringManager

Job bread crumbs
Board hunting -> Company board --> extract job links
[Unhandled] Other job / company aggregators e.g. VC pages

Algo for getting job links
Visit board URL
Check & store list of job IDs via regex HREFs
Check for pagination and get custom code to expand list
If there are no static jobs, check selenium wire for API calls

Dependencies
requests
requests-html
scrapy
spacy
nltk
beautifulsoup
selenium
Chromium
scrapy-splash
wgrep
scrapy-pyppeteer
pyppeteer
mitmproxy (to intercept network requests)
openssl
selenium-wire