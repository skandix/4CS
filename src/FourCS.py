import requests
import shutil
import html
import json
import re
import os

from fake_useragent import UserAgent
from datetime import datetime
from loguru import logger  # best fucking log lib

logger.add("../logs/4CS_Error.log", rotation="1 Week", compression="zip", level="ERROR")
logger.add("../logs/4CS.log", rotation="1 Week", compression="zip", level="INFO")


class fourCS:
    def __init__(self, board, path, search_type, extension, search_term):
        self.board = board
        self.path = ""
        self.search_type = search_type
        self.extension = extension
        self.search_term = search_term

        self._boards_url = "https://a.4cdn.org/boards.json"
        self._valid_boards = []

        self._valid_search_type = ["img", "text", "links"]
        self._valid_threads = []
        self._empty_threads = []
        self._unique = []
        self.replies_threshold = 5  # amount of replies a thread need to be NOT EMPTY

        if self.path != "":
            self.path = path
        elif self.path:
            self.path = "../dl"

        if self.search_type not in self._valid_search_type:
            logger.error(
                f"Please Supply a Valid Search Type.\nAvaliable Search Types \
                {self._valid_search_type}"
            )
            quit()

        self.session = requests.Session()
        # self.user_agent = UserAgent(cache=False)
        self.user_agent = "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1"
        self.session.headers.update({"User-Agent": self.user_agent})

    @logger.catch
    def fetch_threads(self) -> dict:
        """
        fetch_threads fetch all threads from a specific board on 4chan

        Yields:
            [generator object]: [returns generator object with thread id, last_modified, and amount of replies]
        """
        threads = f"https://a.4cdn.org/{self.board}/threads.json"

        for thread_collection in self.session.get(threads).json():
            for thread in thread_collection["threads"]:
                yield thread

    @logger.catch
    def fetch_thread_subject(self, thread_id: str):
        subject = f"https://a.4cdn.org/{self.board}/thread/{thread_id}.json"
        try:
            return html.unescape(self.session.get(subject).json()["posts"][0]["sub"])
        except KeyError:
            comment = self.session.get(subject).json()["posts"][0]["com"]
            return html.unescape(self.rm_html_tags(comment)[:64])
        except Exception:  # this means thread is dead (it returns json decode error)
            return thread_id

    @logger.catch
    def list_valid_boards(self):
        boards = self.session.get(self._boards_url).json()["boards"]
        for board in boards:
            self._valid_boards.append(board["board"])
        return self._valid_boards

    @logger.catch
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

                    # TODO: implement searching the threads for specific keywords..
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
        # sanitize text if strange unicode happens

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

    @logger.catch
    # TODO: this function can be refactored to make use of exsisting code, and not dupe existing code.
    def download(self, content):
        if self.search_type == "img":
            filename = content.split("/")[-1]
            stream = requests.get(content, stream=True)
            with open(filename, "wb+") as file:
                shutil.copyfileobj(stream.raw, file)

        elif self.search_type == "links":
            filename = "Links.txt"
            with open(filename, "a") as file:
                file.write(str(content))
                # shutil.copyfileobj(stream.raw, file)

        elif self.search_type == "text":
            filename = "Text.txt"
            with open(filename, "w+") as file:
                file.write(f"{content}\n")

    def is_it_unique(self, text: str):
        if text not in self._unique:
            self._unique.append(text)
            return True
        else:
            return False

    def times_stomper():
        """
        times_stomper

        Timestamp files and/or folders when scraping a board, migth be an idea to create a "state" file instead
        """
        from datetime import datetime

        ...

    @logger.catch
    def generate_directories(self, foldername: str):
        """
        generate_directories

        Generate folders for threads and boards, for storing files.

        Args:
            foldername (str): [name of the folder]
        """
        # generate folder for threads and board, to put the files in..

        # TODO: cleanup this spaghetti code... yikes
        if os.path.isdir(f"{self.path}"):
            logger.info(f"{self.path} Is existsing.")
            os.chdir(self.path)
            if os.path.isdir(foldername):
                logger.info(f"Folder '{foldername}' Already Exists.")
                os.chdir(foldername)
            else:
                os.mkdir(foldername)
                logger.info(f"Created directory {foldername}")
                os.chdir(foldername)
                logger.info(f"Changed Working directory to {foldername} \n")
        elif os.path.isdir(f"{self.path}") == False:
            logger.info(f"{self.path} Does not exists.")
            os.mkdir(self.path)
            logger.info(f"Creating {self.path}.")
            os.chdir(self.path)
            logger.info(f"Changed Working directory to {self.path} \n")

    def find_empty_threads(self):
        """
        find_empty_threads [summary]

        Helper function to avoid empty Directories, and just to visit the threads that has what we really want

        Returns:
            [list]: [list containing valid and non-empty threads]
        """
        logger.info(f"Looking for Empty Threads!")
        for thread in self.fetch_threads():
            if thread["replies"] >= self.replies_threshold:
                # logger.debug(f'{thread["no"]} - Replies: {thread["replies"]}')
                self._valid_threads.append(thread["no"])
            else:
                self._empty_threads.append(thread["no"])
        return self._valid_threads
