from bs4 import BeautifulSoup
import requests
import sys
import re

for nu in range(1,854):
    url =requests.get("http://www.mjafi.net/action/doSearch?journalCode=mjafi&searchText1=india&occurrences1=all&op1=and&searchText2=&occurrences2=all&catSelect=prod&prodVal=HA&date=range&dateRange=&searchAttempt=-346569843&searchType=advanced&doSearch=Search&contentType=articles&rows=100&startPage={}".format(nu,"#navigation"))
    #url = urlopen(req)
    soup = BeautifulSoup(url.text, 'lxml')
    #print(soup)
    for h2 in soup.find_all('h2', attrs={'class':'title'}):
        a_tag=h2.find_all('a')[1]['href']
        href="http://www.mjafi.net{}".format(a_tag)
        print(href)
