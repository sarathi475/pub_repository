from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import sys
import re
import json
from almamater import out

# USAGE :
# 	python3 bmc_parser.py

#SAMPLE OUTPUT


def remove_whitespace(raw):
    string = str(raw)
    string = string.replace("\n", "")
    string = re.sub(' +', ' ', string)
    return string


def country_part(ins):
    # regular expression for country name
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

    def article_type(soup):
        '''
        Parse article_type for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            article_type= tag.find('meta',attrs={'name':'citation_article_type'})
            if article_type != None:
                article_type=article_type['content']
                return article_type
            else:
                article_type=""
                return article_type


    def access_type(soup):
        '''
        Parse article_type for the given article URL Element
        '''
        for tag in soup.find_all('div', attrs={'class':'OpenAccessLabel'}):
            if tag != None:
                access_type = tag.get_text()
                return access_type
            else:
                access_type = ""
                return access_type


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


    def doi(soup):
        '''
        Parse doi for the given article URL Element
        '''
        try:
            for tag in soup.find_all('head'):
                doi=tag.find('meta',attrs={'name':'citation_doi'})
                if doi != None:
                    doi=doi['content']
                    return doi
                else:
                    doi=""
                    return doi
        except:
            for tag in soup.find_all('head'):
                doi=tag.find('meta',attrs={'name':'DOI'})
                if doi != None:
                    doi=doi['content']
                    return doi
                else:
                    doi=""
                    return doi


    def title(soup):
        '''
        Parse title for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            title = tag.find('meta',attrs={'name':'citation_title'})['content']
            return title


    def author(soup):
        '''
        Parse author for the given article URL Element
        '''
        author = []
        for meta in soup.find_all('meta',attrs={'name':'citation_author'}):
            au=meta['content']
            author.append(au)
        return author

    def institute(soup):
        '''
        Parse institute for the given article URL Element
        '''
        institute = []
        for meta in soup.find_all('meta',attrs={'name':'citation_author_institution'}):
            inst=meta['content']
            institute.append(inst)
        return institute


    def find_institute(aff):
        inst = []
        ind = re.compile(r"India", re.IGNORECASE)
        aff_text = aff.lstrip('0123456789')
        #aff_text = remove_whitespace(aff_text)
        #print(aff_text)
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
        authors = Article.author(soup)
        institutes = Article.institute(soup)

        authors_list=[]
        if len(institutes)>=1:
            for a, au in enumerate(authors):
                for i, inst in enumerate(institutes):
                    if (a==i):
                        author = {}
                        #print(name, ins[n])
                        author['surname'] = au
                        author['given_name'] = ""
                        author['degree'] = ""
                        author['email'] = ""
                        author['orcid'] = ""
                        author['institute'] = Article.find_institute(inst)

                        authors_list.append(author)

        else:
            pass

        return authors_list


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
            issue= tag.find('meta', attrs={'name':'citation_issue'})
            if issue != None:
                issue=issue['content']
                return issue
            else:
                issue=""
                return issue


    def pageno(soup):
        '''
        Parse pageno for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            pageno= tag.find('meta',attrs={'name':'citation_firstpage'})
            if pageno!= None:
                pageno=pageno['content']
                return pageno
            else:
                pageno=""
                return pageno


    def publication_date(soup):
        '''
        Parse publication_date for the given article URL Element
        '''
        try:
            for tag in soup.find_all('head'):
                publication_date= tag.find('meta',attrs={'name':'citation_online_date'})
                if publication_date != None:
                    publication_date=publication_date['content']
                    publication_date=publication_date.replace('/','-')
                    return publication_date
                else:
                    publication_date=""
                    return publication_date
        except:
            for tag in soup.find_all('head'):
                publication_date= tag.find('meta',attrs={'name':'citation_publication_date'})
                if publication_date != None:
                    publication_date=publication_date['content']
                    publication_date=publication_date.replace('/','-')
                    return publication_date
                else:
                    publication_date=""
                    return publication_date


    def abstract(soup):
        '''
        Parse  abstract for the given article URL Element
        '''
        try:
            for tag in soup.find_all('head'):
                abstract=tag.find('meta',attrs={'name':'citation_abstract'})
                if abstract != None:
                    abstract=abstract['content']
                    return abstract
                else:
                    abstract=""
                    return abstract

        except:
            for tag in soup.find_all('head'):
                abstract=tag.find('meta',attrs={'name':'dc.description'})
                if abstract != None:
                    abstract=abstract['content']
                    return abstract
                else:
                    abstract=""
                    return abstract


    def keywords(soup):
        '''
        Parse  keywords for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            key=tag.find('meta',attrs={'name':'citation_keywords'})
            if key != None:
                keywords=key['content']
                return keywords
            else:
                keywords=[]
                for tag in soup.find_all('body'):
                    for span in tag.find_all('span', attrs={'class':'Keyword'}):
                        #print(span)
                        kwrd=span.get_text()
                        keywords.append(kwrd)

                return  ", ".join(keywords)



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


    def main(url):
        soup = BeautifulSoup(url,'lxml')

        article={}
        article['pub_type'] = Article.article_type(soup)
        article['access_type'] = Article.access_type(soup)
        article['journal'] = Article.journal_title(soup)
        article['doi'] = Article.doi(soup)
        article['pmid'] = ""
        article['pmc'] = ""
        article['title'] = Article.title(soup)
        article['authors'] = Article.auth_inst(soup)
        article['volume'] = Article.volume(soup)
        article['issue'] = Article.issue(soup)
        article['pagenum'] = Article.pageno(soup)
        article['date_received'] = None
        article['date_accepted'] = None
        article['date_published'] = Article.publication_date(soup)
        article['abstract_text'] = Article.abstract(soup)
        article['keywords'] = Article.keywords(soup)
        article['pdf_url'] = Article.pdf_link(soup)
        article['html_url'] = Article.html_url(soup)
        #article['full_text'] =Article.full_text(soup)


        return article



if __name__ == "__main__":

    """ [test url: "https://molecularcytogenetics.biomedcentral.com/articles/10.1186/1755-8166-7-S1-I30" ] """
    url_input = sys.argv[1]
    files=Request(url_input, headers={'User-Agent':'Mozilla/5.0'})
    url=urlopen(files)
    result = Article.main(url)
    doi = result['doi']
    if len(doi) > 0:
        doi = "json/" + doi.replace("/", "-")
        #print(result)
        output = doi + '.json'
        print("Writing...!", output)
        with open(output, 'w') as fp:
            json.dump(result, fp)
    else:
        name = sys.argv[1]
        d = name.split('/articles/')
        doi = d[1]
        #print(result)
        doi = doi.replace("/", "-")
        output = "json/" + doi + '.json'
        print("Writing...!", output)
        with open(output, 'w') as fp:
            json.dump(result, fp)
