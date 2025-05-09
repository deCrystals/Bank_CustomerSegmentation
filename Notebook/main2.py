import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from preprocessing import preprocess
from rfm import calculate_rfm
from segmentation import segment_customer
import os

print("Loading Data..........")

df = preprocess('../Dataset/bank_data_C.csv')

print("Data loaded successfully")

print("Calculating RFM............")
rfm = calculate_rfm(df)

rfm = segment_customer(rfm)
rfm_features = rfm[['Recency', 'Frequency', 'Monetary']].copy()

print("RFM Completed")   

print("Starting Clustering........")

scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_features)
n_clusters = 4

kmeans = KMeans(n_clusters=n_clusters, random_state=42)
rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

print('Clustering Completed')

cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
#print(f'Cluster _centers =  {cluster_centers}')

cluster_scores = rfm.groupby('Cluster')[['Recency', 'Frequency', 'Monetary']].mean().round(1)
print(f' The Cluster Scores : \n {cluster_scores}')


print("Clustering Completed Sucessfully")

#os.makedirs('Data', exist_ok=True)
#rfm.to_csv('../Data/bank.csv')
rfm.to_csv('../Dataset/bank.csv')

print("Segmented customer data saved to 'Dataset/bank.csv")
