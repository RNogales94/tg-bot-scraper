from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.singleton import Singleton
import os


class SeleniumChromeDriver(metaclass=Singleton):
    def __init__(self):
        CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH', '/usr/local/bin/chromedriver')
        GOOGLE_CHROME_BIN = os.environ.get('GOOGLE_CHROME_BIN', '/usr/bin/google-chrome-stable')

        options = Options()
        options.binary_location = GOOGLE_CHROME_BIN
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        use_headless = os.environ.get('USE_CHROME_HEADLESS', True)

        if use_headless:
            options.headless = True
        else:
            if use_headless == 'TRUE':
                use_headless = True
            elif use_headless == 'FALSE':
                use_headless = False
            else:
                use_headless = False
            options.headless = use_headless

        options.headless = True

        print('Building Chrome Driver')
        self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)

