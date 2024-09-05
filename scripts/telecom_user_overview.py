import pandas as pd

class Telecom_user_overview:
    def __init__(self, data):
        """
        Initialize the class with the dataset.
        :param data: DataFrame containing the telecom dataset.
        """
        self.data = data

    def top_10_handsets(self):
        """
        Identify the top 10 handsets used by customers.
        :return: DataFrame of top 10 handsets and their counts.
        """
        top_handsets = self.data['Handset'].value_counts().head(10)
        return top_handsets

    def top_3_manufacturers(self):
        """
        Identify the top 3 handset manufacturers.
        :return: DataFrame of top 3 manufacturers and their counts.
        """
        top_manufacturers = self.data['Handset Manufacturer'].value_counts().head(3)
        return top_manufacturers

    def top_5_handsets_per_top_3_manufacturers(self):
        """
        Identify the top 5 handsets for each of the top 3 handset manufacturers.
        :return: Dictionary where keys are manufacturers and values are DataFrames of top 5 handsets for each manufacturer.
        """
        top_3_manufacturers = self.top_3_manufacturers().index
        top_handsets_per_manufacturer = {}

        for manufacturer in top_3_manufacturers:
            top_handsets = self.data[self.data['Handset Manufacturer'] == manufacturer]['Handset'].value_counts().head(5)
            top_handsets_per_manufacturer[manufacturer] = top_handsets

        return top_handsets_per_manufacturer

    def make_recommendation(self):
        """
        Make marketing recommendations based on the handset analysis.
        :return: A marketing recommendation string.
        """
        top_handsets = self.top_10_handsets()
        top_manufacturers = self.top_3_manufacturers()
        
        recommendation = (
            f"Top 10 handsets are primarily dominated by {top_manufacturers.index[0]}, showing high brand loyalty.\n"
            f"Marketing efforts should focus on promoting high-demand models like {top_handsets.index[0]}.\n"
            "Additionally, targeting users of top manufacturers {', '.join(top_manufacturers.index)} could boost customer engagement."
        )
        return recommendation

# Example usage in Jupyter notebook:

# Load dataset (assuming the dataset has 'Handset' and 'Handset Manufacturer' columns)
# telecom_data = pd.read_csv("telecom_dataset.csv")

# Instantiate the class
# analysis = TelecomUserOverview(telecom_data)

# Call methods
# top_10_handsets = analysis.top_10_handsets()
# top_3_manufacturers = analysis.top_3_manufacturers()
# top_5_handsets_per_manufacturer = analysis.top_5_handsets_per_top_3_manufacturers()
# recommendation = analysis.make_recommendation()

# Display results
# print("Top 10 Handsets:\n", top_10_handsets)
# print("\nTop 3 Manufacturers:\n", top_3_manufacturers)
# print("\nTop 5 Handsets per Top 3 Manufacturers:\n", top_5_handsets_per_manufacturer)
# print("\nRecommendation:\n", recommendation)
