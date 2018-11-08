from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy import Selector
from scholar_scraper.items import ScholarScraperItem
from urllib import urlopen, urlencode, unquote
from os import listdir
import re, time, urlparse

class MySpider(BaseSpider):
    name = "scholar"
    allowed_domains = ["scholar.google.com"]
    def __init__(self, filename=None):
        if filename:
            with open(filename, 'r') as f:
                queries = []
                for title in f.readlines():
                    queries.append(title.strip())
                self.start_urls = queries

    def parse(self, response):
        hxs = Selector(response)
        captcha = hxs.xpath('//div[@id="gs_captcha_c"]').extract()
        
        if len(captcha) > 0:
            item = ScholarScraperItem()
            item['title'] = 'ERROR_CAPTCHA'
            print(b'gs_captcha_c' in response.body)
            items = [item]
        else:
            # Saving html in case of errors
            try:
                cluster_url = hxs.xpath('//ul[@id="gs_lnv_ylo"]/li[1]/a/@href').extract()[0]
            except:
                #cluster_url = hxs.xpath('//ul[@id="gs_res_sb_yyl"]/li[1]/a/@href').extract()[0]
                cluster_url = hxs.xpath('//div[@class="gs_fl"]/a[3]/@href').extract()[0]
            cluster = cluster_url[cluster_url.find('cites=')+6:cluster_url.find('&scipsc=')]    
            try:
                start_page_url = hxs.xpath('//div[@id="gs_ad_md"]/a[2]/@href').extract()[0]
            except:
                start_page_url = hxs.xpath('//div[@id="gs_hdr_drw_bs"]/a[1]/@href').extract()[0]
            parsed = urlparse.urlparse(start_page_url)
            try:
                start_page = urlparse.parse_qs(parsed.query)['start'][0]
            except:
                start_page = '0'
            hits = hxs.xpath('//div[@class="gs_r"]')
            page_layout = 'old'
            if len(hits) == 0:
                page_layout = 'new'
                hits = hxs.xpath('//div[@id="gs_res_ccl_mid"]/div')
            print('There are ' + str(len(hits)) + ' results in this page.')
            items = []
            try:
                origin_url = hxs.xpath('(//li[contains(@class, "gs_bdy_sb_sel")]/a/@href)[2]').extract()[0]
            except:
                #origin_url = hxs.xpath('(//li[contains(@class, "gs_bdy_sb_sel")]/a/@href)[1]').extract()[0]
                origin_url = unquote(hxs.xpath('(//div[@id="gs_hdr_drw_bot"]/a/@href)[1]').extract()[0].replace('https://accounts.google.com/Login?hl=en&continue=',''))
            
            # Cited Cluster
            try:
                cited_cluster = hxs.xpath('//div[@id="gs_rt_hdr"]/h2/a/@href').extract()[0]
                cited_cluster = cited_cluster[cited_cluster.find("cluster=")+8:cited_cluster.find("&")]
            except:
                cited_cluster = 'NA'
            
            for hit in hits:
                item = ScholarScraperItem()          
                
                # Origin url
                item['origin_url'] = origin_url
                
                # Metadata source format
                item['meta_source_format'] = hit.xpath('div[@class="gs_ri"]/h3/span[contains(@class, "gs_ctc")]/span[1]/text()').extract()
                
                # Document title
                try:
                    raw_title = ''.join(hit.xpath('div[@class="gs_ri"]/h3/a').extract())
                    if len(raw_title) < 2:
                         raw_title = ''.join(hit.xpath('div[@class="gs_ri"]/h3')).extract()[0].replace('[CITATION][C] ','')
                         
                    item['title'] = re.sub('<[^>]*>', '', raw_title)

                    # Document title link
                    item['title_link'] = ''.join(hit.xpath('div[@class="gs_ri"]/h3/a/@href').extract())
                except:
                    raw_title = ''.join(hit.xpath('div[@class="gs_ri"]/h3').extract())
                    item['title'] = re.sub('<[^>]*>', '', raw_title)
                    item['title_link'] = ''

                # Authors, publication venue, year of publication, metadata source
                raw_authors = ''.join(hit.xpath('div[@class="gs_ri"]/div[@class="gs_a"]').extract())
                item['aut_pub_year'] = raw_authors[18:-6].replace('"', '\"')
                
                if page_layout == 'old':
                    pos_cit = '1'
                else:
                    pos_cit = '3'
                # Cited by
                fir_el_foot = ''.join(hit.xpath('div[@class="gs_ri"]/div[contains(@class, "gs_fl")]/a[{}]/@href'.format(pos_cit)).extract())
                if fir_el_foot[:14] == '/scholar?cites':
                    
                    # Cited by (count)
                    raw_cited_by = ''.join(hit.xpath('div[@class="gs_ri"]/div[contains(@class, "gs_fl")]/a[{}]/text()'.format(pos_cit)).extract())
                    item['cited_by'] = int(re.sub("\D", "", raw_cited_by))
                    
                    #Cited by (link)
                    item['cited_by_link'] =  ''.join(hit.xpath('div[@class="gs_ri"]/div[contains(@class, "gs_fl")]/a[{}]/@href'.format(pos_cit)).extract())
                else:
                    item['cited_by'] = int(0)
                    item['cited_by_link'] = ''
                    
                # Related link
                item['related_link'] = ''.join(hit.xpath('div[@class="gs_ri"]/div[contains(@class, "gs_fl")]/a[contains(@href, "/scholar?q=related")]/@href').extract())
                
                # Versions (count)
                try:
                    raw_versions = ''.join(hit.xpath('div[@class="gs_ri"]/div[contains(@class, "gs_fl")]/a[contains(@href, "/scholar?cluster=")]/text()').extract())
                    item['versions'] = int(re.sub("\D", "", raw_versions))
                except:
                    item['versions'] = ''
                
                # Versions (link)
                item['versions_link'] = ''.join(hit.xpath('div[@class="gs_ri"]/div[contains(@class, "gs_fl")]/a[contains(@href, "/scholar?cluster=")]/@href').extract())
                
                # WoS (citation count)
                raw_wos_count = hit.xpath('div[@class="gs_ri"]/div[contains(@class, "gs_fl")]/*[contains(text(), "Science")]/text()').extract()
                item['wos_cit'] = ''.join(raw_wos_count).replace('Web of Science: ','')
                
                # WoS (UT)
                try:
                    raw_wos_ut = hit.xpath('div[@class="gs_ri"]/div[contains(@class, "gs_fl")]/*[contains(text(), "Science")]/@href').extract()
                    raw_wos_ut = str(''.join(raw_wos_ut))
                    item['wos_ut'] = raw_wos_ut[raw_wos_ut.find('&UT=')+4:raw_wos_ut.find('&SrcURL=')]
                except:
                    item['wos_ut'] = ''
                
                # Full Text
                #item['ft_link'] = hit.xpath('div[contains(@class, "gs_ggs")]/div[1]/a/@href').extract()
                #item['ft_format'] = hit.xpath('div[contains(@class, "gs_ggs")]/div[1]/a/span[2]/text()').extract()
                item['ft_link'] = hit.xpath('div[contains(@class, "gs_ggs")]/div[1]/div[1]/a/@href').extract()
                item['ft_format'] = hit.xpath('div[contains(@class, "gs_ggs")]/div[1]/div[1]/a/span[1]/text()').extract()              
                    
                item['cited_cluster'] = cited_cluster
                item['start_page'] = start_page
                
                items.append(item)
        return items
