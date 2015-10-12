# -*- coding: utf-8 -*-

import shelve
import sys
from urllib.request import urlopen
from socket import timeout
from jinja2 import Template

from config import SAVE_FILE, REQUEST_TIMEOUT, MAIL_SUBJECT, MAIL_TEMPLATE

class Parser():
	def __init__(self):
		self.mail_data = {}
		self.mail_urls = {}

	def create_mail(self):
		if self.mail_data:
			qs = ", ".join(self.mail_data.keys())
			subject = MAIL_SUBJECT.format(qs)
			msg = Template(MAIL_TEMPLATE).render(queries=self.mail_data, urls=self.mail_urls)
			return subject, msg
		else:
			print("Error in creating mail")
			sys.exit()

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

		local_storage = shelve.open(SAVE_FILE)
		try:
			saved_query_data = local_storage[query]
		except KeyError:
			saved_query_data = []
			local_storage[query] = saved_query_data

		diff = self._get_list_diff(data, saved_query_data)

		if len(diff) > 0:	
			local_storage[query] += diff 	# save the diff to stash
		else:
			print ("[parser.py] No new items found")

		local_storage.close()

		return diff
