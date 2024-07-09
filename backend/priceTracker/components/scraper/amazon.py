import time
import random
import urllib.parse
import json
import uuid
import redis
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.orm import Session
from priceTracker import logger
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class AmazonScraper:
    def __init__(self):
        options = Options()
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
        ]
        options.add_argument(f"user-agent={random.choice(user_agents)}")
        options.headless = False
        
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--incognito")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Edge(options=options)
        self.wait = WebDriverWait(self.driver, 20)

        self.print_current_ip()

    def print_current_ip(self):
        self.driver.get('https://api.ipify.org')
        ip_address = self.driver.find_element(By.TAG_NAME, 'body').text
        logger.info(f"Current IP Address: {ip_address}")


    def set_location_and_language(self):
        self.driver.get('https://www.amazon.com/gp/delivery/ajax/address-change.html')
        time.sleep(2)
        self.driver.find_element(By.ID, 'GLUXZipUpdateInput').send_keys('10001')
        self.driver.find_element(By.ID, 'GLUXZipUpdate').click()
        time.sleep(2)
        self.driver.refresh()
        self.driver.get('https://www.amazon.com')
        self.driver.find_element(By.ID, 'icp-nav-flyout').click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, "span.icp-nav-language").click()
        self.driver.find_element(By.CSS_SELECTOR, "input[name='icp-selected-language'][value='en_US']").click()
        self.driver.find_element(By.CSS_SELECTOR, "input[name='icp-done-button']").click()
        time.sleep(2)
        self.driver.refresh()
    
    
    def extract_product_name(self, product_div: webdriver.remote.webelement.WebElement) -> str:
        """
        Extract the product name from the product div element.
        
        Args:
            product_div (webdriver.remote.webelement.WebElement): The product div element.
        
        Returns:
            str: The product name.
        """
        try:
            name_element = product_div.find_element(By.CSS_SELECTOR, 'h2 a span')
            return name_element.text
        except NoSuchElementException:
            logger.warning("Couldn't extract product name.")
            return None
    
    def extract_product_image(self, product_div: webdriver.remote.webelement.WebElement) -> str:
        """
        Extract the product image URL from the product div element.
        
        Args:
            product_div (webdriver.remote.webelement.WebElement): The product div element.
        
        Returns:
            str: The product image URL.
        """
        try:
            image_element = product_div.find_element(By.CSS_SELECTOR, 'img.s-image')
            return image_element.get_attribute('src')
        except NoSuchElementException:
            logger.warning("Couldn't extract product image.")
            return None

    def extract_product_price(self, product_div: webdriver.remote.webelement.WebElement) -> float:
        """
        Extract the product price from the product div element.
        
        Args:
            product_div (webdriver.remote.webelement.WebElement): The product div element.
        
        Returns:
            float: The product price.
        """
        try:
            price_whole = product_div.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text
        except NoSuchElementException:
            try:
                price_whole = product_div.find_element(By.CSS_SELECTOR, 'span.a-offscreen').text
            except NoSuchElementException:
                price_whole = "0"

        try:
            price_fraction = product_div.find_element(By.CSS_SELECTOR, 'span.a-price-fraction').text
        except NoSuchElementException:
            price_fraction = "00"

        product_price_str = price_whole.replace("\u202f", "").replace(",", "").strip() + '.' + price_fraction.strip()
        print(f"product_price_str = {product_price_str}")
        return round(float(product_price_str), 2)

    def extract_product_currency(self, product_div: webdriver.remote.webelement.WebElement) -> str:
        """
        Extract the product currency from the product div element.
        
        Args:
            product_div (webdriver.remote.webelement.WebElement): The product div element.
        
        Returns:
            str: The product currency.
        """
        try:
            product_currency = product_div.find_element(By.CSS_SELECTOR, 'span.a-price-symbol').text
            return product_currency
        except NoSuchElementException:
            logger.warning("Couldn't extract product currency.")
            return "EUR"


    def extract_product_url(self, product_div: webdriver.remote.webelement.WebElement) -> str:
        """
        Extract the product URL from the product div element.
        
        Args:
            product_div (webdriver.remote.webelement.WebElement): The product div element.
        
        Returns:
            str: The product URL.
        """
        try:
            url_element = product_div.find_element(By.CSS_SELECTOR, 'a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')
            return url_element.get_attribute('href')
        except NoSuchElementException:
            logger.warning("Couldn't extract product URL.")
            return None

    def extract_product_data(self, product_div: webdriver.remote.webelement.WebElement) -> dict:
        """
        Extract product data from a product div element.
        
        Args:
            driver (webdriver.Edge): The WebDriver instance.
            wait (WebDriverWait): The WebDriverWait instance.
            product_div (webdriver.remote.webelement.WebElement): The product div element.
        
        Returns:
            dict: A dictionary containing the extracted product data.
        """
        return {
            "id": str(uuid.uuid4()),
            "img": self.extract_product_image(product_div),
            "product_name": self.extract_product_name(product_div),
            "price": self.extract_product_price(product_div),
            "currency": self.extract_product_currency(product_div),
            "url": self.extract_product_url(product_div)
        }

    def search_product(self, search_text: str, max_pages: int = 5) -> list:
        """
        Search for products on Amazon and extract data.
        
        Args:
            driver (webdriver.Edge): The WebDriver instance.
            wait (WebDriverWait): The WebDriverWait instance.
            search_text (str): The search query.
            max_pages (int): The maximum number of pages to scrape.
        
        Returns:
            list: A list of dictionaries containing the scraped product data.
        """
        encoded_search_text = urllib.parse.quote(f'"{search_text}"')
        search_url = f"https://www.amazon.com/s?k={encoded_search_text}&ref=nb_sb_noss"
        self.driver.get(search_url)
        
        time.sleep(random.uniform(2, 5))

        results = []
        for page in range(1, max_pages + 1):
            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.s-main-slot div.s-result-item.s-asin')))
                product_divs = self.driver.find_elements(By.CSS_SELECTOR, 'div.s-main-slot div.s-result-item.s-asin')
                other_product_divs = self.driver.find_elements(By.CSS_SELECTOR, 'div.s-main-slot div.s-result-item li.a-carousel-card')
                if other_product_divs:
                    product_divs.extend(other_product_divs)

                more_product_divs = self.driver.find_elements(By.CSS_SELECTOR, "div.sg-col-20-of-24 div.s-result-item div.sg-col-0-of-12 div.sg-col-16-of-20 div.s-widget div.sg-col div.s-flex-geom div.sg-col-12-of-16 div.s-widget-spacing-large")
                
                if more_product_divs:
                    product_divs.extend(more_product_divs)

                for product_div in product_divs:
                    product_data = self.extract_product_data(product_div)
                    if product_data:
                        results.append(product_data)
                    time.sleep(random.uniform(1, 4))

                try:
                    next_page_link = self.driver.find_elements(By.CSS_SELECTOR, 'a.s-pagination-next')
                    if next_page_link:
                        next_page_url = next_page_link[0].get_attribute('href')
                        self.driver.get(next_page_url)
                        time.sleep(random.uniform(2, 5))
                    else:
                        break
                except Exception as e:
                    logger.warning(f"No more pages or error navigating to the next page: {e}")
                    break
            except TimeoutException as e:
                logger.warning(f"TimeoutException: {e}")
                break

        return results
    
    def scrape_product_price(self, url: str) -> dict:
        self.driver.get(url)
        time.sleep(random.uniform(2, 5))
        self.wait.until(EC.presence_of_element_located((By.ID, 'corePrice_desktop')))
        try:
            core_price_element = self.wait.until(EC.presence_of_element_located((By.ID, 'corePrice_desktop')))
        
            price_element = core_price_element.find_element(By.CSS_SELECTOR, 'span.a-price ')
            product_price = float(price_element.text.replace("$", "").replace(",", ""))
        except NoSuchElementException:
            logger.warning("Couldn't extract product price.")
            product_price = 0.0
        logger.info(f"Scraped product data: {product_price}")
        return product_price
    
    def scrape_product_price2(self, url: str) -> dict:
        self.driver.get(url)
        time.sleep(random.uniform(2, 5))
        self.wait.until(EC.presence_of_element_located((By.ID, 'corePriceDisplay_desktop_feature_div')))
        try:
            core_price_element = self.wait.until(EC.presence_of_element_located((By.ID, 'corePriceDisplay_desktop_feature_div')))
        
            product_price = core_price_element.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text
        except NoSuchElementException:
            logger.warning("Couldn't extract product price.")
            product_price = 0.0
        logger.info(f"Scraped product data: {product_price}")
        return product_price
    
    def scrape_product_page(self, url: str) -> dict:
        """
        Scrape product data from an Amazon product page.
        
        Args:
            driver (webdriver.Edge): The WebDriver instance.
            wait (WebDriverWait): The WebDriverWait instance.
            url (str): The URL of the product page.
        
        Returns:
            dict: A dictionary containing the scraped product data.
        """
        self.driver.get(url)
        time.sleep(random.uniform(2, 5))
        self.wait.until(EC.presence_of_element_located((By.ID, 'productTitle')))
        product_name = self.driver.find_element(By.ID, 'productTitle').text
        product_image = self.driver.find_element(By.CSS_SELECTOR, 'img#landingImage').get_attribute('src')
        try:
            product_price = self.scrape_product_price(url)
        except Exception as e:
            product_price = self.scrape_product_price2(url)
        
        product_currency = "USD"
        return {
            "id": str(uuid.uuid4()),
            "img": product_image,
            "product_name": product_name,
            "price": product_price,
            "currency": product_currency,
            "url": url
        }

    def close(self):
        """
        Closes the Selenium driver.
        """
        self.driver.quit()

def scrape_amazon(db: Session, search_text: str) -> list:
    """
    Scrapes product data from Amazon and saves the results to the database.
    
    args:
        db : Session : The database session
        search_text : str : The name of the product to search for on Amazon
    
    returns:
        list : A list of dictionaries containing the scraped product data
    """
    redis_client = redis.Redis(host='127.0.0.1', port=6380, db=0)
    scraper = AmazonScraper()
    results = scraper.search_product(search_text)
    redis_client.setex(search_text, 3600, json.dumps(results))
    scraper.close()
    return results


def scrape_amazon_price(db: Session, url: str) -> dict:
    """
    Scrapes product data from an Amazon product page and saves the result to the database.
    
    args:
        db : Session : The database session
        url : str : The URL of the Amazon product page
    
    returns:
        dict : A dictionary containing the scraped product data
    """
    scraper = AmazonScraper()
    product_price = scraper.scrape_product_page(url)
    scraper.close()
    return product_price


def scrape_amazon_product_page(db: Session, url: str) -> dict:
    """
    Scrapes product data from an Amazon product page and saves the result to the database.

    args:
        db : Session : The database session
        url : str : The URL of the Amazon product page

    returns:
        dict : A dictionary containing the scraped product data
    """
    scraper = AmazonScraper()
    product_data = scraper.scrape_product_page(url)
    logger.info(f"Scraped product data: {product_data}")
    scraper.close()
    return product_data