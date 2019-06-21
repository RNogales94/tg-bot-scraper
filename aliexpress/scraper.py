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

        local_cookie = {'name': 'aep_usuc_f',
                        'value': 'site=glo&province=919986676578000000&city=919986676578011000&c_tp=EUR&region=ES&b_locale=en_US'}


        self.driver.get(url)
        self.driver.add_cookie({'name': local_cookie['name'],
                                'value': local_cookie['value'],
                                'domain': 'aliexpress.com'
                                })

        # source_html = self.driver.page_source
        # self.soup = BeautifulSoup(source_html, "html.parser")

        if self.__error_captcha():
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
    def __error_captcha():
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
        if price is None:
            return None
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


