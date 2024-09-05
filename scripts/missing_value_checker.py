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
        - For categorical data: Fill with mode (most frequent value)
        - For numerical data: Fill with median
        """
        for column in self.data.columns:
            if self.data[column].dtype == 'object':  # Categorical data (strings, etc.)
                mode_value = self.data[column].mode()[0]  # Get the most frequent value
                self.data[column].fillna(mode_value, inplace=True)
            else:  # Numerical data (integers, floats)
                median_value = self.data[column].median()  # Get the median value
                self.data[column].fillna(median_value, inplace=True)

    def get_cleaned_data(self):
        """
        Return the cleaned dataset after missing value handling.
        :return: DataFrame
        """
        return self.data
