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

    def fill_missing_with_mean(self):
        """
        Fill missing values in numeric columns with the mean of those columns.
        """
        # Select only numeric columns
        numeric_columns = self.data.select_dtypes(include=['number']).columns

        # Fill missing values in numeric columns with the mean of each column
        for col in numeric_columns:
            if self.data[col].isnull().sum() > 0:
                self.data[col].fillna(self.data[col].mean(), inplace=True)
                print(f"Filled missing values in column: {col}")

    def get_cleaned_data(self):
        """
        Return the cleaned dataset after missing value handling.
        :return: DataFrame
        """
        return self.data
