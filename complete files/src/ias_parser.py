from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import sys
import re
import json
from almamater import out
from datetime import datetime
from time import strptime
from datetime import date
from geotext import GeoText
import codecs
from googletrans import Translator

translator = Translator()
# USAGE :
# 	python3 ias_parser.py

#SAMPLE OUTPUT
"""
{'pub_type': 'Journal Article', 'access_type': '', 'journal': 'Journal of Biosciences', 'doi': '', 'pmid': '', 'pmc': '', 'title': 'Target-specific delivery of doxorubicin to human glioblastoma cell line via ssDNA aptamer', 'authors': [{'name': 'ABDULLAH TAHIR BAYRAC¸', 'institute': [[{'apid': '', 'federation': '', 'acronym': '', 'address': 'Department of Bioengineering, Karamanog˘lu Mehmetbey University, Karaman, Turkey.', 'city': '', 'district': '', 'state': '', 'country': 'Turkey.', 'name': 'Karamanog˘lu Mehmetbey University'}]]}, {'name': 'OYA ERCAN AKC¸A', 'institute': [[{'apid': '', 'federation': '', 'acronym': '', 'address': 'Department of Molecular Biology and Genetics, Harran University, Sanlıurfa, Turkey.', 'city': '', 'district': '', 'state': '', 'country': 'Turkey.', 'name': 'Harran University'}]]}, {'name': 'FU¨ SUN I˙NCI EYIDOG˘ AN', 'institute': [[{'apid': '', 'federation': '', 'acronym': '', 'address': 'Department of Elementary Education, Baskent University, Ankara, Turkey.', 'city': '', 'district': '', 'state': '', 'country': 'Turkey.', 'name': 'Baskent University'}]]}, {'name': 'HU¨ SEYIN AVNI O¨ KTEM', 'institute': [[{'apid': '', 'federation': '', 'acronym': '', 'address': 'Department of Biological Sciences, Middle East Technical University, Ankara, Turkey.', 'city': '', 'district': '', 'state': '', 'country': 'Turkey.', 'name': 'Middle East Technical University'}], [{'apid': '', 'federation': '', 'acronym': '', 'address': 'Nanobiz R&D Ltd., Gallium Bld. No.18, METU Science Park, Ankara, Turkey.', 'city': '', 'district': '', 'state': '', 'country': 'Ltd.', 'name': 'Nanobiz R&D Ltd.'}]]}], 'volume': '43', 'issue': '1', 'pagenum': '97-104', 'date_received': None, 'date_accepted': None, 'date_published': '2018-03-01', 'abstract_text': 'Targeted drug delivery approaches have been implementing significant therapeutic gain for cancer treatment since lastdecades. Aptamers are one of the mostly used and highly selective targeting agents for cancer cells. Herein, we address anano-sized targeted drug delivery approach adorned with A-172 glioblastoma cell-line-specific single stranded DNA(ssDNA) aptamer in which the chemotherapeutic agent Doxorubicin (DOX) had been conjugated. DNA aptamer, GMT-3,was previously selected for specific recognition of glioblastoma and represented many advantageous characteristics for drugtargeting purposes. Flow cytometry analysis proved the binding efficiency of the specific aptamer to tumour cell lines. Celltype-specific toxicity of GMT-3:DOX complex was showed by XTT assay and terminated cytotoxic effects were screenedfor both target cell and a control breast cancer cell line. The result of this contribution demonstrated the potential utility ofGMT-3 aptamer-mediated therapeutic drug transportation in the treatment of gliomas specifically. It was concluded thataptamer-mediated drug delivery can be applied successfully for clinical use.', 'keywords': 'A-172; aptamer; doxorubicin; glioblastoma; GMT-3; XTT', 'pdf_url': 'http://www.ias.ac.in/article/fulltext/jbsc/043/01/0097-0104', 'html_url': 'http://www.ias.ac.in/describe/article/jbsc/043/01/0097-0104'}
"""


def remove_whitespace(raw):
    string = str(raw)
    string = string.replace("\n", "")
    string = re.sub(' +', ' ', string)
    return string

def country_part(ins):
    # regular expression for country name
    con = re.compile(r"[A-Z][\w]+\.")
    try:
        countries = GeoText(ins).countries
        #print(countries)
        country = countries[0]
        return country

    except:
        match = re.search(con, ins)
        if match:
            country = match.group(0)
            return country
        else:
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
        for tag in soup.find_all('div',attrs={'class':'col-padded col-shaded'}):
            journal_title = tag.find('h1',attrs={'class':'title-widget'})
            if journal_title != None:
                journal_title=journal_title.get_text()
                #print(journal_title)
                return journal_title
            else:
                journal_title=""
                return journal_title


    def title(soup):
        '''
        Parse title for the given article URL Element
        '''
        for tag in soup.find_all('body'):
            li=tag.find('li',attrs={'class':'journal-article'})
            title = li.find('p',attrs={'class':'journal-article-title gap-below'}).get_text()
            return title

    def find_institute(aff):
        ind = re.compile(r"India", re.IGNORECASE)
        aff_text = aff.lstrip('0123456789')
        #aff_text = remove_whitespace(aff_text)
        #print(aff_text)
        india = re.search(ind, aff_text)
        if india:
            institute = out(aff_text)
            return institute
        else:
            aff_text = aff_text+"."
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
            return institute


    def institute(soup):

        '''
        Parse institute for the given article URL Element
        '''
        institute=[]
        for tag in soup.find_all('body'):
            for div in tag.find_all('div',attrs={'class':'recent-news-text clear-margins'}):
                for ol in div.find_all('ol'):
                    for li in ol.find_all('li'):
                        insti=li.get_text()
                        new=translator.translate(insti)
                        institute.append(new.text)

        #print(institute)
        return institute

    def author(soup):
        '''
        Parse author for the given article URL Element
        '''
        #print(institutes)
        author_list=[]
        for div in soup.find_all('p',attrs={'class':'journal-article-affiliation'}):
            for span in div.find_all('span'):
                author={}
                author['supse']=[]
                for auth in span.find('a'):
                    #print(auth)
                    new=translator.translate(auth)
                    author['name']=new.text
                    #print(auths)
                    #author['name']=auths
                for sup in span.find_all('sup'):
                    sups=sup.get_text().strip()
                    if sups=='1':
                        author['supse'].append(0)
                    elif sups=='2':
                        author['supse'].append(1)
                    elif sups=='3':
                        author['supse'].append(2)
                    elif sups=='4':
                        author['supse'].append(3)
                    elif sups=='5':
                        author['supse'].append(4)
                    elif sups=='6':
                        author['supse'].append(5)
                    elif sups=='7':
                        author['supse'].append(6)
                    elif sups=='8':
                        author['supse'].append(7)
                    elif sups=='9':
                        author['supse'].append(8)
                    elif sups=='10':
                        author['supse'].append(9)
                    else:
                        pass


                author_list.append(author)
        #print(author_list)
        return author_list

    def	auth_inst(soup):
        '''
        Parse auth_inst for the given article URL Element
        '''
        authors_list=[]
        authors=Article.author(soup)
        institutes= Article.institute(soup)
        #print("RETURNED", authors)
        #print("RETURNED", institutes)
        for author in authors:
            authors={}
            authors['surname']=author['name']
            authors['given_name'] = ""
            authors['degree'] = ""
            authors['email'] = ""
            authors['orcid'] = ""
            authors['institute']=[]
            for id in author['supse']:
                inst=institutes[id]
                found_inst=country_part(inst)
                #print(found_inst)
                if "WORLD" in found_inst:
                    institute = out(inst)
                    authors['institute'].append(institute)
                else:
                    institute =Article.find_institute(inst)
                    authors['institute'].append(institute)

                #print(author['name'],author['supse'])
            authors_list.append(authors)

        #print (authors_list)
        return authors_list

    def volume(soup):
        '''
        Parse volume for the given article URL Element
        '''
        for tag in soup.find_all('body'):
            div=tag.find('div',attrs={'class':'journal-article-meta'})
            span= div.find('span',attrs={'class':'journal-article-meta-volume'}).get_text()
            volume=span.replace('Volume','').strip()
            if volume!= None:
                #print(volume)
                return volume
            else:
                volume=""
                return volume

    def issue(soup):
        '''
        Parse issue for the given article URL Element
        '''
        for tag in soup.find_all('body'):
            div=tag.find('div',attrs={'class':'journal-article-meta'})
            span= div.find('span',attrs={'class':'journal-article-meta-issue'}).get_text()
            issue=span.replace('Issue','').strip()
            if issue!= None:
                #print(issue)
                return  issue
            else:
                issue=""
                return issue


    def firstpage(soup):
        '''
        Parse firstpage for the given article URL Element
        '''
        for tag in soup.find_all('body'):
            div=tag.find('div',attrs={'class':'journal-article-meta'})
            span= div.find('span',attrs={'class':'journal-article-meta-page'}).get_text()
            #print (span)
            firstpage=span.replace('pp','').strip()
            if "Article ID" in firstpage:
                firstpage=""
                return firstpage
            elif firstpage!= None:
                #print(firstpage)
                return firstpage
            else:

                firstpage=""
                return firstpage

    def publication_date(soup):
        '''
        Parse publication_date for the given article URL Element
        '''
        for tag in soup.find_all('body'):
            div=tag.find('div',attrs={'class':'journal-article-meta'})
            dates= div.find('span',attrs={'class':'journal-article-meta-date'}).get_text()
            #print (span)
            if dates!=None:
                date=dates.split(" ")
                day="01"
                month=date[0]
                year=date[1]
                dat="-".join([year,month,day])
                #print(dat)
                pub_date=datetime.strptime(dat, '%Y-%B-%d').date()
                #print(pub_date)
                return str(pub_date)
            else:
                pub_date=""

                return pub_date

    def keywords(soup):
        '''
        Parse keywords for the given article URL Element
        '''
        try:
            li_tag= soup.find_all('li',attrs={'class':'journal-article-details'})[1]
            h1=li_tag.find('h1',attrs={'class':'title-median'})
            key=h1.get_text()
            if key=="Keywords":
                keywords= li_tag.find('div',attrs={'class':'recent-news-text clear-margins'}).get_text().strip()
                #print(keywords)
                return keywords
            else:
                keywords=""
                #print(keywords)
                return keywords
        except:

            keywords=""
            #print(keywords)
            return keywords

    def abstract(soup):
        '''
        Parse abstract for the given article URL Element
        '''
        try:
            li_tag= soup.find_all('li',attrs={'class':'journal-article-details'})[2]
            h1=li_tag.find('h1',attrs={'class':'title-median'})
            abst=h1.get_text()
            if abst=="Abstract":
                abstract= li_tag.find('div',attrs={'class':'recent-news-text clear-margins'}).get_text().strip()
                #print(abstract)
                return abstract
            else:
                abstract=""
                return abstract
        except:
            abstract=""
            return abstract

    def pdf_link(soup):
        '''
        Parse pdf_link for the given article URL Element
        '''
        for tag in soup.find_all('body'):
            div= tag.find('div',attrs={'class':'recent-news-text clear-margins'})
            p=div.find('p')
            span= p.find('span',attrs={'class':'text-primary'})
            pdf_link=span.find('a')['href']
            #print (pdf_link)
            if pdf_link != None:
                pdf_link=pdf_link
                return pdf_link
            else:
                pdf_link=""
                return pdf_link

    def html_url(url_input):
        '''
        Parse html_url for the given article URL Element
        '''
        if url_input != None:
            html_url=url_input
            return html_url
        else:
            html_url=""
            return html_url



    def output_dict(url,url_input):
        soup = BeautifulSoup(url,'lxml')
        article={}
        article['pub_type'] = "Journal Article"
        article['access_type'] = ""
        article['journal'] = Article.journal_title(soup)
        article['doi'] = ""
        article['pmid'] =""
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
        article['pdf_url'] = Article.pdf_link(soup)
        article['html_url'] = Article.html_url(url_input)
        #article['full_text'] =Article.full_text(soup)

        return article



if __name__ == "__main__":

    #sample input
    """http://www.ias.ac.in/describe/article/boms/041/01/0002"""
    """http://www.ias.ac.in/describe/article/jbsc/037/05/0911-0919
        http://www.ias.ac.in/describe/article/reso/005/04/0121-0122"""

    url_input = sys.argv[1]
    files=Request(url_input, headers={'User-Agent':'Mozilla/5.0'})
    url=urlopen(files)
    result = Article.output_dict(url,url_input)
    #print(result)
    authors=result['authors']
    if 	len(authors) > 0:
        name = sys.argv[1]
        d = name.split('/article/')
        doi = d[1]
        #print(result)
        doi = doi.replace("/", "-")
        output = "json/" + doi + '.json'
        print("Writing...!", output)
        with open(output, mode='w') as fp:

            json.dump(result, fp)

    else:
        pass
