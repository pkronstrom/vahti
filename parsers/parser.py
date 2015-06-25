# -*- coding: utf-8 -*-

import shelve
import sys
from urllib.request import urlopen
from socket import timeout

from config import SAVE_FILE, REQUEST_TIMEOUT

class Parser():

	def _get_list_diff(self, list1, list2):
		"""
			Compares two given lists and returns the difference
		"""
		return (set(list1) - set(list2))

	def query_data(self, url):
		try:
			html_doc = urlopen(url, timeout=REQUEST_TIMEOUT)
		except timeout:
			print("Request timed out.")
			sys.exit()
		return html_doc

	def compare_to_local(self, query, data):
		"""
			Compares the given data to the database, usign query as a key
		"""

		with shelve.open(SAVE_FILE) as local_storage:
			try:
				saved_query_data = local_storage[query]
			except KeyError:
				saved_query_data = []
				local_storage[query] = saved_query_data

			diff = self._get_list_diff(data, saved_query_data)

			if len(diff) > 0:
				local_storage[query] += diff 	# save the diff to stash

				print ("[parser.py] DIFF:")
				for item in diff:
					print ("[parser.py] " + item)
			else:
				print ("[parser.py] No new items found")

		return diff
