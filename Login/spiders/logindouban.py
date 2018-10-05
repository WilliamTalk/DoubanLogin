# -*- coding: utf-8 -*-
import scrapy
import requests
from PIL import Image


class LogindoubanSpider(scrapy.Spider):
    name = 'logindouban'
    allowed_domains = ['www.douban.com']
    start_urls = ['https://accounts.douban.com/login']

    def start_requests(self):
        url = 'https://accounts.douban.com/login'

        return [scrapy.Request(url=url, callback=self.parse)]

    def after_login(self, response):
        title = response.css('head > title').extract_first()
        print('title*****', title)

    def parse(self, response):
        url = 'https://accounts.douban.com/login'
        imag = response.css('#captcha_image')
        if imag is None:
            imagurl = imag.extract_first()
            res = requests.get(imagurl)
            with open("yanzhengma.jpg", 'wb') as f:
                f.write(res.content)
            im = Image.open('yanzhengma.jpg')
            im.show()

            captcha_id = imag.re('id=(.*?)&')[0]  # .split('?')[1].split('&')[0]
            captcha_solution = input()


            postdata = {
                'source': 'None',
                'redir': 'https://www.douban.com/people/71210780/',
                'form_email': '992621968@qq.com',
                'form_password': 'william072424',
                'captcha-solution': captcha_solution,
                'captcha-id': captcha_id,
                'login': '登录',
            }
        else:
            postdata = {
                'source': 'None',
                'redir': 'https://www.douban.com/people/71210780/',
                'form_email': '*****@qq.com',
                'form_password': '*****',
                'login': '登录',
            }

        yield scrapy.FormRequest(url=url, formdata=postdata, callback=self.after_login, dont_filter=True)
