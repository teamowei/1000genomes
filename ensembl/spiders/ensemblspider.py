# -*- coding: utf-8 -*-
import scrapy
import re
import ensembl.openxls as op
from selenium import webdriver
from ensembl.items  import EnsemblItem,RaceItem


class EnsemblspiderSpider(scrapy.Spider):
    name = 'ensemblspider'
    allowed_domains = ['http://grch37.ensembl.org/']
    # start_urls = ['http://http://grch37.ensembl.org//']
    global rsidInfos
    rsidInfos =op.getxlsUrl()

    start_urls=[]
    for x in rsidInfos:
        if x:
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
            nn_genotype.append(n+"\|"+n)
            rn_genotype.append(n+"\|"+riskAllele)
            rn_genotype.append(riskAllele+"\|"+n)




        driver=webdriver.PhantomJS(executable_path='C:/Users/Wei/Downloads/phantomjs-2.1.1-windows/bin/phantomjs.exe')
        driver.get(response.url+'#1000genomesprojectphase3_table')
        htmls = driver.page_source.replace("\n","").replace("\r","")
        endText_freq="\\(.*?\\) </div>"
        races_name=['EAS','CDX','CHB','CHS']
        #race_freqs=[]
        race_freq_dic={}
        for r in races_name:

            r_pattern='<span class="_ht ht"><b>'+r+'</b></span>(.*?)<span class="open">Hide</span>'

            startText_genotype = "</b>:"
            startText_allele = "</span></b>:"
            pattern = re.compile(r_pattern)
            Info1=pattern.search(htmls).group(1)
            riskf= self.findText(Info1,riskAllele+"\|"+riskAllele+"</b>:",endText_freq).group(1).strip()
            rn_fre=self.max_allele_frequence(Info1,rn_genotype,startText_genotype,endText_freq)
            nn_fre = self.max_allele_frequence(Info1, nn_genotype,startText_genotype,endText_freq)
            r_fre=self.findText(Info1,riskAllele+"</span></b>:",endText_freq).group(1).strip()
            n_fre=self.max_allele_frequence(Info1,n_alleles,startText_allele,endText_freq)
            race_freq = RaceItem(rsid,r_allele1,r_fre,n_fre,riskf,nn_fre,rn_fre)
            #race_freqs.append(race_freq)
            race_freq_dic[r]=race_freq

        item=EnsemblItem()
        item['rsid']=rsid
        item['risk_allele']=riskAllele

        item['r_cdx']=race_freq_dic['CDX'].rf
        item['rr_cdx']=race_freq_dic['CDX'].rrf
        item['nn_cdx']=race_freq_dic['CDX'].nnf
        item['rn_cdx']=race_freq_dic['CDX'].rnf
        item['r_chb']=race_freq_dic['CHB'].rf
        item['rr_chb']=race_freq_dic['CHB'].rrf
        item['nn_chb']=race_freq_dic['CHB'].nnf
        item['rn_chb']=race_freq_dic['CHB'].rnf
        item['r_chs'] =race_freq_dic['CHS'].rf
        item['rr_chs'] =race_freq_dic['CHS'].rrf
        item['nn_chs'] =race_freq_dic['CHS'].nnf
        item['rn_chs'] =race_freq_dic['CHS'].rnf
        item['r_eas'] =race_freq_dic['EAS'].rf
        item['rr_eas'] =race_freq_dic['EAS'].rrf
        item['nn_eas'] =race_freq_dic['EAS'].nnf
        item['rn_eas'] =race_freq_dic['EAS'].rnf


        # if Info1:
        #     print(Info1)
        # pass
        yield item



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

    def max_allele_frequence(self,html,genotypeList,startText_type,endText):
        allele_frequences=[]
        for g in genotypeList:
            startText=g+startText_type
            frequence=self.findText(html,startText,endText)
            if frequence:
                allele_frequences.append(float(frequence.group(1).strip()))

        return max(allele_frequences)



