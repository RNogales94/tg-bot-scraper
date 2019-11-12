from scraper.selenium_web_driver import SeleniumChromeDriver
from selenium.common.exceptions import NoSuchElementException
from utils.url_utils import expand_url
from utils.singleton import Singleton


class AmazonScraper(metaclass=Singleton):

    def __init__(self):
        self.driver = SeleniumChromeDriver().driver

        # Define Properties to scrape
        self.fully_scraped = True
        self.url = None
        self.title = None
        self.description = None
        self.features = None
        self.end_date = None
        self.size = None
        self.old_price = None
        self.price = None
        self.image_url = None
        self.is_captcha = None

    def scrape(self, url):
        print(f'Scrapeando {url}')
        self.url = expand_url(url)

        self.driver.get(self.url)

        print(f'###########################\n[Scraper] {self.driver.title}\n##############################')

        if self.__is_captcha():
            self.is_captcha = True

        else:
            self.is_captcha = False
            self.__get_properties()

        short_description = self.title
        description = self.description
        features = self.features
        standard_price = self.old_price
        end_date = self.end_date
        price = self.price
        url = self.url
        image_url = self.image_url
        size = self.size
        is_captcha = self.is_captcha

        response = {
            'short_description': short_description,
            'description': description,
            'features': features,
            'standard_price': standard_price,
            'end_date': end_date,
            'price': price,
            'url': url,
            'image_url': image_url,
            'size': size,
            'is_captcha': is_captcha,
        }
        return response

        print('[Scraper Info] Done')

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
            print(f'[Scraper] Price: {self.price}')
        except NoSuchElementException:
            try:
                self.price = self.driver.find_element_by_id('priceblock_ourprice').text
                print(f'[Scraper] Price: {self.price}')
            except NoSuchElementException:
                # try:
                #     self.price = str.strip(soup.find_all('span', {'class': 'a-size-medium a-color-price'})[0].contents[0])
                # except:
                #     try:
                #         self.price = str.strip(soup.find('span', {'class': 'a-size-medium a-color-price offer-price a-text-normal'})[0].contents[0])
                #     except Exception as e:
                #         print('[Scraper Error] Price in --> ' + self.url)
                #         self.fully_scraped = False
                print('[Scraper Error] Price in --> ' + self.url)

    def __scrape_old_price(self):
        try:
            price_element = self.driver.find_element_by_id('price')
            css_selector = 'span.priceBlockStrikePriceString.a-text-strike'
            old_price = price_element.find_element_by_css_selector(css_selector).text
            self.old_price = old_price
            print(f'[Scraper] Old Price: {self.old_price}')

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
            print('[Scraper Error] Main image in --> ' + self.url)

        #     self.image_url = str.strip(soup.find(id='imgTagWrapperId').findChild('img')['data-old-hires'])
        #     if self.image_url == '':
        #         self.image_url = str.strip(soup.find(id='imgTagWrapperId').findChild('img')['src'])
        #         if self.image_url.startswith('data:image/jpeg;base64'):
        #             text = soup.find(id='imgTagWrapperId').findChild('img')['data-a-dynamic-image']
        #             self.image_url = capture_urls(text)[0]

        # except Exception as e:
        #     try:
        #         images = str.strip(soup.find(id='imgBlkFront')['data-a-dynamic-image'])
        #         urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', images)
        #         self.image_url = urls[-1]
        #     except Exception as e:
        #         print('[Scraper Error] Main image in --> ' + self.url)
        #         self.fully_scraped = False

    def __scrape_end_date(self):
        try:
            self.end_date = self.driver.find_element_by_xpath('//*[starts-with(@id,"deal_expiry_timer_")]').text
        except NoSuchElementException:
            print('[Scraper Info] No Temporal in --> ' + self.url)

    def is_well_scraped(self):
        return self.fully_scraped

    def has_old_price(self):
        return self.old_price is not None




