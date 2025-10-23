# these are some safeguard functions to help with errors

async def safe_goto(page, url, timeout=30000):
    """Navigate to URL, return True if success, False if failed"""
    try:
        await page.goto(url, timeout=timeout)
        print(f"[Success] navigated to {url}")
        return True
    except Exception as e:
        print(f"[Failure] failed to navigate: {e}")
        return False


async def safe_click(page, selector, timeout=10000):
    """Click an element, return True if success, False if failed"""
    try:
        await page.wait_for_selector(selector, timeout=timeout)
        await page.click(selector)
        print(f"[Success] clicked {selector}")
        return True
    except Exception as e:
        print(f"[Failure] failed to click {selector}: {e}")
        return False


async def safe_fill(page, selector, text, timeout=10000):
    """Fill an input field, return True if success, False if failed"""
    try:
        await page.wait_for_selector(selector, timeout=timeout)
        await page.fill(selector, text)
        print(f"[Success] filled {selector}")
        return True
    except Exception as e:
        print(f"[Failure] failed to fill {selector}: {e}")
        return False


async def safe_get_text(page, selector, timeout=10000):
    """Get text from an element, return text or None if failed"""
    try:
        await page.wait_for_selector(selector, timeout=timeout)
        text = await page.text_content(selector)
        return text
    except Exception as e:
        print(f"[Failure] failed to get text from {selector}: {e}")
        return None


async def see_page_elements(page, selector):
    """find and print elements that match a selector"""
    try:
        elements = await page.query_selector_all(selector)
        print(f"\n[Debug] Found {len(elements)} elements matching '{selector}'")
        
        for i, elem in enumerate(elements[:10]):  # Show first 10
            text = await elem.text_content()
            text = text.strip()[:100] if text else "(no text)"
            print(f"  [{i+1}] {text}")
        
        return len(elements)
    except Exception as e:
        print(f"[Debug] Error: {e}")
        return 0

