# growing tests for core automation 
# run with: python3 test.py

import asyncio
from core_automation import BrowserAutomation

async def test_basic_setup():
    """ test opening and closing the browser """
    print("="*60)
    print("TEST 1: Basic Browser Setup")
    print("="*60)
    
    automation = BrowserAutomation()
    
    try:
        await automation.setup()
        print("[Test] Browser opened successfully!")
        
        await asyncio.sleep(2)
        
        await automation.cleanup()
        print("[Test] Browser closed successfully!")
        
        print("\n[Result] TEST PASSED!\n")
        
    except Exception as e:
        print(f"\n[Result] TEST FAILED: {e}\n")

async def run_all_tests():
    """Run all available tests"""
    await test_basic_setup()

if __name__ == "__main__":
    print("\nRunning tests...\n")
    asyncio.run(run_all_tests())
    print("All tests complete!\n")

