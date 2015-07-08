import sqlite3
from collections import OrderedDict

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

def connect(db_name):
    connection = sqlite3.connect(db_name)
    connection.row_factory = ordered_dict_factory
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')
    cursor.execute('PRAGMA journal_mode = OFF')
    cursor.execute('PRAGMA synchronous = OFF')
    return (connection, cursor,)
