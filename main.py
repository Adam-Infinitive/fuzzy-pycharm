import pandas as pd
import csv
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import theresa
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

# Import Data
sample_data = pd.read_csv('csv-data-main\\ssn-sample-data.csv', index_col=False)
fraud_data = pd.read_csv('csv-data-main\\ssn-fraud-sample-data.csv', index_col=False)


def peek(df):
    col_array = []
    for col in df.columns:
        col_array.append(col.lower())
    print(f"Here are your columns:\n{col_array}")
    col_name = input("Enter a column name to peek or -1 to exit.. ").lower()
    while col_name != "-1":
        if col_name in col_array:
            print(sample_data[col_name])
            col_name = input("Enter a column name to peek or -1 to exit.. ").lower()
        else:
            print(f"\nERROR: That column does not exist in the df. Here are the columns: \n {col_array}")
            col_name = input("Enter a column name to peek or -1 to exit.. ").lower()


def checker(correct_df, wrong_df):
    fname_arr_correct = []
    lname_arr_correct = []
    fullname_arr_correct = []
    ssn_arr_correct = []
    fname_arr_fraud = []
    lname_arr_fraud = []
    fullname_arr_fraud = []
    ssn_arr_fraud = []

    # df --> array
    for fname in correct_df['first name']:
        fname_arr_correct.append(fname)
    for lname in correct_df['last name']:
        lname_arr_correct.append(lname)
    for ssn in correct_df['SSN']:
        ssn_arr_correct.append(ssn)
    for fname in wrong_df['first name']:
        fname_arr_fraud.append(fname)
    for lname in wrong_df['last name']:
        lname_arr_fraud.append(lname)
    for ssn in wrong_df['SSN']:
        ssn_arr_fraud.append(ssn)

    # combine first and last
    for x in range(len(fname_arr_correct)):
        fullname_arr_correct.append(fname_arr_correct[x] + " " + lname_arr_correct[x])
    for x in range(len(fname_arr_correct)):
        fullname_arr_fraud.append(fname_arr_fraud[x] + " " + lname_arr_fraud[x])

    print(f"First Name: {fuzz.ratio(fname_arr_correct,fname_arr_fraud)}")

    print(f"Last Name: {fuzz.ratio(lname_arr_correct,lname_arr_fraud)}")

    print(f"First & Last Name: {fuzz.ratio(fullname_arr_correct,fullname_arr_fraud)}")

    print(f"First & Last Name partial: {fuzz.token_sort_ratio(fullname_arr_correct,fullname_arr_fraud)}")

    print(f"Social: {fuzz.ratio(ssn_arr_correct,ssn_arr_fraud)}")



# def df_checker(sample, fraud):


if __name__ == "__main__":
    # peek(sample_data)
    # print(fuzz.ratio(sample_data["first name"].data, fraud_data["first name"].data))

    # names, ratio = theresa.checker(sample_data, fraud_data)
    #
    # print(f"Names: \n {names} \n")
    # print(f"Ratio: \n {ratio} \n\n\n")
    #
    checker(sample_data, fraud_data)




# Process

# print(process.extract("mark", sample_data['first name']))