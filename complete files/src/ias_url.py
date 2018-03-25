from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import sys


mainlink =sys.argv[1]
journal=mainlink
link = urlopen(journal)
soup = BeautifulSoup(link,'lxml')
for body in soup.find_all('body'): 
    for ul in body.find_all('ul',attrs={'class':'journal-menu'}):
        li=ul.find_all('li')[1]
        a=li.find('a')
        #print(a)
        href=a.get('href')
        #print(href)
        link2 = urlopen(href)
        soup2 = BeautifulSoup(link2,'lxml')
        for tag in soup2.find_all('ul',attrs={'class':'journal-article-issues list-unstyled list-inline'}):
            for li in tag.find_all('li'):
                
                ai=li.find('a')
                href2=ai.get('href')
                #print(href2)
                link3 = urlopen(href2)
                soup3 = BeautifulSoup(link3,'lxml')
                for tag in soup3.find_all('li',attrs={'class':'journal-article-list'}):
                    for li in tag.find_all('p',attrs={'class':'journal-article-list-title'}):
                        
                
                        a2=li.find('a')
                        href3=a2.get('href')
                        print(href3)
