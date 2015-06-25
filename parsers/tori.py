# -*- coding: UTF-8 -*-

from BeautifulSoup import BeautifulSoup
import urllib2
from parser import Parser

class ToriParser(Parser):
	"""
		A Parser for Tori.fi queries
	"""

	def __init__(self):
		self.location = "suomi"
		self.url = "http://tori.fi/{location}/?q={query}"

	def fetch(self, url):
		"""Fetches the query specific titles from Tori.fi"""
		html_doc = urllib2.urlopen(url)
		soup = BeautifulSoup(html_doc.read().decode('ISO-8859-15', 'ignore')) #
		
		temp = soup.findAll("div", attrs={"class": "desc"})

		titles = {} # title as key, url as value

		for item in temp:
			tag = item.find("a")
			name = tag.text
			titles[name] = tag['href']

		return titles

	def run(self, query):
		url = self.url.format(location=self.location, query=query)
		data = self.fetch(url)

		diff = self.compare_to_local(query, data)

		if diff:
			print "[tori.py] following items found: "
			for item in diff:
				print "[tori.py] " + item

			print "[tori.py] Compile a mail here" # and return it
			return "[tori.py] " + str(len(diff)) + " new items found"
