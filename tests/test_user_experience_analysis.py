import unittest
import pandas as pd
from scripts.user_experience_analysis import UserExperienceAnalysis

class TestUserExperienceAnalysis(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Create a sample DataFrame with test data
        data = {
            'IMSI': [1, 1, 2, 2],
            'TCP DL Retrans. Vol (Bytes)': [100, None, 200, 300],
            'TCP UL Retrans. Vol (Bytes)': [50, 60, None, 80],
            'Avg RTT DL (ms)': [10, 20, None, 30],
            'Avg RTT UL (ms)': [15, 25, 35, None],
            'Avg Bearer TP DL (kbps)': [1000, 2000, 1500, None],
            'Avg Bearer TP UL (kbps)': [500, None, 750, 800],
            'Handset Type': ['Smartphone', 'Smartphone', 'Feature Phone', 'Smartphone']
        }
        cls.df = pd.DataFrame(data)
        cls.analysis = UserExperienceAnalysis(cls.df)


    def test_throughput_distribution_per_handset(self):
        # Here we are only testing the existence of the plot
        try:
            self.analysis.throughput_distribution_per_handset()
        except Exception as e:
            self.fail(f"throughput_distribution_per_handset() raised an exception: {e}")

    def test_average_tcp_per_handset(self):
        # Here we are only testing the existence of the plot
        try:
            self.analysis.average_tcp_per_handset()
        except Exception as e:
            self.fail(f"average_tcp_per_handset() raised an exception: {e}")

    def test_kmeans_clustering(self):
        result = self.analysis.kmeans_clustering(n_clusters=2)
        
        # Ensure clustering was performed and data was added
        self.assertIn('Cluster', result.columns)
        self.assertEqual(result['Cluster'].nunique(), 2)  # Check for the number of clusters
        
        # Additional checks on clusters can be added here based on expectations
        
if __name__ == '__main__':
    unittest.main()
