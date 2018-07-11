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
    global rsidInfos
    rsidInfos =op.getxlsUrl()

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
        # Info1=response.xpath('//h2[contains(text(),"1000 Genomes Project Phase 3 allele frequencies")]').extract()[0]

        Info2 = response.xpath('normalize-space(//span[@style="font-weight:bold;font-size:1.2em"])')
        alleles = Info2.extract()[0].split('/')
        rsid=response.xpath('normalize-space(//h1[@class="summary-heading"])').extract()[0].strip(" SNP")
        r_allele1=self.find_risk_allele(rsid,rsidInfos)
        r_allele2=self.allele_reverse(r_allele1)
        n_alleles=[ ]
        nn_genotype=[ ]
        rn_genotype=[ ]
        riskAllele =""


        if r_allele1 in alleles:
            riskAllele=r_allele1
            alleles.remove(riskAllele)
            n_alleles.extend(alleles)
        elif r_allele2 in alleles:
            riskAllele=r_allele2
            alleles.remove(riskAllele)
            n_alleles.extend(alleles)
        else:
            print("risk alleles not in web")

        for n in n_alleles:
            nn_genotype.append(n+"|"+n)
            rn_genotype.append(n+"|"+riskAllele)
            rn_genotype.append(riskAllele+"|"+n)




        driver=webdriver.PhantomJS(executable_path='C:/Users/Wei/Downloads/phantomjs-2.1.1-windows/bin/phantomjs.exe')
        driver.get(response.url+'#1000genomesprojectphase3_table')
        htmls = driver.page_source.replace("\n","").replace("\r","")
        #alleles_ensembl=re.search()

        pattern = re.compile('<span class="_ht ht"><b>AMR</b></span>(.*?)<span class="open">Hide</span>')
        Info1=pattern.search(htmls).group(1)
        riskf= self.findText(Info1,riskAllele+"|"+riskAllele,"</div>").replace("</b>","")





        if Info1:
            print(Info1)
        pass



    def findText(self,htmls,startText,endText):
        pattern=re.compile(startText+"(.*?)"+endText)
        return pattern.search(htmls)

    def allele_reverse(self,allele):
        if allele=="C":
            allele="G"
        elif allele=="G":
            allele="C"
        elif allele=="A":
            allele="T"
        elif allele=="T":
            allele="A"

        return allele

    def find_risk_allele(self,rsid,rsidInfos):
        for x in rsidInfos:
            try:
                if x.rsid==rsid:
                    return x.riskA
            except:
                print(rsid+"not find")