# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.parse import quote_plus

from .parser import Parser

class ToriParser(Parser):
	"""
		A Parser for Tori.fi queries
	"""

	def __init__(self):
		super().__init__()
		self.location = "suomi"
		self.url = "http://tori.fi/{location}/?q={query}"


	def parse_html(self, html_doc):
		"""
			Parses the Tori.fi specific html
		"""
		soup = BeautifulSoup(html_doc.read())
		
		temp = soup.findAll("div", attrs={"class": "desc"})

		titles = {} # title as key, url as value

		for item in temp:
			tag = item.find("a")
			name = tag.text
			titles[name] = tag['href']

		return titles

	def run(self, query):
		url = self.url.format(location=self.location, query=quote_plus(query))
		print(url)
		html_doc = self.query_data(url)
		data = self.parse_html(html_doc)

		diff = self.compare_to_local(query, data)

		self.mail_data[query] = diff
		self.mail_urls[query] = url

		if diff:
			return diff
