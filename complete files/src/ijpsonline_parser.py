from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import sys
import re
import json
from almamater import out

# USAGE :
# 	python3 ijpsonline_parser.py

#SAMPLE OUTPUT

"""{'pub_type': '', 'access_type': '', 'journal': 'Indian Journal of Pharmaceutical Sciences', 'doi': '10.4103/0250-474X.103840', 'pmid': '', 'pmc': '', 'title': 'Development and validation of stability-indicating HPLC method for betamethoasone dipropionate and related substances in topical formulation', 'authors': [{'surname': 'A. S. Vairale', 'given_name': '', 'degree': '', 'email': '', 'orcid': '', 'institute': [{'apid': '', 'federation': '', 'acronym': '', 'address': '.', 'city': '', 'district': '', 'state': '', 'country': 'WORLD', 'name': '.'}]}, {'surname': 'P. Sivaswaroop', 'given_name': '', 'degree': '', 'email': '', 'orcid': '', 'institute': [{'apid': '', 'federation': '', 'acronym': '', 'address': '.', 'city': '', 'district': '', 'state': '', 'country': 'WORLD', 'name': '.'}]}, {'surname': 'S. Bandana', 'given_name': '', 'degree': '', 'email': '', 'orcid': '', 'institute': [{'apid': '', 'federation': '', 'acronym': '', 'address': '.', 'city': '', 'district': '', 'state': '', 'country': 'WORLD', 'name': '.'}]}], 'volume': '74', 'issue': '2', 'pagenum': '', 'date_received': None, 'date_accepted': None, 'date_published': '', 'abstract_text': 'A gradient reversed phase HPLC method was developed and validated for analysis of betamethasone dipropionate, its related substances and degradation products, using Altima C18 column (250×4.6 mm, 5 µm) with a flow rate of 1.0 ml/min and detection wavelength of 240 nm. The mobile phase A is a mixture of water, tetrahydrofuran and acetonitrile in the ratio of 90:4:6 (v/v/v) while mobile phase B is a mixture of acetonitrile, tetrahydrofuran, water and methanol in the ratio of 74:2:4:20 (v/v/v/v). The samples were analyzed using 20 µl injection volume and the column temperature was maintained at 50°. The limit of detection and limit of quantitation were found to be 0.02 µg/ml and 0.07 μg/ml, respectively. The stability-indicating capability of method was established by forced degradation studies and method demonstrated successful separation of drug, its related substances and degradation products. The method was validated as per the International Conference on Harmonization guidelines. The developed method is linear in the range of 0.07 to 200% of specification limits established for all the known related substances; betamethasone17â??propionate, betamethasone 21â??propionate, betamethasone 17â??propionateâ??21â??acetate (RSD <5, 2, 1%, respectively, r2=09991â??0.9999 for sample concentration of 100 µg/ml). The method is sensitive, specific, linear, accurate, precise and stability indicating for the quantitation of drug, its related substances and other degradation compounds.', 'keywords': 'Betmethasone dipropionate, forced degradation, HPLC method, stability indicating, topical formulations', 'pdf_url': 'http://www.ijpsonline.com/articles/development-and-validation-of-stabilityindicating-hplc-method-for-betamethoasone-dipropionate-and-related-substances-in-.pdf', 'html_url': 'http://www.ijpsonline.com/articles/development-and-validation-of-stabilityindicating-hplc-method-for-betamethoasone-dipropionate-and-related-substances-in-topical-fo.html'}"""


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

    def title(soup):
        '''
        Parse title for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            titles = tag.find('meta',attrs={'name':'citation_title'})
            title=titles['content']
            return title
        
    def author(soup):
        '''
        Parse author for the given article URL Element
        '''
        try:
            div=soup.find('div',attrs={'class':'post-author'})
            strong=div.find('strong').get_text()
            strong=strong.replace(" and ", ", ")
            strong=strong.replace("*", "")
            out=strong.split(",")
            string=[]
            for stro in out:
                string.append(stro.strip())
            return string
        except:
            div=soup.find('div',attrs={'class':'post-details pb-0'})
            div2=div.find('div').get_text()
            #print(div2)
            auth=div2.split('\n')
            #print(auth[1])
            strong=auth[1].strip('Author(s):')
            #print(strong)
            strong=strong.replace(" and ", ", ")
            strong=strong.replace("*", "")
            out=strong.split(",")
            string=[]
            for stro in out:
                string.append(stro.strip())
            #print(string)
            return string


    def institute(soup):
        '''
        Parse institute for the given article URL Element
        '''
        try:
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
                string=[]
                for a in insti:
                    string.append(a.strip())

                    #print("EXCEPT", string)
                return string
        except:
            div=soup.find('div',attrs={'class':'post-details pb-0'})
            div2=div.find('div').get_text()
            #print(div2)
            inst=div2.split('\n')
            #print(inst[1])
            strong=inst[2].strip()
            print(strong)
            strongs=strong.replace("\n","--")
            #print (institute)
            out=strongs.split("--")
            #print(insti)
            string=[]
            for stro in out:
                string.append(stro.strip())
            #print(string)
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
        if (firstpage !="" and lastpage !="" ):
        
            pageno=firstpage+"-"+lastpage
            return pageno
        elif(firstpage !=None and lastpage =="" ):
            pageno=firstpage
            return pageno
        else:
            pageno=""
            return pageno
    
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
                for tag in soup.find_all('head'):
                    publication_date= tag.find('meta',attrs={'name':'citation_online_date'})

                    if publication_date != None:
                        publication_date=publication_date['content']
                        publication_date=publication_date.replace('/','-')
                        return publication_date
                    else:
                        publication_date=""

                        return publication_date
    def abstract(soup):
        '''
        Parse abstract for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            p=soup.find('p',attrs={'1style':'text-align: justify;'})
            if p!=None:
                abstract=p.get_text()
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
        Parse html_url for the given article URL Element
        '''
        for tag in soup.find_all('head'):
            html_url= tag.find('meta',attrs={'name':'citation_fulltext_html_url'})
            if html_url != None:
                html_url=html_url['content']
                return html_url
            else:
                html_url=""
                return html_url
    
    def full_text(soup):
        
        '''
        Parse full_text for the given article URL Element
        '''
        for tag in soup.find_all('body'):
            div=tag.find('div',attrs={'class':'entry-content'})
            if div != None:
                full_text=str(div)
                return full_text
            else:
                full_text=""
                return full_text
        
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
        article['pdf_url'] = Article.pdf_link(soup)
        article['html_url'] = Article.html_url(soup)
        #article['full_text'] =Article.full_text(soup)

        return article



if __name__ == "__main__":
    url_input = sys.argv[1]
    files=Request(url_input, headers={'User-Agent':'Mozilla/5.0'})
    url=urlopen(files)
    result = Article.main()
    print(result) 
    """doi = result['doi']
    if len(doi) > 0:
        doi = "" + doi.replace("/", "-")
        #print(result)
        output = doi + '.json'
        print("Writing...!", output)
        with open(output, 'w') as fp:
            json.dump(result, fp)
    else:
        name = sys.argv[1]
        d = name.split('/abstract/')
        doi = d[1]
        #print(result)
        doi = doi.replace("/", "-")
        output = "" + doi + '.json'
        print("Writing...!", output)
        with open(output, 'w') as fp:
            json.dump(result, fp)"""                                                                                                                                                                                                                           
