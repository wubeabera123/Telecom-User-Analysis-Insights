import pandas as pd

class OutlierChecker:
    def __init__(self, data):
        """
        Initialize the class with the dataset.
        :param data: DataFrame containing the telecom dataset.
        """
        self.data = data.copy()  # Create a copy to avoid modifying the original dataset

    def check_outliers(self, column):
        """
        Identify potential outliers in a specified column using the IQR method.
        :param column: The column name to check for outliers.
        :return: Series of outlier values.
        """
        q1 = self.data[column].quantile(0.25)
        q3 = self.data[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        return self.data[(self.data[column] < lower_bound) | (self.data[column] > upper_bound)][column]

    def remove_outliers(self, column):
        """
        Remove outliers from a specified column using the IQR method.
        :param column: The column name to remove outliers from.
        """
        q1 = self.data[column].quantile(0.25)
        q3 = self.data[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        self.data = self.data[(self.data[column] >= lower_bound) & (self.data[column] <= upper_bound)]

    def get_cleaned_data(self):
        """
        Return the cleaned dataset after outlier handling.
        :return: DataFrame
        """
        return self.data
