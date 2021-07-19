#!/usr/bin/env python3
import os
import argparse

# TODO: pros and cons on using asyncio and/or multiprocessing

from src.FourCS import fourCS
from loguru import logger

if __name__ == "__main__":
	"""
	parser = argparse.ArgumentParser("./main")
	parser.add_argument(
		"-b",
		"--board",
		type=str,
		default="",
		required=True,
		help="what board do you want to lurk on? i.e (g, sci)",
	)
	parser.add_argument(
		"-p", "--path", type=str, default=""
	)  # TODO: Need to reimplement
	parser.add_argument(
		"-t",
		"--type",
		type=str,
		default="",
		metavar=["img", "text", "links"],
		required=True,
	)
	parser.add_argument(
		"-e",
		"--extension",
		type=str,
		default="",
		help="specify a certain image file to look for",
	)
	parser.add_argument(
		"-s", "--search", type=str, default=""
	)  # TODO: Need to reimplement

	parser.add_argument("--thread-id", type=str)
	args = parser.parse_args()
	"""
	#def __init__(board, path, search_type, extension, search_term):
	api = fourCS("all", "", "links", "", "")
	#if args.thread_id:
		#for content in api.fetch_specific_thread(args.thread_id):
			#print(content)

	#for thread_id in api.find_empty_threads():
		#logger.info(
		#	f"Working on Thread: {api.fetch_thread_subject(thread_id) or thread_id}"
		#)
		#for content in api.fetch_specific_thread(thread_id):
		#	print(content)
	print(api.list_valid_boards())

	# TODO: Need to reimplement
	# logic for downloading, stuff, will take a look at this late.
	"""
	logger.info(f"Found {len(api.find_empty_threads())} Empty Threads")
	for thread in api.fetch_threads():
		if thread["no"] in api._empty_threads:
			logger.debug(f"Thread is Empty Skipping Folder Creation.")
			...
		elif thread["no"] not in api._empty_threads:
			api.generate_directories(f"{thread['no']}")


		for content in api.fetch_specific_thread(thread["no"]):
			api.download(content)
		logger.info(f"Leaving directory {thread['no']}")
		os.chdir("../")
	"""
