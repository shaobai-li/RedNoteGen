import asyncio
from crawler_client import XHSClient

async def main():
    async with XHSClient() as client:
        note_res = await client.get_note_by_keyword("web3", 1, 20)
        print("# 打印结果...")
        print(note_res)
        input("# 按任意键退出...")
        print("# 退出...")

asyncio.run(main())