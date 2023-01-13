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

Architecture
Company hunter --> board handler --> board parser

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