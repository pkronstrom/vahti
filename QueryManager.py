# -*- coding: UTF-8 -*-

import ToriParser
import config
import smtplib
import codecs
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
#import urllib2

class QueryManager:

	def __init__(self):
		self.parser = ToriParser.ToriParser()

	def main(self):

		if len(sys.argv) > 1:
			self.query = sys.argv[1].decode('latin-1')	# terminal is ISO-LATIN
		else:
			self.query = config.defaultquery.decode('utf-8') # python is then again UTF-8

		print self.query

		parsed_titles_dict = {}
		diff = []

		parsed_titles_dict = self.parser.run(self.query)
		save = self.read_file()	# fetch a list of previously queried parsed_titles
		titles_list = list(parsed_titles_dict.keys())

		diff += self.match(titles_list, save) # compare the fetched items for saved ones

		if len(diff) > 0:
			self.write_to_file(diff)	# save the new query result in config file

			print u"Following new items were found:"

			for item in diff:
				print item

			print u"Sending mail to " + config.gmail_recipient

			diff_dict = dict((k,v) for (k,v) in parsed_titles_dict.iteritems() if k not in save)

			self.mail(diff_dict)

		else:
			print u"NO NEW ITEMS FOUND"

	def read_file(self):
		#use a+ to create a file if it doesn't exist yet
		file = open(config.save_file, "a+")
		list = []

		with codecs.open(config.save_file, 'a+', encoding='utf8') as file:
			for line in file:
				list.append(line.strip())
		
		#file.close()

		return list

	def write_to_file(self, list):

		#file = open(config.save_file, "a")
		with codecs.open(config.save_file, 'a', encoding='utf8') as file:
			for line in list:
				file.write(line)
				file.write('\n')
		
		#file.close()
		
	def match(self, list1, list2):
		return (set(list1) - set(list2))

	def mail(self, diff):

		#Parse the message
		msg = u"<h3>Following new titles were found in Tori.fi:</h3>"
		msg += u"<b>Query: </b> <a href='" + self.parser.parse_url(self.query) + u"'>" + self.query + u"</a><br></div><ul>"

		for title, url in diff.iteritems():
			msg += u"<li><a href='"
			msg += url#.encode('utf-8')
			msg += u"'>"
			msg += title#.encode('utf-8')
			msg += u"</a></li>"

		msg += u"</ul>"
		
		msg = u"" + msg + u""

		subject = config.gmail_subject.format(self.query)

		print subject

		#Parse the headers
		headers = [u"From: " + config.gmail_user, u"Subject: " + subject, u"To: " + config.gmail_recipient, u"MIME-Version: 1.0", u"Content-Type: text/html; charset=UTF-8"]
		headers = "\r\n".join(headers)

		#Connect the mailserver and send the message
		try:
			mailServer = smtplib.SMTP("smtp.gmail.com", 587)
			mailServer.ehlo()
			mailServer.starttls()
			mailServer.ehlo()
			mailServer.login(config.gmail_user, config.gmail_pwd)
			mailServer.sendmail(config.gmail_user, config.gmail_recipient, headers.encode('utf-8') + "\r\n\r\n" + msg.encode('utf-8'))
			mailServer.close()
		except smtplib.SMTPAuthenticationError:
			print u"Incorrect Gmail login. - Mail was not sent."

if __name__=="__main__":
	manager = QueryManager()
	manager.main()