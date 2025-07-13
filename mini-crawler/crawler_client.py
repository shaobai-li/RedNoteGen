from typing import Dict
from playwright.async_api import async_playwright
import os
import asyncio

class XHSClient:

    def __init__(self):
        self._host = "https://edith.xiaohongshu.com"
        self._domain = "https://www.xiaohongshu.com"

        self.browser_data_dir = os.path.join(os.getcwd(), "browser_data")
        self.headers: Dict[str, str] = dict()
        self.playwright = None
        self.browser_context = None
        self.playwright_page = None

    async def __aenter__(self):
        print("Starting browser...")
        self.playwright = await async_playwright().start()

        self.browser_context = await self.playwright.chromium.launch_persistent_context(
                user_data_dir=self.browser_data_dir,
                accept_downloads=True,
                headless=False,
                viewport={"width": 1920, "height": 1080},
            )
        
        self.playwright_page = await self.browser_context.new_page()

        await self.playwright_page.goto(self._domain, timeout=30000)

        return self
    
    async def __aexit__(self, exc_type, exc_value, exc_tb):
        print("Closing browser...")
        await self.playwright_page.close()
        await self.browser_context.close()
        await self.playwright.stop()



async def main():
    async with XHSClient() as client:
        print("Press Enter to close the page...")
        input()

if __name__ == "__main__":
    asyncio.run(main())