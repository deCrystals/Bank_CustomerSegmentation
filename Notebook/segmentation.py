import pandas as pd
import numpy as np


def assign_rfm_scores(rfm):
    rfm = rfm.copy()
    print('Calculating RFM Scores .......')
    
    try:
        rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1], duplicates='drop')
        rfm['F_Score'] = rfm['Frequency'].apply(freq_score)
        rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5], duplicates='drop')
        rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
        rfm['Scores'] = rfm['R_Score'].astype(int) + rfm['F_Score'].astype(int) + rfm['M_Score'].astype(int)
    except ValueError as e:
        print(f"Error assigning scores: {e}. Check if data has enough variability.")
        rfm['R_Score'] = 1
        rfm['F_Score'] = 1
        rfm['M_Score'] = 1
        rfm['RFM_Score'] = '111'
        rfm['Scores'] = 3
    return rfm


def freq_score(f):
    if f == 1:
        return 1
    elif f == 2:
        return 2
    elif f == 3:
        return 3
    elif f == 4:
        return 4
    else:
        return 5


def assign_segment(rfm):
    def segment_label(score):
        if score >= 12:
            return 'High Value'
        elif score >= 9:
            return 'Loyal'
        elif score >= 6:
            return 'Potential'
        else:
            return 'At Risk'
    
    rfm['Segment'] = rfm['Scores'].apply(segment_label)
    return rfm


def segment_customer(df):
    df = assign_rfm_scores(df)
    df = assign_segment(df)
    return df

