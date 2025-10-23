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

