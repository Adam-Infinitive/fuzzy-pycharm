import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import csv
import pandas as pd
from auth import awscreds

ENDPOINT = awscreds.ENDPOINT
PORT = "5432"
USR = awscreds.USR
REGION = "us-east-1"
DBNAME = "postgres"
PASSWORD = awscreds.PASS

conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASSWORD)
cur = conn.cursor()
# auto commit changes
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)


# create table customers
def create_tb_customers():
    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS customers (
        SSN varchar(9),
        last_name varchar(30),
        first_name varchar(30),
        address varchar(150),
        city varchar(40),
        state varchar (2),
        zip varchar(5),
        primary key(SSN))""")
    except Exception as e:
        print(f"Create table failed due to: {e}")


# create table 'new_customers' - we will insert new_customers into customers if they do not already exist
def create_tb_new_customers():
    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS new_customers (
        SSN varchar(9),
        last_name varchar(30),
        first_name varchar(30),
        address varchar(150),
        city varchar(40),
        state varchar (2),
        zip varchar(5),
        primary key(SSN))""")
    except Exception as e:
        print(f"Create table failed due to: {e}")


def select_all_customers():
    try:
        cur.execute("""SELECT * FROM customers;""")
        query_results = cur.fetchall()
        print(query_results)
    except Exception as e:
        print(f"select failed: {e}")


def select_all_new_customers():
    try:
        cur.execute("""SELECT * FROM new_customers;""")
        query_results = cur.fetchall()
        print(query_results)
    except Exception as e:
        print(f"select failed: {e}")


# insert customers csv into table
def insert_customers_csv():
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


# insert new_customers csv into table
def insert_new_customers_csv():
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


# if new_customers do not exist customers table, insert them into customers !! Helper methods below !!
def check_missing_customers():

    # Select * from customers and import into pandas df
    try:
        select_query = pd.read_sql_query(
            '''select
              SSN,
              last_name,
              first_name,
              address,
              city,
              state,
              zip
              from customers''', conn)

        customers_df=pd.DataFrame(select_query, columns=['ssn', 'last_name', 'first_name', 'address', 'city', 'state', 'zip'])
    except Exception as e:
        print(f"Failed to insert customers into pandas df: {e}")

    # Select * from new_customers and import into pandas df
    try:
        select_query = pd.read_sql_query(
            '''select
              SSN,
              last_name,
              first_name,
              address,
              city,
              state,
              zip
              from new_customers''', conn)

        new_customers_df=pd.DataFrame(select_query, columns=['ssn', 'last_name', 'first_name', 'address', 'city', 'state', 'zip'])
    except Exception as e:
        print(f"Failed to insert new_customers into pandas df: {e}")

    try:
        print("Checking for missing customers..")
        missing_customers = find_missing_values(new_customers_df, customers_df)
        print(missing_customers)
        insert_missing_customers(missing_customers)
    except Exception as e:
        print(f"Error checking for missing customers: {e}")


def find_missing_values(new_customers, customers):
    result = new_customers[~new_customers.isin(customers)]
    return result.dropna()


def insert_missing_customers(df):
    tuples = [tuple(x) for x in df.to_numpy()]
    print(tuples)
    try:
        insert_sql = """INSERT INTO customers VALUES(%s, %s, %s, %s, %s, %s, %s)"""
        cur.executemany(insert_sql, tuples)
    except Exception as e:
        print(f"Error inserting values {e}")


if __name__ == "__main__":
    create_tb_customers()
    create_tb_new_customers()
    insert_customers_csv()
    insert_new_customers_csv()
    check_missing_customers()
