import numpy as np
import matplotlib.pyplot as mtp
import pandas as pd
from sklearn.cluster import KMeans

dataset = pd.read_csv('./dataset/Mall_Customers.csv')

x = dataset.iloc[:, [3, 4]].values  

wcss_list = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(x)
    wcss_list.append(kmeans.inertia_)

mtp.plot(range(1, 11), wcss_list, marker='o')
mtp.title('The Elbow Method Graph')
mtp.xlabel('Number of Clusters (k)')
mtp.ylabel('WCSS (Within-Cluster Sum of Squares)')
mtp.show()

kmeans = KMeans(n_clusters=5, init='k-means++', random_state=42)
y_predict = kmeans.fit_predict(x)

colors = ['blue', 'green', 'red', 'cyan', 'magenta']
labels = ['Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4', 'Cluster 5']

for i in range(5):
    mtp.scatter(x[y_predict == i, 0], x[y_predict == i, 1], s=100, c=colors[i], label=labels[i])

mtp.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], 
            s=300, c='yellow', label='Centroids', edgecolors='black')

mtp.title('Clusters of Customers')
mtp.xlabel('Annual Income (k$)')
mtp.ylabel('Spending Score (1-100)')
mtp.legend()
mtp.show()
