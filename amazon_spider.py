#don't forget tue user agents in SETTINGS

#https://github.com/rejoiceinhope/scrapy-proxy-pool

#https://pypi.org/project/scrapy-user-agents/
#https://www.youtube.com/watch?v=090tLVr0l7s&list=PLhTjy8cBISEqkN-5Ku_kXG4QW33sxQo0t&index=24

import scrapy

from ..items import AmazontutorialItem


class AmazonSpiderSpider(scrapy.Spider):
	name = 'amazon'
	page_number = 2
	start_urls = ['https://www.amazon.com/s?bbn=1&rh=n%3A283155%2Cn%3A%211000%2Cn%3A1%2Cp_n_publication_date%3A1250226011&dc&fst=as%3Aoff&qid=1606224210&rnid=1250225011&ref=lp_1_nr_p_n_publication_date_0']

	def parse(self, response):
		items = AmazontutorialItem()

		product_name = response.css('.a-color-base.a-text-normal::text').extract()
		product_author = response.css('.sg-col-12-of-28 span.a-size-base+ .a-size-base::text').extract()
		product_price = response.css('.a-spacing-top-small .a-price-whole::text').extract()
		product_imagelink = response.css('.s-image::attr(src)').extract()

		items['product_name'] = product_name
		items['product_author'] = product_author
		items['product_price'] = product_price
		items['product_imagelink'] = product_imagelink

		yield items

		next_page = 'https://www.amazon.com/s?i=stripbooks&bbn=1&rh=n%3A283155%2Cn%3A1000%2Cn%3A1%2Cp_n_publication_date%3A1250226011&dc&page=' + str(self.page_number) + '&fst=as%3Aoff&qid=1606229780&rnid=1250225011&ref=sr_pg_2'
		if self.page_number <= 3: #you can specify any number of pages you, here I specified 3 just for clarity
			self.page_number += 1
			yield response.follow(next_page, callback = self.parse)
