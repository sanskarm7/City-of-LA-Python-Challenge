# this will be where my core code will go

# i will use playwright to look up amazon products and get prices
# unfortunately, i cannot think of a way to simulate "logging in"

import asyncio
from playwright.async_api import async_playwright
from utils import safe_goto, safe_click, safe_fill, safe_get_text
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
    
    async def cleanup(self):
        """ close the browser """
        print("\n[Cleanup] Closing browser...")
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("[Cleanup] Done\n")

