from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import sys
import re
import json
import parse_json
from parse_json import Institute, Federation, Main
from almamater import out

# USAGE :
# 	python3 ijpsonline_parser.py

#SAMPLE OUTPUT

"""{'pub_type': '', 'access_type': '', 'journal': 'Indian Journal of Pharmaceutical Sciences', 'doi': '10.4172/pharmaceutical-sciences.1000328', 'pmid': '', 'pmc': '', 'title': 'Design and Synthesis of New Bioactive 1,2,4-Triazoles, Potential Antitubercular and Antimicrobial Agents', 'authors': [{'surname': 'R. Singh', 'given_name': ' ', 'degree': ' ', 'email': ' ', 'orcid': ' ', 'institute': {'apid': 'APINS00717', 'name': 'Indian Council of Medical Research (ICMR), New Delhi', 'acronym': 'ICMR', 'federation': 'ICMR', 'city': 'New Delhi', 'state': 'New Delhi', 'country': 'India.'}}, {'surname': 'S. K. Kashaw', 'given_name': ' ', 'degree': ' ', 'email': ' ', 'orcid': ' ', 'institute': {'apid': 'APINS00717', 'name': 'Indian Council of Medical Research (ICMR), New Delhi', 'acronym': 'ICMR', 'federation': 'ICMR', 'city': 'New Delhi', 'state': 'New Delhi', 'country': 'India.'}}, {'surname': 'V. K. Mishra', 'given_name': ' ', 'degree': ' ', 'email': ' ', 'orcid': ' ', 'institute': {'apid': 'APINS00717', 'name': 'Indian Council of Medical Research (ICMR), New Delhi', 'acronym': 'ICMR', 'federation': 'ICMR', 'city': 'New Delhi', 'state': 'New Delhi', 'country': 'India.'}}, {'surname': 'M. Mishra', 'given_name': ' ', 'degree': ' ', 'email': ' ', 'orcid': ' ', 'institute': {'apid': 'APINS00717', 'name': 'Indian Council of Medical Research (ICMR), New Delhi', 'acronym': 'ICMR', 'federation': 'ICMR', 'city': 'New Delhi', 'state': 'New Delhi', 'country': 'India.'}}, {'surname': 'V. Rajoriya', 'given_name': ' ', 'degree': ' ', 'email': ' ', 'orcid': ' ', 'institute': {'apid': 'APINS00717', 'name': 'Indian Council of Medical Research (ICMR), New Delhi', 'acronym': 'ICMR', 'federation': 'ICMR', 'city': 'New Delhi', 'state': 'New Delhi', 'country': 'India.'}}, {'surname': 'V.  Kashaw1', 'given_name': ' ', 'degree': ' ', 'email': ' ', 'orcid': ' ', 'institute': {'apid': 'APINS00717', 'name': 'Indian Council of Medical Research (ICMR), New Delhi', 'acronym': 'ICMR', 'federation': 'ICMR', 'city': 'New Delhi', 'state': 'New Delhi', 'country': 'India.'}}], 'volume': '80', 'issue': '1', 'Firstpage': '36', 'Lastpage': '45', 'date_received': '', 'date_accepted': '', 'date_published': '2018-02-01', 'abstract': 'A New series of 1,2,4-triazole derivatives were synthesized using appropriate synthetic route and structures were confirmed by infrared spectroscopy, proton nuclear magnetic resonance, carbon-13 nuclear magnetic resonance, mass spectroscopy and elemental analysis. Antimycobacterial activity of the synthesized compounds (1-12) was carried out and percent reduction in relative light units was calculated using luciferase reporter phage assay. Percent reduction in relative light units for isoniazid was also calculated. The test compounds showed significant antitubercular potential against Mycobacterium tuberculosis H37Rv and clinical isolates, S, H, R and E resistant M. tuberculosis, when tested in vitro. Compound 8 and 12 showed better antitubercular activity compared to reference isoniazid against M. tuberculosis H37Rv strain while compounds 5, 8 and 12 found superior to isoniazid against clinical isolates: S, H, R and E resistant M. tuberculosis. Synthesized compounds were also tested in vitro against representative bacterial and fungal strains. Tested compounds showed better antibacterial activities (minimum inhibitory concentration) against Gram-positive bacteria compared to Gram-negative. Compound 5 showed better antibacterial activity than ampicillin against B. subtilis. Compound 12 in the series displayed most potent antifungal activity, which was comparable to reference fluconazole against both the fungal strains.', 'keywords': '1,2,4-Triazole, antibacterial, antimicrobial activity, Schiff base, isoniazid, LRP assay, Mycobacterium tuberculosis, thiol group', 'pdf_url': 'http://www.ijpsonline.com/articles/design-and-synthesis-of-new-bioactive-124triazoles-potential-antitubercular-and-antimicrobial-agents.pdf', 'html_url': 'http://www.ijpsonline.com/articles/design-and-synthesis-of-new-bioactive-124triazoles-potential-antitubercular-and-antimicrobial-agents-3427.html', 'full_text': ''} """


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
            title = tag.find('meta',attrs={'name':'citation_title'})['content']
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
            keywords= tag.find('meta',attrs={'name':'keywords'})
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
    def publication_date(soup):
        '''
        Parse publication_date for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            publication_date= tag.find('meta',attrs={'name':'citation_publication_date'})

            if publication_date != None:
                publication_date=publication_date['content']
                publication_date=publication_date.replace('/','-')
                return publication_date
            else:
                publication_date=""

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
    def lastpage(soup):
        '''
        Parse lastpage for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            lastpage= tag.find('meta',attrs={'name':'citation_lastpage'})
            if lastpage != None:
                lastpage=lastpage['content']
                return lastpage
            else:
                lastpage=""
                return lastpage

    def pageno(soup):
        '''
        Parse pageno for the given article URL Element
        '''
        firstpage = Article.firstpage(soup)
        lastpage = Article.lastpage(soup)
        pageno=firstpage+"-"+lastpage

        return pageno

    def abstract(soup):
        '''
        Parse abstract for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            abstract= tag.find('meta',attrs={'name':'citation_abstract'})
            if abstract != None:
                abstract=abstract['content']
                return abstract
            else:
                p=soup1.find('p',attrs={'style':'text-align: justify;'})
                print(p.get_text())

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
    def full_text(soup):
        '''
        Parse abstract for the given article URL Element
        '''
        body=soup1.find('body')
        for p in body.find_all('p'):
            return str(p)

    def institute(soup):
        '''
        Parse institute for the given article URL Element
        '''
        try:
            div=soup.find('div',attrs={'class':'post-author'}).find_all('p')[1]
            #p=div.find_all('p')[1]
            p=div.get_text()
            #print("[1]", p)
            institute=p.replace("\n","--")
            #print (institute)
            insti=institute.split("--")
            #print(insti)
            string=[]
            for a in insti:
                string.append(a.strip())
            #print("TRY", string)
            return string
        except:
            div=soup.find('div',attrs={'class':'post-author'}).find_all('p')[0]
            p=div.get_text()
            #print("[0]", p)
            insti=p.split('\n')
            #print (insti)
            del insti[0]
            #print(insti)
            string=[]
            for a in insti:
                string.append(a.strip())

                #print("EXCEPT", string)
            return string

    def author(soup):
        '''
        Parse author for the given article URL Element
        '''
        div=soup.find('div',attrs={'class':'post-author'})
        strong=div.find('strong').get_text()
        strong=strong.replace(" and ", ", ")
        strong=strong.replace("*", "")
        out=strong.split(",")
        string=[]
        for stro in out:
            string.append(stro.strip())

        return string

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
            inst.append(institute)
        return inst
    def	auth_inst(soup):
        '''
        Parse auth_inst for the given article URL Element
        '''
        authors=Article.author(soup)
        institutes= Article.institute(soup)
        #print("RETURNED", authors)
        #print("RETURNED", institutes)

        authors_list=[]
        if len(institutes)>1:
            for m, auth in enumerate(authors):
                #print(m, auth)
                for n, inst in enumerate(institutes):
                    inst=inst.strip()
                    #print (inst)
                    au=auth[-1:]
                    ins=inst[0:]
                    if (au==ins):
                        #print(auth, inst)
                        author ={}
                        author['surname']    = auth.strip('0123456789')
                        author['given_name'] = ""
                        author['degree']	 = ""
                        author['email']		 = ""
                        author['orcid']		 = ""
                        author['institute']	 = Article.find_institute(inst)
                        authors_list.append(author)
                        #print(pas)

                    elif (ins not in ['1','2','3','4','5','6','7','8','9','0']) and (au not in ['1','2','3','4','5','6','7','8','9','0']) :
                        #print(auth, inst)
                        author ={}
                        author['surname']    = auth.strip('0123456789')
                        author['given_name'] = ""
                        author['degree']	 = ""
                        author['email']		 = ""
                        author['orcid']		 = ""
                        author['institute']	 = Article.find_institute(inst)
                        authors_list.append(author)
                        #print(pas)

        elif len(institutes)==1:
            for auth in authors:
                #print (auth, institutes)
                author ={}
                author['surname']    = auth.strip('0123456789')
                author['given_name'] = ""
                author['degree']	 = ""
                author['email']		 = ""
                author['orcid']		 = ""
                author['institute']	 = Article.find_institute(institutes[0])
                authors_list.append(author)

        else:
            pass

        #print (authors_list)
        return authors_list

    def main():
        soup = BeautifulSoup(url,'lxml')

        article={}
        article['pub_type'] = ""
        article['access_type'] = ""
        article['journal'] = Article.journal_title(soup)
        article['doi'] = Article.doi(soup)
        article['pmid'] =""
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
        #article['pdf_url'] = Article.pdf_link(soup)
        #article['html_url'] = Article.html_url(soup)
        #article['full_text'] =Article.full_text(soup)

        return article



if __name__ == "__main__":
    url_input = sys.argv[1]
    files=Request(url_input, headers={'User-Agent':'Mozilla/5.0'})
    url=urlopen(files)
    result = Article.main()
    doi = result['doi']
    doi = "data/" + doi.replace("/", "-")
    #print(result)
    output = doi + '.json'
    print("Writing...!", output)
    with open(output, 'w') as fp:
        json.dump(result, fp)
