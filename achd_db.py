#! /usr/bin/env python
#-*- coding: utf-8 -*-
# achd database


import sqlite3

conn = sqlite3.connect("achd_db.db")
curs = conn.cursor()

#qry_add_constraint = '''ALTER TABLE inspection ADD CONSTRAINT '''

qry_drop_table = 'DROP TABLE if exists assessment;'
#curs.execute(qry_drop_table)
#conn.commit()

qry_inspection = '''CREATE TABLE IF NOT EXISTS inspection (
    client_id TEXT,
    address TEXT, 
    city TEXT,
    phone TEXT,
    client_name TEXT,
    state TEXT,
    zipcode TEXT,
    date_open TEXT,
    municipality TEXT,
    --Inspection specific information
    inspect_id TEXT,
    inspector TEXT,
    re_inspection TEXT,
    inspection_date TEXT,
    --Inspection Details
    purpose TEXT,
    placarding TEXT,
    re_inspection_date TEXT,
    nc_violation_count TEXT
    );
    '''

client_id,address,city,phone,client_name,
state,zipcode,date_open,municipality,
inspect_id,inspector,re_inspection,
inspection_date,purpose,placarding,
re_inspection_date,nc_violation_count
#curs.execute(qry_inspection)
#conn.commit()
    ##Assessment catagories
qry_assessment = '''CREATE TABLE IF NOT EXISTS assessment (
    inspect_id TEXT UNIQUE, 
    food_source_condition TEXT,
    cooking_temperatures TEXT,
    consumer_advisory TEXT,
    reheating_temperatures TEXT,
    cooling_food TEXT,
    hot_holding_temperatures TEXT,
    cold_holding_temperatures TEXT,
    facilities_maintain_temperature TEXT,
    date_marking TEXT,
    probe_type_thermometer TEXT,
    cross_contamination_prevention TEXT,
    employee_health TEXT,
    personal_hygiene TEXT,
    sanitization TEXT,
    water_supply TEXT,
    waste_water_disposal TEXT,
    plumbing TEXT,
    handwashing_facilities TEXT,
    pest_management TEXT,
    certified_manager TEXT,
    demonstration_of_knowledge TEXT,
    other_exectional_activities TEXT
    );
    '''
#curs.execute(qry_assessment)
#conn.commit()

# removed non_critical_violations_field TEXT 
#         critical_violations_field TEXT

qry_violation = '''CREATE TABLE IF NOT EXISTS violation (
                   inspect_id TEXT UNIQUE,
                   non_critical_violation TEXT,
                   critical_violation TEXT
                   ); 
                '''
#curs.execute(qry_violation)
#conn.commit()


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
    ?,?,?,?,?,
    ?,?,?,?,?,
    ?,?,?,?,?,
    ?,?
    );
    '''

qry_insert_ass = '''INSERT INTO assessment (
    food_source_condition,
    cooking_temperatures,
    consumer_advisory,
    reheating_temperatures,
    cooling_food,
    hot_holding_temperatures,
    cold_holding_temperatures,
    facilities_maintain_temperature,
    date_marking,
    probe_type_thermometer,
    cross_contamination_prevention,
    employee_health,
    personal_hygiene,
    sanitization,
    water_supply,
    waste_water_disposal,
    plumbing,
    handwashing_facilities,
    pest_management,
    certified_manager,
    demonstration_of_knowledge,
    other_exectional_activities) 
    VALUES (
    ?,?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?  
    );
    '''

qry_insert_violation = ''' INSERT INTO violation (
    inspect_id,
    non_critical_violation,
    critical_violation) VALUES (
    ?, ?, ?
    );
    '''