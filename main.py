from src.FourCS import fourCS
from loguru import logger # best fucking log lib
import os

# TODO: make so that it doesn't make a folder if there's nothing in a thread..
# TODO: Find out why shit dien'st get into the folder it's supposed to go... WTF!

if __name__ == '__main__':
	# TODO: make shit faster with threading, each thread get its own processing thread :) 
	# so 60 4chan threads get 60 processing threads.
	api = fourCS('gif', '', 'links', '', 'github')

	# TODO: Implement Threading here to make this go a bit faster :) 

	logger.info(f"Found {len(api.find_empty_threads())} Empty Threads")

	for thread in (api.fetch_threads()):
		if thread['no'] in api._empty_threads:
			logger.info(f'Thread is Empty Skipping Folder Creation.')
			break
		elif thread['no'] not in api._empty_threads:
			api.generate_directories(f"{thread['no']}")

		logger.info(f"\nWorking on Thread: {thread['no']}")
		for content in (api.fetch_specific_thread(thread['no'])):
			#api.download(content)
			print (content)

		logger.info(f"Leaving directory {thread['no']}")
		os.chdir('../') # Leaving the directory before making a new one !