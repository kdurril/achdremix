#! usr/bin/python
"ACHD inspection record retrieval"
"open previously gathered inspection ids"
"save pdf files for reference"
"convert pdf to text"
"convert text to xml"
"convert xml to fulltext Postgresql"

import json, re, time, codecs, urllib2, StringIO, gzip
import glob
import subprocess
#import tempfile, os 
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from random import random



def get_id():
    "retrieve inspection id from achd_output file"
    with open("achd/achd_output_20140316.json", "rb") as achd_o:
        achd_j = json.loads(achd_o.read())
    return achd_j

base_restaurant = 'http://webapps.achd.net/Restaurant/RestaurantDetail.aspx?ID='
base_inpsection = 'http://hdas01.achd.net/reports/rwservlet?food_rep_insp&P_ENCOUNTER='

def convert_pdf():
    "Get file pdf, send to pdf2txt"
    "Change inputs to represent the input file and output file"
    "move files from start folder to done folder after job"

    inspect = glob.glob('Inspections/*')
    
    def processor(pdf):
        "use number of original in txt version"
        pat = re.search('([0-9]{4,}).pdf', pdf)
        id_num = pat.group(1)
        subprocess.Popen(['pdf2txt.py', '-o', 'txt/'+id_num+'.txt', pdf])

    pool = Pool()
    pool.map(processor, inspect)
    pool.close
    pool.join



def getpdf_basic(start, end):
    "Crawl for inspection pdf files"
    "add multithreading, get rid of for statement, use map"
    
    base_inspection = 'http://hdas01.achd.net/reports/rwservlet?food_rep_insp&P_ENCOUNTER='
    
    achd_j = get_id() 
    start = int(start)
    end = int(end)
    for x in range(start, end):
        for view in achd_j[x]['inspect']:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0'), ('Accept-encoding', 'gzip')]
            viewout = opener.open(base_inspection+view)
            #compresseddata = viewout.read()
            #compressedstream = StringIO.StringIO(compresseddata)
            #gzipper = gzip.GzipFile(fileobj=compressedstream)
            #comp_viewout = gzipper.read()
            with open('Inspections/'+view+'.pdf', "w") as pdfout:
                #convert = convert_pdf_to_text_with_pdf2txt(viewout.read())
                pdfout.write(viewout.read())
                time.sleep(2)


#achd_j = get_id()
#getpdf_basic(6000,8117)
#convert_pdf()
