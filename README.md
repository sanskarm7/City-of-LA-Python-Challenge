# City of LA Python Challenge

Browser automation using Playwright to search and extract product information from Amazon.

### Core

Browser automation that:
- Opens a browser
- Searches Amazon for products
- Extracts product name and price
- Has proper error handling

### Files:
- `config.py` - configuration management
- `utils.py` - safe wrapper functions for browser operations
- `core_automation.py` - main automation class
- `core_main.py` - complete demo
- `test.py` - test suite

## Setup for Core Challenge

```bash
# create a virtual environment
python3 -m venv venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt
playwright install chromium
```

## Usage

### Run the demo:
```bash
python3 core_main.py
```

### Run tests:
```bash
python3 core_test.py
```

## How It Works

1. **BrowserAutomation class** - controls the browser
2. **search_amazon(product_name)** - searches for a product
3. **get_first_product_info()** - extracts name and price
4. **Error handling** - safe wrappers prevent crashes

