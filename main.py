#!/usr/bin/env python3

import os
import argparse
import asyncio

from src.FourCS import fourCS
from loguru import logger


# TODO: implement async
if __name__ == "__main__":
    """
    parser = argparse.ArgumentParser("Reee")
    parser.add_argument("-b", "--board", type=str, default="g")
    parser.add_argument("-p", "--path", type=str, default="")
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        default="",
        metavar=["img", "text", "links"],
        required=True,
    )
    parser.add_argument("-e", "--extension", type=str, default="")
    parser.add_argument("-s", "--search", type=str, default="github")
    args = parser.parse_args()
    """

    #api = fourCS(args.board, args.path, args.type, args.extension, args.search)
    api = fourCS("g", "", "links", "", "")
    api.find_empty_threads()
    for thread_id in api._valid_threads:
        #logger.info(f"Working on Thread: {thread_id} ")
        for content in api.fetch_specific_thread(thread_id):
            print(content)
    #print(thread['no'] != api._empty_threads)P
    """
    logger.info(f"Found {len(api.find_empty_threads())} Empty Threads")
    for thread in api.fetch_threads():
        if thread["no"] in api._empty_threads:
            logger.debug(f"Thread is Empty Skipping Folder Creation.")
            ...
        elif thread["no"] not in api._empty_threads:
            api.generate_directories(f"{thread['no']}")


        for content in api.fetch_specific_thread(thread["no"]):
            api.download(content)
        logger.info(f"Leaving directory {thread['no']}")
        os.chdir("../")
    """
