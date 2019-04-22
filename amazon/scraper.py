from bs4 import BeautifulSoup

import re
from scraper.selenium_web_driver import SeleniumChromeDriver
from selenium.common.exceptions import NoSuchElementException


def captureURLs(text):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    return urls


class AmazonScraper:
    def __init__(self, url):
        print(f'Scrapeando {url}')

        self.fully_scraped = True
        self.url = url
        self.title = None
        self.description = None
        self.features = None
        self.end_date = None
        self.size = None
        self.old_price = None
        self.price = None
        self.image_url = None
        self.is_captcha = None

        self.driver = SeleniumChromeDriver().driver
        self.driver.get(url)

        source_html = self.driver.page_source
        self.soup = BeautifulSoup(source_html, "html.parser")

        # Scrape properties
        print(self.soup)

        if self.soup.title.text == 'Amazon CAPTCHA':
            self.is_captcha = True

        else:
            self.is_captcha = False
            self.__scrape_price()
            self.__scrape_description()
            self.__scrape_features()
            self.__scrape_old_price(self.soup)
            self.__scrape_title(self.soup)
            self.__scrape_size(self.soup)
            self.__scrape_img_url(self.soup)
            self.__scrape_end_date(self.soup)

        print('[Scraper Info] Done')

    def __scrape_description(self):
        try:
            self.description = self.driver.find_element_by_id('productDescription').find_element_by_css_selector('p').text
        except NoSuchElementException:
            print('[Scraper Error] Description in --> ' + self.url)

    def __scrape_features(self):
        try:
            self.features = self.driver.find_element_by_id('feature-bullets').text
        except NoSuchElementException:
            print('[Scraper Error] Features in --> ' + self.url)

    def __scrape_price(self):
        soup = self.soup
        try:
            self.price = str.strip(soup.find(id='priceblock_dealprice').contents[0])
        except:
            try:
                self.price = str.strip(soup.find(id='priceblock_ourprice').contents[0])
            except:
                try:
                    self.price = str.strip(soup.find_all('span', {'class': 'a-size-medium a-color-price'})[0].contents[0])
                except:
                    try:
                        self.price = str.strip(soup.find('span', {'class': 'a-size-medium a-color-price offer-price a-text-normal'})[0].contents[0])
                    except Exception as e:
                        print('[Scraper Error] Price in --> ' + self.url)
                        self.fully_scraped = False

    def __scrape_old_price(self, soup):
        try:
            self.old_price = str.strip(soup.find_all('span', {'class': 'a-text-strike'})[0].contents[0])
        except Exception as e:
            print('[Scraper Warning] Old price')

    def __scrape_title(self, soup):
        try:
            self.title = str.strip(soup.find(id='productTitle').contents[0])
        except Exception as e:
            print('[Scraper Error] Title in --> ' + self.url)
            self.fully_scraped = False

    def __scrape_size(self, soup):
        try:
            self.size = str.strip(soup.find(id='variation_size_name').find('option', selected=True).contents[0])
        except Exception as e:
            print('[Scraper Info] No sizes in --> ' + self.url)

    def __scrape_img_url(self, soup):
        try:
            self.image_url = str.strip(soup.find(id='imgTagWrapperId').findChild('img')['data-old-hires'])
            if self.image_url == '':
                self.image_url = str.strip(soup.find(id='imgTagWrapperId').findChild('img')['src'])
                if self.image_url.startswith('data:image/jpeg;base64'):
                    text = soup.find(id='imgTagWrapperId').findChild('img')['data-a-dynamic-image']
                    self.image_url = captureURLs(text)[0]

        except Exception as e:
            try:
                images = str.strip(soup.find(id='imgBlkFront')['data-a-dynamic-image'])
                urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', images)
                self.image_url = urls[-1]
            except Exception as e:
                print('[Scraper Error] Main image in --> ' + self.url)
                self.fully_scraped = False

    def __scrape_end_date(self, soup):
        try:
            self.end_date = str.strip(soup.find(id=lambda x: x and x.startswith('deal_expiry_timer_')).contents[0])
        except Exception as e:
            print('[Scraper Info] No Temporal in --> ' + self.url)

    def is_well_scraped(self):
        return self.fully_scraped

    def has_old_price(self):
        return self.old_price is not None

    def to_dict(self):
        response = {
                'short_description': self.title,
                'description': self.description,
                'features': self.features,
                'standard_price': self.old_price,
                'end_date': self.end_date,
                'price': self.price,
                'url': self.url,
                'image_url': self.image_url,
                'size': self.size
             }
        return response


