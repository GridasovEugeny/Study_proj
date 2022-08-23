import scrapy
from scrapy.crawler import CrawlerProcess
import os
import pandas as pd
import re


df = pd.read_csv('tmp_urls.csv')

reg_geekjob = r'https://geekjob'
reg_proglib = r'https://proglib'
reg_career = r'https://career'
reg_hhru = r'https://hh\.ru'

geekjob_urls_filter = df.apply(lambda x: not (re.search(reg_geekjob, x['urls']) is None), axis=1)

proglib_urls_filter = df.apply(lambda x: not (re.search(reg_proglib, x['urls']) is None), axis=1)

career_urls_filter = df.apply(lambda x: not (re.search(reg_career, x['urls']) is None), axis=1)
hhru_urls_filter = df.apply(lambda x: not (re.search(reg_hhru, x['urls']) is None), axis=1)

geek_job = df[geekjob_urls_filter]
prog_lib = df[proglib_urls_filter]
career = df[career_urls_filter]
hh_ru = df[hhru_urls_filter]



#Совершенно не понмаю зачем писать новый класс для каждого сайта, а не создавать обьекты одного класса с параметрами.
#Но в документации так.
class SpiderGeekjob(scrapy.Spider):
    name = "Geekjob_vacancy_spider"
    index = list()
    
    def start_requests(self):
        for index, row in geek_job.iterrows():
            self.index.append(index)
            yield scrapy.Request(url=row['urls'], callback=self.parse)

    def parse(self, response):
        df.loc[self.index.pop(0), 'desc_html'] = response.css("section.col.s12.m12.main").get()

            
class SpiderProglib(scrapy.Spider):
    name = "Proglib_vacancy_spider"
    index = list()
    
    def start_requests(self):
        for index, row in prog_lib.iterrows():
            self.index.append(index)
            yield scrapy.Request(url=row['urls'], callback=self.parse)

    def parse(self, response):
        df.loc[self.index.pop(0), 'desc_html'] = response.xpath("/html/body/div[1]/div[2]/div[2]/div/div/main/article").get()
        
class SpiderCareer(scrapy.Spider):
    name = "Career_vacancy_spider"
    index = list()
    
    def start_requests(self):
        for index, row in career.iterrows():
            self.index.append(index)
            yield scrapy.Request(url=row['urls'], callback=self.parse)

    def parse(self, response):
        df.loc[self.index.pop(0), 'desc_html'] = response.css("div.col-xs-12.col-lg-9").get()

class SpiderHHru(scrapy.Spider):
    name = "HHru_vacancy_spider"
    index = list()
    
    def start_requests(self):
        for index, row in hh_ru.iterrows():
            self.index.append(index)
            yield scrapy.Request(url=row['urls'], callback=self.parse)

    def parse(self, response):
        df.loc[self.index.pop(0), 'desc_html'] = response.css("div.tmpl_hh_wrapper").get()

            
            

process = CrawlerProcess()
process.crawl(SpiderGeekjob)
process.crawl(SpiderProglib)
process.crawl(SpiderCareer)
process.crawl(SpiderHHru)
process.start() # the script will block here until all crawling jobs are finished
df.to_csv('tmp_urls.csv', index=False)