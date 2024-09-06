import pandas as pd

class OutlierChecker:
    def __init__(self, data):
        """
        Initialize the class with the dataset.
        :param data: DataFrame containing the dataset with potential outliers.
        """
        self.data = data.copy()  # Create a copy to avoid modifying the original dataset

    def check_outliers(self, column):
        """
        Identify potential outliers in a specified column using the IQR method.
        :param column: The column name to check for outliers.
        :return: Series of outlier values.
        """
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
        
        if self.data[column].dtype not in ['int64', 'float64']:
            raise ValueError(f"Column '{column}' is not numeric.")

        q1 = self.data[column].quantile(0.25)
        q3 = self.data[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # Debugging: Print bounds and outliers
        print(f"Q1: {q1}, Q3: {q3}, IQR: {iqr}, Lower Bound: {lower_bound}, Upper Bound: {upper_bound}")

        outliers = self.data[(self.data[column] < lower_bound) | (self.data[column] > upper_bound)][column]
        print(f"Detected Outliers: {outliers.tolist()}")  # Debugging line
        return outliers

    def remove_outliers(self, column):
        """
        Remove outliers from a specified column using the IQR method.
        :param column: The column name to remove outliers from.
        """
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
        
        if self.data[column].dtype not in ['int64', 'float64']:
            raise ValueError(f"Column '{column}' is not numeric.")

        q1 = self.data[column].quantile(0.25)
        q3 = self.data[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # Debugging: Print bounds
        print(f"Q1: {q1}, Q3: {q3}, IQR: {iqr}, Lower Bound: {lower_bound}, Upper Bound: {upper_bound}")

        self.data = self.data[(self.data[column] >= lower_bound) & (self.data[column] <= upper_bound)]
        print(f"Data after removing outliers:\n{self.data}")  # Debugging line

    def get_cleaned_data(self):
        """
        Return the cleaned dataset after outlier handling.
        :return: DataFrame
        """
        return self.data
