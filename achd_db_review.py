#achd_db_review
#check the transformations of the records
from achd_db import conn, curs

labels = ['client_id', 'address', 'city', 'phone', 'client_name',\
            'state', 'zipcode', 'date_open', 'municipality', 'inspector_id',\
            'inspector', 're_inspection', 'inspection_date', 'purpose',\
            'placarding', 're_inspection_date', 'nc_violation_count']

#if a column has null data that should not, parse that record again
state_ch = curs.execute('''SELECT client_id, count(state) AS countState 
	                       FROM inspection 
	                       WHERE state = ""; ''')
state = state_ch.fetchall()
state

#If column has non state data, reparse file
#reparse all non-PA entries
#non-empty strings are from another category, adjust accordingly
#most are client_name
#zipcode
#data_open or inspection_date
state_count = curs.execute('''SELECT state, count(state) AS countState 
	                       FROM inspection 
	                       GROUP BY state 
	                       ORDER BY state; ''')
state_count.fetchall()

unique_review = curs.execute(''' SELECT inspect_id
	                             FROM inspection
	                             GROUP BY inspect_id
	                             HAVING COUNT(inspect_id) > 2
	                            ''')
unique_review.fectchall()

unique_delete = "DELECT FROM inspection WHERE inspect_id IN ("+unique_review+");"