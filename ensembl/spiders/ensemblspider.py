# -*- coding: utf-8 -*-
import scrapy
import re
import ensembl.openxls as op
from selenium import webdriver
from ensembl.items  import EnsemblItem


class EnsemblspiderSpider(scrapy.Spider):
    name = 'ensemblspider'
    allowed_domains = ['http://grch37.ensembl.org/']
    # start_urls = ['http://http://grch37.ensembl.org//']
    rsidInfos=op.getxlsUrl()

    start_urls=[]
    for x in rsidInfos:
        start_url=x.rsidUrl
        start_urls.append(start_url)

    def parse(self, response):
        # wholepages=response.xpath('//html').extract()[0]
        # rsid_Info= response.xpath('//div[@id="ensembl_panel_2"]').extract()[0]
        # rsid_name=rsid_Info.xpath('./h1[@class="summary-heading"]/text()').extract()[0]
        # rsid_alleles=rsid_Info.xpath('./div[@style="font-weight:bold;font-size:1.2em"]/text()').extract()[0]
        # Info1=response.xpath('//div[@class="1000genomesprojectphase3_table"]').extract()[0]
        # if Info1:
        #
        #     InfoTable=Info1.xpath('./')
        # pass
        driver=webdriver.PhantomJS(executable_path='C:/Users/Wei/Downloads/phantomjs-2.1.1-windows/bin/phantomjs.exe')
        driver.get(response.url)
        htmls = driver.page_source
        a=driver.page_source
