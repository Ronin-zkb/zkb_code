# -*- coding: utf-8 -*-
import scrapy
from sanxin.items import SanxinItem

class SanxinSpiderSpider(scrapy.Spider):
    name = 'sanxin_spider'
    allowed_domains = ['https://www.jd.com/pinpai']
    start_urls = ['https://www.jd.com/pinpai/655-15127.html/']
    # 爬取页数
    page_num = 7
    # 当前爬取页
    index_page = 1

    # item属性
    phone_name = ''
    running_memory = ''
    battery_life = ''
    body_color = ''
    front_pixel = ''
    post_pixel = ''

    def parse(self, response):
        phone_list = response.xpath('//div[@id="J_goodsList"]//li[@class="gl-item"]')
        for phone in phone_list:
            item = SanxinItem()
            item['price'] = phone.xpath('.//div[@class="p-price"]//i/text()').extract_first()
            if item['price'] is None:
                item['price'] = 0

            # 获取详情页超链接
            detail_url = "https://" + phone.xpath('.//div[@class="p-img"]/a/@href').extract_first()

            # 新建一个请求，去获取详情页的数据
            req = scrapy.Request(detail_url, callback=self.parse_detail, meta={'item': item})
            yield req
        # 获取下一页链接
        next_page_url = "https://www.jd.com/pinpai/655-15127.html?&stop=1&vt=2&bs=1&cid2=653&cid3=655&ev=exbrand_%E4%B8%89%E6%98%9F%EF%BC%88SAMSUNG%EF%BC%89%5E&click=0&page=" + str(
            self.index_page * 2 - 1) + "&s=" + str((self.index_page - 1) * 60 + 1)
        # 发送新的请求获取下一页的列表页面
        if self.index_page <= self.page_num:
            self.index_page += 1
            print("1" * 50 + next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_detail(self, response):
        # 获取item对象
        item = response.meta['item']
        # 获取手机信息
        phone_info_list = response.xpath('//div[@id="detail"]//ul[@class="parameter2 p-parameter-list"]/li')
        for phone_info in phone_info_list:
            temp_text = phone_info.xpath('./text()')
            if "商品名称" in temp_text.extract_first():
                self.phone_name = phone_info.xpath('./@title').extract_first()
            elif "电池容量" in temp_text.extract_first():
                self.battery_life = phone_info.xpath('./@title').extract_first()
            elif "运行内存" in temp_text.extract_first():
                self.running_memory = phone_info.xpath('./@title').extract_first()
            elif "机身颜色" in temp_text.extract_first():
                self.body_color = phone_info.xpath('./@title').extract_first()
            elif "前摄主摄" in temp_text.extract_first():
                self.front_pixel = phone_info.xpath('./@title').extract_first()
            elif "后摄主摄" in temp_text.extract_first():
                self.post_pixel = phone_info.xpath('./@title').extract_first()

        item['phone_name'] = self.phone_name
        item['battery_life'] = self.battery_life
        item['running_memory'] = self.running_memory
        item['body_color'] = self.body_color
        item['front_pixel'] = self.front_pixel
        item['post_pixel'] = self.post_pixel
        yield item