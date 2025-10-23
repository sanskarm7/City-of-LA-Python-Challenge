# main demo for the required core automation
# this shows the complete workflow: open browser, search, extract info, close

import asyncio
from core_automation import BrowserAutomation

# what you'll find is that this is very brittle. in the event that you search
# for a product like a "Google Home", you'll see results that push Amazon's 
# product, and that messes up the parsing. As a result, we can try to use AI
# to help us find the correct product. (optional challenge 1)

# i am aware that the required cord challenge mentioned searching for a specific product.
# i tried sticking to this through the testing suite in main_test.py
async def main():
    """ complete demo of the automation """
    print("\n" + "="*60)
    print("CITY OF LA CHALLENGE - REQUIRED CORE DEMO")
    print("Browser Automation with Playwright")
    print("="*60 + "\n")
    
    automation = BrowserAutomation()
    
    try:
        # setup browser
        await automation.setup()
        
        # search for a product
        print("Enter in a product to search for on Amazon) : ",end="")
        product_to_search = input()
        product_to_search = product_to_search.strip()

        if not product_to_search:
            print("\n[Error] Product cannot be empty!")
            return

        print(f"\nStarting search for {product_to_search}...\n")
        print(f"Task: Find '{product_to_search}' on Amazon\n")
        
        success = await automation.search_amazon(product_to_search)
        
        if not success:
            print("\n[Error] Search failed!")
            return
        
        # extract product info
        product = await automation.get_first_product_info()
        
        if not product:
            print("\n[Error] Could not extract product info!")
            return
        
        # display results
        print("\n" + "="*60)
        print("SUCCESS! FOUND PRODUCT:")
        print("="*60)
        print(f"Name:  {product['name']}")
        print(f"Price: ${product['price']}")
        print("="*60 + "\n")

        await asyncio.sleep(3)
        
    except Exception as e:
        print(f"\n[Error] Something went wrong: {e}\n")
    
    finally:
        await automation.cleanup()
    
    print("Demo complete!\n")


if __name__ == "__main__":
    asyncio.run(main())

