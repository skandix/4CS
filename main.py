import asyncio
import aiohttp

from FourCS.FourCS import fourCS
from loguru import logger as log


api = fourCS("g", "", "links", "", "")

links_status_code = {}


async def fetch_content(session, content):
    async with session.get(content, timeout=5) as response:
        return response.status


async def main(thread_id):
    try:
        thread_subject = api.fetch_thread_subject(thread_id) or thread_id
        log.info(f"Working on Thread: {thread_subject}")
        async with aiohttp.ClientSession() as session:
            tasks = [
                fetch_content(session, content)
                for content in api.fetch_specific_thread(thread_id)
            ]
            results = await asyncio.gather(*tasks)
            for status_code in results:
                links_status_code[status_code] = (
                    links_status_code.get(status_code, 0) + 1
                )
    except Exception as e:
        log.error(f"Error while processing thread {thread_id}: {str(e)}")


if __name__ == "__main__":
    ith = api.find_empty_threads()
    loop = asyncio.get_event_loop()
    coros = [main(thread_id) for thread_id in ith]
    loop.run_until_complete(asyncio.gather(*coros))
    loop.close()
    print(f"{links_status_code=}\n4chan Thread Count: {len(ith)}")
