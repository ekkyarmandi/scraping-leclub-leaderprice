# Scraping LeClub LeaderPrice

Scraping script for scraping product data from [LeClub Leader Price](leclubleaderprice.fr) using scrapy.

### Set up
First make sure scrapy have been installed on your local machine. You can use command line below to install all the module from this project.
```terminal
pipi install -r requirements.txt
```
Second you can specify the collections url you want to crawl by looking into [leclub.py](spiders/leclub.py)

### How to run
Run the `leclub` crawler for collecting the product name and it's url by typing crawl command line below.
```terminal
scrapy crawl leclub
```
And run `products` crawler for collecting product details.
```
scrapy crawl products
```

You also can add "-o" \<filename> output parameter on the crawl command line to have the output.