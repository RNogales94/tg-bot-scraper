from bs4 import BeautifulSoup

from selenium.common.exceptions import NoSuchElementException
from scraper.selenium_web_driver import SeleniumChromeDriver

from utils.web_utils import expand_url


class AliexpressScraper:
    def __init__(self, url):
        print(f'Scrapeando {url}')
        url = expand_url(url)

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

        if self.__error_captcha(self.soup):
            self.is_captcha = True
            self.fully_scraped = False

        else:
            self.is_captcha = False
            self.title = self.__scrape_title()
            self.price = self.__scrape_price()
            self.price = self.__format_price(self.price)
            self.old_price = self.__scrape_old_price()
            self.old_price = self.__format_price(self.old_price)
            self.image_url = self.__scrape_img_url()

            self.description = self.__scrape_description()
            self.features = self.__scrape_features()
            self.size = self.__scrape_size()
            self.end_date = self.__scrape_end_date()

            if self.title is not None and self.price is not None and self.image_url is not None:
                self.fully_scraped = True


    @staticmethod
    def __error_captcha(soup):
        return False

    def __scrape_title(self):
        try:
            title = self.driver.find_element_by_class_name('product-title').text
        except NoSuchElementException:
            try:
                title = self.driver.find_element_by_class_name('product-name').text
            except NoSuchElementException:
                print('[Scraper Error] Title in --> ' + self.url)
                title = None

        return title

    def __scrape_price(self):
        try:
            price = self.driver.find_element_by_class_name('product-price-current').find_element_by_class_name('product-price-value').text
        except NoSuchElementException:
            try:
                price = self.driver.find_element_by_class_name('p-price-content').text
            except NoSuchElementException:
                print('[Scraper Error] Price in --> ' + self.url)
                price = None

        return price

    def __scrape_old_price(self):
        try:
            old_price = self.driver.find_element_by_class_name('product-price-original').find_element_by_class_name('product-price-value').text
        except NoSuchElementException:
            try:
                old_price = self.driver.find_element_by_class_name('p-del-price-content').text
            except NoSuchElementException:
                print('[Scraper Error] Old Price in --> ' + self.url)
                old_price = None

        return old_price

    @staticmethod
    def __format_price(price):
        print(price)
        if len(price.split()) == 2:
            currency, amount = price.split()
        elif len(price.split()) == 4:
            currency, amount, _, _ = price.split()
        else:
            print(f'Price Format Error {price}')
            return None
        amount.replace(',', '.')
        price = amount + currency
        return price

    def __scrape_description(self):
        return None

    def __scrape_features(self):
        return None

    def __scrape_size(self):
        return None

    def __scrape_end_date(self):
        return None

    def __scrape_img_url(self):
        try:
            father = self.driver.find_element_by_class_name('image-viewer')
            img_url = father.find_element_by_class_name('magnifier-image').get_attribute('src')
        except NoSuchElementException:
            try:
                father = self.driver.find_element_by_class_name('ui-image-viewer')
                img_url = father.find_element_by_tag_name('img').get_attribute('src')
            except NoSuchElementException:
                img_url = None
        return img_url

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






# urls = [
# 'http://s.click.aliexpress.com/e/cmKQ0LEo',
# 'http://s.click.aliexpress.com/e/b4dj7tZA',
# 'http://s.click.aliexpress.com/e/bSNeQdbK',
# 'http://s.click.aliexpress.com/e/cODenJTK',
# 'http://s.click.aliexpress.com/e/fo3wXms',
# 'http://s.click.aliexpress.com/e/ff3wCU0',
# 'http://s.click.aliexpress.com/e/IptPVuM',
# 'http://s.click.aliexpress.com/e/bKU0YC0s',
# 'http://s.click.aliexpress.com/e/e0tM9Gy',
# 'http://s.click.aliexpress.com/e/NK8ProG',
# 'http://s.click.aliexpress.com/e/bCCZGVI0',
# 'http://s.click.aliexpress.com/e/TbQAfrK',
# 'http://s.click.aliexpress.com/e/cmKQ0LEo',
# 'http://s.click.aliexpress.com/e/cdcN96Y',
# 'http://s.click.aliexpress.com/e/bALHPYFq',
# 'http://s.click.aliexpress.com/e/bSYmNaFA',
# 'http://s.click.aliexpress.com/e/b8a71yYo',
# 'http://s.click.aliexpress.com/e/i7yUpLE',
# 'http://s.click.aliexpress.com/e/c3Ad6Blq',
# 'http://s.click.aliexpress.com/e/Yzt0YjA',
# 'http://s.click.aliexpress.com/e/SBhzjyy',
# 'http://s.click.aliexpress.com/e/bypOmruM',
# 'http://s.click.aliexpress.com/e/b5H42QBq',
# 'http://s.click.aliexpress.com/e/nkaA3rE',
# 'http://s.click.aliexpress.com/e/bAMSokla',
# 'http://s.click.aliexpress.com/e/gREJ2ne',
# 'http://s.click.aliexpress.com/e/c47PIFxS',
# 'http://s.click.aliexpress.com/e/ckrkSLBE',
# 'http://s.click.aliexpress.com/e/cfu1GiaG',
# 'http://s.click.aliexpress.com/e/ihX7NHW',
# 'http://s.click.aliexpress.com/e/bzHIKg0',
# 'http://s.click.aliexpress.com/e/fYWI86M',
# 'http://s.click.aliexpress.com/e/bBuI2d9O',
# 'http://s.click.aliexpress.com/e/cWBBzVnK',
# 'http://s.click.aliexpress.com/e/bEUwmKPO',
# 'http://s.click.aliexpress.com/e/b1mo3doM',
# 'http://s.click.aliexpress.com/e/24tkFTS',
# 'http://s.click.aliexpress.com/e/c3whEN0c',
# 'http://s.click.aliexpress.com/e/cdcN96Y',
# 'http://s.click.aliexpress.com/e/bALHPYFq',
# 'http://s.click.aliexpress.com/e/bSYmNaFA',
# 'http://s.click.aliexpress.com/e/b8a71yYo',
# 'http://s.click.aliexpress.com/e/i7yUpLE',
# 'http://s.click.aliexpress.com/e/biLR0IAk',
# 'http://s.click.aliexpress.com/e/c3Ad6Blq',
# 'http://s.click.aliexpress.com/e/Yzt0YjA',
# 'http://s.click.aliexpress.com/e/cC5LBGSG',
# 'http://s.click.aliexpress.com/e/SBhzjyy',
# 'http://s.click.aliexpress.com/e/b5H42QBq',
# 'http://s.click.aliexpress.com/e/cNKj8U0u',
# 'http://s.click.aliexpress.com/e/nkaA3rE',
# 'http://s.click.aliexpress.com/e/b1ZNqSyC',
# 'http://s.click.aliexpress.com/e/bAMSokla',
# 'http://s.click.aliexpress.com/e/gREJ2ne',
# 'http://s.click.aliexpress.com/e/ckrkSLBE',
# 'http://s.click.aliexpress.com/e/cfu1GiaG',
# 'http://s.click.aliexpress.com/e/ihX7NHW',
# 'http://s.click.aliexpress.com/e/bzHIKg0',
# 'http://s.click.aliexpress.com/e/fYWI86M',
# 'http://s.click.aliexpress.com/e/clYB9Ay0',
# 'http://s.click.aliexpress.com/e/bBuI2d9O',
# 'http://s.click.aliexpress.com/e/FgLs5n2',
# 'http://s.click.aliexpress.com/e/b3Tju7yU'
# ]
#
# from aliexpress.scraper import AliexpressScraper
# url = 'http://s.click.aliexpress.com/e/cmTHqhA0'
#
# def scrape(url):
#     scr = AliexpressScraper(url)
#     if not scr.is_well_scraped():
#         print(f'CHECK IT {url}')
#     scr = scr.to_dict()
#     print(scr)
#     return scr
#
# for url in urls:
# scrape(url)

# url = 'http://s.click.aliexpress.com/e/cdcN96Y'
# # url = ' http://s.click.aliexpress.com/e/cmTHqhA0'
# url = expand_url(url)
# print(url)
# p = start(url)
# print(p)
