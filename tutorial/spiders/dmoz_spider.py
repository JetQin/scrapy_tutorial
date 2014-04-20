from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys

class DmozSpider(CrawlSpider):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    name="dmoz"
    
    # allowed_domains=["dygod.net"]
    # start_urls=["http://dygod.net"]

    # rules = (
    #     Rule(SgmlLinkExtractor(allow=[r'dygod\.net/\w+']), callback='parse_site',follow=True),
    #     Rule(SgmlLinkExtractor(allow=[r'dygod\.net/html/gndy/dyzz\w+']), callback='parse_site',follow=True),)
    #     # r'\d{4}/\d{2}/\w+' : regular expression for http://isbullsh.it/YYYY/MM/title URLs
    
    allowed_domains=["upstream.hkbici.com"]
    start_urls=["http://upstream.hkbici.com"]

    rules = (
        Rule(SgmlLinkExtractor(allow=[r'upstream\.hkbici\.com//\w+']), callback='parse_site',follow=True),
        Rule(SgmlLinkExtractor(allow=[r'upstream\.hkbici\.com//thread\w+']), callback='parse_site',follow=True),)
        # r'\d{4}/\d{2}/\w+' : regular expression for http://isbullsh.it/YYYY/MM/title URLs


    def parse_site(self, response):
        # soup = BeautifulSoup(response)
        # print(soup.prettify())
         sel = Selector(response)
         # sites = sel.css('a[href*=ftp]::attr(href)').extract()
         sel = sel.xpath("//html").extract()

         soup = BeautifulSoup(str(sel))

         # for link in soup.find_all('p'):
            # if u'\u25ce\u7b80\u3000\u3000\u4ecb' in link:
               # print link.string
         linkurl=""
         for link in soup.find_all('a'):
            if "ftp" in link.get("href"):
               linkurl = link.get("href").decode("unicode_escape")

        # print(soup.prettify())
        # print sites
         title = soup.title.string.decode("unicode_escape")
         img = soup.img['src'].decode("unicode_escape")

         db = MongoClient().upstream
         db.upstream.insert({"title":title,"link":linkurl,"desc":img,"img":img})

        # for site in sites:
            
        #     link = site
        #     index = str(link).rfind("/")
        #     title = link[index+1:len(link)]
        #     desc = title

        #     print title, link, desc
        #     if link!="" and title!="" and desc!="":
        #         print "insert mongo"
                