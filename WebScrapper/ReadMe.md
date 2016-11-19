This Python web scrapper was written to obtain information, including funding year, amount, purpose and program, of projects funded by the Bill & Melinda Gates foundation (http://gatesfoundation.org).

##required Python library
In addition to the default libraries, urllib and datetime, two other libraries are required: 
   [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)  
   [selenium] (http://selenium-python.readthedocs.io)  


##work flow
Step 1: query the grant-database website for one year.  
Step 2: On the webpage of the query results, get the links of each project (HTML).  
Step 3: Go to the link of the project and obtain the information.  
Step 4: Repeat Step 3 until every project information on this page is obtained.  
Step 5: Repeat Step 2 until every page of the query results is visited.  
Step 6: Repeat Step 1 until every year is queried.  
