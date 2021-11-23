#!/usr/bin/env python3
from src.FourCS import fourCS
from loguru import logger as log

# board = ["g", "sci", "b"]
# board = "g"

API = fourCS()
for BOARD in API.list_valid_boards():
    log.warning(f"=== /{BOARD}/ ===")
    log.info(f"Found {len(API.find_empty_threads(BOARD))} Empty Threads")
    for THREAD in API.fetch_threads(BOARD):
        THREAD_ID = THREAD["no"]
        if THREAD_ID not in API._EMPTY_THREADS:
            log.info(
                f"Working on Thread: {API.fetch_thread_subject(THREAD_ID, BOARD) or THREAD_ID}"
            )
            for CONTENT in API.fetch_specific_thread(THREAD_ID, BOARD):
                print(CONTENT)
