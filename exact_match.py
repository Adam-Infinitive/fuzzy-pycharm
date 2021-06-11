import pandas as pd
import csv
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
from csv import reader

# Import Data
check_data = pd.read_csv('csv-data-main/check-data.csv', index_col=False)
sample_data = pd.read_csv('csv-data-main/sample-data.csv', index_col=False)
fraud_data = pd.read_csv('csv-data-main\\ssn-fraud-sample-data.csv', index_col=False)

def checker(check, sample):
    check_arr = []
    verify_arr = []
    match_arr = []
    for x in range(len(check)):
        check.columns = ['','','','','','','']
        check_arr.append(str(check.loc[[x]].to_string(index=False)))
    for x in range(len(sample)):
        sample.columns = ['','','','','','','']
        verify_arr.append(str(sample.loc[[x]].to_string(index=False)))

    for x in check_arr:
        if x in verify_arr:
            print("FOUND MATCH!!")
            print(x + "\n")
            match_arr.append(x)

checker(check_data,sample_data)