# -*- coding: UTF-8 -*-

import ToriParser
import config
import smtplib
import urllib2

class QueryManager:

	def __init__(self):
		self.parser = ToriParser.ToriParser()

	def main(self):
		parsed_titles = {}
		diff = []

		for query in config.query:
			parsed_titles[query] = self.parser.run(query)

		save = self.read_file() #fetch a list of previously queried titles


		for titles in parsed_titles.values():
			diff += self.match(titles, save)

		if len(diff) > 0:
			self.write_to_file(diff) #save the new query result in config file

			print "Following new items were found:"

			for item in diff:
				print item

			print "Sending mail to " + config.gmail_recipient

			self.mail(diff)

		else:
			print "NO NEW ITEMS FOUND"

	def read_file(self):

		#use a+ to create a file if it doesn't exist yet
		file = open(config.save_file, "a+")
		list = []
		
		for line in file:
			list.append(line.strip())
		
		file.close()
		
		return list

	def write_to_file(self, list):

		file = open(config.save_file, "a")
		
		for line in list:
			file.write(line)
			file.write('\n')
		
		file.close()
		
	def match(self, list1, list2):
		return (set(list1) - set(list2))

	def mail(self, diff):

		#Parse the message
		msg = "<b>Following titles were added to Tori.fi:</b><br><br><ul>"
		for item in diff:
			msg += "<li>"
			msg += item
			msg += "</li><br>"
		
		for item in config.query:
			msg += "</ul><br><a href='" + self.parser.parseUrl(item) + "'>Query term: " + item + "</a><br>"
		
		msg = "" + msg + ""

		#Parse the headers
		headers = ["From: " + config.gmail_user, "Subject: " + config.gmail_subject, "To: " + config.gmail_recipient, "MIME-Version: 1.0", "Content-Type: text/html; charset=UTF-8"]
		headers = "\r\n".join(headers)

		#Connect the mailserver and send the message
		try:
			mailServer = smtplib.SMTP("smtp.gmail.com", 587)
			mailServer.ehlo()
			mailServer.starttls()
			mailServer.ehlo()
			mailServer.login(config.gmail_user, config.gmail_pwd)
			mailServer.sendmail(config.gmail_user, config.gmail_recipient, headers + "\r\n\r\n" + msg)
			mailServer.close()
		except smtplib.SMTPAuthenticationError:
			print "Incorrect Gmail login. - Mail was not sent."

if __name__=="__main__":
	manager = QueryManager()
	manager.main()