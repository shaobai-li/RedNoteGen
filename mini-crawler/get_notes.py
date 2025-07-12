import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as playwright:

        chromium = playwright.chromium

        browser = await chromium.launch(headless=False)


        user_data_dir = os.path.join(
            os.getcwd(), "browser_data"
        )
        
        browser_context = await chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            accept_downloads=True,
            headless=False,
            viewport={"width": 1920, "height": 1080},
        )



        page = await browser_context.new_page()

        await page.goto("https://www.xiaohongshu.com", timeout=30000)


        input("# 等待扫码登录，登录成功后按任意键继续...")
        print("# 登录成功...")

        input("# 按任意键退出...")
        print("# 退出...")
        await browser.close()

asyncio.run(main())