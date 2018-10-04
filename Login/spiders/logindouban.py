# -*- coding: utf-8 -*-
import scrapy
import requests
import  urllib.request


class LogindoubanSpider(scrapy.Spider):
    name = 'logindouban'
    allowed_domains = ['www.douban.com']
    start_urls = ['https://accounts.douban.com/login']

    def start_requests(self):
        url='https://accounts.douban.com/login'
        keyword = urllib.parse.quote('登录')
        print('sfdfegregr',keyword)
        yield  scrapy.Request(url=url,callback=self.parse)


    def after_login(self,response):
        title=response.css('head > title').extract_first()
        print('title*****',title)


    def parse(self, response):
        imag=response.css('#captcha_image::attr(src)')
        imagurl=imag.extract_first()
        res=requests.get(imagurl)
        with open("yanzhengma.jpg",'wb') as f:
            f.write(res.content)
        captcha_id=imag.re('id=(.*?)&')#.split('?')[1].split('&')[0]
        captcha_solution=input()
        url = 'https://accounts.douban.com/login'
        keyword=urllib.parse.quote('登录')
        postdata = {
            'source': 'None',
            'redir': 'https://www.douban.com/people/71210780/',
            'form_email': '******@qq.com',
            'form_password': '*********',
            'captcha - solution': captcha_solution,
            'captcha - id': captcha_id,
            'login': keyword,
        }
        yield scrapy.FormRequest(url=url,formdata=postdata,callback=self.after_login,dont_filter=True)


