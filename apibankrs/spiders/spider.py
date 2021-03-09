import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import ApibankrsItem
from itemloaders.processors import TakeFirst


class ApibankrsSpider(scrapy.Spider):
	name = 'apibankrs'
	start_urls = ['https://www.apibank.rs/en/latest/']

	def parse(self, response):
		post_links = response.xpath('//a[contains(@class, "news-item")]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="news-item-title"]/text()').get()
		description = response.xpath('//div[@class="news-item-text"]//text()[normalize-space()]').getall()
		description = [remove_tags(p).strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="news-item-date"]/text()').get()

		item = ItemLoader(item=ApibankrsItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
