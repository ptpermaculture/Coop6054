#! /usr/bin/env python

# Accepts csv file of product information and inserts into appropriate database fields.

DEBUG = True;
verbose = True;

# mapping headers to database fields
product_code = "code"
description = "product"
brand = "company"
#weight/vol
price_wholesale = "price of product"
#price/100g
#quantity
#total price

def login():
    import psycopg2
    try:
        conn = psycopg2.connect("dbname=coop_db host=localhost user=django_user password=Ginkgoale5")
    except:
        print "Unable to connect to the database."
    cur = conn.cursor()
    if DEBUG:
        cur.execute("SELECT * FROM coop_web_distributor;")
        print(cur.fetchone())
    return conn, cur

def process_csv(csvfile, conn, cur):
   file = open(csvfile)
   headers = file.readline().rstrip().split(',');
   headers = [header.strip('"') for header in headers]
   rows = [line.rstrip().split(',') for line in file]
   stripped_rows = []
   for row in rows:
       row = [rec.strip('"') for rec in row]
       stripped_rows.append(row)
   rows = stripped_rows
   rowdicts = [dict(zip(headers, row)) for row in rows]
   if DEBUG:
       for row in rows:
           print(row)
       print(rows[0])
       print(headers)
       print(rowdicts[0])
   for d in rowdicts:
       p_c = d[product_code]
       des = d[description]
       b = d[brand]
       p_w = d[price_wholesale]
       if p_c != '': 
           query = "INSERT INTO coop_web_product (product_code, description, brand, price_wholesale) VALUES ('"+p_c+"', '"+des+"', '"+b+"', '"+p_w+"');"
           cur.execute(query)
   if conn: conn.commit()
   if verbose: print(len(rows), 'rows loaded')


if __name__ == '__main__':
    import sys
    csvfile = "pemco.csv"
    if len(sys.argv) > 1: csvfile = sys.argv[1]
    conn, cur = login()
    process_csv(csvfile, conn, cur)
