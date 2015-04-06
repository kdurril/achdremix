#usr/bin/python
#build for python 3.4
#ACHD Inspection parsing
''' The ACHD pdf files are useful for reference sake and human readability
    However, the text of each document needs to be machine readable for 
    analysis at an aggregate level. This module will parse and restructure the
    text. 

    Get list of documents to convert. Test subset for structure consistency.
    Parse file. Add it to a json file.
'''

import glob
import json
import random
from collections import namedtuple
from os.path import getsize

def file_queue():
    "Get list of files"
    inspect = glob.glob('txt/*')
    inspect = [x for x in inspect if getsize(x) <= 3000]
    return inspect

def alt_queue():
    "get output of logged error files"
    with open('log.txt' , 'r') as inspect:
        logAlt = inspect.read()
        logAlt = logAlt.split('\n')
        return logAlt

def sample_set(full_set):
    "Pull 10 test files as a sample"
    sample = [full_set[random.randint(5,3000)] for x in range(10)]
    return sample

def open_file(txtfile):
    "Open file and readlines"
    
    with open(txtfile, 'r') as t_file:
        file_by_lines = t_file.readlines()
        #file_by_lines = [x.strip('\n') for x in file_by_lines]

    return file_by_lines

class TextEval(object):
    '''Structure text file'''
    #Restuarant data extraction w parse stem
    #restaurant and inspection data w parse_stem, parse_tuple
    #Assessment category data w block_pair
    #Violation data w post_block

    def __init__ (self, txtfile):
        def open_file(txtfile):
            "Parse the text file into dictionary"
            with open(txtfile, 'r') as t_file:
                file_by_lines = t_file.readlines()
                return file_by_lines

        self.textlines = open_file(txtfile)

    def block_base(self):
        block = list()
        start = self.textlines.index("Assessment Categories:\n")

        return start

    def find_block(self):
        '''Find the block of Assessment Categories'''
        block = list()
        start = self.textlines.index("Assessment Categories:\n")
        for x in self.textlines[start+2:]:
            block.append(x)
            if x == '\n': break
        block.pop()
        return block

    def find_block_data(self):
        '''Find the corresponding data for Assessment Categories'''
        block = list()
        start = self.textlines.index("Assessment Categories:\n")
        offset = len(self.find_block())+1
        tag_start = start+offset+2
        tag_end = tag_start+offset
        for x in self.textlines[tag_start:tag_end]:
            block.append(x)
        block.pop()
        return block

    def block_pair(self):
        '''pair find_block with find_block_data'''
        labels = [x.rstrip() for x in self.find_block()]
        data = [x.rstrip() for x in self.find_block_data()]
        pairs = zip(labels, data)
        return list(pairs)

    def post_block(self):
        '''Return data after Assement Categories block'''
        block = list()
        start = self.textlines.index("Assessment Categories:\n")
        offset = len(self.find_block())+1
        tag_start = start+offset+2
        tag_end = tag_start+offset
        for x in self.textlines[tag_end-1:]:
            block.append(x)
        return block

    def parse_simple(self):
        "simple parse based on index only"
        visit = list()
        ifind = [9, 10, 11, 12, 16, 20, 24, 26,\
                27, 34, 35, 36, 37, 45, 46 ,47, 48]
        labels = ['client_id', 'address', 'city', 'phone', 'client_name',\
                'state', 'zipcode', 'date_open', 'municipality', 'inspector_id',\
                'inspector', 're_inspection', 'inspection_date', 'purpose',\
                'placarding', 're_inspection_date', 'nc_violation_count']
        data = [self.textlines[n].strip('\n') for n in ifind]
        visit = zip(labels, data)
        visit = list(visit)


        return visit

    def parse_stem(self):
        "Assign data to dictionary"
        #data prior to Assessment Categories should be consistent
        visit = dict()

        #Restaurant information
        try:
            visit['client_id'] = self.textlines[9].strip('\n')
        except IndexError as e:
            return None
        try:
            visit['address'] = self.textlines[10].strip('\n')
        except IndexError as e:
            return None
        try:
            visit['city'] = self.textlines[11].strip('\n')
        except IndexError as e:
            return None
        try:
            visit['phone'] = self.textlines[12].strip('\n')
        except IndexError as e:
            return None
        try:    
            visit['client_name'] = self.textlines[16].strip('\n')
        except IndexError as e:
            return None
        try:    
            visit['state'] = self.textlines[20].strip('\n')
        except IndexError as e:
            return None
        try:    
            visit['zipcode'] = self.textlines[24].strip('\n')
        except IndexError as e:
            return None
        
        try:
            dateopen = self.textlines[26].split(':')
            dateopen = dateopen[1]
            dateopen = dateopen.strip('\n')
            dateopen = dateopen.lstrip()
            visit['date_open'] = dateopen
        except IndexError as e:
            visit['date_open'] = ""
        try:    
            muni = self.textlines[27].split(':')
            muni = muni[1]
            muni = muni.strip('\n')
            muni = muni.lstrip()
            visit['municipality'] = muni
        except IndexError as e:
            visit['municipality'] = ""

            #Inspection specific information
        try:    
            visit['inspect_id'] = self.textlines[34].strip('\n')
        except IndexError as e:
            visit['inspect_id'] = ""
        try:    
            visit['inspector'] = self.textlines[35].strip('\n')
        except IndexError as e:
            visit['inspector'] = ""
        try:    
            visit['re_inspection'] = self.textlines[36].strip('\n')
        except IndexError as e:
            visit['re_inspection'] = ""
        try:
            visit['inspection_date'] = self.textlines[37].strip('\n')
        except IndexError as e:
            visit['inspection_date'] = ""

        #Inspection Details
        #relative to 'Inspection Details'
        try:
            visit['purpose'] = self.textlines[45].strip('\n')
        except IndexError as e:
            visit['purpose'] = ""
        try:
            visit['placarding'] = self.textlines[46].strip('\n')
        except IndexError as e:
            visit['placarding'] = ""
        try:
            visit['re_inspection_date'] = self.textlines[47].strip('\n')
        except IndexError as e:
            visit['re_inspection_date'] = ""
        try:
            visit['nc_violation_count'] = self.textlines[48].strip('\n')
        except IndexError as e:
            visit['nc_violation_count'] = ""

        return visit

    def parse_violation(self):
        '''Parse violation data'''
        #Critical Violations
        visit = self.parse_stem()
        if 'Critical Violation' in self.textlines[95:]:
            start_text = 'Critical Violation:\n'
            end_text = 'Non Critical Violation:\n'
            start_index = self.textlines.index(start_text)
            end_index = self.textlines.index(end_text) - 1
            visit['critical'] = self.textlines[start_index:end_index]

        #Non Critical Violations
        if 'Non Critical Violation:' in self.textlines[95:]:
            start_text = 'Non Critical Violation:'
            end_text = ""
            start_index = self.textlines.index(start_text)
            end_index = file_by_lines[-1]
            visit['non_critical'] = self.textlines[start_index:]

        return visit
    

    def parse_tuple(self):
        '''Convert dict to named tuple'''
        visit = namedtuple( 'Inspection',
        ['client_id', 
        'address', 
        'city', 
        'phone', 
        'client_name', 
        'state', 
        'zipcode', 
        'date_open', 
        'municipality', 
        'inspect_id', 
        'inspector', 
        're_inspection',
        'inspection_date', 
        'purpose', 
        'placarding', 
        're_inspection_date', 
        'nc_violation_count'])
        
        if self.parse_stem() is None:
            return visit
        else:
            visit = visit(**self.parse_stem())

            return visit

def inspection_labels():
    labels = ['Client ID:\n',
    'Address:\n',
    'City:\n',
    'Phone:\n',
    'Client Name:\n',
    'State:\n',
    'Zip:\n',
    'Date Open:\n',
    'Municipality:\n',
    'Inspect ID:\n',
    'Inspector Name:\n',
    'Re Inspection:\n',
    'Inspection Date:\n',
    'Purpose:\n',
    'Placarding:\n',
    'Re Inspection Date:\n',
    'Non Critical Violations #:\n',
    'Food Source/Condition\n',
    'Cooking Temperatures\n',
    'Consumer Advisory\n',
    'Reheating Temperatures\n',
    'Cooling Food\n',
    'Hot Holding Temperatures\n',
    'Cold Holding Temperatures\n',
    'Facilities to Maintain Temperature\n',
    'Date Marking of Food\n',
    'Probe-Type Thermometers\n',
    'Cross-Contamination Prevention\n',
    'Employee Health\n',
    'Personal Hygiene\n',
    'Sanitization\n',
    'Water Supply\n',
    'Waste Water Disposal\n',
    'Plumbing\n',
    'Handwashing Facilities\n',
    'Pest Management\n',
    'Certified Manager\n',
    'Demonstration of Knowledge\n',
    'Critical Violation:\n',
    'Non Critical Violations:\n']

    return labels

def parse_stem(file_by_lines):

    visit = dict()
    #Search strategies
    #Hard code
    #Find initial text, make rest relative
    #Such that there are 21 Assessment categories
    #Find 'Demonstration of Knowledge' plus 1 line, take next 20
    #Violation data functions differently

    #Restaurant information
    visit['client_id'] = file_by_lines[9]
    visit['address'] = file_by_lines[10]
    visit['city'] = file_by_lines[11]
    visit['phone'] = file_by_lines[12]
    
    visit['client_name'] = file_by_lines[16]
    visit['state'] = file_by_lines[20]
    visit['zipcode'] = file_by_lines[24]

    visit['date_open'] = file_by_lines[26]
    visit['municipality'] = file_by_lines[27]

    #Inspection specific information
    visit['inspect_id'] = file_by_lines[34]
    visit['inspector'] = file_by_lines[35]
    visit['re_inspection'] = file_by_lines[36]
    visit['inspection_date'] = file_by_lines[37]

    return visit

def parse_dict(file_by_lines):

    visit = dict()
    #Search strategies
    #Hard code
    #Find initial text, make rest relative
    #Such that there are 21 Assessment categories
    #Find 'Demonstration of Knowledge' plus 1 line, take next 20
    #Violation data functions differently

    #Restaurant information
    visit['client_id'] = file_by_lines[9]
    visit['address'] = file_by_lines[10]
    visit['city'] = file_by_lines[11]
    visit['phone'] = file_by_lines[12]
    
    visit['client_name'] = file_by_lines[16]
    visit['state'] = file_by_lines[20]
    visit['zipcode'] = file_by_lines[24]

    visit['date_open'] = file_by_lines[26]
    visit['municipality'] = file_by_lines[27]

    #Inspection specific information
    visit['inspect_id'] = file_by_lines[34]
    visit['inspector'] = file_by_lines[35]
    visit['re_inspection'] = file_by_lines[36]
    visit['inspection_date'] = file_by_lines[37]

    #Inspection Details
    #relative to 'Inspection Details'
    visit['purpose'] = file_by_lines[45]
    visit['placarding'] = file_by_lines[46]
    visit['re_inspection_date'] = file_by_lines[47]
    visit['nc_violation_count'] = file_by_lines[48]

    #Assessment catagories
    #relative to 'Assessment Categories:'
    visit['food_source_condition'] = file_by_lines[74]
    visit['cooking_temperatures'] = file_by_lines[75]
    visit['consumer_advisory'] = file_by_lines[76]
    visit['reheating_temperatures'] = file_by_lines[77]
    visit['cooling_food'] = file_by_lines[78]
    visit['hot_holding_temperatures'] = file_by_lines[79]
    visit['cold_holding_temperatures'] = file_by_lines[80]
    visit['facilities_maintain_temperature'] = file_by_lines[81]
    visit['date_marking'] = file_by_lines[82]
    visit['probe_type_thermometer'] = file_by_lines[83]
    visit['cross_contamination_prevention'] = file_by_lines[84]
    visit['employee_health'] = file_by_lines[85]
    visit['personal_hygiene'] = file_by_lines[86]
    visit['sanitization'] = file_by_lines[87]
    visit['water_supply'] = file_by_lines[88]
    visit['waste_water_disposal'] = file_by_lines[89]
    visit['plumbing'] = file_by_lines[90]
    visit['handwashing_facilities'] = file_by_lines[91]
    visit['pest_management'] = file_by_lines[92]
    visit['certified_manager'] = file_by_lines[93]
    visit['demonstration_of_knowledge'] = file_by_lines[94]

    #Critical Violations
    if 'Critical Violation' in file_by_lines[95:]:
        start_text = 'Critical Violation:'
        end_text = 'Non Critical Violation:'
        start_index = file_by_lines.index(start_text)
        end_index = file_by_lines.index(end_text) - 1
        visit['critical'] = file_by_lines[start_index:end_index]

    #Non Critical Violations
    if 'Non Critical Violation:' in file_by_lines[95:]:
        start_text = 'Non Critical Violation:'
        end_text = ""
        start_index = file_by_lines.index(start_text)
        end_index = file_by_lines[-1]
        visit['non_critical'] = file_by_lines[start_index:]

    return visit

def jsonify(visit):
    achd_json = json.dumps(visit)
    with open("inspection.json", "a") as achd_out:
        achd_out.write(achd_json)

def parse_tuple():

    visit = namedtuple( 'Inspection',
    ['client_id', 
    'address', 
    'city', 
    'phone', 
    'client_name', 
    'state', 
    'zipcode', 
    'date_open', 
    'municipality', 
    'inspect_id', 
    'inspector', 
    're_inspection',
    'inspection_date', 
    'purpose', 
    'placarding', 
    're_inspection_date', 
    'nc_violation_count',
    'food_source_condition',
    'cooking_temperatures', 
    'consumer_advisory',
    'reheating_temperatures',  
    'cooling_food',
    'hot_holding_temperatures', 
    'cold_holding_temperatures', 
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
    )

    return visit

def index_search(file_by_lines, labels):
    "search for index of label"
    "include EOL to "
    bin1 = list()
    for term in labels:
        for line in file_by_lines:
            if term in line:
                #'Assign index of line to the tuple'
                bin1.append((term, file_by_lines.index(line)))
                break # remove break to find multiple violations
    return bin1

def index_search_2(file_by_lines, labels):
    "search for index of label"
    for term in labels:
        for line in file_by_lines:
            if term in line:
                #'Assign index of line to the tuple'
                print(term, file_by_lines.index(line))        
        


def parse_min():
    '''named tuple example'''
    visit = namedtuple( 'Inspection',
    ['client_id', 
    'address', 
    'city', 
    'phone', 
    'client_name', 
    'state', 
    'zipcode', 
    'date_open', 
    'municipality', 
    'inspect_id', 
    'inspector', 
    're_inspection',
    'inspection_date', 
    'purpose', 
    'placarding', 
    're_inspection_date', 
    'nc_violation_count'])
    return visit