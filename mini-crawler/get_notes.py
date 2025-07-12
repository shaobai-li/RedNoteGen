import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(headless=False)

        browser_context = await browser.new_context()

        page = await browser_context.new_page()

        await page.goto("https://www.xiaohongshu.com", timeout=30000)


        print("# 等待扫码登录，登录成功后按任意键继续...")
        print("# 登录成功...")

        input("# 按任意键退出...")
        print("# 退出...")
        await browser.close()

asyncio.run(main())