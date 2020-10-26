from src.FourCS import fourCS
from loguru import logger
import os

# TODO: implement async
if __name__ == "__main__":
    api = fourCS("g", "", "links", "", "github")
    logger.info(f"Found {len(api.find_empty_threads())} Empty Threads")

    for thread in api.fetch_threads():
        if thread["no"] in api._empty_threads:
            logger.info(f"Thread is Empty Skipping Folder Creation.")
            break
        # elif thread['no'] not in api._empty_threads:
        # api.generate_directories(f"{thread['no']}")

        logger.info(f"\nWorking on Thread: {thread['no']}")
        for content in api.fetch_specific_thread(thread["no"]):
            #api.download(content)
            print(content)

        # logger.info(f"Leaving directory {thread['no']}")
        # os.chdir('../') # Leaving the directory before making a new one !