#!/usr/bin/python
import sqlite3
from os import path   
import csv
import sys 

def convert_to_csv(db_name):
    print path.join(db_name)
    conn = sqlite3.connect(path.join(db_name))
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    #zf = zipfile.ZipFile('zipfile_write.zip', mode='w')
    for table in tables:
        table = table[0]
        if table.startswith("features"):
            cursor.execute('SELECT S.name, * FROM ' + table + ' AS C JOIN sequences AS S ON C.sequences_id = S.id')
            column_names = [column_name[0] for column_name in cursor.description]
            #print column_names
            if column_names == ['name', 'sequences_id', 'strand', 'position', 'value', 'id', 'uuid', 'name', 'length', 'topology']:
                print table
                print "Position type"
                with open(path.join(table + '.txt'), 'w') as csv_file:
                    csv_writer = csv.writer(csv_file, delimiter='\t')
                    csv_writer.writerow(['Locus', 'Strand', 'Start', 'End', 'Value'])
                    while True:
                        try:
                            line = cursor.fetchone()
                            if line:
                                csv_writer.writerow([line[0], line[2], line[3], line[3], line[4]])
                            else:
                                #zf.write(path.join(table + '.txt'))
                                break
                        except csv.Error:
                            break
            elif column_names == ['name', 'sequences_id', 'strand', 'start', 'end', 'value', 'id', 'uuid', 'name', 'length', 'topology']:
                print table
                print "Segment type"
                with open(path.join(table + '.txt'), 'w') as csv_file:
                    csv_writer = csv.writer(csv_file, delimiter='\t')
                    csv_writer.writerow(['Locus', 'Strand', 'Start', 'End', 'Value'])
                    while True:
                        try:
                            line = cursor.fetchone()
                            if line:
                                csv_writer.writerow([line[0], line[2], line[3], line[4], line[5]])
                            else:
                                #zf.write(path.join(table + '.txt'))
                                break
                        except csv.Error:
                            break
            elif column_names == ['name', 'sequences_id', 'strand', 'start', 'end', 'name', 'common_name', 'gene_type', 'id', 'uuid', 'name', 'length', 'topology']:
                print table
                print "Annotation type"
            elif 'value0' in column_names:
                print table
                print "matrix"
                value_columns = filter(lambda x: 'value' in x, column_names)
                cont = 0
                c = cursor.fetchall()
                for i in value_columns:
                    print i
                    with open(path.join(table + i + '.txt'), 'w') as csv_file:
                        csv_writer = csv.writer(csv_file, delimiter='\t')
                        csv_writer.writerow(['Locus', 'Strand', 'Start', 'End', 'Value'])
                        for x in range(0,len(c)):
                                line = c[x]
                                if line:
                                    print x
                                    csv_writer.writerow([line[0], line[2], line[3], line[4], line[5+cont]])
                                else:
                                    break
                        cont = cont + 1



convert_to_csv(sys.argv[1])