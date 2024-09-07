import unittest
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
from scripts.user_engagement_analysis import UserEngagementAnalysis  # Update this import with your actual module

class TestUserEngagementAnalysis(unittest.TestCase):
    def setUp(self):
        """Set up a sample dataset for testing."""
        data = {
            'MSISDN/Number': ['user1', 'user2', 'user3', 'user1', 'user2'],
            'Bearer Id': [1, 2, 3, 4, 5],
            'Dur. (ms)': [1000, 2000, 3000, 4000, 5000],
            'Total UL (Bytes)': [1000, 2000, np.nan, 4000, 5000],
            'Total DL (Bytes)': [5000, np.nan, 3000, 4000, 1000],
            'Handset Type': ['app1', 'app2', 'app1', 'app2', 'app3']
        }
        self.data = pd.DataFrame(data)
        self.engagement_analysis = UserEngagementAnalysis(self.data)

    def test_aggregate_metrics_per_customer(self):
        """Test the aggregation of metrics per customer."""
        agg_data = self.engagement_analysis.aggregate_metrics_per_customer()
        expected_columns = ['MSISDN/Number', 'session_frequency', 'total_session_duration', 'total_traffic']
        self.assertTrue(all(col in agg_data.columns for col in expected_columns))
        self.assertEqual(len(agg_data), 3)  # 3 unique users

    def test_top_10_customers_per_metric(self):
        """Test that the top 10 customers per metric are correctly calculated."""
        agg_data = self.engagement_analysis.aggregate_metrics_per_customer()
        top_customers = self.engagement_analysis.top_10_customers_per_metric(agg_data)
        self.assertIn('session_frequency', top_customers)
        self.assertIn('total_session_duration', top_customers)
        self.assertIn('total_traffic', top_customers)

    def test_normalize_and_cluster(self):
        """Test k-means clustering and that the cluster labels are added."""
        agg_data = self.engagement_analysis.aggregate_metrics_per_customer()
        clustered_data, kmeans = self.engagement_analysis.normalize_and_cluster(agg_data, n_clusters=2)
        self.assertIn('cluster', clustered_data.columns)
        self.assertEqual(len(clustered_data['cluster'].unique()), 2)  # 2 clusters

    def test_aggregate_traffic_per_application(self):
        """Test aggregation of traffic per application."""
        top_users_per_app = self.engagement_analysis.aggregate_traffic_per_application()
        self.assertIn('total_traffic', top_users_per_app.columns)
        # self.assertEqual(len(top_users_per_app), 3)  # 3 unique handsets

if __name__ == '__main__':
    unittest.main()
