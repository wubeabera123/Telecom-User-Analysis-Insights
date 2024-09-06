import unittest
import pandas as pd
from scripts.missing_value_checker import MissingValueChecker  # Adjust the import path as necessary

class TestMissingValueChecker(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame with missing values
        self.df = pd.DataFrame({
            'Category': ['A', 'B', None, 'A', 'C'],
            'Value': [10, None, 30, 40, None],
            'AnotherCategory': [None, 'X', 'Y', None, 'X']
        })
        self.checker = MissingValueChecker(self.df)

    def test_check_missing(self):
        expected_missing = pd.Series({'Category': 1, 'Value': 2, 'AnotherCategory': 2})
        result = self.checker.check_missing().sort_index()
        pd.testing.assert_series_equal(result, expected_missing.sort_index())

    def fill_missing_with_mean(self):
    # Fill missing values
        self.checker.fill_missing_with_mean()
        
        # Expected results with corrected data types
        expected_df = pd.DataFrame({
            'Category': ['A', 'B', 'A', 'A', 'C'],
            'Value': [10, 30, 30, 40, 30],
            'AnotherCategory': ['X', 'X', 'Y', 'X', 'X']
        })
        expected_df['Value'] = expected_df['Value'].astype('int64')  # Ensure correct dtype

        result_df = self.checker.get_cleaned_data()
        pd.testing.assert_frame_equal(result_df, expected_df)

def test_get_cleaned_data(self):
    # Fill missing values
    self.checker.fill_missing_by_type()
    cleaned_data = self.checker.get_cleaned_data()
    
    # Define the expected cleaned DataFrame with corrected data types
    expected_cleaned_df = pd.DataFrame({
        'Category': ['A', 'B', 'A', 'A', 'C'],
        'Value': [10, 30, 30, 40, 30],
        'AnotherCategory': ['X', 'X', 'Y', 'X', 'X']
    })
    expected_cleaned_df['Value'] = expected_cleaned_df['Value'].astype('int64')  # Ensure correct dtype

    pd.testing.assert_frame_equal(cleaned_data, expected_cleaned_df)


if __name__ == '__main__':
    unittest.main()
