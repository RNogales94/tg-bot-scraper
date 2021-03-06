from scraper.selenium_web_driver import SeleniumChromeDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import money_parser
from utils.url_utils import expand_url
from utils.singleton import Singleton
import os

import re


class AmazonScraper(metaclass=Singleton):

    def __init__(self):
        self.driver = SeleniumChromeDriver().driver
        self.api_key = os.environ.get('SCRAPEAPI_KEY', 'adfe255be6ddb5488a7fcef4bde677c6')

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
        print(f'Scrapeando {url}')
        self.__reset_scraper()
        self.url = expand_url(url)

        if self.api_key is None:
            self.driver.get(self.url)
        else:
            country = 'ue'
            url = f'http://api.scraperapi.com/?api_key={self.api_key}&url={self.url}&country_code={country}'
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


    def __is_captcha(self):
        """
        Boolean method, return if selenium driver arrives to Amazon CAPTCHA page.
        :return: True or False
        """
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
            self.title = self.driver.find_element_by_id('productTitle').text
            print(f'[Scraper] Short Description: {self.title}')
        except NoSuchElementException as e:
            print('[Scraper Error] Title in --> ' + self.url)
            self.fully_scraped = False

    def __scrape_description(self):
        try:
            product_descripition_el = self.driver.find_element_by_id('productDescription')
            self.description = product_descripition_el.find_element_by_css_selector('p').text
            print(f'[Scraper] Description: {self.description}')
            if self.description == '':
                paragraphs = product_descripition_el.find_elements_by_css_selector('p')
                paragraphs = list(map(lambda x: x.text.strip(), paragraphs))
                self.description = '\n'.join(paragraphs).strip()
        except NoSuchElementException:
            print('[Scraper Error] Description in --> ' + self.url)

    def __scrape_features(self):
        try:
            self.features = self.driver.find_element_by_id('feature-bullets').text
            print(f'[Scraper] Features: {self.features}')
        except NoSuchElementException:
            print('[Scraper Error] Features in --> ' + self.url)

    def __scrape_price(self):
        try:
            self.price = self.driver.find_element_by_id('priceblock_dealprice').text
            print(f'[Scraper] Price: {self.price} - using -> priceblock_dealprice')
        except NoSuchElementException:
            try:
                self.price = self.driver.find_element_by_id('priceblock_ourprice').text
                print(f'[Scraper] Price: {self.price} - using -> priceblock_ourprice')
            except NoSuchElementException:
                try:
                    self.price = self.driver.find_element_by_id('priceblock_saleprice').text
                    print(f'[Scraper] Price: {self.price} - using -> priceblock_saleprice')
                except NoSuchElementException:
                    try:
                        self.price = self.driver.find_element_by_id('buyNewSection').text
                        print(f'[Scraper] Price: {self.price} - using -> buyNewSection')
                    except NoSuchElementException:
                        try:
                            el = self.driver.find_element_by_id('olpLinkWidget_feature_div')
                            self.price = el.find_element_by_class_name('a-color-price').text
                            print(f'[Scraper] Price: {self.price} - using -> olpLinkWidget_feature_div')
                        except NoSuchElementException:
                            try:
                                el = self.driver.find_element_by_id('olp-upd-new-freeshipping')
                                self.price = el.find_element_by_class_name('a-color-price').text
                                print(f'[Scraper] Price: {self.price} - using -> olp-upd-new-freeshipping')
                            except NoSuchElementException:
                                try:
                                    self.price = self.driver.find_element_by_id('price_inside_buybox').text
                                    print(f'[Scraper] Price: {self.price} - using -> price_inside_buybox')
                                except NoSuchElementException:
                                    try:
                                        el = self.driver.find_element_by_id('price')
                                        self.price = el.find_element_by_class_name('a-color-price').text
                                        print(f'[Scraper] Price: {self.price} - using -> price')
                                    except NoSuchElementException:
                                        try:
                                            el = self.driver.find_element_by_id('olp-new')
                                            self.price = el.find_element_by_class_name('a-color-price').text
                                            print(f'[Scraper] Price: {self.price} - using -> olp-new')
                                        except NoSuchElementException:
                                            print('[Scraper Error] Price in --> ' + self.url)

    def __scrape_old_price(self):
        try:
            price_element = self.driver.find_element_by_id('price')
            css_selector = 'span.priceBlockStrikePriceString.a-text-strike'
            old_price = price_element.find_element_by_css_selector(css_selector).text
            self.old_price = old_price
            print(f'[Scraper] Old Price: {self.old_price}')
        except NoSuchElementException:
            try:
                price_element = self.driver.find_element_by_id('price')
                old_price = price_element.find_element_by_class_name('priceBlockStrikePriceString').text
                self.old_price = old_price
                print(f'[Scraper] Old Price: {self.old_price}')
            except NoSuchElementException:
                try:
                    el = self.driver.find_element_by_id('buyBoxInner')
                    self.old_price = el.find_element_by_class_name('a-text-strike').text
                except NoSuchElementException:
                    print('[Scraper Warning] Old price in --> ' + self.url)

    def __scrape_size(self):
        try:
            sizes_element = self.driver.find_element_by_id('variation_size_name')
            self.size = sizes_element.find_element_by_class_name('dropdownSelect').text.strip()
            print(f'[Scraper] Size: {self.size}')

            # self.size = str.strip(soup.find(id='variation_size_name').find('option', selected=True).contents[0])
        except NoSuchElementException:
            print('[Scraper Info] No sizes in --> ' + self.url)

    def __scrape_image_url(self):
        try:
            image_element = self.driver.find_element_by_id('imgTagWrapperId')
            self.image_url = image_element.find_element_by_tag_name('img').get_attribute('src')
            print(f'[Scraper] image_url: {self.image_url}')

        except NoSuchElementException:
            try:
                el = self.driver.find_element_by_id('img-wrapper')
                self.image_url = el.find_element_by_tag_name('img').get_attribute('src')
                print(f'[Scraper] image_url: {self.image_url}')

            except NoSuchElementException:
                print('[Scraper Error] Main image in --> ' + self.url)

    def __scrape_end_date(self):
        try:
            self.end_date = self.driver.find_element_by_xpath('//*[starts-with(@id,"deal_expiry_timer_")]').text
        except NoSuchElementException:
            print('[Scraper Info] No Temporal in --> ' + self.url)

    def __scrape_coupon(self):
        try:
            coupon_link = WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located((By.ID, 'applicable_promotion_list_sec')))
            ActionChains(self.driver).move_to_element(coupon_link).perform()
            coupon_text = self.driver.find_element_by_id('a-popover-content-3').text

            pattern = r'Ahorra un (?P<discount>\d+([\,\.]\d+)?)%.*c.digo\s(?P<code>\S+).*'
            match = re.search(pattern, coupon_text)
            if match is not None:
                self.coupon_code = match.group('code')
                self.coupon_discount = match.group('discount')
                self.coupon_price = float(money_parser.price_dec(self.price)) * float(self.coupon_discount) / 100
                self.coupon_price = f'{round(self.coupon_price, 2)} €'

        except (NoSuchElementException, TimeoutException):
            print('[Scraper Info] No Coupon in --> ' + self.url)
            try:
                coupon_text = self.driver.find_element_by_id('applicable_promotion_list_sec').text
                pattern = r'\s+(?P<discount>(\d+)[\.\,]?(\d+)?%) OFF: (?P<code>\w+)\.\s+'
                match = re.search(pattern, coupon_text)
                if match is not None:
                    self.coupon_code = match.group('code')
                    self.coupon_discount = match.group('discount')
                    self.coupon_price = float(money_parser.price_dec(self.price)) * float(self.coupon_discount) / 100
                    self.coupon_price = f'{round(self.coupon_price, 2)} €'

            except (NoSuchElementException, TimeoutException):
                print('[Scraper Info] No Coupon in --> ' + self.url)
        except Exception as e:
            print('[ERROR Scraper Info] Exception is not being well handled in coupon scraper--> \n' + str(e))






