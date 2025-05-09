import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.tseries.offsets import DateOffset
from datetime import datetime, timedelta

def preprocess(file):
    df = pd.read_csv(file)
    df['CustomerDOB'] = pd.to_datetime(df['CustomerDOB'], format= "%d/%m/%Y")
    df['TransactionDate'] =pd.to_datetime(df['TransactionDate'], format= "%d/%m/%Y")
    df = df[df['TransactionAmount'] != 0]
    df = df[df['CustGender'] != 'T']
    invalid_dob = pd.Timestamp('1800-01-01 00:00:00')
    # Calculate median of valid dates
    median_dob = df.loc[df['CustomerDOB'] != invalid_dob, 'CustomerDOB'].median()
    # Replace invalid dates with the median
    df.loc[df['CustomerDOB'] == invalid_dob, 'CustomerDOB'] = median_dob
    df.loc[df['CustomerDOB'] > df['TransactionDate'], 'CustomerDOB'] -= DateOffset(years=100)
    df['CustomerAge'] =(df['TransactionDate'] - df['CustomerDOB']).dt.days //365

    #df.to_csv('../Da/clean_data.csv', index=False)
    return df