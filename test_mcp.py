# test suite for MCP, LLM, and AI orchestrator
# tests all components of optional challenge 1

import asyncio
from playwright.async_api import async_playwright
from mcp_context import print_page_context
from llm_client import LLMClient
from ai_orchestrator import AIOrchestrator
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
            print(f"\nStep {i}:")
            print(f"Action: {step.get('action')}")
            if 'selector' in step:
                print(f"Selector: {step.get('selector')}")
            if 'text' in step:
                print(f"Text: {step.get('text')}")
            if 'url' in step:
                print(f"URL: {step.get('url')}")
    else:
        print("\n[Test] Failed to generate plan")
    
    print("\n" + "="*60 + "\n")


async def test_ai_orchestrator_simple():
    """test AI orchestrator with a simple goal"""
    print("\n" + "="*60)
    print("TEST: AI Orchestrator - Simple Goal")
    print("="*60 + "\n")
    
    orchestrator = AIOrchestrator()
    
    try:
        await orchestrator.setup()
        
        # test with a simple search goal
        result = await orchestrator.execute_goal(
            goal="Search for dinosaur toys",
            start_url="https://www.amazon.com"
        )
        
        # check results
        if result["success"]:
            print(f"\n[Test] Test passed!")
            print(f"[Test] Executed {result['steps_executed']} steps")
            print(f"[Test] Final URL: {result['final_url']}")
        else:
            print(f"\n[Test] Test failed: {result.get('error')}")
        
        await asyncio.sleep(2)
        
    finally:
        await orchestrator.cleanup()
    
    print("\n" + "="*60 + "\n")


async def test_ai_orchestrator_multiple_goals():
    """test AI orchestrator with different goals"""
    print("\n" + "="*60)
    print("TEST: AI Orchestrator - Multiple Goals")
    print("="*60 + "\n")
    
    orchestrator = AIOrchestrator()
    
    goals_to_test = [
        "Search for a dinosaur",
        "Search for google home",
    ]
    
    try:
        await orchestrator.setup()
        
        for i, goal in enumerate(goals_to_test, 1):
            print(f"\n--- Testing Goal {i}/{len(goals_to_test)} ---")
            print(f"Goal: {goal}\n")
            
            result = await orchestrator.execute_goal(
                goal=goal,
                start_url="https://www.amazon.com"
            )
            
            if result["success"]:
                print(f"Goal {i} succeeded")
            else:
                print(f"Goal {i} failed")
            
            await asyncio.sleep(2)
        
        print(f"\n[Test] Tested {len(goals_to_test)} different goals")
        
    finally:
        await orchestrator.cleanup()
    
    print("\n" + "="*60 + "\n")


async def test_step_execution():
    """test individual step execution"""
    print("\n" + "="*60)
    print("TEST: Individual Step Execution")
    print("="*60 + "\n")
    
    orchestrator = AIOrchestrator()
    
    try:
        await orchestrator.setup()
        await orchestrator.page.goto("https://www.amazon.com")
        await asyncio.sleep(2)
        
        # test different types of steps
        test_steps = [
            {"action": "fill", "selector": "#twotabsearchtextbox", "text": "test"},
            {"action": "wait", "seconds": 1},
            {"action": "click", "selector": "#nav-search-submit-button"}
        ]
        
        passed = 0
        for i, step in enumerate(test_steps, 1):
            print(f"\nTesting step {i}: {step['action']}")
            success = await orchestrator.execute_step(step)
            if success:
                passed += 1
                print(f"Step {i} passed")
            else:
                print(f"Step {i} failed")
        
        print(f"\n[Test] {passed}/{len(test_steps)} steps passed")
        
        await asyncio.sleep(2)
        
    finally:
        await orchestrator.cleanup()
    
    print("\n" + "="*60 + "\n")


async def run_all_tests():
    """run all test cases"""
    print("\n" + "="*70)
    print("  OPTIONAL CHALLENGE 1 - TEST SUITE")
    print("="*70 + "\n")
    
    print("Running tests for MCP, LLM, and AI Orchestrator...\n")
    
    # test 1: MCP context extraction
    await test_mcp_context()
    
    # test 2: LLM client
    test_llm_client()
    
    # test 3: AI orchestrator simple goal
    await test_ai_orchestrator_simple()
    
    # test 4: individual step execution
    await test_step_execution()
    
    await test_ai_orchestrator_multiple_goals()
    
    print("\n" + "="*70)
    print("  ALL TESTS COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    # run individual tests:
    # asyncio.run(test_mcp_context())
    # test_llm_client()
    # asyncio.run(test_ai_orchestrator_simple())
    # asyncio.run(test_step_execution())
    
    # or run all tests:
    asyncio.run(run_all_tests())

