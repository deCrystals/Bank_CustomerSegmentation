import pandas as pd
from datetime import timedelta

def calculate_rfm(df):
    today = df['TransactionDate'].max() + timedelta(days=1)
    rfm = df.groupby('CustomerID').agg({
        'TransactionDate': lambda x: (today - x.max()).days,
        'TransactionID': 'count',
        'TransactionAmount': 'sum'
    }).rename(columns={
        'TransactionDate':'Recency',
        'TransactionID':'Frequency',
        'TransactionAmount':'Monetary'
    })

    demographics = df.groupby('CustomerID').agg({
        'CustGender': 'first',
        'CustLocation': 'first',
        'CustAccountBalance': 'first',
        'CustomerAge': 'first'
    })

    rfm = rfm.merge(demographics, how='left', on='CustomerID')

    rfm.to_csv('../Data/rfm.csv')


    return rfm