import scrapy
from pyppeteer import launch

class AjaxSpider(scrapy.Spider):
    name = "ajax"
    start_urls = [
        "https://www.phonepe.com/careers/job-openings/",
    ]

    async def _get_content(self, url):
        browser = await launch()
        page = await browser.newPage()
        await page.goto(url)

        # Wait for the dynamic content to load
        await page.waitForSelector(".content")

        # Extract the data
        data = await page.evaluate("""() => {
            return document.querySelector(".content").innerText;
        }""")

        await browser.close()
        print("Data is: ", data)
        return data

    def parse(self, response):
        
        return self._get_content(response.url)