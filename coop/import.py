#! /usr/bin/env python

filename = 'pemco.csv'
ENDDB = ''
ENDREC = '\n'
RECSEP = ','
def readProductFile(filename=filename):
    file = open(filename)
    import sys
    sys.stdin = file
    db = {}
    key = input()
    while key !=ENDDB:
        rec = {}
        field = input()
        while field !=ENDREC:
            name, value = field.split(RECSEP)
            rec[name] = eval(value)
            field = input()
        db[key] = rec
        key = input()
    return db

if __name__ == '__main__':
    print(readProductFile())
