# -*- coding: utf-8 -*-

from optparse import OptionParser
import smtplib

from parsers import *
from config import SAVE_FILE, RECIPIENT, GMAIL_USER, GMAIL_PWD, RECIPIENT

class Vahti:

	def __init__(self):
		self.optparser = OptionParser()
		self.optparser.add_option("-c", "--clear", action="callback", callback=self.clear_db, help="Clear the database.")
		self.optparser.add_option("-q", "--query", dest="query", help="The string to query for, i.e. JJFI99992261500081870")
		self.optparser.add_option("-p", "--parser", dest="parser", choices=["tori", "posti"], help="The parser used: [tori, posti]")
		self.optparser.add_option("-e", "--email", dest="email", help="Recipient's e-mail address")
		(options, args) = self.optparser.parse_args()

		if options.query:
			self.queries = options.query.split(",")
		else:
			self.optparser.error('Please specify a query string. See --help')

		if options.parser:
			parser_list = {
				"tori" : tori.ToriParser,
				"posti": posti.PostiParser
			}
			self.parser = parser_list[options.parser]()
		else:
			self.optparser.error('Please specify a parser. See --help')

		if options.email:
			self.recipient = options.email
		else:
			self.recipient = RECIPIENT

	def main(self):
		diff = []
		for query in self.queries:
			diff = self.parser.run(query)

		if diff:
			print("[vahti.py] New items found! Sending mail...")
			subject, msg = self.parser.create_mail()
			self.mail(subject, msg)

		else:
			print("[vahti.py] No new items found")

	def clear_db(self, option, opt, value, parser):
		import sys
		import shelve

		db = shelve.open(SAVE_FILE)
		db.clear()
		db.close()

		print("Database cleared.")

		sys.exit()

	def mail(self, subject, msg):
		"""
			Parses the mail and sends it to the address specified in the config.py file
		"""

		# Parse the mail headers
		headers = [
					"From: " + GMAIL_USER,
					"Subject: " + subject,
					"To: " + self.recipient,
					"MIME-Version: 1.0",
					"Content-Type: text/html; charset=UTF-8"
					]

		headers = "\r\n".join(headers)
		headers += "\r\n\r\n"
		headers += msg

		# Connect to the mailserver and send the message
		try:
			mailServer = smtplib.SMTP("smtp.gmail.com", 587)
			#mailServer.set_debuglevel(1)
			mailServer.ehlo()
			mailServer.starttls()
			mailServer.ehlo()
			mailServer.login(GMAIL_USER, GMAIL_PWD)
			mailServer.sendmail(GMAIL_USER, self.recipient, headers.encode('utf-8'))
			mailServer.close()
			print("[vahti.py] Mail sent to " + self.recipient)

		except smtplib.SMTPAuthenticationError:
			print("Incorrect Gmail login. - Mail was not sent.")

if __name__=="__main__":
	vahti = Vahti()
	vahti.main()
