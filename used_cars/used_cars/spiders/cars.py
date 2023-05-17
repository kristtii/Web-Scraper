from scrapy_playwright.page import PageMethod
import scrapy
from scrapy.loader import ItemLoader
from used_cars.items import UsedCarsItem

class CarsSpider(scrapy.Spider):
    name = "cars"
    
    def start_requests(self):
        yield scrapy.Request(
            "https://www.allenchevy.com/used-inventory/index.htm?year=1994-2021&gclid=Cj0KCQiA8t2eBhDeARIsAAVEga0u3xK1ohR38jYqnu9PuABCwZUYR1pUsSIucvClti2taMnR6yHBbJcaAtHcEALw_wcB",
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                    PageMethod("wait_for_selector", "//li[22]//div[@class='vehicle-card-details-container']"),
                ]             
            } 
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        cars = response.css("ul.vehicle-card-list h2 a::text").getall()
        price = response.css("span.price-value::text").getall()
        mileage = response.css("li.odometer::text").getall()
        for car in cars:
            yield{
                "car": car,
                "price": price,
                "mileage": mileage
            }
        await page.screenshot(path="snip.png", full_page = True)
        await page.close()
