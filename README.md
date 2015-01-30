Torivahti
==========

A script to poll Tori.fi search and notify the user on new items.

Change config.py accordingly and run QueryManager.py to begin! This script isn't a daemon so it should be run on Crontab or Scheduler to automate the process.

Add search query as a command line parameter. Here's a fully working crontab line for searching nintendos in tori.fi:

```
*/15 * * * * python QueryManager.py nintendo
```

The initial version is quite crude on its own - don't expect it to categorize search queries or any other fancy stuff.
