import pandas as pd

class MissingValueChecker:
    def __init__(self, data):
        """
        Initialize the class with the dataset.
        :param data: DataFrame containing the telecom dataset.
        """
        self.data = data.copy()  # Create a copy to avoid modifying the original dataset

    def check_missing(self):
        """
        Check for missing values in the dataset.
        :return: DataFrame of columns with the count of missing values.
        """
        missing_data = self.data.isnull().sum()
        return missing_data[missing_data > 0].sort_values(ascending=False)

    def fill_missing_by_type(self):
        """
        Fill missing values based on data type:
        - For categorical data: Fill with mode (most frequent value), and handle 'undefined' by replacing with 'unknown'
        - For numerical data: Fill with median
        """
        for column in self.data.columns:
            if self.data[column].dtype == 'object':  # Categorical data (strings, etc.)
                # Replace 'undefined' with 'unknown'
                self.data[column] = self.data[column].replace('undefined', 'unknown')
                # Get the mode (most frequent value)
                mode_value = self.data[column].mode()
                if not mode_value.empty:  # Check if mode is not empty
                    # Replace missing values with the mode and reassign the column
                    self.data[column] = self.data[column].fillna(mode_value[0])
                else:
                    print(f"No mode found for column: {column}. Skipping fill.")
            else:  # Numerical data (integers, floats)
                median_value = self.data[column].median()  # Get the median value
                # Replace missing values with the median and reassign the column
                self.data[column] = self.data[column].fillna(median_value)
                # Convert numerical columns to int64 if they don't have any NaNs left
                if self.data[column].isnull().sum() == 0:
                    self.data[column] = self.data[column].astype('int64')


    def get_cleaned_data(self):
        """
        Return the cleaned dataset after missing value handling.
        :return: DataFrame
        """
        return self.data
