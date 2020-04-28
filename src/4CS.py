import requests
import json
import re

from fake_useragent import UserAgent
from datetime import datetime
from loguru import logger # best fucking log lib
from os import getcwd

valid_search_type = ['img', 'text', 'links']

class fourCS:
	"""
	params:
		board: specify the board you want to fetch things from
		path: path to store data, if none is specified, use cwd
		search_type: link,text or img
		extension: file extension
		search:  search string
	"""
	

	def __init__(self, board, path, search_type, extension, search):
		self.board = board
		self.path = path
		if self.path is None:
			self.path = f"{getcwd()}"

		self.search_type = search_type
		if self.search_type not in valid_search_type:
			logger.error(f'Please Supply a Valid Search Type.\nAvaliable Search Types {valid_search_type}')

		self.extension = extension
		self.search = search
		self.boards_api = "https://a.4cdn.org/boards.json"
		self.session = requests.Session()

		self.user_agent = UserAgent()
		self.session.headers.update({'User-Agent': self.user_agent.random})

	def fetch_boards(self):
		""" Fetch alll imageboard on 4chan """
		avaliable_board = (list([board_name['board'] for board_name in self.session.get(self.boards_api).json()['boards']])) # FUCK LONG BOII
		if self.board in avaliable_board:
			logger.info(f"Found {self.board} in list of boards")

		elif self.board not in avaliable_board:
			logger.error(f"Can't find {self.board} in list of boards, please select on that does exists")


	def fetch_threads(self):
		""" Fetch all threads from a specific board on 4chan """
		threads = f"https://a.4cdn.org/{self.board}/threads.json"

		for thread_collection in self.session.get(threads).json():
			for thread in (thread_collection['threads']):
				yield thread

	def fetch_specific_thread(self, thread_id:int):
		""" Fetch all data from a specific thread """

		#avaliable_board = (list([j['board'] for j in self.session.get(self.boards_api).json()['boards']]))
		#https://a.4cdn.org/b/thread/826294846.json

		thread = f"https://a.4cdn.org/{self.board}/thread/{thread_id}.json"

		try: 
			for thread_page in (self.session.get(thread).json()['posts']):
				if self.search_type == 'img':
					try:
						return (f"https://i.4cdn.org/{self.board}/{thread_page['tim']}{thread_page['ext']}")
					except KeyError as Error: # this usually means that the post doesn't have the key, meaning it doesn't contain an image  
						pass
					

				elif self.search_type == 'text':
					try:
						yield (self.sanitize_text(thread_page['com']))
					except KeyError as Error:
						pass

				elif self.search_type == 'links':
					try:
						clean_text = self.sanitize_text(thread_page['com'])
						links = (self.find_urls(clean_text))

						#if type(links) == str:
						return (links)

					except KeyError as Error:
						pass
					
		except json.decoder.JSONDecodeError as e: #this is usually due to that the thread is not existsing.
			pass

	def sanitize_text(self, loot:str):
		""" sanitize text if strange unicode happens """
		#pattern = re.compile(u'(?:<style.+?>.+?</style>|<script.+?>.+?</script>|<(?:!|/?[a-zA-Z]+).*?/?>|&gt;&gt;\d{9,})')
		#pattern = u'(</blockquote|</div|>|<div class|<span class|<a href|<hr|<br|<wbr|&lt;3|&quot;|&gt;|</a|class=\"|quotelink\"p[0-9]{9}|=\"deadlink\"[0-9]{9}|</span|=\"quote\")'
		pattern = u'(<a href=\"#p[0-9]{9}\" class=\"quotelink\">&gt;&gt;[0-9]{9}</a>|<br>|<span class=\"quote\">|&gt;|</span>|<span class="deadlink">|&quot;|[\n])'
		no_html = re.sub(pattern, '', loot)

		fix_apostrophe = re.compile(u'(&#039;)')
		return re.sub(fix_apostrophe, "'", no_html)
		#return (loot)

	def remove_urls(self, loot):
		pattern = re.compile(u'(https?|ftp|http)://[^\s/$.?#].[^\s]*')
		return (re.sub(pattern, '', loot))

	def find_urls(self, loot):
		pattern = re.compile(u'((https?|http?|ftp)://[^\s/$.?#].[^\s]*)')
		match = re.search(pattern, loot)
		if type(match) == str:			
			return (match).group(0)

	def download(self, url):
		""" pass in urls for to be downloaded """
		from shutil import copyfileobj
		
		filename = (url.split('/')[-1])
		#with open(filename, 'wb+') as file:
		#copyfileobj(, filename)
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

	def dupe_checker():
		"""
		checking if file exsists already or not..
		"""
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
	scraper = fourCS('b', None, 'links', '', 'github')
	for thread in (scraper.fetch_threads()):
		for post in (scraper.fetch_specific_thread(thread['no'])):
			print (post)