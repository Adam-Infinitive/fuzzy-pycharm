import pandas as pd
import csv
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
from csv import reader

# Import Data
test_data = pd.read_csv('csv-data-main\\sample-data-simple.csv', index_col=False)
sample_data = pd.read_csv('csv-data-main\\ssn-sample-data.csv', index_col=False)
fraud_data = pd.read_csv('csv-data-main\\ssn-fraud-sample-data.csv', index_col=False)

def checker()
for x in range(len(simple_data)):
    simple_data.columns = ['','','','','','','']
    print(str(simple_data.loc[[x]].to_string(index=False)))

