import sqlite3
from collections import OrderedDict
import csv

def unique_key(dct, key):
    if key in dct:
        return unique_key(dct, '_{0}'.format(key))
    else:
        return key 

def ordered_dict_factory(cursor, row):
    dct = OrderedDict()
    for i, column_name in enumerate(cursor.description):
        key = unique_key(dct, column_name[0])
        dct[key] = row[i]
    return dct

class Dumper(object):

    def __init__(self, db_name='qux.db'):
        connection = sqlite3.connect(db_name) 
        connection.row_factory = ordered_dict_factory
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON')
        self.cursor = cursor

    def dump(self, sql, csv_file_name):
        if sql is None or csv_file_name is None:
            raise Exception('sql or csv_file_name is None')
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        with open(csv_file_name, 'wb') as f:
            w = csv.writer(f, quoting=csv.QUOTE_MINIMAL, delimiter=',')
            w.writerow(data[0].keys())
            w.writerows([d.values() for d in data])
