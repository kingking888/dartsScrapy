# dartsScrapy
###### A Scrapy project that scrapes Professional Darts data

In order to scrape oddsportal.com Scrapy will utilise the [splash-plugin](https://github.com/scrapy-plugins/scrapy-splash)
to wait for javascript to render the data. In order for Splash requests to work you will need to run them in a [docker](https://docs.docker.com/get-started/)
container.

1. Run the docker container: ```$ docker run -p 8050:8050 scrapinghub/splash```

2. Open seperate terminal, navigate to the **first** *dartsScrapy* folder, run ```$ scrapy crawl splashSpider```



