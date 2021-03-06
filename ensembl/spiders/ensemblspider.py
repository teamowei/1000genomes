# -*- coding: utf-8 -*-
import scrapy
import re
import operator
import traceback
import time
import ensembl.openxls as op
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
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
        try:
            Info2 = response.xpath('normalize-space(//span[@style="font-family:Courier,monospace;white-space:nowrap;margin-left:5px;padding:2px 4px;background-color:#F6F6F6"])')
            baseInfo = Info2.extract()[0].split('\xa0\xa0')
            rsid=baseInfo[2]
            ref_alleles= baseInfo[3].split(',')
            ALT_alleles=baseInfo[4].split(",")
            r_allele1=self.find_risk_allele(rsid,rsidInfos)
            n_alleles = []
            nn_genotype = []
            rn_genotype = []
            rr_genotype = []
            riskAllele = []
            races_name = ['EAS', 'CDX', 'CHB', 'CHS']
            race_freq_dic = {}
            riskf, rn_fre, nn_fre, r_fre, n_fre = 0, 0, 0, 0, 0
            if r_allele1:
                r_allele2 = self.allele_reverse(r_allele1)
                if r_allele1 in ref_alleles and r_allele2 in ref_alleles:
                    riskAllele.append(ref_alleles)
                    n_alleles.extend(ALT_alleles)
                elif r_allele1 in ALT_alleles and r_allele2 in ALT_alleles:
                    riskAllele.extend(ALT_alleles)
                    n_alleles.extend(ref_alleles)
                elif r_allele1 in ref_alleles:
                    riskAllele.append(r_allele1)
                    n_alleles.extend(ALT_alleles)
                elif r_allele2 in ref_alleles and r_allele1 not in ALT_alleles and r_allele1 not in ref_alleles:
                    riskAllele.append(r_allele2)
                    n_alleles.extend(ALT_alleles)
                elif r_allele1 in ALT_alleles:
                    riskAllele.append(r_allele1)
                    ALT_alleles.remove(r_allele1)
                    n_alleles.extend(ref_alleles)
                    n_alleles.extend(ALT_alleles)
                elif r_allele2 in ref_alleles:
                    riskAllele.append(r_allele2)
                    n_alleles.extend(ALT_alleles)
                elif r_allele2 in ALT_alleles:
                    riskAllele.append(r_allele2)
                    ALT_alleles.remove(r_allele2)
                    n_alleles.extend(ref_alleles)
                    n_alleles.extend(ALT_alleles)
                else:
                    print(rsid+" risk alleles not in web")


                for n in n_alleles:
                    for p in riskAllele:
                        nn_genotype.append(n+"\|"+n)
                        rn_genotype.append(n+"\|"+p)
                        rn_genotype.append(p+"\|"+n)
                        rr_genotype.append(p+"\|"+p)

                nn_genotype=list(set(nn_genotype))
                rn_genotype=list(set(rn_genotype))
                rr_genotype=list(set(rr_genotype))

                dcap = dict(DesiredCapabilities.PHANTOMJS)
                dcap["phantomjs.page.settings.userAgent"] = (
                    "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
                )
                driver=webdriver.PhantomJS(executable_path='C:/Users/Wei/Downloads/phantomjs-2.1.1-windows/bin/phantomjs.exe',desired_capabilities=dcap)
                driver.get(response.url+'#1000genomesprojectphase3_table')
                time.sleep(1)
                js = "var q=document.documentElement.scrollTop=10000"
                driver.execute_script(js)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
                time.sleep(3)
                htmls = driver.page_source.replace("\n","").replace("\r","")
                endText_freq="\\(.*?\\) </div>"

                for r in races_name:

                    r_pattern='<span class="_ht ht"><b>'+r+'</b></span>(.*?)<span class="open">Hide</span>'

                    startText_genotype = "</b>:"
                    startText_allele = "</span></b>:"
                    pattern = re.compile(r_pattern)
                    result=pattern.search(htmls)


                    if result:
                        Info1=result.group(1)

                        # riskFreqText=self.findText(Info1, r1 + "\|" + r1 + "</b>:", endText_freq)
                        # riskf= riskFreqText.group(1).strip() if riskFreqText is not None else 0
                        riskf=self.max_allele_frequence(Info1,rr_genotype,startText_genotype,endText_freq)
                        rn_fre=self.max_allele_frequence(Info1,rn_genotype,startText_genotype,endText_freq)
                        nn_fre = self.max_allele_frequence(Info1, nn_genotype,startText_genotype,endText_freq)
                        r_fre = self.max_allele_frequence(Info1,riskAllele,"</span></b>:",endText_freq)
                        #r_fre = r_FreqText.group(1).strip() if r_FreqText is not None else 0
                        n_fre=self.max_allele_frequence(Info1,n_alleles,"</span></b>:",endText_freq)
                    race_freq = RaceItem(rsid,r_allele1,r_fre,n_fre,riskf,nn_fre,rn_fre)
                    race_freq_dic[r]=race_freq
            else :
                for r in races_name:
                    race_freq = RaceItem(rsid, "", r_fre, n_fre, riskf, nn_fre, rn_fre)
                    race_freq_dic[r] = race_freq


            item=EnsemblItem()
            item['rsid']=rsid
            item['risk_allele']=r_allele1

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
        #except Exception as e:
        except:
            #print(e)
            traceback.print_exc()
            print(rsid + "is wrong")



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
            else:
                allele_frequences.append(0)

        return max(allele_frequences)



