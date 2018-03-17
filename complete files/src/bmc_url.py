from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import sys

href =sys.argv[1]
journal="{}{}".format(href,"/articles")
#print(journal)
link = urlopen(journal)
soup1 = BeautifulSoup(link,'lxml')
for span in soup1.find_all('span',attrs={'class':'c-search-navbar__pagination-label'})[0]:
    if span!=None:
        page=span.split('of')
        del page[0]
        #print (page)
        page_num=''.join(page)
        page_number=int(page_num)+1
        #print (page_number)
        for no in range(1,page_number):
            main_link=("{}{}{}".format(journal,"?searchType=journalSearch&sort=PubDate&page=",no))
            #print(main_link)
            link2 = urlopen(main_link)
            soup2 = BeautifulSoup(link2,'lxml')
            #print(soup2)
            for h3 in soup2.find_all('h3',attrs={'class':'c-teaser__title'}):
                a=h3.find('a')['href']
                url="{}{}".format(href,a)
                print (url)
    else:
        pass
            
