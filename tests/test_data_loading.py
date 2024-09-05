import unittest
import os
from io import StringIO
from scripts.data_Loading import Data_Loading

class TestCSVReader(unittest.TestCase):

    def setUp(self):
        # Prepare a sample CSV content
        self.sample_csv = StringIO("""col1,col2,col3
1,2,3
4,5,6
7,8,9
""")
        self.empty_csv = StringIO("")  # Empty CSV content
        
        # Create temporary file paths
        self.sample_file_path = 'sample.csv'
        self.empty_file_path = 'empty.csv'
        self.nonexistent_file_path = 'nonexistent.csv'
        
        # Write the sample CSV data to temporary files
        with open(self.sample_file_path, 'w') as f:
            f.write(self.sample_csv.getvalue())
        
        with open(self.empty_file_path, 'w') as f:
            f.write(self.empty_csv.getvalue())

    def tearDown(self):
        # Remove temporary files after tests
        if os.path.exists(self.sample_file_path):
            os.remove(self.sample_file_path)
        if os.path.exists(self.empty_file_path):
            os.remove(self.empty_file_path)

    def test_load_data_success(self):
        csv_reader = Data_Loading(self.sample_file_path)
        csv_reader.load_data()
        raw_data = csv_reader.get_data()
        self.assertIsNotNone(raw_data)
        self.assertEqual(raw_data.shape, (3, 3))  # Check if data shape matches expected (3 rows, 3 columns)
        print(raw_data.head())  # Example usage

    def test_load_data_file_not_found(self):
        csv_reader = Data_Loading(self.nonexistent_file_path)
        csv_reader.load_data()
        raw_data = csv_reader.get_data()
        self.assertIsNone(raw_data)  # Expecting None since file does not exist

    def test_load_data_empty_file(self):
        csv_reader = Data_Loading(self.empty_file_path)
        csv_reader.load_data()
        raw_data = csv_reader.get_data()
        self.assertIsNone(raw_data)  # Expecting None since file is empty

    def test_get_data_without_loading(self):
        csv_reader = Data_Loading(self.sample_file_path)
        raw_data = csv_reader.get_data()
        self.assertIsNone(raw_data)  # Expecting None since load_data was not called

if __name__ == '__main__':
    unittest.main()
