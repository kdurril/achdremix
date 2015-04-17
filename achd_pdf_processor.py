#!/usr/bin/python3
#-*- coding: utf-8 -*-
"ACHD inspection record retrieval"
"open previously gathered inspection ids"
"save pdf files for reference"
"convert pdf to text"
"convert text to fulltext Postgresql"

import re
import subprocess
from multiprocessing import Pool
import glob
#import tempfile, os 
#from multiprocessing.dummy import Pool as ThreadPool


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