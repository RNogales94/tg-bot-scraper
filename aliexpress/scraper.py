import os
from selenium.common.exceptions import NoSuchElementException
from scraper.selenium_web_driver import SeleniumChromeDriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.url_utils import expand_url


class AliexpressScraper:
    def __init__(self):

        self.driver = SeleniumChromeDriver().driver
        self.api_key = None  # os.environ.get('SCRAPEAPI_KEY', 'adfe255be6ddb5488a7fcef4bde677c6')

        # Define Properties to scrape
        self.__reset_scraper()

    def __reset_scraper(self):
        self.fully_scraped = True
        self.url = None
        self.title = None
        self.description = None
        self.features = None
        self.end_date = None
        self.size = None
        self.old_price = None
        self.price = None
        self.coupon_code = None
        self.coupon_discount = None
        self.coupon_price = None
        self.image_url = None
        self.is_captcha = None
        self.driver.delete_all_cookies()

    def scrape(self, url):
        self.__reset_scraper()
        self.url = expand_url(url)

        if self.api_key is None:
            self.driver.get(self.url)
        else:
            url = f'http://api.scraperapi.com/?api_key={self.api_key}&url={self.url}'
            self.driver.get(url)

        print(f'###########################\n[Scraper] {self.driver.title}\n##############################')

        if self.__is_captcha():
            self.is_captcha = True

        else:
            self.is_captcha = False
            self.__get_properties()

        response = {
            'short_description': self.title,
            'description': self.description,
            'features': self.features,
            'standard_price': self.old_price,
            'end_date': self.end_date,
            'price': self.price,
            'coupon_code': self.coupon_code,
            'coupon_discount': self.coupon_discount,
            'coupon_price': self.coupon_price,
            'url': self.url,
            'image_url': self.image_url,
            'size': self.size,
            'is_captcha': self.is_captcha,
        }

        print('[Scraper Info] Done')

        return response


        # if self.__error_captcha():
        #     self.is_captcha = True
        #     self.fully_scraped = False
        #
        # else:
        #     self.is_captcha = False
        #     self.title = self.__scrape_title()
        #     self.price = self.__scrape_price()
        #     self.price = self.__format_price(self.price)
        #     self.old_price = self.__scrape_old_price()
        #     self.old_price = self.__format_price(self.old_price)
        #     self.image_url = self.__scrape_img_url()
        #
        #     self.description = self.__scrape_description()
        #     self.features = self.__scrape_features()
        #     self.size = self.__scrape_size()
        #     self.end_date = self.__scrape_end_date()
        #
        # if self.title is not None and self.price is not None and self.image_url is not None:
        #     self.fully_scraped = True

    def __is_captcha(self):
        """
        Boolean method, return if selenium driver arrives to Aliexpress CAPTCHA page.
        :return: True or False
        """
        # todo --> change for aliexpress captcha
        if self.driver.title in ['Amazon CAPTCHA', '503 - Service Unavailable Error']:
            return True
        else:
            return False

    def __get_properties(self):
        self.__scrape_title()
        self.__scrape_description()
        self.__scrape_features()
        self.__scrape_price()
        self.__scrape_old_price()
        self.__scrape_size()
        self.__scrape_image_url()
        self.__scrape_end_date()
        self.__scrape_coupon()

    def __scrape_title(self):
        try:
            self.title = self.driver.find_element_by_class_name('product-title').text
        except NoSuchElementException:
            try:
                self.title = self.driver.find_element_by_class_name('product-name').text
            except NoSuchElementException:
                print('[Scraper Error] Title in --> ' + self.url)
                self.title = None

    def __scrape_price(self):
        try:
            self.price = self.driver.find_element_by_class_name('product-price-current').find_element_by_class_name('product-price-value').text
        except NoSuchElementException:
            try:
                self.price = self.driver.find_element_by_class_name('p-price-content').text
            except NoSuchElementException:
                print('[Scraper Error] Price in --> ' + self.url)
                self.price = None

    def __scrape_old_price(self):
        try:
            self.old_price = self.driver.find_element_by_class_name('product-price-original').find_element_by_class_name('product-price-value').text
        except NoSuchElementException:
            try:
                self.old_price = self.driver.find_element_by_class_name('p-del-price-content').text

            except NoSuchElementException:
                print('[Scraper Error] Old Price in --> ' + self.url)
                self.old_price = None

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

    def __scrape_image_url(self):
        try:
            # father = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'image-viewer')))

            father = self.driver.find_element_by_class_name('image-viewer')
            self.image_url = father.find_element_by_class_name('magnifier-image').get_attribute('src')
        except NoSuchElementException:
            try:
                father = self.driver.find_element_by_class_name('ui-image-viewer')
                self.image_url = father.find_element_by_tag_name('img').get_attribute('src')
            except NoSuchElementException:
                self.image_url = None

    def __scrape_coupon(self):
        return None


