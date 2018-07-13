# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class RaceItem(object):
    def __init__(self,rsid,riskA,rf,nf,rrf,nnf,rnf):
        self.rf=rf
        self.nf=nf
        self.rrf=rrf
        self.nnf=nnf
        self.rnf=rnf
        self.rsid=rsid
        self.riskA=riskA


class EnsemblItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    rsid=scrapy.Field()
    risk_allele=scrapy.Field()
    r_cdx=scrapy.Field()
    rr_cdx=scrapy.Field()
    nn_cdx=scrapy.Field()
    rn_cdx=scrapy.Field()
    r_chb=scrapy.Field()
    rr_chb=scrapy.Field()
    nn_chb=scrapy.Field()
    rn_chb=scrapy.Field()
    r_chs =scrapy.Field()
    rr_chs =scrapy.Field()
    nn_chs =scrapy.Field()
    rn_chs =scrapy.Field()
    r_eas =scrapy.Field()
    rr_eas =scrapy.Field()
    nn_eas =scrapy.Field()
    rn_eas =scrapy.Field()



