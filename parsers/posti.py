# -*- coding: UTF-8 -*-

from BeautifulSoup import BeautifulSoup
from parser import Parser
import urllib2

class PostiParser(Parser):
	"""
		A Parser for Posti.fi seuranta
	"""

	def __init__(self):
		self.lang = "fi"
		self.url = "http://www.posti.fi/itemtracking/posti/search_by_shipment_id?lang={lang}&ShipmentId={tracking_no}"

	def fetch(self, url):
		html_doc = urllib2.urlopen(url)
		soup = BeautifulSoup(html_doc.read().decode('ISO-8859-15', 'ignore')) #
		
		temp = soup.findAll("div", attrs={"id": "shipment-event-table-cell"})

		titles = {} # title as key, url as value

		for item in temp:
			tag = item.find("div")
			name = tag.text
			titles[name] = None

		return titles

	def run(self, query):
		url = self.url.format(lang=self.lang, tracking_no=query)
		data = self.fetch(url)

		diff = self.compare_to_local(query, data)

		if diff:
			print "[posti.py] Compile a mail here" # and return it

			return "[posti.py] " + str(len(diff)) + " new items found"



