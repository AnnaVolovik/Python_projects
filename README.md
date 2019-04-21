#  A series of projects on Python 3 in a single Flask app

1) **Web parsing**
A simple web parser that computes a number of tags in the url provided, or returns an exception, and saves the results to a database
- requests
- BeautifulSoup
- SQLAlchemy

2) **Web parsing: Selenium**
A web scraper, that uses Selenium to open pop up windows as well as requests and BeautifulSoup, and openpyxl library 
to save the result into Microsoft Word spreadsheet
- Selenium & requests & BeautifulSoup
- SQLAlchemy
- openpyxl 

3) **Web parsing: asyncio, aiohttp**
A web scraper that demonstrates usage of asyncIO and aiohttp to speed up parsing of multiple pages
 - asyncio, aiohttp
 - BeautifulSoup
 
4) **Nested Data & Recursion**
The project demontrsates using recursive calls to process tree-like data
- recursion

**Setup**

`python manage.py initdb`

`python manage.py runserver`



