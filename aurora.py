import psycopg2
import sys
import boto3
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import csv
import pandas as pd
import checker as check

ENDPOINT = "database-1.cluster-c5taqjr7582g.us-east-1.rds.amazonaws.com"
PORT = "5432"
USR = "asiwiec"
REGION = "us-east-1"
DBNAME = "postgres"

conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user='postgres',
                        password="Sonny51299?")  # ,ssl_ca='[full path]rds-combined-ca-bundle.pem')
cur = conn.cursor()

# auto commit changes
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# create table customers
try:
    cur.execute("""CREATE TABLE IF NOT EXISTS customers (
    SSN int,
    last_name varchar(30),
    first_name varchar(30),
    address varchar(150),
    city varchar(40),
    state varchar (2),
    zip int,
    primary key(SSN))""")
except Exception as e:
    print(f"Create table failed due to: {e}")

# create table 'new_customers' - we will validate later if they are duplicates
try:
    cur.execute("""CREATE TABLE IF NOT EXISTS new_customers (
    SSN int,
    last_name varchar(30),
    first_name varchar(30),
    address varchar(150),
    city varchar(40),
    state varchar (2),
    zip int,
    primary key(SSN))""")
except Exception as e:
    print(f"Create table failed due to: {e}")

# Insert initial data into customers
# try:
#     cur.execute(""" INSERT INTO customers values(
#     100996544,
#     'siwiec',
#     'adam',
#     '123 legacy drive',
#     'palm beach',
#     'FL',
#     33410)
#     """)
# except Exception as e:
#     print(f"Insert failed/values already exist: {e}")

# Select all from Customers
try:
    cur.execute("""SELECT * FROM customers;""")
    query_results = cur.fetchall()
    print(query_results)
except Exception as e:
    print(f"select failed: {e}")

# insert sample csv into table
try:
    with open(r'csv-data-main/sample-data.csv', 'r') as f:
        reader=csv.reader(f)
        next(reader)  # Skip the header row.
        for row in reader:
            cur.execute(
                "INSERT INTO customers VALUES (%s, %s, %s, %s, %s, %s, %s)",
                row
            )
    print("successful sample-data.csv insert")
except Exception as e:
    print(f"csv insert failed: {e}")

# insert check csv into table
try:
    with open(r'csv-data-main/check-data.csv', 'r') as f:
        reader=csv.reader(f)
        next(reader)  # Skip the header row.
        for row in reader:
            cur.execute(
                "INSERT INTO new_customers VALUES (%s, %s, %s, %s, %s, %s, %s)",
                row
            )
    print("successful check-data.csv insert")
except Exception as e:
    print(f"csv insert failed: {e}")


# select data from SQL and import into pandas df
try:
    SQL_Query = pd.read_sql_query(
        '''select
          SSN,
          last_name,
          first_name,
          address,
          city,
          state,
          zip
          from customers''', conn)

    customers_df=pd.DataFrame(SQL_Query, columns=['ssn', 'last_name', 'first_name', 'address', 'city', 'state', 'zip'])
except Exception as e:
    print(f"failed to insert into pandas df: {e}")

print(customers_df)

# select NEW customers data from SQL and import into pandas df
try:
    SQL_Query = pd.read_sql_query(
        '''select
          SSN,
          last_name,
          first_name,
          address,
          city,
          state,
          zip
          from new_customers''', conn)

    new_customers_df=pd.DataFrame(SQL_Query, columns=['ssn', 'last_name', 'first_name', 'address', 'city', 'state', 'zip'])
except Exception as e:
    print(f"failed to insert into pandas df: {e}")

print(new_customers_df)

# this doesn't work yet ##########################################

#if new_customers do not exist customers table, insert them into customers
def insert_df_customers(df):
    ssn = df['ssn'].to_string(index=False)
    try:
        insert_sql = """INSERT INTO customers VALUES %s, %s, %s, %s, %s, %s, %s"""
        cur.execute(insert_sql, (100886777, df['last_name'].to_string(index=False),
                                 df['first_name'].to_string(index=False), df['address'].to_string(index=False),
                    df['city'].to_string(index=False), df['state'].to_string(index=False), df['zip'].to_string(index=False)))
    except Exception as e:
        print(f"Error inserting values {e}")
    # print(df)
    # try:
    #     cur.execute('''INSERT INTO customers VALUES df['ssn'], df['last_name'], df['first_name'], df['address'],
    #     df['city'], df['state'], df['zip']''')
    # except Exception as e:
    #     print(f"Error inserting values {e}")


try:
    print("Checking for missing customers..")
    missing_customers = check.find_missing_values(new_customers_df, customers_df)
    print(missing_customers)
    # if missing_customers:
    print("Inserting missing customers into customers table...")
    insert_df_customers(missing_customers)
except:
    print("error checking for missing customers")

