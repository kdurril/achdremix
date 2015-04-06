#achd_db_build

from inspection_parse import alt_queue, TextEval
from achd_db import conn, curs, qry_insert_inspect
from os.path import getsize

#get the string file locations
achd_files = alt_queue()


for doc in achd_files:
    work_doc = TextEval(doc)
    work_tuple = work_doc.parse_tuple()
    #
    assessment = list()
    assessment.append(work_tuple.inspect_id)
    assessment.extend(work_doc.block_pair())
    #
    violation = list()
    violation.append(work_tuple.inspect_id)
    violation.extend(work_doc.post_block())
    if len(str(work_tuple.inspect_id)) > 5:
    	'''
        try: 
            curs.execute(qry_insert_inspect, work_tuple)
            conn.commit()
        except ValueError as e:
            with open('log.txt', 'a') as logger:
            	logger.write(doc+'\n')
        '''
        try:
        	curs.execute(qry_insert_ass, assessment)
            conn.commit()
        except ValueError as e:
            with open('log_assessment.txt', 'a') as logger:
            	logger.write(doc+'\n')
        try:
        	curs.execute(qry_insert_violation, violation)
            conn.commit()
        except ValueError as e:
            with open('log_violation.txt', 'a') as logger:
            	logger.write(doc+'\n')

