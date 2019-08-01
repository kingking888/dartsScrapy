import scrapy
from scrapy_splash import SplashRequest 
import sys
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
sys.path.insert(0, '/home/franticoreo/dartsWebScraper/dartsScrapy/dartsScrapy')



from items import DartsItem

class MySpider(CrawlSpider):
    name = "splashSpider"
    allowed_domains = ['www.oddsportal.com']

    # start_urls = ["https://www.oddsportal.com/darts/europe/european-championship/results/"]
    start_urls = ["https://www.oddsportal.com/site-map-active/"]

    # Rule(SgmlLinkExtractor(allow=r"page=\d+"), callback="parseTournaments_items", follow= True)
    # tournamentExtractor = LinkExtractor(allow=r"https?://www.oddsportal.com/darts/\w+-*/.*")
    # tournamentExtractor = LinkExtractor(allow=r"https?://www.oddsportal.com/darts/.*")

    # rules = [
    #     Rule(tournamentExtractor,
    #     callback="parseTournaments", follow= True)
    # ]

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield SplashRequest(url=url, callback=self.parseTournaments, args={'wait':3})



    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.getTournaments)


    def getTournaments(self, response):
        for link in response.xpath('//a[re:test(@href, "\/darts\/\w+-*\w+-*\w*\/\w+.*")]/@href'):
            url = link.get()+'/results'
            yield SplashRequest(url=response.urljoin(url), callback=self.parseTournaments, args={'wait':1.5})
                    
        # yield tournamentLinks






    def parseTournaments(self, response):
        '''
        loop through all of tournament table rows
        if class 'dark center': ignore
        if class 'center nob-border': get th element and span text to get date    
        set date
        get table rows containing class deactivate
        get game details
        repeat
        '''
        # x = LinkExtractor(allow=r"https://www.oddsportal.com/darts/*").extract_links(response)
        # print(x.extract_links)



        item = DartsItem()


        # number of table rows
        # returns a selectorlist
        tableRows = response.xpath('//table[contains(@id, "tournamentTable")]/tbody/tr')
        count = 1
        for row in tableRows:
            item['tournamentName'] = response.xpath('//h1/text()').get()
            

            if row.xpath('./self::tr[contains(@class, "dark center") or contains(@class, "table-dummyrow")]'): # contains class dark center
                continue
            # get date from table header
            if row.xpath('./self::tr[contains(@class, "center nob-border")]'):
                item['gameDate'] = row.xpath('./self::tr[contains(@class, "center nob-border")]/th/span/text()').get()
            # get game rows for date
            if row.xpath('./self::tr[contains(@class, "deactivate")]'):
                item['playersNames'] = row.xpath('normalize-space(./self::tr/td[contains(@class, "name table-participant")])').get()
                item['player1Odds'] = row.xpath('normalize-space(./self::tr/td[contains(@class, "odds-nowrp")])').get()
                item['player2Odds'] = row.xpath('normalize-space(./self::tr/td[contains(@class, "result-ok odds-nowrp")])').get()
                item['score'] = row.xpath('./self::tr/td[@class="center bold table-odds table-score"]/text()').get()
                # print(tournamentName, gameDate,playersNames,score)
                yield item

        # follow to next year of tournament 
        # find active cell and get following sibling (the preceding year on menu)
        nextPage = response.xpath('(//div[@class="main-menu2 main-menu-gray"]/ul/li[.//span[@class="active"]]/following-sibling::li//a/@href)[1]').get()
        print(nextPage)
        # if another preceding year continue Splash request / scraping
        if nextPage is not None:
            nextPage = response.urljoin(nextPage)
            yield SplashRequest(url=nextPage, callback=self.parseTournaments, args={'wait': 3})  


        
        
    