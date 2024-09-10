import pandas as pd

class TelecomUserOverview:
    def __init__(self, data):
        # Make a copy of the data to avoid modifying the original dataframe
        self.data = data.copy()

    def aggregate_user_data(self):
        # Corrected syntax for summing both 'Total DL (Bytes)' and 'Total UL (Bytes)'
        aggregated_data = self.data.groupby('IMSI').agg(
            total_session_duration=('Dur. (ms)', 'sum'),
            total_data_volume_dl=('Total DL (Bytes)', 'sum'),
            total_data_volume_ul=('Total UL (Bytes)', 'sum')
        ).reset_index()
        
        # Adding a new column for the total data volume (download + upload)
        aggregated_data['total_data_volume'] = aggregated_data['total_data_volume_dl'] + aggregated_data['total_data_volume_ul']
        return aggregated_data

    def top_10_handsets(self):
        # Returning the top 10 most used handsets based on frequency
        return self.data['Handset Type'].value_counts().head(10)

    def top_3_manufacturers(self):
        # Returning the top 3 handset manufacturers based on frequency
        return self.data['Handset Manufacturer'].value_counts().head(3)

    def make_recommendation(self):
        # Generate recommendations based on top handsets and manufacturers
        top_handsets = self.top_10_handsets()
        top_manufacturers = self.top_3_manufacturers()
        recommendation = (
            f"Focus marketing efforts on promoting {top_handsets.index[0]}, and target users of top brands: {', '.join(top_manufacturers.index)}."
        )
        return recommendation
