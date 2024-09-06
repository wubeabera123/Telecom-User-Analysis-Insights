import unittest
import pandas as pd
import numpy as np
from io import StringIO
from scripts.eda_analysis import EDAAnalysis  # Adjust import as needed

class TestEDAAnalysis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a sample DataFrame for testing
        data = {
            'Dur. (ms)': np.random.randint(1000, 5000, size=100),
            'Total DL (Bytes)': np.random.randint(10000, 50000, size=100),
            'Total UL (Bytes)': np.random.randint(10000, 50000, size=100),
            'Social Media DL (Bytes)': np.random.randint(1000, 5000, size=100),
            'Google DL (Bytes)': np.random.randint(1000, 5000, size=100),
            'Email DL (Bytes)': np.random.randint(1000, 5000, size=100),
            'YouTube DL (Bytes)': np.random.randint(1000, 5000, size=100),
            'Netflix DL (Bytes)': np.random.randint(1000, 5000, size=100),
            'Gaming DL (Bytes)': np.random.randint(1000, 5000, size=100),
            'Other DL (Bytes)': np.random.randint(1000, 5000, size=100),
        }
        cls.df = pd.DataFrame(data)
        cls.eda = EDAAnalysis(cls.df)

    def test_describe_variables(self):
        """Test if describe_variables() returns the correct data types."""
        head = self.eda.describe_variables()
        self.assertEqual(head.shape[0], 5)  # Default head is 5 rows
        self.assertTrue('Dur. (ms)' in self.eda.data.columns)
        self.assertTrue('Total DL (Bytes)' in self.eda.data.columns)

    def test_segment_users_by_decile(self):
        """Test if segment_users_by_decile() runs without errors."""
        try:
            self.eda.segment_users_by_decile()
        except Exception as e:
            self.fail(f"segment_users_by_decile() failed with error: {e}")

    def test_analyze_basic_metrics(self):
        """Test if analyze_basic_metrics() runs without errors."""
        try:
            self.eda.analyze_basic_metrics()
        except Exception as e:
            self.fail(f"analyze_basic_metrics() failed with error: {e}")

    def test_compute_dispersion_parameters(self):
        """Test if compute_dispersion_parameters() computes variance and std dev."""
        try:
            self.eda.compute_dispersion_parameters()
        except Exception as e:
            self.fail(f"compute_dispersion_parameters() failed with error: {e}")

    def test_plot_univariate_analysis(self):
        """Test if plot_univariate_analysis() runs without errors."""
        try:
            self.eda.plot_univariate_analysis()
        except Exception as e:
            self.fail(f"plot_univariate_analysis() failed with error: {e}")

    def test_bivariate_analysis(self):
        """Test if bivariate_analysis() runs without errors."""
        try:
            self.eda.bivariate_analysis()
        except Exception as e:
            self.fail(f"bivariate_analysis() failed with error: {e}")

    def test_correlation_analysis(self):
        """Test if correlation_analysis() runs without errors."""
        try:
            self.eda.correlation_analysis()
        except Exception as e:
            self.fail(f"correlation_analysis() failed with error: {e}")

    def test_pca_analysis(self):
        """Test if pca_analysis() runs without errors."""
        try:
            self.eda.pca_analysis()
        except Exception as e:
            self.fail(f"pca_analysis() failed with error: {e}")

if __name__ == '__main__':
    unittest.main()
