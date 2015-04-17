#!/usr/bin/python3
"ACHD inspection record retrieval"
"open previously gathered inspection ids"
"save pdf files for reference"
"convert pdf to text"
"convert text to xml"
"convert xml to fulltext Postgresql"

import json, re, time, codecs, urllib.request
from itertools import chain

import subprocess
#import tempfile, os 
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import glob


#find difference from october to april
#october and october inspect list structure differ
#october is simple list, october is nested list

a = "achd_output_2014_10_22.json"
b = "achd_output_2015_04_07.json"


def get_id(json_output):
    "retrieve inspection id from achd_output file"
    with open(json_output, "r") as achd_output:
        achd_j = json.loads(achd_output.read())
    return achd_j

october = get_id(a)
april = get_id(b)

october_id = [list(chain(x['inspect'])) for x in october]
october_id = list(chain.from_iterable(october_id))
april_id = [list(chain.from_iterable(x['inspect'])) for x in april]
april_id = list(chain.from_iterable(april_id))

new_id = set(april_id).difference(set(october_id))

#base_restaurant = 'http://webapps.achd.net/Restaurant/RestaurantDetail.aspx?ID='
#base_inpsection = 'http://hdas01.achd.net/reports/rwservlet?food_rep_insp&P_ENCOUNTER='

def getpdf_basic(start, end):
    "Crawl for inspection pdf files"
    "Adjusted for python34"
    "add multithreading, get rid of for statement, use map"
    
    base_inspection = 'http://hdas01.achd.net/reports/rwservlet?food_rep_insp&P_ENCOUNTER='
    # http://hdas01.achd.net/reports/rwservlet?food_rep_insp&P_ENCOUNTER=201205230014
    #achd_j = get_id() 
    start = int(start)
    end = int(end)
    for x in range(start, end):
        #for view in achd_j[x]['inspect']:
        for inspection in new_id:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0.1) Gecko/20100101 Firefox/37.0.1'), ('Accept-encoding', 'gzip')]
            with opener.open(base_inspection+inspection) as viewout:
                #compresseddata = viewout.read()
                #compressedstream = StringIO.StringIO(compresseddata)
                #gzipper = gzip.GzipFile(fileobj=compressedstream)
                #comp_viewout = gzipper.read()
                with open('Inspections_2014_04_07/'+inspection+'.pdf', "wb") as pdfout:
                    #convert = convert_pdf_to_text_with_pdf2txt(viewout.read())
                    pdfout.write(viewout.read())
                    time.sleep(2)

def convert_pdf():
    "Get file pdf, send to pdf2txt"
    "Change inputs to represent the input file and output file"
    "move files from start folder to done folder after job"

    inspect = glob.glob('Inspections_converted/*.pdf')
    
    def processor(pdf):
        "use number of original in txt version"
        pat = re.search('([0-9]{4,}).pdf', pdf)
        id_num = pat.group(1)
        subprocess.Popen(['pdf2txt.py', '-o', 'txt_html/'+id_num+'.html', pdf])

    pool = Pool(4)
    pool.map(processor, inspect)
    pool.close
    pool.join


#convert_pdf()
#getpdf_basic(4000,6000)
