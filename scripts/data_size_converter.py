import pandas as pd

class DataSizeConverter:
    def __init__(self, data, columns):
        """
        Initialize the class with the dataset and the columns to convert.
        :param data: DataFrame containing the telecom dataset.
        :param columns: List of columns to convert to megabytes.
        """
        self.data = data.copy()  # Copy to avoid modifying the original dataset
        self.columns = columns

    def convert_to_megabytes(self, size):
        """
        Convert a data size to megabytes.
        Assumes size is in string format or a numerical value with a unit (e.g., '500KB', '3MB', '1000B').
        """
        size = str(size).strip().upper()  # Convert to uppercase and strip any spaces
        if 'KBPS' in size:
            return float(size.replace('KBPS', '')) / (1024 * 8)  # Convert kilobits per second to MB
        elif 'KB' in size:
            return float(size.replace('KB', '')) / 1024  # Convert KB to MB
        elif 'MB' in size:
            return float(size.replace('MB', ''))  # Already in MB
        elif 'B' in size:
            return float(size.replace('B', '')) / (1024 * 1024)  # Convert bytes to MB
        else:
            # Handle cases where there's no unit (assume it's in bytes)
            try:
                return float(size) / (1024 * 1024)
            except ValueError:
                return None  # Return None if unable to convert

    def clean_data(self):
        """
        Convert all specified columns to megabytes.
        """
        for column in self.columns:
            self.data[column] = self.data[column].apply(self.convert_to_megabytes)

    def get_cleaned_data(self):
        """
        Return the cleaned dataset with converted values.
        """
        return self.data
