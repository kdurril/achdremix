#!/usr/bin/env python3
#
#revised parser for achd documents

import json
from collections import OrderedDict
from itertools import chain

def parse(doc):
    "Parses readlines docs"
    "Use deconstructed version for testing"
    
    tags_tuple = ('Client ID:\n',
        'Inspect ID:\n',
        'Assessment Categories:\n',
        'Critical Violation:\n',
        'Non Critical Violations:\n')
    
    visit = OrderedDict()

    if 'Client ID:\n' in doc:
        client = doc.index(tags_tuple[0])
        visit['client_id'] = doc[client+5].strip('\n')
        visit['address'] = doc[client+6].strip('\n')
        visit['city'] = doc[client+7].strip('\n')
        visit['phone'] = doc[client+8].strip('\n')

        visit['client_name'] = doc[client+12].strip('\n')
        visit['state'] = 'PA'
        visit['zipcode'] = doc[client+20].strip('\n')
        visit['date_open'] = doc[client+22][11:].strip('\n')
        visit['municipality'] = doc[client+23][14:].strip('\n')
    
    if 'Inspect ID:\n' in doc:
        inspect = doc.index(tags_tuple[1])
        #Inspection specific information
        visit['inspect_id'] = doc[inspect+5].strip('\n')
        visit['inspector'] = doc[inspect+6].strip('\n')
        visit['re_inspection'] = doc[inspect+7].strip('\n')
        visit['inspection_date'] = doc[inspect+8].strip('\n')

        #Inspection Details
        #relative to 'Inspection Details'
    if 'Purpose:\n' in doc:
        try:
            visit['purpose'] = doc[inspect+16].strip('\n')
        except:
            visit['purpose'] = ''
    if 'Placarding:\n' in doc:
        try:
            visit['placarding'] = doc[inspect+17].strip('\n')
        except:
            visit['placarding'] = ''
    if 'Re Inspection Date:\n' in doc:
        try:
            visit['re_inspection_date'] = doc[inspect+18].strip('\n')
        except:
            visit['re_inspection_date'] = ''
    if 'Non Critical Violations #\n' in doc:    
        try:
            visit['nc_violation_count'] = doc[inspect+19].strip('\n')
        except:
            visit['nc_violation_count'] = ''
    
    #Assessment Details
    if 'Assessment Categories:\n' in doc:
        
        assess_start = doc.index(tags_tuple[2])+2
        assess_len = doc[assess_start:].index('\n')
        assess_end = assess_start+assess_len
        data_start = assess_end+1
        data_end = data_start+assess_len
        labels = doc[assess_start:assess_end]
    
        data = doc[data_start:data_end]
        paired = zip(labels, data)
    
        for k,v in paired:
            visit[k.strip('\n')] = v.strip('\n')
    if 'Non Critical Violations:\n' in doc:
        if visit['nc_violation_count'].strip('\n') != '0':
            ncv = doc.index(tags_tuple[4])      
            visit['non_critical'] = doc[ncv:]
        
    if 'Critical Violation:\n' in doc:
        cv = doc.index(tags_tuple[3])
        ncv = doc.index(tags_tuple[4])
        visit['critical_violation'] = "".join(doc[cv:ncv])
    
    return visit

class ParseDoc(object):
    "mirrors parse function with accessible subparts"
    def __init__(self, f_obj_name):
        self.f_obj_name = f_obj_name
        with open(f_obj_name, 'r') as f:
            self.f_obj = f.readlines()
        self.tags_tuple = ('Client ID:\n',
            'Inspect ID:\n',
            'Assessment Categories:\n',
            'Critical Violation:\n',
            'Non Critical Violations:\n')
        
        self.tags = [self.f_obj.index(tag) for tag in self.tags_tuple]
        self.visit = OrderedDict()
        
    def client(self):
        "parse client specific items"
        doc = self.f_obj
        visit = OrderedDict()
        if 'Client ID:\n' in doc:
            client = doc.index(self.tags_tuple[0])
            visit['client_id'] = doc[client+5].strip('\n')
            visit['address'] = doc[client+6].strip('\n')
            visit['city'] = doc[client+7].strip('\n')
            visit['phone'] = doc[client+8].strip('\n')

            visit['client_name'] = doc[client+12].strip('\n')
            visit['state'] = 'PA'
            visit['zipcode'] = doc[client+20].strip('\n')
            visit['date_open'] = doc[client+22][11:].strip('\n')
            visit['municipality'] = doc[client+23][14:].strip('\n')
            
            for k,v in visit.items():
                self.visit[k] = v
            
            return visit
        
    def inspection(self):
        "parse inspection specific items"
        doc = self.f_obj
        visit = OrderedDict()
        
        if 'Inspect ID:\n' in doc:
            inspect = doc.index(self.tags_tuple[1])
            #Inspection specific information
            visit['inspect_id'] = doc[inspect+5].strip('\n')
            visit['inspector'] = doc[inspect+6].strip('\n')
            visit['re_inspection'] = doc[inspect+7].strip('\n')
            visit['inspection_date'] = doc[inspect+8].strip('\n')

            #Inspection Details
            #relative to 'Inspection Details'
            if 'Purpose:\n' in doc:
                try:
                    visit['purpose'] = doc[inspect+16].strip('\n')
                except:
                    visit['purpose'] = ''
            if 'Placarding:\n' in doc:
                try:
                    visit['placarding'] = doc[inspect+17].strip('\n')
                except:
                    visit['placarding'] = ''
            if 'Re Inspection Date:\n' in doc:
                try:
                    visit['re_inspection_date'] = doc[inspect+18].strip('\n')
                except:
                    visit['re_inspection_date'] = ''
            if 'Non Critical Violations #\n' in doc:    
                try:
                    visit['nc_violation_count'] = doc[inspect+19].strip('\n')
                except:
                    visit['nc_violation_count'] = ''
            
            for k,v in visit.items():
                self.visit[k] = v
                
            return visit
        
    def assessment(self):
        "parse assessment information"
        doc = self.f_obj
        visit = OrderedDict()
        if 'Assessment Categories:\n' in doc:
            assess_start = doc.index(self.tags_tuple[2])+2
            assess_len = doc[assess_start:].index('\n')
            assess_end = assess_start+assess_len
            data_start = assess_end+1
            data_end = data_start+assess_len

            labels = doc[assess_start:assess_end]
            data = doc[data_start:data_end]
            paired = zip(labels, data)

            for k,v in paired:
                visit[k.strip('\n')] = v.strip('\n')
                
            for k,v in visit.items():
                self.visit[k] = v
                
        return visit
    
    def non_critical(self):
        "parse non_critical assessment"
        doc = self.f_obj
        visit = OrderedDict()
        if 'Non Critical Violations:\n' in doc:
            if 'nc_violation_count' in self.visit:
                if self.visit['nc_violation_count'] != '0':
                    ncv = doc.index(self.tags_tuple[4])      
                    visit['non_critical'] = doc[ncv:]
                    return visit
                
                    for k,v in visit.items():
                        self.visit[k] = v
            elif self.inspection()['nc_violation_count'] != '0':
                    ncv = doc.index(self.tags_tuple[4])      
                    visit['non_critical'] = doc[ncv:]    
                    
                    for k,v in visit.items():
                        self.visit[k] = v
                        
                    return visit
        
    def critical(self):
        "parse critical assessment"
        doc = self.f_obj
        visit = OrderedDict()
        if 'Critical Violation:\n' in doc:
            cv = doc.index(self.tags_tuple[3])
            ncv = doc.index(self.tags_tuple[4])
            visit['critical_violation'] = "".join(doc[cv:ncv])
            
            for k,v in visit.items():
                self.visit[k] = v
                
            return visit

def from_db(id_list):
    "generator for parse function from inspection number list"
    "original list created from db"
    for x in id_list:
        with open ('txt/'+str(x)+'.txt','r') as f:
            yield f.readlines()

def from_files():
    "generator for parse from txt files directly"
    sample_set = glob.iglob('txt/*.txt')
    for x in sample_set:
        with open(x, 'r') as f:
            yield f.readlines()

def create_json():            
    with open('achd_all.json', 'a') as out:
        out.write(json.dumps(\
            list(parse(y) for y in from_files())))

kys = ['food_source_condition',
         'cooking_temperatures',
         'consumer_advisory',
         'reheating_temperatures',
         'cooling_food',
         'hot_holding_temperatures',
         'facilities_maintain_temperature',
         'date_marking',
         'probe_type_thermometer',
         'cross_contamination_prevention',
         'employee_health',
         'personal_hygiene',
         'sanitization',
         'water_supply',
         'waste_water_disposal',
         'plumbing',
         'handwashing_facilities',
         'pest_management',
         'certified_manager',
         'demonstration_of_knowledge']

if __name__ == '__main__':
    create_json()