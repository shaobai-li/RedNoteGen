import asyncio
from playwright.async_api import async_playwright
import os
from typing import Optional, List, Tuple
from playwright.async_api import Cookie
from signature import sign, get_search_id

def convert_cookies(cookies: Optional[List[Cookie]]) -> Tuple[str, dict]:

    if not cookies:
        return "", {}
    cookie_str = ";".join([f"{cookie.get('name')}={cookie.get('value')}" for cookie in cookies])
    cookie_dict = dict()
    for cookie in cookies:
        cookie_dict[cookie.get('name')] = cookie.get('value')
    
    return cookie_str, cookie_dict


async def get_headers(browser_context, page, cookie_str, cookie_dict):
    
    # 请求头的初始化
    headers = dict()
    headers.update(
        {
            # "User-Agent": user_agent,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Cookie": cookie_str,
            "Origin": "https://www.xiaohongshu.com",
            "Referer": "https://www.xiaohongshu.com",
            "Content-Type": "application/json;charset=UTF-8",
        }
    )    
    
    encrypt_params = await page.evaluate(
            "([url, data]) => window._webmsxyw(url,data)", [uri, data]
        )

    local_storage = await page.evaluate("() => window.localStorage")

    signs = sign(
        a1=cookie_dict.get("a1", ""),
        b1=local_storage.get("b1", ""),
        x_s=encrypt_params.get("X-s", ""),
        x_t=str(encrypt_params.get("X-t", "")),
    )

    signs_for_headers = {
        "X-S": signs["x-s"],
        "X-T": signs["x-t"],
        "x-S-Common": signs["x-s-common"],
        "X-B3-Traceid": signs["x-b3-traceid"],
    }

    headers.update(signs_for_headers)

    return headers




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


        cookie_str, cookie_dict = convert_cookies(
            await browser_context.cookies()
        )

                
        search_id = get_search_id()

        uri = "/api/sns/web/v1/search/notes"

        data = {
            "keyword": "web3",
            "page": 1,
            "page_size": 20,
            "search_id": search_id,
            # "sort": sort.value,
            # "note_type": note_type.value,
        }


        headers = await get_headers(browser_context, page, uri, data, cookie_str, cookie_dict)



        input("# 按任意键退出...")
        print("# 退出...")
        await browser.close()

asyncio.run(main())