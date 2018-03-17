from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import sys

main_link=Request("http://www.ijpsonline.com/archive.html",headers={'User-Agent':'Mozilla/5.0'})
link=urlopen(main_link)
soup=BeautifulSoup(link,'lxml')
#print (soup)
for li in soup.find_all('li',attrs={'class':'col-xs-4'}):
    a=li.find('a')['href']
    href="http://www.ijpsonline.com/{}".format(a)
    #print(href)
    link1=Request(href,headers={'User-Agent':'Mozilla/5.0'})
    url=urlopen(link1)
    soup1=BeautifulSoup(url,'lxml')
    #print (soup1)
    for h2 in soup1.find_all('h2',attrs={'class':'post-title'}):
        href2=h2.find('a')['href']
        print(href2)

