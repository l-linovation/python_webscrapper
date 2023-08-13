This Python web scrapper was written to obtain information, including funding year, amount, purpose and program, of projects funded by the Bill & Melinda Gates foundation (http://gatesfoundation.org).

##Required Python library
In addition to the default libraries, urllib and datetime, two other libraries are required: 
   [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)  and [selenium] (http://selenium-python.readthedocs.io).

##Browsers and dependencies
[Chrome](https://www.google.com/chrome/) and [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) are required to run this script.
##work flow
Step 1: query the grant-database website for one year. 
Step 2: On the webpage of the query results, get the links of each project (HTML).
Step 3: Go to the link of the project and obtain the information.
Step 4: Repeat Step 3 until every project information on this page is obtained.
Step 5: Repeat Step 2 until every page of the query results is visited.
Step 6: Repeat Step 1 until every year is queried.

##Run the script
python WebScrap.py
