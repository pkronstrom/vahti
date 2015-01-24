# -*- coding: UTF-8 -*-

from BeautifulSoup import BeautifulSoup
import urllib2

class ToriParser:

	def __init__(self):
		self.location = "suomi"

	def parse_url(self, query):
		"""Parses the query specific URL for Tori.fi"""
		return ("http://tori.fi/" + self.location + "/?q=" + query) #add parameters if needed

	def get_data(self, url):
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
		url = self.parse_url(query) #parse the URL
		return self.get_data(url) #get the data from Tori.fi