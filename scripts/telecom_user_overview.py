import pandas as pd

class TelecomUserOverview:
    def __init__(self, data):
        """
        Initialize the class with the dataset.
        :param data: DataFrame containing the telecom dataset.
        """
        self.data = data.copy()  # Create a copy of the dataset to avoid modifying the original

    def aggregate_user_data(self):
        """
        Aggregate the following information per user:
        - Number of xDR sessions
        - Total session duration
        - Total download (DL) data
        - Total upload (UL) data
        - Total data volume (DL + UL)
        
        :return: DataFrame with aggregated user behavior information.
        """
        # Assuming 'IMSI' represents the user and 'Dur. (ms)' represents session duration
        aggregated_data = self.data.groupby('IMSI').agg(
            number_of_xdr_sessions=('Bearer Id', 'count'),  # Count the number of xDR sessions
            total_session_duration=('Dur. (ms)', 'sum'),  # Sum of session durations
            total_dl_data=('Total DL (Bytes)', 'sum'),  # Sum of download data
            total_ul_data=('Total UL (Bytes)', 'sum')  # Sum of upload data
        ).reset_index()
        
        # Calculate total data volume (DL + UL)
        aggregated_data['total_data_volume'] = aggregated_data['total_dl_data'] + aggregated_data['total_ul_data']
        
        return aggregated_data

    def get_user_data_overview(self):
        """
        Provide a quick summary of the user behavior overview data.
        """
        aggregated_data = self.aggregate_user_data()
        print("Aggregated User Data Overview:")
        print(aggregated_data.head())
        return aggregated_data

    def top_10_handsets(self):
        """
        Identify the top 10 handsets used by customers.
        :return: DataFrame of top 10 handsets and their counts.
        """
        top_handsets = self.data['Handset Type'].value_counts().head(10)
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
            top_handsets = self.data[self.data['Handset Manufacturer'] == manufacturer]['Handset Type'].value_counts().head(5)
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
