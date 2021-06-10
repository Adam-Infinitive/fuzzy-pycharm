import pandas as pd
import csv
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# function that first checks if the name occurs exactly in both columns
# if it doesn't, it runs token_set_ratio on the pair
def checker(correct_options,wrong_options):
    names_array = []
    ratio_array = []
    for wrong_option in wrong_options:
        if wrong_option in correct_options:
            names_array.append(wrong_option)
            ratio_array.append('100')
        else:
            x=process.extractOne(wrong_option, correct_options, scorer=fuzz.token_set_ratio)
            names_array.append(x[0])
            ratio_array.append(x[1])
    return names_array, ratio_array
