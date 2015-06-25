Vahti
==========

Vahti is a tool that keeps track on given websites and notifies the user on new items via email.

Currently only **posti.fi parcel tracking** and **tori.fi** are supported. However, new parsers can now be easily added.

This script isn't a daemon so it should be run on Crontab or Scheduler to automate the process. The script is tested to be working on Python 3.4 and depends on BeautifulSoup4.

## Usage

1. Change settings in config.py accordingly
2. (Install Python 3.x) and install requirements with pip ```pip install -r requirements.txt```
3. Run the script with options ```python vahti.py [options]```
	- *-h, --help* to show the script help message
	- *-p, --parser* to select which parser to use (currently you can select from "tori" or "posti")
	- *-q, --query* to give the query string (i.e. posti tracking number or tori.fi search query). Separate multiple queries with space.
	- *-e, --email* to specify a different email recipient
	- *-c, --clear* to empty the database

Some query examples:
```
python vahti.py --parser tori --query nintendo --email workmail@work.fi
python vahti.py -p tori --query "sohva tuoli pöytä"
python vahti.py -p posti -q JJFI99992261500081870
```

Clear the database
```
python vahti.py --clear
```

Here's a fully working crontab line for searching nintendos in tori.fi and tracking parcels:
```
*/15 * * * * python vahti.py --parser tori --query nintendo
```

Unfortunately currently the script supports only one parser at a time, so if you want to use both tori and posti at the same time, you will need to add several crontab lines.