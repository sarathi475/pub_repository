from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import sys

mainlink =sys.argv[1]
journal=mainlink
link = urlopen(journal)
soup = BeautifulSoup(link,'lxml')
for body in soup.find_all('body'): 
    a=body.find('a',attrs={'id':'browse-volumes-and-issues'})
    vol=a.get('href')
    volume="https://link.springer.com{}".format(vol)
    #volume list
    #print(volume)
    #volume=Request("https://link.springer.com/journal/volumesAndIssues/10765")
    link2 = urlopen(volume)
    soup2 = BeautifulSoup(link2,'lxml')
    body = soup2.find('body')
    for a in body.find_all('a',attrs={'class':'title'}):
        #print(a)
        vol_list=a.get('href')
        volumes="https://link.springer.com{}".format(vol_list)
        #volume list_all
        #print(volumes)
        link3 = urlopen(volumes)
        soup3 = BeautifulSoup(link3,'lxml')
        body2 = soup3.find('body')
        #print(body2)
        for h3 in body2.find_all('h3',attrs={'class':'title'}):
            #print(h3)
            lists=h3.find('a')['href']
            #print(lists)
            vol_data="https://link.springer.com{}".format(lists)
            #volume list_all
            print(vol_data)
                
