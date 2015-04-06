#!/usr/bin/env
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from achd.items import AchdItem
import re
from itertools import chain

class AchdSpider(BaseSpider):

    name = 'achdspider'
    allowed_domains = ['http://webapps.achd.net/Restaurant/']
    base_url = 'http://webapps.achd.net/Restaurant/RestaurantDetail.aspx?ID='
    
    with open("../r_id.txt", "r+") as rids:
        r_read = rids.read()
        
    start_urls = [base_url+'''{r_id}'''.format(r_id=str(x)) for x in r_read.split("\n")]

    


    #rules = [Rule(SgmlLinkExtractor(allow=['/tor/\d+']), 'parse_torrent')]

    def parse(self, response):
        x = HtmlXPathSelector(response)
        

        def idstringfind(pattern, string):
            idstring = list()
            idtext = string
            pat_compile = re.compile(pattern)
            idstring = pat_compile.findall(idtext)
            return idstring

        re_pat = '''RestaurantDetail\.aspx\?ID=(?P<rest_id>[0-9]{4,})'''
        inspect_pat = "ENCOUNTER=([0-9]{4,})"
        
        r_url = idstringfind(re_pat, response.url)

        #Identifers: Name, Address, Contact, Phone
        items = []
        torrent = AchdItem()
        torrent['r_id'] = r_url
        torrent['name'] = x.select('//span[@id="ctl00_ContentPlaceHolder1_RDetail1_lblName"]/text()').extract()
        torrent['address'] = x.select('//span[@id="ctl00_ContentPlaceHolder1_RDetail1_lblStreet"]/text()').extract()
        torrent['contact'] = x.select('//span[@id="ctl00_ContentPlaceHolder1_RDetail1_lblContact"]/text()').extract()
        torrent['phone'] = x.select('//span[@id="ctl00_ContentPlaceHolder1_RDetail1_lblPhone"]/text()').extract()

        #inspection table
        #for each <tr> in the table, extract the <td>  
        inspect = x.select('//table[@id="ctl00_ContentPlaceHolder1_RDetail1_gvInspection"]/descendant::tr')
        visits = []
        #for record in inspect.select('td'):
        #    torrent['r_date'] = record
        #    torrent['r_type'] = record
        #    torrent['r_encounter'] = set(record.select('a/@href').extract())
        #    visits.append(record.select('//a/@href'))
        inspect_td = set(x.select('//a/@href').extract())
        ch = chain.from_iterable(inspect_td)
        inspect_map = [idstringfind(inspect_pat,x) for x in inspect_td]

        torrent['inspect'] = inspect_map
        items.append(torrent)

        return items

        #http://stackoverflow.com/questions/406121/flattening-a-shallow-list-in-python
        #[idstringfind(inspect_pat, x) for x in set(x.select('//a/@href').extract())]