import httpx
import json
import re

from bs4 import BeautifulSoup
from loguru import logger as log

# from main import THREAD


log.add("../logs/4CS_Error.log", rotation="1 Week", compression="zip", level="ERROR")
log.add("../logs/4CS.log", rotation="1 Week", compression="zip", level="INFO")

# ['3', 'a', 'aco', 'adv', 'an', 'b', 'bant', 'biz', 'c', 'cgl', 'ck', 'cm', 'co', 'd', 'diy', 'e', 'f', 'fa', 'fit', 'g', 'gd', 'gif', 'h', 'hc', 'his', 'hm', 'hr', 'i', 'ic', 'int', 'jp', 'k', 'lgbt', 'lit', 'm', 'mlp', 'mu', 'n', 'news', 'o', 'out', 'p', 'po', 'pol', 'pw', 'qa', 'qst', 'r', 'r9k', 's', 's4s', 'sci', 'soc', 'sp', 't', 'tg', 'toy', 'trash', 'trv', 'tv', 'u', 'v', 'vg', 'vip', 'vm', 'vmg', 'vp', 'vr', 'vrpg', 'vst', 'vt', 'w', 'wg', 'wsg', 'wsr', 'x', 'xs', 'y']


class fourCS:
    def __init__(self):
        self._EMPTY_THREADS = list()

        self.replies_threshold = 5  # amount of replies a thread need to be NOT EMPTY
        self._boards_url = "https://a.4cdn.org/boards.json"

        self.user_agent = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1"
        }
        self.session = httpx.Client(headers=self.user_agent)

    @log.catch
    def fetch_threads(self, board) -> dict:
        """
        fetch_threads fetch all threads from a specific board on 4chan

        Yields:
            [generator object]: [returns generator object with thread id, last_modified, and amount of replies]
        """

        THREADS = f"https://a.4cdn.org/{board}/threads.json"

        for THREAD_COLLECTION in self.session.get(THREADS).json():
            for THREAD in THREAD_COLLECTION["threads"]:
                yield THREAD

    @log.catch
    def fetch_thread_subject(self, thread_id: str, board: str) -> str:
        SUBJECT = f"https://a.4cdn.org/{board}/thread/{thread_id}.json"
        try:
            TITLE = self.session.get(SUBJECT).json()["posts"][0]["sub"]
            return self.sanitize_text(TITLE)
        except KeyError:
            COMMENT = self.session.get(SUBJECT).json()["posts"][0]["com"]
            return self.sanitize_text(f"{COMMENT}")

        except Exception:  # this means thread is dead (it returns json decode error)
            return thread_id

    @log.catch
    def list_valid_boards(self) -> list[str]:
        _VALID_BOARDS = list()
        BOARDS = self.session.get(self._boards_url).json()["boards"]
        for BOARD in BOARDS:
            _VALID_BOARDS.append(BOARD["board"])
        return _VALID_BOARDS

    def sanitize_text(self, sanitize_text) -> str:
        return BeautifulSoup(sanitize_text, "lxml").text

    @log.catch
    def fetch_specific_thread(self, thread_id: int, board: str) -> object:
        """
        fetch_specific_thread

        Fetch all data from a specific thread
        And of a certain type that's specified in

        Yields:
            [generator object]: []
        """
        THREAD_SKEL = f"https://a.4cdn.org/{board}/thread/{thread_id}.json"
        try:
            for SPECIFIC_THREAD in self.session.get(THREAD_SKEL).json()["posts"]:
                try:
                    THREAD_RESP = SPECIFIC_THREAD["com"]
                    THREAD_DATA = self.find_urls(self.sanitize_text(THREAD_RESP))
                    if THREAD_DATA:
                        yield THREAD_DATA
                except KeyError as Error:
                    ...

        except json.decoder.JSONDecodeError as e:  # this is usually due to that the thread is not existsing.
            ...

    def find_urls(self, source):  # TODO: REWORK
        REGEX_PATTERN = re.compile(
            r"(^|)(https?|ftp|http)://[\w\.\=/\?\-\&\%\(\#\+\\@]+"
        )
        REGEX_MATCH = re.search(REGEX_PATTERN, source)

        if REGEX_MATCH:
            return REGEX_MATCH.group()

    def is_it_unique(self, text: str, _UNIQUE: list = []) -> bool:
        if text not in _UNIQUE:
            _UNIQUE.append(text)
            return True
        else:
            return False

    def find_empty_threads(self, board) -> list:
        """
        find_empty_threads [summary]

        Helper function to avoid empty threads, and just to visit the threads that has what we really want

        Returns:
            [list]: [list containing valid and non-empty threads]
        """

        _VALID_THREADS = list()

        log.info(f"Looking for Empty Threads!")
        for THREAD in self.fetch_threads(board):
            REPLIES = THREAD["replies"]
            THREAD_ID = THREAD["no"]

            if REPLIES >= self.replies_threshold:
                # log.debug(f"{THREAD_ID} - Replies: {REPLIES}")
                _VALID_THREADS.append(THREAD_ID)
            else:
                self._EMPTY_THREADS.append(THREAD_ID)
        return _VALID_THREADS

    def _load_json(self) -> dict:
        """
        Load Json from ./json/parsed_threads.json
        Returns:
            dict: [json dict]
        """
        log.debug("Loading from Json")
        with open("./json/parsed_threads.json", "r") as fp:
            return json.load(fp)

    def _write_json(self, _data: dict):
        """
        Write Parsed data to ./json/parsed_threads.json
        Args:
            _data (dict): [json data to write]
        """
        log.debug("Writing to Json")
        with open("./json/parsed_threads.json", "w") as fp:
            json.dump(_data, fp, indent=4)
