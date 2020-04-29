import requests
import shutil
import json
import re
import os

from fake_useragent import UserAgent
from datetime import datetime
from loguru import logger # best fucking log lib

valid_search_type = ['img', 'text', 'links']
logger.add('../logs/4CS_Error.log', rotation='1 Week', compression='zip', level='ERROR')
logger.add('../logs/4CS.log', rotation='1 Week', compression='zip', level='INFO')

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
		self.search_type = search_type
		self.extension = extension
		self.search = search

		# Variable Checks
		if self.path == '':
			self.path = f"{os.getcwd()}"
		
		if self.search_type not in valid_search_type:
			logger.error(f'Please Supply a Valid Search Type.\nAvaliable Search Types {valid_search_type}')
			quit()

		# Session & User Agent
		self.session = requests.Session()
		self.user_agent = UserAgent()
		self.session.headers.update({'User-Agent': self.user_agent.random})

	@logger.catch
	def fetch_threads(self):
		""" Fetch all threads from a specific board on 4chan """
		threads = f"https://a.4cdn.org/{self.board}/threads.json"

		for thread_collection in self.session.get(threads).json():
			for thread in (thread_collection['threads']):
				yield thread

	@logger.catch
	def fetch_specific_thread(self, thread_id:int):
		""" Fetch all data from a specific thread """
		thread = f"https://a.4cdn.org/{self.board}/thread/{thread_id}.json"

		try: 
			for thread_page in (self.session.get(thread).json()['posts']):
				if self.search_type == 'img':
					# TODO: implement searching the threads for specific keywords..
					#if self.search:
						#if re.search(self.search,"sdafasdf",flags=re.I):
					#	pass
					#elif self.search == '':
					try:
						yield (f"https://i.4cdn.org/{self.board}/{thread_page['tim']}{thread_page['ext']}")
					except KeyError as Error: # this usually means that the post doesn't have the key, meaning it doesn't contain an image
						pass

				elif self.search_type == 'text':
					try:
						clean_text = self.sanitize_text(thread_page['com'])
						even_cleaner = self.remove_urls(clean_text)
						yield even_cleaner
					except KeyError as Error:
						pass

				elif self.search_type == 'links':
					try:
						clean_text = self.sanitize_text(thread_page['com'])
						links = (self.find_urls(clean_text))
						if (type(links) == str):
							yield links
					except KeyError as Error:
						pass
		except json.decoder.JSONDecodeError as e: #this is usually due to that the thread is not existsing.
			pass

	def sanitize_text(self, loot:str):
		""" sanitize text if strange unicode happens """
		# someone have a more efficient regex that this that works, please make a pr accordingly.		
		pattern = u'(<a href=\"#p[0-9]{9}\" class=\"quotelink\">&gt;&gt;[0-9]{9}</a>|<br>|<span class=\"quote\">|&gt;|</span>|<span class="deadlink">|&quot;|[\n]|<a href=[\"\S\"]+ class=[\"\S\"]+</a>|<wbr>)'
		no_html = re.sub(pattern, '', loot)

		fix_apostrophe = re.compile(u'(&#039;)')
		return re.sub(fix_apostrophe, "'", no_html)

	def remove_urls(self, loot):
		pattern = re.compile(u'(https?|ftp|http)://[^\s/$.?#].[^\s]*')
		return (re.sub(pattern, '', loot))

	def find_urls(self, loot):
		pattern = re.compile(u'((https?|http?|ftp)://[^\s/$.?#].[^\s]*)')
		match = re.search(pattern, loot)

		if match:
			return (match.group(0))

	def download(self, url):
		""" pass in urls for to be downloaded """		
		filename = (url.split('/')[-1])
		stream = (requests.get(url, stream=True))
		with open(filename, 'wb+') as file:
			shutil.copyfileobj(stream.raw, file)

	def times_stomper():
		from datetime import datetime
		""" timestamp the files that contains fuck loads of urls or text from 4chan """
		pass

	@logger.catch
	def generate_directories(self,foldername:str):
		"""
		generate folder for threads and board, to put the files in..
		"""
		foldername = str(foldername) # type casting in python, is straange

		if os.path.isdir(f"{self.path}"):
			logger.info(f"{self.path} Is existsing.")
			os.chdir(self.path)
			if os.path.isdir(foldername):
				logger.info(f'Folder \'{foldername}\' Already Exists.')
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