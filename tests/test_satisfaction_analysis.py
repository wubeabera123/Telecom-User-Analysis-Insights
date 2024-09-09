import unittest
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from scripts.user_satisfaction_analysis import UserSatisfactionAnalysis  # Import the class from your file

class TestUserSatisfactionAnalysis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Sample mock data for testing
        cls.mock_data = pd.DataFrame({
            'IMSI': [208200300000001, 208200300000002, 208200300000003, 208200300000004, 208200300000005],
            'Avg RTT DL (ms)': [50, 60, 70, 80, 90],
            'Avg Bearer TP DL (kbps)': [1000, 1500, 2000, 2500, 3000],
            'TCP DL Retrans. Vol (Bytes)': [10000, 15000, 20000, 25000, 30000]
        })

        # Mock cluster and experience labels
        cls.cluster_labels = [0, 0, 1, 1, 0]
        cls.experience_labels = [0, 0, 1, 1, 0]

        # Create instance of UserSatisfactionAnalysis
        cls.analysis = UserSatisfactionAnalysis(cls.mock_data, cls.cluster_labels, cls.experience_labels)

    def test_calculate_engagement_score(self):
        """Test engagement score calculation"""
        self.analysis.calculate_engagement_score()
        self.assertIn('Engagement Score', self.analysis.data.columns)
        self.assertEqual(len(self.analysis.data['Engagement Score']), len(self.mock_data))

    def test_calculate_experience_score(self):
        """Test experience score calculation"""
        self.analysis.calculate_experience_score()
        self.assertIn('Experience Score', self.analysis.data.columns)
        self.assertEqual(len(self.analysis.data['Experience Score']), len(self.mock_data))

    def test_calculate_satisfaction_score(self):
        """Test satisfaction score calculation"""
        self.analysis.calculate_satisfaction_score()
        self.assertIn('Satisfaction Score', self.analysis.data.columns)
        self.assertTrue(np.all(self.analysis.data['Satisfaction Score'] >= 0))

    def test_get_top_10_satisfied_customers(self):
        """Test getting top 10 satisfied customers"""
        self.analysis.calculate_satisfaction_score()  # Satisfaction scores must be calculated first
        top_customers = self.analysis.get_top_10_satisfied_customers()
        self.assertEqual(len(top_customers), len(self.mock_data))  # Since we have 5 rows of data
        self.assertIn('Satisfaction Score', top_customers.columns)
        self.assertIn('IMSI', top_customers.columns)

    def test_predict_satisfaction_score(self):
        """Test satisfaction score prediction using Linear Regression"""
        self.analysis.calculate_engagement_score()
        self.analysis.calculate_experience_score()
        self.analysis.calculate_satisfaction_score()
        self.analysis.predict_satisfaction_score()
        self.assertIn('Predicted Satisfaction Score', self.analysis.data.columns)

    def test_run_kmeans_on_scores(self):
        """Test k-means clustering on engagement and experience scores"""
        self.analysis.calculate_engagement_score()
        self.analysis.calculate_experience_score()
        self.analysis.run_kmeans_on_scores()
        self.assertIn('Satisfaction Cluster', self.analysis.data.columns)
        self.assertTrue(set(self.analysis.data['Satisfaction Cluster']).issubset([0, 1]))

    def test_aggregate_per_cluster(self):
        """
        Test the aggregation of satisfaction and experience scores per cluster.
        """
        # Ensure engagement, experience, and satisfaction scores are calculated first
        self.analysis.calculate_engagement_score()
        self.analysis.calculate_experience_score()
        self.analysis.calculate_satisfaction_score()
        
        # Now, aggregate the scores per cluster
        self.analysis.run_kmeans_on_scores()  # Ensures 'Satisfaction Cluster' is assigned
        aggregated_scores = self.analysis.aggregate_per_cluster()
        
        # Assert that the result has the expected structure
        expected_columns = ['Satisfaction Cluster', 'Satisfaction Score', 'Experience Score']
        self.assertTrue(all(column in aggregated_scores.columns for column in expected_columns))



if __name__ == '__main__':
    unittest.main()
