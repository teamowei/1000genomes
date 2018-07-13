# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook,load_workbook
import os

class EnsemblPipeline(object):

    def open_spider(self,spider):
        self.wb=Workbook()
        self.ws=self.wb.active
        self.ws.append(['rsid', 'riskAllele','f_r_cdx','f_rr_cdx','f_nn_cdx','f_rn_cdx','f_r_chb','f_rr_chb',	'f_nn_chb','f_rn_chb','f_r_chs','f_rr_chs','f_nn_chs',	'f_rn_chs','f_r_eas','f_rr_eas','f_nn_eas','f_rn_eas'])

    def process_item(self, item, spider):
        line = [item['rsid'], item['r_cdx'],item['rr_cdx'],item['nn_cdx'],item['rn_cdx'],item['r_chb'],item['rr_chb'],item['nn_chb'],item['rn_chb'],item['r_chs'],item['rr_chs'],item['nn_chs'],item['rn_chs'],item['r_eas'],item['rr_eas'],item['nn_eas'],item['rn_eas'] ]
        self.ws.append(line)
        return item

    def close_spider(self, spider):
        save_file=os.getcwd()+"\\result.xlsx"
        print('done')
        self.wb.save(save_file)
