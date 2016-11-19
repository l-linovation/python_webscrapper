'''
[Purpose]
Get information about projects funded by BMG foundation. Scrap dynamic JavaScript and HTML webpage.
To do that:
First, query the grant-database website for each year. On the webpage of the query results, go through each page (coded in JavaScript) and get the links of each project (HTML).
Then get each project url and parse the HTML.
[Date]
Nov. 6, 2016
'''

from bs4 import BeautifulSoup
import urllib
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import datetime

def loadWeb(driver, url, year = ""):
    '''Load the webpage; wait till it's fully loaded'''
    driver.get(url)
    try:
        WebDriverWait(driver, 15).until(
            expected_conditions.text_to_be_present_in_element(
                (By.CLASS_NAME, 'label'), year))
    except:
        try:
            WebDriverWait(driver, 15).until(
                expected_conditions.text_to_be_present_in_element(
                    (By.CLASS_NAME, 'next_link'), 'Next'))
        except:
            try:
                WebDriverWait(driver, 15).until(
                expected_conditions.text_to_be_present_in_element(
                    (By.CLASS_NAME, 'next_link'), 'First'))
            except:
                # TODO: to put something here so that the program knows there is an loading error here
                #raise Exception('Page not loading :(')
                print "Page not loaded." # placeholder

def project_href(driver, webURL = "", tagn = "span", classn = "sans-serif strong"):
    '''Get the hyperlink of every project on this page'''
    currProjectLinks = []
    soup = BeautifulSoup(driver.page_source)
    linkList_temp = soup.find_all(tagn, class_= classn)
    for element in linkList_temp:
        currProjectLinks = currProjectLinks + [webURL + element.a["href"]]
    return currProjectLinks

def max_page_no (driver, last_link_text):
    '''get the last page's url, get the max page number'''
    link = driver.find_element_by_link_text(last_link_text)
    link.click()
    last_url = driver.current_url
    last_page_number = str(last_url)[-2:]
    url_pagepre = str(last_url)[: -2]
    return (last_page_number, url_pagepre)

def extract_text(element):
    '''Extract the text from the BeautifulSoup HTML element'''
    element.extract().get_text(strip = True).encode('utf-8', 'ignore')  # This did not convert the html text to plain text successfully

def get_info(soupObj, keys, tagn1 = "div", classn1 = "articleWrapper", institute_tagn = "h2", others_tagn="span"):
    '''Parse HTML, get the project's institue, funded date, funding amount, project topic, project location (program) and project purpose'''
    adict = {}
    content = soupObj.find_all(tagn1, class_ = classn1)
    institute = content[0].find(institute_tagn).get_text()
    adict.update({"Institute": institute})
    otherInfo = content[0].find_all(others_tagn)
    for element in otherInfo:
        for k in keys:
            if k in element["id"]:
                adict.update({k: extract_text(element)})
    return adict

def scrapHTML(urls, outfp, headers):
    '''Scrap HTML webpage and save the infomation of interest to the output file'''
    '''
    urls: urls of the websites
    outfp: file path of the output file
    headers: headers in the output file
    '''
    fo = open(outfp, "w")
    fo.write("\t".join(headers) + "\n")
    for url in set(urls):
        r = urllib.urlopen(url).read()
        soup = BeautifulSoup(r)
        info = get_info(soup, [k for k in headers if k != "Institute"], tagn1 = "div", classn1 = "articleWrapper", institute_tagn = "h2", others_tagn="span")
        try:
            fo.write("\t".join([info[item] for item in headers]) + "\n")
        except:
            print url
            print info
    fo.close()

def scrap(webURL, years, requestURLprefix, outfp, headers, chromedriver):
    '''Scrap a JavaScript coded webpage, get links to HTML coded webpage where the useful information is located and write out the useful information to a file'''
    '''
    webURL: url of the JavaScript coded webpage
    years: a list of years, will be used to load the database-query webpage (coded in JavaScript)
    requestURLprefix: prefix of the database-query webpage; add the year to this will be the web link for the first page of projects funded in that year
    outfp: output file path
    header: headers in the output file
    chromedriver: file path to chrome driver
    '''
    projectLinks = list()
    for year in years:
        print "Extracting year:" + str(year)
        driver = webdriver.Chrome(chromedriver)
        loadWeb(driver, url = requestURLprefix + str(year), year = str(year))
        projectLinks += project_href(driver, webURL, tagn = "span", classn = "sans-serif strong")
        '''get the last page's url, get the max page number'''
        last_page_number, pageURL_prefix = max_page_no (driver, last_link_text = "Last")
        driver.close()
        driver.quit()
        '''open each dynamic web page, coded in JavaScript and get the links for each project'''
        for page in range(84, int(last_page_number) + 1):  # Should be range(1, int(last_page_number) +1), range(84, int(last_page_number) +1) is to make the testing faster
            driver = webdriver.Chrome(chromedriver)
            loadWeb(driver = driver, url = pageURL_prefix + str(page))
            projectLinks += project_href(driver, webURL, tagn = "span", classn = "sans-serif strong")
            print "Current total project links: " + str(len(projectLinks))
            driver.close()
            driver.quit()
    scrapHTML(set(projectLinks), outfp, headers)

if __name__ == "__main__":
    print "Starts at ",
    print datetime.datetime.now()
    chromedriver = "/Users/linliu/Downloads/chromedriver" #raw_input("Type the file path of Chrome driver \n") #"/Users/linliu/Downloads/chromedriver"
    print chromedriver
    webURL = "http://www.gatesfoundation.org"
    requestURL1 = "http://www.gatesfoundation.org/How-We-Work/Quick-Links/Grants-Database#q/k="
    scrap(webURL, range(2009, 2010), requestURL1, \
    "BMF.txt", ["Date", "Institute","Program", "Amount", "Topic", "Purpose"], chromedriver)  # I used range(2009, 2010) for testing phase
    print "Ends at ",
    print datetime.datetime.now()
