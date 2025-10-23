# test the MCP context provider
# this shows what structured info the AI will see about a webpage

import asyncio
from playwright.async_api import async_playwright
from mcp_context import print_page_context
import config


async def test_mcp_context():
    """test MCP context extraction on Amazon"""
    print("\n" + "="*60)
    print("TEST: MCP Context Provider")
    print("="*60 + "\n")
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=config.HEADLESS)
    page = await browser.new_page()
    
    try:
        # go to amazon
        print("Going to Amazon...")
        await page.goto("https://www.amazon.com")
        await asyncio.sleep(2)
        
        # extract and print the context
        context = await print_page_context(page)
        
        print(f"\n[Test] The AI would receive this structured data")
        print(f"[Test] Total elements found: {len(context['interactive_elements'])}")
        
        await asyncio.sleep(2)
        
    finally:
        await browser.close()
        await playwright.stop()
    
    print("\n[Test] Done. This is what MCP provides to the AI.\n")


if __name__ == "__main__":
    asyncio.run(test_mcp_context())

