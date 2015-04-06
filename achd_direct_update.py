#-*- coding: utf-8 -*-
#The ACHD Screen Scraping project
#Gather initial restaurant id
#must use javascript for multipage zipcodes

from selenium import webdriver
from BeautifulSoup import BeautifulSoup
import re, time, codecs, urllib2, StringIO, gzip
#from multiprocessing import Pool
#from multiprocessing.dummy import Pool as ThreadPool
from random import random

#zip code list
zlm = ['15212', '15222', '15213', '15219', '15146', '15237', \
       '15205', '15108', '15203', '15120', '15235', '15236', \
       '15206', '15136', '15217', '15132', '15122', '15238', \
       '15210', '15221', '15017', '15102', '15224', '15044', \
       '15216', '15220', '15201', '15202', '15084', '15090', \
       '15106', '15101', '15241', '15227', '15143', '15025', \
       '15239', '15147', '15232', '15218', '15137', '15234', \
       '15226', '15215', '15065', '15228', '15229', '15139', \
       '15208', '15037', '15209', '15131', '15104', '15071', \
       '15231', '15024', '15207', '15223', '15211', '15275', \
       '15116', '15233', '15214', '15110', '15145', '15243', \
       '15129', '15045', '15261', '15144', '15204', '15126', \
       '15135', '15133', '15112', '15148', '15140', '15014', \
       '16046', '15123', '15076', '15225', '15142', '15056', \
       '15034', '15086', '15057', '15035', '15030', '15282', \
       '15127', '15088', '15018', '16127', '15026', '15015', \
       '15007', '15240', '15063', '15046', '15031', '15260', \
       '15082', '15051', '15230', '15091', '15068', '15049', \
       '15006', '15003', '43449', '16066', '16059', '15321', \
       '15075', '15064', '15047', '15032', '43952', '26505', \
       '26062', '15276', '15259', '15244', '15200', '15083', \
       '15067', '15038', '15020', '15012', '15001', '15146']

# Open the Firefox browser
#driver = webdriver.Firefox()
#driver.get('http://webapps.achd.net/Restaurant')
#inputzip = driver.find_element_by_name('ctl00$ContentPlaceHolder1$txtZip')
## inputzip.send_keys('15226')
#inputcity = driver.find_element_by_name('ctl00$ContentPlaceHolder1$txtCity')
#inputnum = driver.find_element_by_name('ctl00$ContentPlaceHolder1$txtNum')
#inputmuni = driver.find_element_by_name("ctl00$ContentPlaceHolder1$ddlMuni")
#inputplacard = driver.find_element_by_name("ctl00$ContentPlaceHolder1$ddlPlacard")
#inputsend = driver.find_element_by_name('ctl00$ContentPlaceHolder1$btnFind')

## for each zip code in the ACHD database, query the restaurants and save the pages
## or add the restaurant id to a text document
## if zip code has more than 500 restaurants, you must use an additional query term
## to reduce the result set

## open the ACHD site
## find the zip code field
## enter the zip code
## find the find button
## click the find button to query the zip code
## create a new UTF-8 document based on the zip code
## write the current page data to the document
## close the document
## search the text for a Page$ number string
## Then for each Page$number string on the source page, go to the new page
## at each page, save the contents to a file based on the zip code and current Page$num
## close the document
## wait ten seconds and move to the next page

## if one must search by muni
## inputmuni = driver.find_element_by_name("ctl00$ContentPlaceHolder1$ddlMuni")
## munielement = inputmuni.find_elements_by_xpath('//select/option')
## munielement finds option values for Priority Code, Municipality and Placard Status
## if len(munielement) == 174
## Priority Code is munielement[0:3]
## Placard Status is munielement[-4:-1]
## Municipality is all other munielement[5:169]
## leave out option 4 because it is the "Please Select" element that has no actionable value
## inputsend = driver.find_element_by_name('ctl00$ContentPlaceHolder1$btnFind')
## inputsend.click()


## Page must have table to pull information from
## search has result if the container <div id="ctl00_ContentPlaceHolder1_UpdatePanel1"> has a <div> with a <table> in it
## search has result if the len(<div id="ctl00_ContentPlaceHolder1_UpdatePanel1">) text is > 0
## search has result if "Client Name" in driver.page_source == true
## search has no result if len(driver.page_source) <= 20920

## if Page has info, check to see if it has multiple pages of info

def launch():
    driver = webdriver.Firefox()
    return driver

driver = webdriver.Firefox()

def initialize(zipcode):
        '''zipcode is the zip code to query'''
        #driver = webdriver.Firefox()
        driver.get('http://webapps.achd.net/Restaurant')
        inputzip = driver.find_element_by_name('ctl00$ContentPlaceHolder1$txtZip')
        inputzip.send_keys(str(zipcode))
        inputsend = driver.find_element_by_name('ctl00$ContentPlaceHolder1$btnFind')
        inputsend.click()
        
def pagenav():
        '''pull the pages of the query into a list'''
        '''use the initial page of that query for all navigation'''
        pcount = ('Page\\$\\d')
        getpage = re.compile(pcount)
        s_pcount = getpage.findall(driver.page_source)
        return s_pcount	

def idstringfind():
        idstring = list()
        idtext = driver.page_source
        re_pat = '''RestaurantDetail\.aspx\?ID=(?P<rest_id>[0-9]{4,})'''
        pat_compile = re.compile(re_pat)
        idstring = pat_compile.findall(idtext)
        return idstring


# set the page navigation based on first page
def pnavloop():
    pnav = pagenav()
    idstring = idstringfind()
    #idstring.extend(idstringfind())
    if len(pnav) >= 1:
        for y in pnav:
            driver.execute_script("__doPostBack('ctl00$ContentPlaceHolder1$gvFSO', '"+y+"')")
            time.sleep(random()*2+10)
            idstring.extend(idstringfind())
    with open("r_id.txt", "a+") as idsheet:
        output = ""
        for r_id in idstring:
            output = output + r_id + "\n"
        idsheet.write(output)

def run_zip():
    for zipcode in zlm:
        initialize(zipcode)
        pnavloop()
        time.sleep(random()*2+2)

run_zip()

def go_zip(zipcode):
    driver = webdriver.Firefox()
    time.sleep(random()*2+1)
    initialize(zipcode)
    pnavloop()
    time.sleep(random()*2+1)

def pooled_zip():
    pool = ThreadPool(2)
    results = pool.map(go_zip, zlm[:4])
    pool.close()
    pool.join()


"""
zlmcount = 0

#for x in zlm:
#    print zlmcount
#    initialize(x)
#    pnav = pagenav()
#    pnavloop()
#    zlmcount += 1
	

## Date Extract (may also use text)
###############
def date_ex(date):
    re_date = re.compile('\d{2}\/\d{2}\/\d{4}')
    date_g = re_date.search(date)

    date_out = date_g.group()

    return date_out

## URL Extract
##############
def encounter_id(url):
    '''enter url, extract id'''
    url_pat = 'ENCOUNTER=([0-9]{4,})'
    url_c = re.compile(url_pat)
    url_x = url_c.search(url)
    url_out = url_x.group(1)

    return url_out


id_file = open('August2012.txt', 'r')
re_id_pat = '\d{4,15}'
re_id_comp = re.compile(re_id_pat)
id_list_test = re_id_comp.findall(id_file.read())
id_file.close()

##Inspection Record Extraction
##############################
def inspect_ex_direct(file_o, rest_id):
    '''Inspection record extraction directly from achd site'''
    '''file_o is a url string'''

    soup = BeautifulSoup(file_o)
        
    if len(str(soup)) <= 3000:
        achdout = open('inspect_test_id.csv','a')
        achdout.write('''{0}\t\t\t\n'''.format(rest_id))
        achdout.close()


    elif len(str(soup)) > 3000:

        inspection = soup.table.table.table.table.table
        inspectlist = [x for x in inspection if len(x) > 1]
        inspectlen = len(inspectlist)
        lenmin = inspectlen - (inspectlen-1)
        lenmax = inspectlen
        
        for d in range(lenmin, lenmax):
            idtag = rest_id
            datetag = str( date_ex(str([e for e in inspectlist[d]][1])))
            typetag = str([e for e in inspectlist[d]][2].text)
            encounter = str(encounter_id(str([e for e in inspectlist[d]][3])))
        
            achdout = open('inspect.csv','a')
            achdout.write('''{0}\t{1}\t'{2}'\t{3}\n'''.format(rest_id, datetag, typetag, encounter))
            achdout.close()


## Contact Information Extraction
#################################
def contact_ex_direct(file_o, rest_id):
    '''Contact record extract'''
    soup = BeautifulSoup(file_o)
    inspectlist = soup('span')
    name = inspectlist[0].text
    address = inspectlist[1].text
    contact = inspectlist[2].text
    encounter = inspectlist[3].text
    
    achdout = open('contact.csv','a')
    achdout.write('''{0}\t{1}\t{2}\t{3}\t{4}\n'''.format(rest_id, inspectlist[0].text, inspectlist[1].text, inspectlist[2].text, inspectlist[3].text))
    achdout.close()



for rest_id in id_list_test[7000:]:
    #'''Use gzip for compressed download'''
    url = "{0}{1}".format("http://webapps.achd.net/Restaurant/RestaurantDetail.aspx?ID=", rest_id)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.17.1'), ('Accept-encoding', 'gzip')]
    
    usock = opener.open(url)

    compresseddata = usock.read()
    compressedstream = StringIO.StringIO(compresseddata)
    gzipper = gzip.GzipFile(fileobj=compressedstream)
    url_r = gzipper.read()
    
    contact_ex_direct(url_r, rest_id)
    inspect_ex_direct(url_r, rest_id)
    time.sleep(random.random()*1+2)


    
'''
for rest_id in id_list_test[6090:6091]:
    url = "{0}{1}".format("http://webapps.achd.net/Restaurant/RestaurantDetail.aspx?ID=", rest_id)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0.1')]
    #opener.addheaders = [('Accept-encoding', 'gzip')]
    usock = opener.open(url)
    url_r = usock.read()
    contact_ex_direct(url_r, rest_id)
    inspect_ex_direct(url_r, rest_id)
    time.sleep(random.random()*1+2)
'''
## gzip source and explaination http://www.diveintopython.net/http_web_services/gzip_compression.html

"""