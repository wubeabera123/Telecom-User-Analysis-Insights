import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

class UserExperienceAnalysis:
    def __init__(self, data):
        self.data = data

    def treat_missing_outliers(self, column):
        """Handle missing values and outliers."""
        # Replace missing values with the median
        self.data[column].fillna(self.data[column].median(), inplace=True)

    def aggregate_customer_info(self):
        """Task 3.1: Aggregate network parameters per customer (average values)."""
        tcp_column = 'TCP DL Retrans. Vol (Bytes)'
        rtt_column = 'Avg RTT DL (ms)'
        throughput_column = 'Avg Bearer TP DL (kbps)'
        handset_column = 'Handset Type'

        # Treat missing values and outliers for each column
        self.treat_missing_outliers(tcp_column)
        self.treat_missing_outliers(rtt_column)
        self.treat_missing_outliers(throughput_column)

        # Aggregate customer data
        customer_agg = self.data.groupby('IMSI').agg({
            tcp_column: 'mean',
            rtt_column: 'mean',
            throughput_column: 'mean',
            handset_column: 'first'
        }).reset_index()

        return customer_agg

    def top_bottom_frequent_values(self, column):
        """Task 3.2: Compute and list top, bottom, and most frequent values."""
        top_10 = self.data[column].nlargest(10)
        bottom_10 = self.data[column].nsmallest(10)
        most_frequent = self.data[column].mode().tolist()[:10]

        return top_10, bottom_10, most_frequent

    def throughput_distribution_per_handset(self):
        """Task 3.3: Distribution of average throughput per handset type."""
        throughput_column = 'Avg Bearer TP DL (kbps)'
        handset_column = 'Handset Type'
        
        # Aggregate data for throughput per handset type
        throughput_per_handset = self.data.groupby(handset_column)[throughput_column].mean().reset_index()

        # Plot distribution
        plt.figure(figsize=(12, 6))
        sns.barplot(x=handset_column, y=throughput_column, data=throughput_per_handset)
        plt.title('Average Throughput per Handset Type')
        plt.xlabel('Handset Type')
        plt.ylabel('Average Throughput (kbps)')
        plt.xticks(rotation=45)
        plt.show()

    def average_tcp_per_handset(self):
        """Task 3.3: Average TCP retransmission per handset type."""
        tcp_column = 'TCP DL Retrans. Vol (Bytes)'
        handset_column = 'Handset Type'

        # Aggregate data for TCP retransmission per handset type
        tcp_per_handset = self.data.groupby(handset_column)[tcp_column].mean().reset_index()

        # Plot average TCP retransmission
        plt.figure(figsize=(12, 6))
        sns.barplot(x=handset_column, y=tcp_column, data=tcp_per_handset)
        plt.title('Average TCP Retransmission per Handset Type')
        plt.xlabel('Handset Type')
        plt.ylabel('Average TCP Retransmission (Bytes)')
        plt.xticks(rotation=45)
        plt.show()

    def kmeans_clustering(self, n_clusters=3):
        """Task 3.4: Perform k-means clustering and describe each cluster."""
        # Prepare data for clustering
        clustering_data = self.data[['Avg RTT DL (ms)', 'Avg Bearer TP DL (kbps)', 'TCP DL Retrans. Vol (Bytes)']]
        clustering_data.fillna(clustering_data.median(), inplace=True)
        
        # Normalize data
        normalized_data = (clustering_data - clustering_data.mean()) / clustering_data.std()

        # Apply k-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        clusters = kmeans.fit_predict(normalized_data)
        self.data['Cluster'] = clusters

        # Describe each cluster
        cluster_description = self.data.groupby('Cluster').agg({
            'Avg RTT DL (ms)': ['mean', 'std'],
            'Avg Bearer TP DL (kbps)': ['mean', 'std'],
            'TCP DL Retrans. Vol (Bytes)': ['mean', 'std'],
            'Handset Type': lambda x: x.mode().iloc[0]  # Most frequent handset type
        }).reset_index()

        return self.data, cluster_description
