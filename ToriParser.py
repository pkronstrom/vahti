# -*- coding: UTF-8 -*-

from BeautifulSoup import BeautifulSoup
import urllib2

class ToriParser:

	def __init__(self):
		self.location = "uusimaa"

	def parseUrl(self, query):
		"""Parses the query specific URL for Tori.fi"""
		return ("http://tori.fi/" + self.location + "/?q=" + query) #add parameters if needed

	def getData(self, url):
		"""Fetches the query specific titles from Tori.fi"""
		html_doc = urllib2.urlopen(url)
		soup = BeautifulSoup(html_doc)
		
		temp = soup.findAll("div", attrs={"class": "desc"})
		
		titles = []

		for item in temp:
			name = item.find("a").text.encode('utf-8')
			titles.append(name)

		return titles

	def run(self, query):
		url = self.parseUrl(query) #parse the URL
		return self.getData(url) #get the data from Tori.fi