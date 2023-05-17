import scrapy
from used_cars.items import UsedCarsItem
import json

class CarsSpider(scrapy.Spider):
    name = "car"
    
    start_urls = ['https://www.allenchevy.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_USED:inventory-data-bus1/getInventory?gclid=Cj0KCQiA8t2eBhDeARIsAAVEga0u3xK1ohR38jYqnu9PuABCwZUYR1pUsSIucvClti2taMnR6yHBbJcaAtHcEALw_wcB&year=1994-2021&start=0']
    
    def parse(self, response):
        dt = json.loads( response.body )        

        for car in dt['inventory']:
            item = UsedCarsItem()
            item['engineSize'] = car.get('engineSize')
            item['fuelType'] = car.get('fuelType')
            item['make'] = car.get('make')
            item['model'] = car.get('model')
            item['trim'] = car.get('trim')
            item['salePrice'] = car.get('salePrice')
            item['newOrUsed'] = car.get('newOrUsed')
            yield item
            
            for start_page in range(0, 181, 18):
                yield scrapy.Request(
                    f"https://www.allenchevy.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_USED:inventory-data-bus1/getInventory?gclid=Cj0KCQiA8t2eBhDeARIsAAVEga0u3xK1ohR38jYqnu9PuABCwZUYR1pUsSIucvClti2taMnR6yHBbJcaAtHcEALw_wcB&year=1994-2021&start={start_page}"
                )