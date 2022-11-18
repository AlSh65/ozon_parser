import scrapy
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
import time
from random import randint


class OzonParserSpider(scrapy.Spider):
    name = 'ozon_parser'
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    # options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    links_limit = 100
    links_count = 0

    def start_requests(self):
        for page in range(3, 4):
            driver = webdriver.Chrome(options=self.options)
            stealth(driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                    )
            driver.get(f"https://www.ozon.ru/category/smartfony-15502/?page={page}&sorting=rating")
            time.sleep(6)
            urls_list = []
            link_smartphones = driver.find_elements(By.CLASS_NAME, 'k6o')
            for link in link_smartphones:
                link = link.get_attribute('href')
                if link is not None:
                    self.links_count += 1
                    if self.links_limit >= self.links_count:
                        urls_list.append(link)
            driver.quit()
        for url in urls_list:
            driver = webdriver.Chrome(options=self.options)
            stealth(driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                    )
            driver.get(url)
            scroll = ScrollOrigin.from_viewport(10, 10)
            ActionChains(driver).scroll_from_origin(scroll, 0, 10000).perform()
            time.sleep(randint(3, 5))
            versions = driver.find_elements(By.TAG_NAME, "dd")
            for version in versions:
                if version.text.startswith("Android ") or version.text.startswith("iOS "):
                    with open("../../os.txt", "a") as f:
                        f.write(f'{version.text}\n')

        driver.quit()

    # def parse(self, response):
    #     pass
