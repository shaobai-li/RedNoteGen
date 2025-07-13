from typing import Dict, Optional, List, Tuple
from playwright.async_api import async_playwright, Cookie
import os
import asyncio
from signature import get_search_id, sign
import json
import httpx

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

    async def get_note_by_keyword(self, keyword: str, page: int = 1, page_size: int = 20):
        
        print("# 准备数据和请求头...")

        uri = "/api/sns/web/v1/search/notes"

        data = {
            "keyword": keyword,
            "page": page,
            "page_size": page_size,
            "search_id": get_search_id()
        }

        await self.get_headers(uri, data)

        json_str = json.dumps(data, separators=(",", ":"), ensure_ascii=False)

        print("# 发送请求...")
        note_res = await self.request(
            method="POST",
            url=f"{self._host}{uri}",
            data=json_str,
            headers=self.headers
        )

        return note_res

    async def get_headers(self, uri: str, data):
        
        cookie_str, cookie_dict = self.convert_cookies(
            await self.browser_context.cookies()
        )
        self.headers.update({            
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Cookie": cookie_str,
            "Origin": "https://www.xiaohongshu.com",
            "Referer": "https://www.xiaohongshu.com",
            "Content-Type": "application/json;charset=UTF-8",
        })    
    
        encrypt_params = await self.playwright_page.evaluate(
            "([url, data]) => window._webmsxyw(url,data)", [uri, data]
        )

        local_storage = await self.playwright_page.evaluate("() => window.localStorage")

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

        self.headers.update(signs_for_headers)

    async def request(self, method, url, **kwargs):

        return_response = kwargs.pop("return_response", False)

        async with httpx.AsyncClient() as client:

            response = await client.request(method, url=url, timeout=10, **kwargs)

        if return_response:
            return response.text
        
        data: Dict = response.json()

        if data["success"]:
            return data.get("data", data.get("success", {}))
        else:
            return None

    def convert_cookies(self, cookies: Optional[List[Cookie]]) -> Tuple[str, dict]:

        if not cookies:
            return "", {}
        cookie_str = ";".join([f"{cookie.get('name')}={cookie.get('value')}" for cookie in cookies])
        cookie_dict = dict()
        for cookie in cookies:
            cookie_dict[cookie.get('name')] = cookie.get('value')
        
        return cookie_str, cookie_dict


async def main():
    async with XHSClient() as client:
        print("Press Enter to close the page...")
        input()

if __name__ == "__main__":
    asyncio.run(main())