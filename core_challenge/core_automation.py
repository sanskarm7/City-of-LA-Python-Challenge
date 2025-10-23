# this will be where my core code will go

# i will use playwright to look up amazon products and get prices
# unfortunately, i cannot think of a way to simulate "logging in"

import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from playwright.async_api import async_playwright
from utils import safe_goto, safe_click, safe_fill, safe_get_text, see_page_elements
import config

class BrowserAutomation:
    
    def __init__(self):
        self.browser = None
        self.page = None
    
    async def setup(self):
        """ start the browser and create page """

        print("\n[Setup] Starting browser...")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=config.HEADLESS) # false because we want to see browser
        self.page = await self.browser.new_page()
        print("[Setup] Browser ready!\n")
    
    async def search_amazon(self, product_name):
        """ go to amazon and search for a product """
        print(f"\n[Search] Looking for: {product_name}")
        
        # first go to amazon
        success = await safe_goto(self.page, "https://www.amazon.com")
        if not success:
            return False
        
        await asyncio.sleep(2)
        
        # find and fill the search box - upon inspecting the page, the search box is id "twotabsearchtextbox"
        success = await safe_fill(self.page, "#twotabsearchtextbox", product_name)
        if not success:
            return False
        
        # click the search button - upon inspecting the page, the search button is id "nav-search-submit-button"
        success = await safe_click(self.page, "#nav-search-submit-button")
        if not success:
            return False
        
        await asyncio.sleep(2)
        
        print("[Search] Search completed!\n")
        return True
    
    async def get_first_product_info(self):
        """ get the name and price of the first product in results """
        print("[Extract] Getting product information...")
        
        # inspection shows that product title is found in an h2 specifically in the product result
        # price is in a span with class "a-price-whole"
        product_name = None
        name_selector = "[data-component-type='s-search-result'] h2"
        
        product_name = await safe_get_text(self.page, name_selector)
        if product_name and product_name.strip():
            print(f"[Extract] Found name using selector: {name_selector}")
        else: 
            print("[Extract] Could not find product name")
            return None
        
        product_price = None
        price_selector = ".a-price-whole"
        
        product_price = await safe_get_text(self.page, price_selector)
        if not product_price:
            print("[Extract] Could not find product price")
            return None
        
        result = {
            "name": product_name.strip(),
            "price": product_price.strip()
        }
        
        print(f"[Extract] Found product: {result['name']}") 
        print(f"[Extract] Price: ${result['price']}")
        
        return result
     
    async def cleanup(self):
        """ close the browser """
        print("\n[Cleanup] Closing browser...")
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("[Cleanup] Done\n")

    # dev assistance functions for debugging
    async def debug_current_page(self):
        """ helper to see what's on the page - useful for finding selectors """
        print("\n" + "="*60)
        print("DEBUG: What's on this page?")
        print("="*60)
        
        # look for matching elements on the page
        await see_page_elements(self.page, "h2")
        await see_page_elements(self.page, ".a-price-whole")
        
        print("="*60 + "\n")

