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
    except ValueError as e:
        print(f"Error assigning scores: {e}. Check if data has enough variability.")
        rfm['R_Score'] = 1
        rfm['F_Score'] = 1
        rfm['M_Score'] = 1
        rfm['RFM_Score'] = '111'
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
    
    def segment_label(row):
        r, f, m = int(row['R_Score']), int(row['F_Score']), int(row['M_Score'])
        
        # High Value - customers with high monetary value
        if m >= 4 and f >= 3:
            return 'High Value'  # High spending and frequent transactions
            
        # Loyal - customers who have been active for a while with good engagement
        elif r >= 3 and f >= 3 and m >= 2:
            return 'Loyal'  # Consistent activity over time
            
        # New Customer - recently active but limited history
        elif r >= 4 and f <= 2:
            return 'Potential'  # Very recent activity but few transactions
            
        # At Risk - declining activity or low recency
        else:
            return 'At Risk'  # Low engagement or inactive
    
    rfm['Segment'] = rfm.apply(segment_label, axis=1)  # Uncommented this line
    return rfm


def segment_customer(df):
    df = assign_rfm_scores(df)
    df = assign_segment(df)  # Changed to assign the return value back to df
    return df
