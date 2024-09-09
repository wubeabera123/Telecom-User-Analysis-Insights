import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class TelecomUserOverview:
    def __init__(self, data):
        self.data = data.copy()

    def aggregate_user_data(self):
        aggregated_data = self.data.groupby('IMSI').agg(
            number_of_xdr_sessions=('Bearer Id', 'count'),
            total_session_duration=('Dur. (ms)', 'sum'),
            total_dl_data=('Total DL (Bytes)', 'sum'),
            total_ul_data=('Total UL (Bytes)', 'sum')
        ).reset_index()
        aggregated_data['total_data_volume'] = aggregated_data['total_dl_data'] + aggregated_data['total_ul_data']
        return aggregated_data

    def get_user_data_overview(self):
        return self.aggregate_user_data()

    def top_10_handsets(self):
        return self.data['Handset Type'].value_counts().head(10)

    def top_3_manufacturers(self):
        return self.data['Handset Manufacturer'].value_counts().head(3)

    def top_5_handsets_per_top_3_manufacturers(self):
        top_3_manufacturers = self.top_3_manufacturers().index
        top_handsets_per_manufacturer = {}
        for manufacturer in top_3_manufacturers:
            top_handsets = self.data[self.data['Handset Manufacturer'] == manufacturer]['Handset Type'].value_counts().head(5)
            top_handsets_per_manufacturer[manufacturer] = top_handsets
        return top_handsets_per_manufacturer

    def make_recommendation(self):
        top_handsets = self.top_10_handsets()
        top_manufacturers = self.top_3_manufacturers()
        recommendation = (
            f"Top 10 handsets are primarily dominated by {top_manufacturers.index[0]}, showing high brand loyalty.\n"
            f"Marketing efforts should focus on promoting high-demand models like {top_handsets.index[0]}.\n"
            "Additionally, targeting users of top manufacturers {', '.join(top_manufacturers.index)} could boost customer engagement."
        )
        return recommendation
