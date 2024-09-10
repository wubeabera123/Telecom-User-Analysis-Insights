# user_engagement_analysis.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

class UserEngagementAnalysis:
    def __init__(self, data):
        self.data = data

    def aggregate_metrics_per_customer(self):
        """Aggregate session frequency, session duration, and total traffic per customer (MSISDN/Number)."""
        
        # Convert 'Total UL (Bytes)' and 'Total DL (Bytes)' to numeric, handle non-numeric with 'coerce'
        self.data['Total UL (Bytes)'] = pd.to_numeric(self.data['Total UL (Bytes)'], errors='coerce')
        self.data['Total DL (Bytes)'] = pd.to_numeric(self.data['Total DL (Bytes)'], errors='coerce')

        if self.data['Total UL (Bytes)'].isnull().all() or self.data['Total DL (Bytes)'].isnull().all():
            raise ValueError("Columns 'Total UL (Bytes)' or 'Total DL (Bytes)' have invalid data and could not be converted to numeric.")

        # Perform aggregation: total_traffic sums UL and DL per user
        agg_data = self.data.groupby('MSISDN/Number').agg(
            session_frequency=('Bearer Id', 'count'),
            total_session_duration=('Dur. (ms)', 'sum'),
            total_traffic=('Total UL (Bytes)', 'sum')
        ).reset_index()

        agg_data['total_traffic'] += self.data.groupby('MSISDN/Number')['Total DL (Bytes)'].sum().values
        return agg_data

    def top_10_customers_per_metric(self, agg_data):
        """Get the top 10 customers per engagement metric."""
        top_customers = {}
        top_customers['session_frequency'] = agg_data.nlargest(10, 'session_frequency')
        top_customers['total_session_duration'] = agg_data.nlargest(10, 'total_session_duration')
        top_customers['total_traffic'] = agg_data.nlargest(10, 'total_traffic')

        return top_customers

    def normalize_and_cluster(self, agg_data, n_clusters=3):
        """Normalize the metrics and run K-Means clustering."""
        metrics = agg_data[['session_frequency', 'total_session_duration', 'total_traffic']]
        scaler = StandardScaler()
        normalized_metrics = scaler.fit_transform(metrics)

        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        agg_data['cluster'] = kmeans.fit_predict(normalized_metrics)

        return agg_data, kmeans

    def compute_cluster_statistics(self, clustered_data):
        """Compute min, max, average & total metrics for each cluster."""
        cluster_stats = clustered_data.groupby('cluster').agg(
            min_session_frequency=('session_frequency', 'min'),
            max_session_frequency=('session_frequency', 'max'),
            avg_session_frequency=('session_frequency', 'mean'),
            total_session_frequency=('session_frequency', 'sum'),
            min_session_duration=('total_session_duration', 'min'),
            max_session_duration=('total_session_duration', 'max'),
            avg_session_duration=('total_session_duration', 'mean'),
            total_session_duration=('total_session_duration', 'sum'),
            min_traffic=('total_traffic', 'min'),
            max_traffic=('total_traffic', 'max'),
            avg_traffic=('total_traffic', 'mean'),
            total_traffic=('total_traffic', 'sum')
        ).reset_index()

        return cluster_stats
