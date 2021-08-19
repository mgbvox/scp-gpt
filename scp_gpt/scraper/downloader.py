import asyncio
import aiohttp
from pydantic import HttpUrl
from typing import List, Any


async def get_url(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as resp:
        return await resp.text()


async def get_many_urls(session: aiohttp.ClientSession, urls: List[str]):
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_url(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


async def main(urls: List[str]):
    async with aiohttp.ClientSession() as session:
        data = await get_many_urls(session, urls)
        return data
