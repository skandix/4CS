import requests
import html
import json
import re

from loguru import logger as log

log.add("../logs/4CS_Error.log", rotation="1 Week", compression="zip", level="ERROR")
log.add("../logs/4CS.log", rotation="1 Week", compression="zip", level="INFO")


class fourCS:
    def __init__(self):
        self.board = "g"
        self.search_type = "links"
        self.extension = ""
        self._EMPTY_THREADS = list()

        self.replies_threshold = 5  # amount of replies a thread need to be NOT EMPTY
        self._boards_url = "https://a.4cdn.org/boards.json"
        self.session = requests.Session()

        self.user_agent = "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1"
        self.session.headers.update({"User-Agent": self.user_agent})

    def _process_boards(self, boards):
        if isinstance(boards, str):
            ...
        elif isinstance(boars, list):
            ...

    @log.catch
    def fetch_threads(self) -> dict:
        """
        fetch_threads fetch all threads from a specific board on 4chan

        Yields:
            [generator object]: [returns generator object with thread id, last_modified, and amount of replies]
        """
        THREADS = f"https://a.4cdn.org/{self.board}/threads.json"

        for THREAD_COLLECTION in self.session.get(THREADS).json():
            for THREAD in THREAD_COLLECTION["threads"]:
                yield THREAD

    @log.catch
    def fetch_thread_subject(self, thread_id: str):
        SUBJECT = f"https://a.4cdn.org/{self.board}/thread/{thread_id}.json"
        try:
            return html.unescape(self.session.get(SUBJECT).json()["posts"][0]["sub"])
        except KeyError:
            COMMENT = self.session.get(SUBJECT).json()["posts"][0]["com"]
            return html.unescape(self.rm_html_tags(COMMENT)[:64])
        except Exception:  # this means thread is dead (it returns json decode error)
            return thread_id

    @log.catch
    def list_valid_boards(self):
        _VALID_BOARDS = list()
        boards = self.session.get(self._boards_url).json()["boards"]
        for board in boards:
            _VALID_BOARDS.append(board["board"])
        return _VALID_BOARDS

    @log.catch
    def fetch_specific_thread(self, thread_id: int):
        """
        fetch_specific_thread

        Fetch all data from a specific thread
        And of a certain type that's specified in

        Yields:
            [generator object]: []
        """
        thread = f"https://a.4cdn.org/{self.board}/thread/{thread_id}.json"

        try:
            for thread_page in self.session.get(thread).json()["posts"]:
                if self.search_type == "img":
                    try:
                        if self.extension == thread_page["ext"]:
                            yield (
                                f"https://i.4cdn.org/{self.board}/{thread_page['tim']}{thread_page['ext']}"
                            )
                        elif self.extension == "":
                            yield (
                                f"https://i.4cdn.org/{self.board}/{thread_page['tim']}{thread_page['ext']}"
                            )
                    except KeyError as Error:  # this usually means that the post doesn't have the key, meaning it doesn't contain an image
                        ...

                elif self.search_type == "text":
                    try:
                        dirty_text = thread_page["com"]
                        no_url_text = self.remove_urls(dirty_text)
                        sanitized_text = self.sanitize_text(no_url_text)
                        yield sanitized_text.lstrip()
                    except KeyError as Error:
                        ...

                elif self.search_type == "links":
                    try:
                        clean_text = thread_page["com"]
                        links = self.find_urls(clean_text)
                        if type(links) == str:
                            yield links
                    except KeyError as Error:
                        ...
        # this is usually due to that the thread is not existsing.
        except json.decoder.JSONDecodeError as e:
            ...

    def rm_html_tags(self, text):
        """
        rm_html_tags

        [extended_summary]

        Args:
            text ([str]): [takes in html infested text]

        Returns:
            [str]: [return clean text, without html]
        """
        loot = re.sub("<.*?>", "", text).replace(">", "")
        return loot

    def sanitize_text(self, loot: str):
        """
        sanitize_text

        Sanitize the text from html tags, and unwanted unicode

        Args:
            loot (str): [text]

        Returns:
            [str]: [sanitized string]
        """
        # loot = html.unescape(loot) # render "unicode" such as gt and amp signs
        unicode_code = [
            ('<a href="\#\w+" class="quotelink">>>\d+', ""),
            ("<.*?>", " "),
            ("(>>\d{8}|>)", ""),
        ]

        for old, new in unicode_code:
            loot = re.sub(old, new, loot)
        return loot

    # can convert remove and find urls to a higher order function, to avoid repeating code.
    def remove_urls(self, loot):
        loot = html.unescape(loot)
        loot = re.sub("<wbr>", "", loot)
        pattern = re.compile("(https?|ftp|http)://[\w\.\=/\?\-\&\%\(\#\+\\@]+")
        return re.sub(pattern, "", loot)

    def find_urls(self, loot):
        loot = html.unescape(loot)
        loot = re.sub("<wbr>", "", loot)
        pattern = re.compile("(https?|ftp|http)://[\w\.\=/\?\-\&\%\(\#\+\\@]+")
        match = re.search(pattern, loot)

        if match:
            return match.group()

    def is_it_unique(self, text: str, _UNIQUE: list = []):
        if text not in _UNIQUE:
            _UNIQUE.append(text)
            return True
        else:
            return False

    def find_empty_threads(self):
        """
        find_empty_threads [summary]

        Helper function to avoid empty Directories, and just to visit the threads that has what we really want

        Returns:
            [list]: [list containing valid and non-empty threads]
        """
        _VALID_THREADS = list()

        log.info(f"Looking for Empty Threads!")
        for thread in self.fetch_threads():
            if thread["replies"] >= self.replies_threshold:
                log.debug(f'{thread["no"]} - Replies: {thread["replies"]}')
                _VALID_THREADS.append(thread["no"])
            else:
                self._EMPTY_THREADS.append(thread["no"])
        return _VALID_THREADS
