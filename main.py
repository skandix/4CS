#!/usr/bin/env python3
from os import link
from src.FourCS import fourCS
from loguru import logger as log

# boards = ["g", "sci", "b"]
boards = ["g"]

linkStore = {}
THREAD_CONTENT = list()

API = fourCS()
for BOARD in boards:
    log.warning(f"=== /{BOARD}/ ===")
    # log.info(f"Found {len(API.find_empty_threads(BOARD))} Empty Threads")
    for THREAD in API.fetch_threads(BOARD):
        THREAD_ID = THREAD["no"]
        if THREAD_ID not in API._EMPTY_THREADS:
            TITLE = API.fetch_thread_subject(THREAD_ID, BOARD) or THREAD_ID
            log.info(f"Working on Thread: {TITLE}")
            for CONTENT in API.fetch_specific_thread(THREAD_ID, BOARD):
                THREAD_CONTENT.append(CONTENT)
            linkStore[THREAD_ID] = {
                "title": TITLE,
                "board": BOARD,
                "urls": [THREAD_CONTENT or []],
            }
            API._write_json(linkStore)
            THREAD_CONTENT = list()
