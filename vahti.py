# -*- coding: UTF-8 -*-

from parsers import *
import config

from optparse import OptionParser
import smtplib
import codecs

class Vahti:

	def __init__(self):
		self.optparser = OptionParser()
		self.optparser.add_option("-q", "--query", dest="query", help="The string to query for, i.e. JJFI99992261500081870")
		self.optparser.add_option("-p", "--parser", dest="parser", choices=["tori", "posti"], help="The parser used: [tori, posti]")
		self.optparser.add_option("-e", "--email", dest="email", help="Recipient's e-mail address")
		self.optparser.add_option("-d", "--delete", action="callback", callback=self.delete_db, help="Deletes the database.")
		(options, args) = self.optparser.parse_args()

		if options.query:
			self.queries = options.query.split(" ")
		#else:
		#	self.optparser.error('Please specify a query string. See --help')

		if options.parser:
			parser_list = {
				"tori" : tori.ToriParser,
				"posti": posti.PostiParser
			}
			self.parser = parser_list[options.parser]()
		#else:
		#	self.optparser.error('Please specify a parser. See --help')

		if options.email:
			self.recipient = options.email
		else:
			self.recipient = config.recipient

	def main(self):
		for query in self.queries:
			diff = self.parser.run(query)

		if diff:
			print "[vahti.py] New items found! Sending mail..."
		else:
			print "[vahti.py] No new items found"

	def delete_db(self, option, opt, value, parser):
		import os, sys
		try:
			filename = config.save_file + ".db"
			os.remove(filename)
		except OSError:
			self.optparser.error("Database " + filename + " doesn't exist.")

		print "Database deleted."

		sys.exit()

	def mail(self, diff):

		#Parse the message
		msg = u"<h3>Following new titles were found in Tori.fi:</h3>"
		msg += u"<b>Query: </b> <a href='" + self.parser.parse_url(self.query) + u"'>" + self.query + u"</a><br></div><ul>"

		for title, url in diff.iteritems():
			if url:
				msg += u"<li><a href='"
				msg += url #.encode('utf-8')
				msg += u"'>"
				msg += title #.encode('utf-8')
				msg += u"</a></li>"
			else:
				msg += "<li>"
				msg += title
				msg += "</li>"

		msg += u"</ul>"
		
		msg = u"" + msg + u""

		subject = config.gmail_subject.format(self.query)

		print subject

		#Parse the headers
		headers = [u"From: " + config.gmail_user, u"Subject: " + subject, u"To: " + self.recipient, u"MIME-Version: 1.0", u"Content-Type: text/html; charset=UTF-8"]
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
	vahti = Vahti()
	vahti.main()