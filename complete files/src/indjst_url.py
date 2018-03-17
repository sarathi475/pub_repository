from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import sys
import re
main_link=Request("http://www.indjst.org/index.php/indjst/issue/archive", headers = {'User-Agent':'Mozilla/5.0'})
link = urlopen(main_link)
soup = BeautifulSoup(link,'lxml')
#print(soup)
for tag in soup.find_all('div', attrs = {'id':'issue'}):
    href=tag.find('a')['href']
    #print(href)
    link1 = urlopen(href)
    soup1 = BeautifulSoup(link1,'lxml')
    #print(soup1)
    for td in soup1.find_all('td',attrs = {'class':'tocTitle'}):
        href2=td.find('a')['href']
        print(href2)
    
    
    
		
	
