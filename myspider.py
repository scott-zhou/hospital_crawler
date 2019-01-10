import scrapy
# from urllib.parse import urlparse
import time
import random

# domain_title = {}
# key_words = [
#     '院训',
# ]


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = [
        'http://www.a-hospital.com/w/%E5%85%A8%E5%9B%BD%E5%8C%BB%E9%99%A2%E5%88%97%E8%A1%A8']
    # start_urls = ['https://stackoverflow.com']
    # start_urls = ['http://www.shcz.com/front/shouye.aspx']

    allowed_domains = ['a-hospital.com', 'www.a-hospital.com']

    custom_settings = {
        'DEPTH_LIMIT': 100,
        'CLOSESPIDER_ITEMCOUNT': 100000
    }
    random.seed()

    # def _parse_and_set_domain(self, response):
    #     domain = urlparse(response.url).netloc
    #     if domain not in domain_title:
    #         for title in response.css('head>title'):
    #             domain_title[domain] = \
    #                 title.css('title ::text').extract_first().strip('\r\n\t ')
    #             break
    #     return domain

    def parse(self, response):
        time.sleep(random.randint(5, 30))
        if response.meta['depth'] >= self.custom_settings['DEPTH_LIMIT']:
            return
        yield from self.parse_hospital(response)
        # domain = self._parse_and_set_domain(response)
        # if domain == 'www.a-hospital.com':
        #     yield from self.parse_hospital(response)
        #     return
        # yield from self.parse_specific_hospital(response, domain)

    # def parse_specific_hospital(self, response, domain):
    #     for obj in response.css('*'):
    #         content = obj.css('::text').extract_first()
    #         if not content:
    #             continue
    #         if type(content) == str:
    #             content = content.strip('\r\n\t ')
    #         for key in key_words:
    #             if content.find(key) >= 0:
    #                 yield {domain_title[domain]: content}

    #     for a in response.css('a'):
    #         # Ignore <a> without href
    #         if not a.css('::attr(href)'):
    #             continue
    #         # Ignore empty or '#' or main urls
    #         url = scrapy.http.response.text._url_from_selector(a)
    #         if not url or url == '#' or url.startswith('mailto:'):
    #             continue
    #         # For a specific hospital, ignore out links
    #         next_domain = urlparse(url).netloc
    #         if next_domain and next_domain != domain:
    #             continue
    #         yield response.follow(a, self.parse)

    def parse_hospital(self, response):
        target_item = {}
        for title in response.xpath('//div/h2/span[contains(text(), "概况")]'):
            title_s = title.xpath('text()').extract_first().strip('\r\n\t ')
            descript = title.xpath('../following-sibling::p[1]')
            if descript:
                descript_s = descript.extract_first().strip('\r\n\t ')
            if title_s and descript_s:
                target_item[title_s] = descript_s
        if target_item:
            yield target_item

        for a in response.xpath('//li/b/a[@href]'):
            yield response.follow(a, self.parse)
        for a in response.xpath('//a[contains(@title,"医院列表") and @href]'):
            yield response.follow(a, self.parse)
        # Not crawle external hospital webside now
        # for li in response.css('li'):
        #     is_url_to_hospital = False
        #     for b in li.css('b::text'):
        #         b_text = b.extract()
        #         if b_text and b_text.find('医院网站') >= 0:
        #             is_url_to_hospital = True
        #             break
        #     if is_url_to_hospital:
        #         for a in li.css('a'):
        #             yield response.follow(a, self.parse)
