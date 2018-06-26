# -*- coding: utf-8 -*-
import scrapy
import ensembl.openxls as op
from ensembl.items  import EnsemblItem


class EnsemblspiderSpider(scrapy.Spider):
    name = 'ensemblspider'
    allowed_domains = ['http://grch37.ensembl.org/']
    # start_urls = ['http://http://grch37.ensembl.org//']
    start_urls=op.getxlsUrl()

    def parse(self, response):
        Info1=response.xpath('//div[@class="1000genomesprojectphase3_table"]').extract()[0]
        if Info1:
            InfoTable=Info1.xpath('./')
