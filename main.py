from src.FourCS import fourCS
from loguru import logger # best fucking log lib
import os


if __name__ == '__main__':
	# TODO: make shit faster with threading, each thread get its own processing thread :) 
	# so 60 4chan threads get 60 processing threads.
	scraper = fourCS('g', '/home/skandix/gitclones/4CS/dl/g', 'links', '', 'nigga')

	for thread in (scraper.fetch_threads()):
		scraper.generate_directories(f"{thread['no']}")
		logger.info(f"\nWorking on Thread: {thread['no']}")
		for content in (scraper.fetch_specific_thread(thread['no'])):
			print (content)
			#logger.info(f"Downloading {content}")
			#scraper.download(content)

		logger.info(f"Leaving directory {thread['no']}")
		os.chdir('../') # Leaving the directory before making a new one !