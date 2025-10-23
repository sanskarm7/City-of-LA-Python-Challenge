# MCP (Model Context Protocol) implementation
# this extracts structured info about the current webpage for the AI

async def get_page_context(page):
    """
    extract structured information about the current page
    this is what i'll send to the AI so it knows what's on the page
    
    returns dict with:
    - title: page title
    - url: current url  
    - interactive_elements: list of buttons, inputs, links the AI can interact with
    """
    
    # basic page info
    title = await page.title()
    url = page.url
    
    # we use javascript to extract this info from the browser
    # BeautifulSoup could be used too, but playwright would probably
    # be better with JavaScript.
    elements = await page.evaluate("""
        () => {
            const interactive = [];
            
            // find all buttons, inputs, and links
            const selectors = ['button', 'input', 'a'];
            
            selectors.forEach(selector => {
                document.querySelectorAll(selector).forEach((el, idx) => {
                    // only include visible elements
                    if (el.offsetParent !== null) {
                        interactive.push({
                            tag: el.tagName.toLowerCase(),
                            type: el.type || '',
                            text: el.innerText?.substring(0, 100) || '',
                            placeholder: el.placeholder || '',
                            id: el.id || '',
                            name: el.name || '',
                            href: el.href || ''
                        });
                    }
                });
            });
            
            return interactive.slice(0, 50); // lets limit to 20 elements
        }
    """)
    
    context = {
        "title": title,
        "url": url,
        "interactive_elements": elements
    }
    
    return context


async def print_page_context(page):
    """helper to see what context we're getting"""
    context = await get_page_context(page)
    
    print("\n" + "="*60)
    print("PAGE CONTEXT (What the AI sees)")
    print("-"*60)
    print(f"Title: {context['title']}")
    print(f"URL: {context['url']}")
    print(f"\nInteractive Elements: {len(context['interactive_elements'])}")
    
    # show first 5 elements as example
    for i, elem in enumerate(context['interactive_elements'][:5]):
        print(f"\n  Element {i+1}:")
        print(f"    Tag: {elem['tag']}")
        if elem['id']:
            print(f"    ID: {elem['id']}")
        if elem['text']:
            print(f"    Text: {elem['text'][:50]}...")
    
    print("\n" + "="*60 + "\n")
    
    return context

