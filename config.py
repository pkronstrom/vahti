# -*- coding: UTF-8 -*-

# File to save the queried data between calls
# insert name without extension
SAVE_FILE = u"database"

# How long the website is queried in seconds before the connection times out
REQUEST_TIMEOUT = 3

if True:
	# I have saved my sensitive data in environment variables
	# change the conditional to False and modify the details below else
	import os
	GMAIL_USER = os.environ.get('GMAIL_USER')
	GMAIL_PWD = os.environ.get('GMAIL_PWD')
	RECIPIENT = os.environ.get('VAHTI_RECIPIENT')
else:
	GMAIL_USER = "sender@gmail.com"
	GMAIL_PWD = "hunter2"
	RECIPIENT = "my.own.email@work.com"

MAIL_SUBJECT = u"Vahti [{}] - New items found!"

# In Jinja2 format
MAIL_TEMPLATE = """
	<h3>An exciting update!</h3>
	<br />

	{% for query, results in queries.items() %}
		<b>Query: </b> <a href="{{ urls.get(query) }}">{{ query }}</a>
		<br />
		<div>
			<ul>
				{% for result in results %}
				<li>{{ result }}</li>
				{% endfor %}
			</ul>
		</div>
	{% endfor %}
"""