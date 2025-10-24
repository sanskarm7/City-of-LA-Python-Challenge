# does the actual orchestration of the AI-driven automation

import asyncio
from playwright.async_api import async_playwright
from mcp_context import get_page_context
from llm_client import LLMClient
from utils import safe_goto, safe_click, safe_fill
import config


class AIOrchestrator:
    """
    the ai orchestrator brings everything together:
    1. uses MCP to get page context
    2. asks LLM for a plan
    3. executes the plan using our automation utilities
    """
    
    def __init__(self):
        self.browser = None
        self.page = None
        self.llm_client = LLMClient()
    
    async def setup(self):
        """start the browser"""
        print("\n[Setup] Starting AI-driven automation...")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=config.HEADLESS)
        self.page = await self.browser.new_page()
        print("[Setup] Browser ready!\n")
    
    async def cleanup(self):
        """close the browser"""
        print("\n[Cleanup] Closing browser...")
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("[Cleanup] Done\n")
    
    async def execute_step(self, step):
        """execute a single action from the AI's plan"""
        action = step.get("action")
        
        print(f"  → {action}", end="")
        if "selector" in step:
            print(f" ({step['selector']})", end="")
        if "text" in step:
            print(f" with '{step['text']}'", end="")
        print()
        
        try:
            if action == "goto":
                success = await safe_goto(self.page, step["url"])
                return success
            
            elif action == "fill":
                success = await safe_fill(self.page, step["selector"], step["text"])
                return success
            
            elif action == "click":
                success = await safe_click(self.page, step["selector"])
                return success
            
            elif action == "wait":
                seconds = step.get("seconds", 2)
                await asyncio.sleep(seconds)
                print(f"    [Success] waited {seconds} seconds")
                return True
            
            else:
                print(f"[Warning] Unknown action: {action}")
                return False
                
        except Exception as e:
            print(f"[Failure] Error: {e}")
            return False
    
    async def execute_goal(self, goal, start_url=None):
        """
        execute a goal using AI
        
        args passed in:
            goal: what you want to accomplish (example:"search for dinossaurs on Amazon")
            start_url: optional starting URL (if None, uses current page)
        
        returns:
            dict with success status and any results
        """
        print("\n" + "-"*60)
        print("AI AUTOMATION")
        print("="*60)
        print(f"Goal: {goal}\n")
        
        # go to starting URL if provided
        if start_url:
            print(f"Starting at: {start_url}")
            await safe_goto(self.page, start_url)
            await asyncio.sleep(2)
        
        # step 1: get page context using MCP
        print("\n[Step 1] Getting page context (MCP)...")
        page_context = await get_page_context(self.page)
        print(f"Found {len(page_context['interactive_elements'])} interactive elements")
        
        # step 2: ask AI for a plan
        print("\n[Step 2] Asking AI for a plan...")
        plan = self.llm_client.generate_plan(goal, page_context)
        
        if not plan:
            print("\n[Error] AI could not generate a plan")
            return {"success": False, "error": "No plan generated"}
        
        print(f"  AI generated {len(plan)} steps")
        
        # step 3: execute the plan
        print("\n[Step 3] Executing AI's plan...")
        for i, step in enumerate(plan, 1):
            print(f"\nStep {i}/{len(plan)}:")
            success = await self.execute_step(step)
            
            if not success:
                print(f"\n[Warning] Step {i} failed, but continuing...")
            
            await asyncio.sleep(1)
        
        print("\n" + "="*60)
        print("EXECUTION COMPLETE")
        print("="*60)
        
        return {
            "success": True,
            "steps_executed": len(plan),
            "final_url": self.page.url
        }


async def demo():
    """demo of the ai orchestrator"""
    orchestrator = AIOrchestrator()
    
    try:
        await orchestrator.setup()
        
        # example
        result = await orchestrator.execute_goal(
            goal="Search for a dinosaur on Amazon",
            start_url="https://www.amazon.com"
        )
        
        await asyncio.sleep(5)
        
        print(f"\nResult: {result}")
        
    finally:
        await orchestrator.cleanup()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("OPTIONAL CHALLENGE 1: AI Brain with MCP")
    print("="*60 + "\n")
    
    asyncio.run(demo())

