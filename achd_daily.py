#!/usr/bin/python3
#
# This is a daily file for downloading achd inspections

import time,\
       urllib.request,\
       urllib.error
import datetime as dt
from os import mkdir, path

def url_prep(delta=1, count=49):
    "Create iterator of urls, default yesterday, 49 inspections"
    
    url_stem = "http://hdas01.achd.net/reports/rwservlet?food_rep_insp&P_ENCOUNTER="
    d = dt.date.today()
    d1 = dt.timedelta(days=delta)
    day = '{:%Y%m%d}'.format(d-d1)
    base_stem = url_stem+day+'00'
    zfil = (str(x).zfill(2) for x in range(1, count))
    encounters = (base_stem+x for x in zfil)
    return encounters
    
def grab_pdf(inspection):
    "Takes inspection from url_prep, download pdf"
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent',\
        '''Mozilla/5.0 
        (X11; Ubuntu; Linux x86_64; rv:37.0.1) 
        Gecko/20100101 Firefox/37.0.1'''),\
        ('Accept-encoding', 'gzip')]
    folder = inspection[-12:-4]
    pdffile = inspection[-12:]
    with opener.open(inspection) as viewout:
        if path.isdir(folder) == False:
            mkdir(folder)
        else:    
            outputfolder = folder+'/'+pdffile+'.pdf'
            with open(outputfolder, "wb") as pdfout:
                pdfout.write(viewout.read())
                time.sleep(2)

if __name__ == '__main__':

    encounters = url_prep(delta=1, count=55)

    for inspection in encounters:
        try:
            grab_pdf(inspection)
        except urllib.error.HTTPError as e:
            print("fail, {}".format(e.code))