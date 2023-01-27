# first-scraper-project

* This script uses Selenium and BeautifulSoup to scrape item title, price and description  from a website, you can choose website from (varle.lt, skelbiu.lt, ebay), and saves the remaining item info to a CSV file.

* The script count how much page we need then use website search field and collect all possible URL from that page.

* When all items URL is in list, the script navigates to a given URL and scrape item information

## How to use it

Open terminal

* Run python: 
    poetry run python
* import scraper:
    from scraper import Scraper
* define:
    scraper = Scraper()
* run scraper:
    scraper.scrape((write how much item you need(int)),(write item keyword(str)), (choose website))

    example:
    scraper.scrape(200, "graphic card", ["ebay"])


As soon as the code is launched, the scraper will scrape the items and create a new file called ebay_tmp.csv(only now just this name) that contains your scraped item information.