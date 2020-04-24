import requests
import json

from fake_useragent import UserAgent
from datetime import datetime
from loguru import logger # best fucking log lib

class 4chanScraper()

	def __init__(self):
		self.board = board
		self.path = path
		self.file_type = file_type
		self.extension = extension
		self.search = search
		self.debug = False
		self.api_url = ""
		self.session = request.Session()
		self.user_agent = UserAgent()

	def fetch_api(self, api_url):
		"""
		global function to get data from api,
		and serve it a fake useragent :)
		as i don't want to get fingerprinted
		"""
		self.session.headers.update({'User-Agent': self.user_agent.random})
		return self.session.get(self.api_url).text

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

	def sanitize():
		"""
		sanitize text if strange unicode happens
		"""
		pass

	def get_links():
		"""
		get all the links from a text with the use of regex..
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