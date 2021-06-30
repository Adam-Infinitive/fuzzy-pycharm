import pandas as pd
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

# Import Data
check_data = pd.read_csv('csv-data-main/check-data.csv', index_col=False)
sample_data = pd.read_csv('csv-data-main/sample-data.csv', index_col=False)
fraud_data = pd.read_csv('csv-data-main/ssn-fraud-sample-data.csv', index_col=False)


def find_missing_values(check, sample):
    result = check[~check.isin(sample)]
    return result.dropna()


def checker(check, sample):
    check_arr = []
    verify_arr = []
    match_arr = []
    missing_arr = []
    for x in range(len(check)):
        check.columns = ['','','','','','','']
        check_arr.append(str(check.loc[[x]].to_string(index=False)))
    for x in range(len(sample)):
        sample.columns = ['','','','','','','']
        verify_arr.append(str(sample.loc[[x]].to_string(index=False)))

    for x in check_arr:
        if x in verify_arr:
            print("FOUND MATCH!!")
            # print(x + "\n")
            match_arr.append(x)
        if x not in verify_arr:
            missing_arr.append(x)
            print(f"This row does not exist in sample:\n {x}")
    return missing_arr

def checker2(check, sample):
    check_arr = pd.DataFrame
    verify_arr = pd.DataFrame
    match_arr = pd.DataFrame
    missing_df = pd.DataFrame
    for x in range(len(check)):
        check.columns = ['','','','','','','']
        # check_arr.append(str(check.loc[[x]].to_string(index=False)))
    for x in range(len(sample)):
        sample.columns = ['','','','','','','']
        # verify_arr.append(str(sample.loc[[x]].to_string(index=False)))
    # print(check)
    for index, row in check.iterrows():
        print(row)
        # if x in verify_arr:
        #     print("FOUND MATCH!!")
        #     # print(x + "\n")
        #     match_arr.append(x)
        # if x not in verify_arr:
        #     missing_df.append(x, ignore_index=True, verify_integrity=False, sort=False)
        #     print(f"This row does not exist in sample:\n {x}")
    return missing_df