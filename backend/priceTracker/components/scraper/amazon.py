"""
The AmazonScraper class uses Selenium to scrape product data from Amazon. It has a method search_product which takes a product name as input and returns a list of product data. The search_product method searches for the product on Amazon and extracts the product name, image, price, and URL. 
The scrape_amazon function uses the AmazonScraper class to scrape product data from Amazon and saves the results to the database. It takes a product name as input and returns the scraped results.
"""
import time
import random
import urllib.parse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.orm import Session


from priceTracker.components.models import ProductResult

class AmazonScraper:
    def __init__(self):
        options = Options()
        options.headless = True
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        
    def get_product_data(self, product_div):
        try:
            image_url, product_name, product_price, product_url = None, None, None, None
            
            try:
                image_element = product_div.find_element(By.CSS_SELECTOR, 'img.s-image')
                image_url = image_element.get_attribute('src')
            except Exception as e:
                print("Error extracting image:", e)

            try:
                name_element = product_div.find_element(By.CSS_SELECTOR, 'h2 a span')
                product_name = name_element.text
            except Exception as e:
                print("Error extracting name:", e)

            try:
                price_element = product_div.find_element(By.CSS_SELECTOR, 'span.a-price')
                price_whole_element = price_element.find_element(By.CSS_SELECTOR, 'span.a-price-whole')
                price_fraction_element = price_element.find_element(By.CSS_SELECTOR, 'span.a-price-fraction')
                product_price_str = price_whole_element.text.replace("\u202f", "").replace(",", "").strip() + '.' + price_fraction_element.text.strip()
                product_price = round(float(product_price_str), 2)  # Ensure rounding to 2 decimal places
            except Exception as e:
                print("Error extracting price:", e)

            try:
                url_element = product_div.find_element(By.CSS_SELECTOR, 'a.a-link-normal.s-no-hover.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')
                product_url = "https://www.amazon.fr" + url_element.get_attribute('href')
            except Exception as e:
                print("Error extracting url:", e)

            if image_url and product_name and product_price is not None and product_url:
                return {"img": image_url, "name": product_name, "price": product_price, "url": product_url}
            else:
                print("Incomplete product data")
                return None
        except Exception as e:
            print(f"Error extracting product data: {e}")
            return None

    def search_product(self, product_name, max_pages=5):
        encoded_product_name = urllib.parse.quote(product_name)
        search_url = f"https://www.amazon.fr/s?k={encoded_product_name}"
        self.driver.get(search_url)

        time.sleep(random.uniform(2, 5))

        results = []
        for page in range(1, max_pages + 1):
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.s-main-slot div.s-result-item.s-asin')))
            product_divs = self.driver.find_elements(By.CSS_SELECTOR, 'div.s-main-slot div.s-result-item.s-asin')
            
            for product_div in product_divs:
                product_data = self.get_product_data(product_div)
                if product_data:
                    results.append(product_data)
                
                time.sleep(random.uniform(1, 3))
            
            try:
                next_page_link = self.driver.find_elements(By.CSS_SELECTOR, 'li.a-last a')
                if next_page_link:
                    next_page_url = next_page_link[0].get_attribute('href')
                    self.driver.get(next_page_url)
                    
                    time.sleep(random.uniform(2, 5))
                else:
                    break
            except Exception as e:
                print(f"No more pages or error navigating to the next page: {e}")
                break
        
        return results
    
    def close(self):
        self.driver.quit()

def scrape_amazon(db: Session, product_name: str):
    scraper = AmazonScraper()
    results = scraper.search_product(product_name)
    scraper.close()

    for result in results:
        product = ProductResult(
            name=result['name'],
            img=result['img'],
            url=result['url'],
            price=result['price'],
            search_text=product_name,
            source='Amazon'
        )
        db.add(product)
        db.commit()
        db.refresh(product)

    return results
