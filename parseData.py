#!/usr/bin/env python

import os, sys, csv, psycopg2, argparse

# db variables
db = {
    'dbname': 'db2-project',
    'user': 'boubou',
    'host': 'localhost',
    'password': ''
}
try:
    conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s" % (db['dbname'], db['user'], db['host'], db['password']))
    conn.set_isolation_level(0)
except:
    print "I am unable to connect to the database"
    quit()

cur = conn.cursor()

# get command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--all', action='store_true')
parser.add_argument('vars', nargs='*')

args = parser.parse_args()

# This is the path where you want to search
path = '.'
# this is the extension you want to detect
extension = '.csv'
# this is the map between fileNames and SQL structure
fileToSQL = {
    'account': ['"acc-number"', '"dollar-balance"', '"branch-number"'],
    'branch': ['"branch-number"', '"branch-name"', 'city'],
    'client': ['"client-number"', 'lastname', 'firstname', '"marital-status"', '"postal-code"', 'phone', 'city'],
    'owns': ['"acc-number"', '"client-number"']
}


# functions
def getFileName(file_name_path):
    lastSlash = file_name_path.rfind('/')

    startIndex = 0 if lastSlash == 1 else lastSlash + 1
    endIndex = lastDot = file_name_path.rfind('.')

    return file_name_path[startIndex:endIndex]

def loadAllCSV():
    for root, dirs_list, files_list in os.walk(path):
        for file_name in files_list:
            if os.path.splitext(file_name)[-1] == extension:
                file_name_path = os.path.join(root, file_name)
                print file_name_path
                loadCSV(file_name_path)


def loadCSV(file_name_path):
    if extension not in file_name_path:
        file_name_path += extension

    tableName = getFileName(file_name_path)
    if tableName not in fileToSQL:
        print "\t%s not found in map" % file_name_path
        return

    tableFields = fileToSQL[tableName]
    numFields = len(tableFields)
    columns = '(' + ','.join(tableFields) + ')'
    print tableName

    with open(file_name_path, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            row = row[0:numFields]
            if row[0] == '':
                continue

            parameters = '(' + ','.join(['%s' for i in range(numFields)]) + ')'

            try:
                query = """INSERT INTO {} {} VALUES {}""".format(tableName, columns, parameters)
                cur.execute(query, tuple(row))
            except Exception as e:
                print "Bad line %s -- %s" % (row, e)



# main
if not args.all and not args.vars:
    print "Either use --all to process all data files or specify every desired relative paths to files separated by spaces"
    print "e.g. --all or data/<file1> other/dir/<file2> ..."
elif args.all:
    loadAllCSV()
else:
    for arg in args.vars:
        print arg
        loadCSV(arg)
