"""
Module: File Handler
Author: Hussain Ali Khan
Version: 1.0.1
Last Modified: 27/11/2018 (Tuesday)
"""


import pandas as pd
import json


def save_as_csv(filename, data):
    df = pd.DataFrame(data)
    df.to_csv(filename + ".csv")


def save_as_json(filename, data):
    with open(filename + '.json', 'w') as file:
        json.dump(data, file)
