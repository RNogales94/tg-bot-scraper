from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.singleton import Singleton
import os


@Singleton
class SeleniumChromeDriver:
    def __init__(self):
        CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH', '/usr/local/bin/chromedriver')
        GOOGLE_CHROME_BIN = os.environ.get('GOOGLE_CHROME_BIN', '/usr/bin/google-chrome')

        options = Options()
        options.binary_location = GOOGLE_CHROME_BIN
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        # options.headless = True

        print('Building Chrome Driver')
        self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)

