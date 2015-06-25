# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
from .parser import Parser
from config import REQUEST_TIMEOUT

class PostiParser(Parser):
	"""
		A Parser for Posti.fi seuranta
	"""

	def __init__(self):
		super().__init__()
		self.lang = "fi"
		self.url = "http://www.posti.fi/itemtracking/posti/search_by_shipment_id?lang={lang}&ShipmentId={tracking_no}"

	def parse_html(self, html_doc):
		"""
			Parses the Posti.fi specific html
		"""
		soup = BeautifulSoup(html_doc.read())
		temp = soup.findAll("div", attrs={"id": "shipment-event-table-cell"})

		titles = {} # title as key, url as value

		for item in temp:
			tag = item.find("div")
			name = tag.text
			titles[name] = None

		return titles

	def run(self, query):
		url = self.url.format(lang=self.lang, tracking_no=query)
		html_doc = self.query_data(url)
		data = self.parse_html(html_doc)

		diff = self.compare_to_local(query, data)

		self.mail_data[query] = diff
		self.mail_urls[query] = url

		if diff:
			return diff



