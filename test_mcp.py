# test the MCP context provider
# this shows what structured info the AI will see about a webpage

import asyncio
from playwright.async_api import async_playwright
from mcp_context import print_page_context
import config

from llm_client import LLMClient


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



def test_llm_client():
    """test the LLM client with a simple example"""
    print("\n" + "-"*60)
    print("TEST: LLM Client")
    print("="*60 + "\n")
    
    # create a fake page context for testing
    fake_context = {
        "title": "Amazon.com",
        "url": "https://www.amazon.com",
        "interactive_elements": [
            {"tag": "input", "id": "twotabsearchtextbox", "placeholder": "Search Amazon", "text": ""},
            {"tag": "input", "id": "nav-search-submit-button", "text": "Go", "placeholder": ""}
        ]
    }
    
    # create client
    client = LLMClient()
    
    # generate a plan
    goal = "Search for wireless mouse"
    print(f"Goal: {goal}\n")
    
    plan = client.generate_plan(goal, fake_context)
    
    # show the plan
    if plan:
        print("\n[Test] Claude generated this plan:")
        for i, step in enumerate(plan, 1):
            print(f"\n  Step {i}:")
            print(f"    Action: {step.get('action')}")
            if 'selector' in step:
                print(f"    Selector: {step.get('selector')}")
            if 'text' in step:
                print(f"    Text: {step.get('text')}")
            if 'url' in step:
                print(f"    URL: {step.get('url')}")
    else:
        print("\n[Test] Failed to generate plan")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    #asyncio.run(test_mcp_context())
    test_llm_client()

