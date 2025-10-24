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


# add an Anthropic API key to .env:
ANTHROPIC_API_KEY=your_key_here
```

## Usage

### Required Core (Fixed Automation)
```bash
cd core_challenge
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


### Optional Challenge 1 (AI + MCP):

This challenge uses an claude agent and MCP to make browswer automation intelligent and adaptive.

#### The Three Key Components:

**1. MCP Context Provider (`mcp_context.py`)**
- Extracts structured information about the current webpage
- Gathers all interactive elements (buttons, inputs, links)
- Provides accessibility data (IDs, names, ARIA labels, text content)
- Sends this context to the AI so it understands what's on the page

**2. LLM Client (`llm_client.py`)**
- Interfaces with Claude AI (Anthropic)
- Receives: user's goal + page context from MCP
- Generates: step-by-step action plan in JSON format
- Returns: structured commands like `[{"action": "fill", "selector": "#search", "text": "laptop"}, ...]`

**3. AI Orchestrator (`ai_orchestrator.py`)**
- Brings everything together
- Gets page context using MCP
- Asks LLM for a plan based on the goal
- Executes each step using our safe automation utilities
- Handles errors and continues execution

#### Why This Matters:

**Traditional Automation (Required Core):**
```python
# fixed steps
await automation.search_amazon("dinosaur")
await automation.get_first_product_info()
```

**AI-Driven Automation (Optional Challenge 1):**
```python
# natural language goal
await orchestrator.execute_goal("Search for dinosaurs on Amazon")
```