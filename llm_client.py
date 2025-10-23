# this is the actual LLM client

# DISCLAIMER: YOU NEED TO HAVE AN ANTHROPIC API KEY SET IN THE .ENV FILE IN ORDER TO USE THIS

# i've tested this with mine, and it works. i was not sure of whether I should be sharing my personal
# key, so it is not included in this repo.

import json
from anthropic import Anthropic
import config


class LLMClient:
    """client for talking to claude 3.5 sonnet"""
    
    def __init__(self):
        if not config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not set in .env file")
        
        self.client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.model = "claude-3-5-sonnet-20241022"
    
    def generate_plan(self, goal, page_context):
        """
        send the goal and page context to Claude
        get back a list of actions to perform
        
        args passed in:
            goal: what the user wants to do
            page_context: the MCP context
        
        returns:
            list of actions like [{"action": "fill", "selector": "#search", "text": "dinosaur"}, ...]
        """
        
        # this is the system prompt that teaches Claude what actions it can use
        system_prompt = """You are a web automation expert. Given a user's goal and the current webpage state, generate a step-by-step plan.

                        Available actions:
                        - fill: Fill an input field
                        Format: {"action": "fill", "selector": "css selector", "text": "text to type"}
                        
                        - click: Click an element  
                        Format: {"action": "click", "selector": "css selector"}
                        
                        - goto: Navigate to URL
                        Format: {"action": "goto", "url": "https://example.com"}

                        - wait: Wait for page to load
                        Format: {"action": "wait", "seconds": 2}

                        Based on the page context, choose the best selectors. Prefer IDs over other selectors.
                        Return ONLY a JSON array of actions. No explanation, just the JSON."""

        # get theuser prompt with goal and context
        user_prompt = f"""Goal: {goal}

                        Current Page:
                        Title: {page_context['title']}
                        URL: {page_context['url']}

                        Interactive Elements:
                        """
            
        # add info about each element
        for i, elem in enumerate(page_context['interactive_elements'][:10]):
            user_prompt += f"\n{i+1}. {elem['tag']}"
            if elem['id']:
                user_prompt += f" (id='{elem['id']}')"
            if elem['text']:
                user_prompt += f" - '{elem['text'][:50]}'"
            if elem['placeholder']:
                user_prompt += f" - placeholder: '{elem['placeholder']}'"
        
        user_prompt += "\n\nGenerate the action plan as a JSON array:"
        
        print("\n[LLM] Sending request to Claude...")
        
        # call Claude API
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        # extract the text response
        response_text = response.content[0].text
        
        print(f"[LLM] Received response from Claude")
        
        # parse the JSON plan
        try:
            # i noticed sometimes it returns like this: ```json ... ```
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            plan = json.loads(response_text.strip())
            print(f"[LLM] Generated plan with {len(plan)} steps")
            return plan
            
        except json.JSONDecodeError as e:
            print(f"[LLM] Failed to parse response: {e}")
            print(f"[LLM] Response was: {response_text}")
            return []




if __name__ == "__main__":
    print("\n[Info] This is the LLM Client module")
    print("[Info] It will be used by the AI orchestrator")
    print("[Info] Run test_mcp.py to test it\n")
