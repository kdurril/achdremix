#! /usr/bin/env python
#-*- coding: utf-8 -*-
# achd database in postgresql
# intended for full text search

import psycopg2
import re
import glob
from achd_db import qry_inspection
import sqlite3

#open db connection to achdtext
#http://initd.org/psycopg/docs/usage.html
#get sqlite data https://coderwall.com/p/byoycg
#http://www.sqlite.org/cli.html
con = psycopg2.connect(database="postgres", user="kenneth")
curr = con.cursor()

conn = sqlite3.connect("achd_db.db")
curs = conn.cursor()

curs.execute('SELECT * FROM inspection')
inspectout = curs.fectchall()

qry_createdb = '''CREATE TABLE IF NOT EXISTS achdtext(inspect_id BIGINT PRIMARY KEY, client_id TEXT, doc TEXT, docvec TSVECTOR);'''

qyr_alterdb = "ALTER TABLE achdtext ADD COLUMN docvector tsvector"

qry_updatedb = "UPDATE TABLE achdtext SET docvetor = to_tsvector(doc)"

qry_text_insert = '''INSERT INTO achdtext (inspect_id, client_id, doc, docvec) VALUES (%s,%s,%s,%s);'''

qry_copy_from = '''COPY achd inspect_id, client_id, doc FROM'''

qry_create_index = "CREATE INDEX docvec_indx ON achdtext USING gin(docvector);"

qry_update_client_id = "UPDATE achdtext SET client_id = substring(doc from '\d{4,}');"

#http://www.postgresql.org/docs/9.3/static/textsearch-tables.html
firsttext = "SELECT inspect_id FROM achdtext WHERE docvector @@ to_tsquery('blood');"


def achd_populate():

    inspect = glob.glob('/home/kenneth/Documents/scripts/achd/txt/*.txt')
    
    def get_id(filename):
        "extract inspection id from inspect string"
        pat = re.search('([0-9]{4,}).txt', filename)
        id_num = pat.group(1)
        return id_num

    def populate(filename):
        "insert text files into postgresql" 
        #revise with a copy from statement
        #if keeping insert, use prepare statment
        #see manual chapter 14 

        id_num = get_id(filename)
        with open(filename, "r") as achd_text:
            curr.execute(qry_text_insert,[int(id_num),"", "", achd_text.read()])
    for x in inspect:
        try:
            populate(x)
        except:
            print(x)
    con.commit()


#curr.execute(qry_inspection)
#con.commit()
#achd_populate()

with open("/home/kenneth/Documents/scripts/achd/achdout.csv", "r") as inspectfile:
    curr.copy_from(inspectfile, "inspection", 
        columns=["client_id", "address", "city", "phone","client_name", "state",
        "zipcode", "date_open", "municipality", "inspect_id", "inspector",
        "re_inspection","inspection_date","purpose", "placarding", 
        "re_inspection_date", "nc_violation_count"])
    con.commit()

qry_insert_inspect = '''INSERT INTO inspection (
    client_id,
    address, 
    city,
    phone,
    client_name,
    state,
    zipcode,
    date_open,
    municipality,
    
    inspect_id,
    inspector,
    re_inspection,
    inspection_date,

    purpose,
    placarding,
    re_inspection_date,
    nc_violation_count)
    VALUES (
    %s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,
    %s,%s
    );
    '''
#Move supervised data in original Sqlite to Postgresql
#Extract from sqlite more to postgresql
#could have used copy from in postgresql with csv
get_achd = curs.execute("SELECT * FROM inspection;")
fetch_achd = curs.fetchall()

curr.executemany(qry_insert_inspect, fetch_achd)
con.commit()