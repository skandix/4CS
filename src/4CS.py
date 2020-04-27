import requests
import json

from fake_useragent import UserAgent
from datetime import datetime
from loguru import logger # best fucking log lib
from os import getcwd

class fourCS:
	"""
	params:
		board: specify the board you want to fetch things from
		path: path to store data, if none is specified, use cwd
		file_type: link,text or img
		extension: file extension
		search:  search string
	"""
	def __init__(self, board, path, file_type, extension, search):
		self.board = board
		self.path = path
		if self.path is None:
			self.path = f"{getcwd()}"

		self.file_type = file_type
		self.extension = extension
		self.search = search
		self.debug = False
		self.boards_api = "https://a.4cdn.org/boards.json"
		self.thread_api = "https://a.4cdn.org/po/catalog.json"
		self.session = requests.Session()

		self.user_agent = UserAgent()
		self.session.headers.update({'User-Agent': self.user_agent.random})

	def fetch_boards(self):
		avaliable_board = (list([board_name['board'] for board_name in self.session.get(self.boards_api).json()['boards']]))
		if self.board in avaliable_board:
			logger.info(f"Found {self.board} in list of boards")

		elif self.board not in avaliable_board:
			logger.error(f"Can't find {self.board} in list of boards, please select on that does exists")


	def fetch_threads(self, thread_id:int):
		#avaliable_board = (list([j['board'] for j in self.session.get(self.boards_api).json()['boards']]))
		#https://a.4cdn.org/b/thread/826294846.json
		thread = f"https://a.4cdn.org/{self.board}/thread/{thread_id}.json"
		thread_pages = [page for page in (self.session.get(thread).json()['posts'])]
		avaliable_threads = [thread['no'] for thread in thread_pages]
		
		print (avaliable_threads)


	def fetch_specific_thread():
		pass

	def fetch_api(self):
		return (session.get())
		"""
		global function to get data from api,
		and serve it a fake useragent :)
		as i don't want to get fingerprinted
		"""
		
		pass

	def download(self, url:str, filename:str):
		"""
		pass in urls for to be downloaded
		"""
		from shutil import copyfileobj
		if "http" or "https" not in url:
			url = f"https://{url}"
		stream_data = self.session.get(url, stream=True)

		with open(filename, 'wb+') as file:
			copyfileobj(stream.raw, filename)

		pass

	def times_stomper():
		from datetime import datetime
		"""
		timestamp the files that contains fuck loads of urls or text from 4chan
		"""
		pass

	def board_title():
		"""
		return the title for the specific board
		"""
		pass

	def valid_boards(self):
		fetch_api()


	def dupe_checker():
		"""
		checking if file exsists already or not..
		"""
		pass

	def sanitize():
		"""
		sanitize text if strange unicode happens
		"""
		pass

	def get_links(loot:str, action:str):
		""" get all the links from a text with the use of regex... """

		if action == "del":
			pattern = re.compile(u'(https?|ftp|http)://[^\s/$.?#].[^\s]*')
			return re.sub(pattern, '', loot)
	
		elif action == "find":
			pattern = re.compile(u'((https?|http?|ftp)://[^\s/$.?#].[^\s]*)')
			match = re.search(pattern, loot)
			if match:
				return (match).group(0)
		else:
			return (f"Please enter a valid Action!")

	def get_images(loot:str):
		pass

	def get_text(loot:str):
		pass


	def generate_directories(foldername:str):
		"""
		generate folder for threads and board, to put the files in..
		"""
		from os import path, mkdir, chdir
		if path.isdir(foldername):
			logger.info(f'Folder \'{foldername}\' Already Exists.')
			chdir(foldername)
		else:
			mkdir(foldername)
			logger.debug(f"Created directory {foldername}")
			chdir(foldername)
			logger.debug(f"Changed Working directory to {foldername} \n")

		pass


if __name__ == '__main__':

	import argparse
	
	parser = argparse.ArgumentParser()
	parser.add_argument("--board", "-b", type=str, help="")
	parser.add_argument("--path", "-p", type=str, help="Set a specific path to download to")
	parser.add_argument("--type", "-t", type=str, help="set a specific type to download (img, text or links)")
	parser.add_argument("--ext", "-e", type=str, help="download a specific image extension, only works for img type downloads")
	parser.add_argument("--search", "-s", type=str, help="search for a specific board [EXPERIMENTAL]")
	parser.add_argument("--debug", "-d", type=bool, help="will print thread ID for debugging purposes")
	args = parser.parse_args()
	
	# board, path, file_type, extension, search
	scraper = fourCS('b', None, 'img', '', 'github')
	#scraper = fourCS(args.board, args.path, args.type,  args.ext, args.search)
	#scraper.fetch_boards()
	print (scraper.fetch_threads(826294846))