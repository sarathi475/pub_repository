#!/usr/bin/env python3

import sys
import re
import json
from bs4 import BeautifulSoup
import requests
from almamater import out
from geotext import GeoText

# USAGE :
# 	python3 mjafi_parser.py

#SAMPLE OUTPUT
#cities  = json.load(open('data/cities.json', 'r'))

def remove_whitespace(raw):
    string = str(raw)
    string = string.replace("\n", "")
    string = re.sub(' +', ' ', string)
    return string


def country_part(ins):
    # regular expression for country name
    countries = GeoText(ins).countries
    if countries:
        return countries[0]

    else:
        con   = re.compile(r"[A-Z][\w]+\.")
        country = "WORLD"
        try:
            match = re.search(con, ins)
            if match:
                country = match.group(0)
            return country
        except:
            country = "WORLD"

        return country



def name_part(ins):
    insp  = re.compile(r"institute|Laboratory|centre|college|Research|Foundation|university|vidya|Kalamandalam|Facility|academy|Ltd|hospital|Medical School|Istituto|Scientifico|Technology|Research|Technical", re.IGNORECASE)
    num = re.compile(r"[0-9]+\.")
    mail = re.compile(r"Electronic Address: [a-z][\w][@][a-z][\w]+\.")
    #name = re.sub(con, "", ins.strip())
    name = re.sub(mail, "", ins.strip())
    name = re.sub(num, "", ins.strip())
    parts = ins.split(',')

    for part in parts:
        m = re.search(insp, part)
        if m:
            name = part.strip()

    return name


class Article:

    def journal_title(soup):
        '''
        Parse journal_title for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            journal_title = tag.find('meta',attrs={'name':'citation_journal_title'})
            if journal_title != None:
                journal_title=journal_title['content']
                return journal_title
            else:
                journal_title=""
                return journal_title


    def title(soup):
        '''
        Parse title for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            title = tag.find('meta',attrs={'name':'citation_title'})
            if title != None:
                title=title['content']
                return title
            else:
                for tag in soup.find_all('head'):
                    title= tag.find('meta',attrs={'property':'og:title"'})
                    if title != None:
                        title=title['content']
                        return title
                    else:
                        title=""
                        return title




    def doi(soup):
        '''
        Parse doi for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            doi = tag.find('meta',attrs={'name':'citation_doi'})
            if doi != None:
                doi=doi['content']
                return doi
            else:
                doi=""
                return doi


    def keywords(soup):
        '''
        Parse keywords for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            keywords= tag.find('meta',attrs={'name':'citation_keywords'})
            if keywords != None:
                keywords=keywords['content']
                return keywords
            else:
                keywords=""
                return keywords


    def volume(soup):
        '''
        Parse volume for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            volume= tag.find('meta',attrs={'name':'citation_volume'})
            if volume != None:
                volume=volume['content']
                return volume
            else:
                volume=""
                return volume


    def issue(soup):
        '''
        Parse issue for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            issue= tag.find('meta',attrs={'name':'citation_issue'})
            if issue != None:
                issue=issue['content']
                return issue
            else:
                issue=""
                return issue


    def articletype(soup):
        '''
        Parse publication_date for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            articletype= tag.find('meta',attrs={'property':'og:type'})

            if articletype != None:
                articletype=articletype['content']
                return articletype
            else:
                articletype=""
                return articletype


    def publication_date(soup):
        '''
        Parse publication_date for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            publication_date= tag.find('meta',attrs={'name':'citation_date'})

            if publication_date != None:
                publication_date=publication_date['content']
                publication_date=publication_date.replace('/','-')
                return publication_date
            else:
                publication_date = None
                return publication_date


    def firstpage(soup):
        '''
        Parse firstpage for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            firstpage= tag.find('meta',attrs={'name':'citation_firstpage'})
            if firstpage != None:
                firstpage=firstpage['content']
                return firstpage
            else:
                firstpage=""
                return firstpage



    def abstract(soup):
        '''
        Parse abstract for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            abstract= tag.find('meta',attrs={'property':'og:description'})
            if abstract != None:
                abstract=abstract['content']
                return abstract
            else:
                for tag in soup.find_all('head'):
                    abstract= tag.find('meta',attrs={'name':'citation_abstract'})
                    if abstract != None:
                        abstract=abstract['content']
                        return abstract
                    else:

                        abstract=""
                        return abstract




    def pdf_link(soup):
        '''
        Parse pdf_link for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            pdf_link= tag.find('meta',attrs={'name':'citation_pdf_url'})
            if pdf_link != None:
                pdf_link=pdf_link['content']
                return pdf_link
            else:
                pdf_link=""
                return pdf_link

    def html_url(soup):
        '''
        Parse fulltext_html_url for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            fulltext_html_url= tag.find('meta',attrs={'name':'citation_fulltext_html_url'})
            if fulltext_html_url != None:
                fulltext_html_url=fulltext_html_url['content']
                return fulltext_html_url
            else:
                fulltext_html_url=""
                return fulltext_html_url


    def author(soup):
        '''
        Parse author for the given article URL Element
        '''
        author = []
        for meta in soup.find_all('meta',attrs={'name':'citation_author'}):
            auth=meta['content']
            author.append(auth)
        return author

    def institute(soup):
        '''
        Parse institute for the given article URL Element
        '''
        inst = []
        for tag in soup.find_all('body'):
            insti= tag.find('div',attrs={'class':'affiliation'})
            if insti != None:
                institute=insti.get_text()
                # print(institute)

                inst.append(institute)
            else:
                for tag in soup.find_all('head'):
                    institute= tag.find('meta',attrs={'name':'citation_author_institution'})
                    if institute != None:
                        institute=institute['content']
                        inst.append(institute)
        return inst


    def find_institute(aff):

        inst = []
        ind = re.compile(r"India", re.IGNORECASE)
        aff_text = aff.lstrip('0123456789')

        india = re.search(ind, aff_text)
        if india:
            institute = out(aff_text)
            inst.append(institute)

        else:
            aff_text = aff+"."
            institute={}
            institute['apid']      = ""
            institute['federation']= ""
            institute['acronym']   = ""
            institute['address']   = aff_text
            institute['city']      = ""
            institute['district']  = ""
            institute['state']     = ""
            institute['country']   = country_part(aff_text)
            institute['name']      = name_part(aff_text)

            inst.append(institute)
        return inst

    def auth_inst(soup):
        '''
        Parse auth_inst for the given article URL Element
        '''

        auth = Article.author(soup)
        ins = Article.institute(soup)
        authors_list=[]
        if len(auth) == len(ins):
            for a, au in enumerate(auth):
                for i, inst in enumerate(ins):
                    if (a==i):
                        author = {}
                        author['surname'] = au
                        author['given_name'] = ""
                        author['degree'] = ""
                        author['email'] = ""
                        author['orcid'] = ""
                        author['institute'] = Article.find_institute(inst)
                        authors_list.append(author)
        elif len(ins) == 1:
            for a, au in enumerate(auth):
                author = {}
                author['surname'] = au
                author['given_name'] = ""
                author['degree'] = ""
                author['email'] = ""
                author['orcid'] = ""
                author['institute'] = Article.find_institute(ins[0])
                authors_list.append(author)
        else:
            pass

        return authors_list

    def main(url):
        soup = BeautifulSoup(url.text,'lxml')
        #print(soup)
        article={}
        article['pub_type'] =Article.articletype(soup)
        article['access_type'] =""
        article['journal'] = Article.journal_title(soup)
        article['doi'] = Article.doi(soup)
        article['pmid'] = ""
        article['pmc'] = ""
        article['title'] = Article.title(soup)
        article['authors'] = Article.auth_inst(soup)
        article['volume'] = Article.volume(soup)
        article['issue'] = Article.issue(soup)
        article['pagenum'] = Article.firstpage(soup)
        article['date_received'] = None
        article['date_accepted'] = None
        article['date_published'] = Article.publication_date(soup)
        article['abstract_text'] = Article.abstract(soup)
        article['keywords'] = Article.keywords(soup)
        #article['pdf_url'] = Article.pdf_link(soup)
        #article['html_url'] = Article.html_url(soup)

        return article



if __name__ == "__main__":

    url_input = sys.argv[1]
    url=requests.get(url_input)
    result = Article.main(url)
    #print(result)

    doi = result['doi']
    if doi != None:
        doi = "json/" + doi.replace("/", "-")
        #print(result)
        output = doi + '.json'
        print("Writing...!", output)
        with open(output, 'w') as fp:
            json.dump(result, fp)
    else:

        doi = sys.argv[1].replace("http://www.mjafi.net/article/", "")
        doi =doi.replace('/', "")
        doi =doi.replace('(', "")
        doi =doi.replace(')', "")
        #print(result)
        output = doi + '.json'
        print("Writing...!", output)
        with open(output, 'w') as fp:
            json.dump(result, fp)
