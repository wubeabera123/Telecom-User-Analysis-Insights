import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

class UserSatisfactionAnalysis:
    def __init__(self, data, cluster_labels=None, experience_labels=None):
        self.data = data
        self.cluster_labels = cluster_labels
        self.experience_labels = experience_labels

    def handle_missing_values(self, columns):
        """Impute missing values in specified columns using the median."""
        for column in columns:
            self.data.loc[:, column].fillna(self.data[column].median(), inplace=True)
    
    def calculate_engagement_score(self):
        """Assign engagement score based on the distance from the less engaged cluster."""
        # Handle missing values in relevant columns before KMeans
        columns_to_impute = ['Avg RTT DL (ms)', 'Avg Bearer TP DL (kbps)', 'TCP DL Retrans. Vol (Bytes)']
        self.handle_missing_values(columns_to_impute)
        
        # Perform KMeans clustering
        kmeans_engagement = KMeans(n_clusters=3, random_state=0).fit(self.data[columns_to_impute])
        centroids_engagement = kmeans_engagement.cluster_centers_
        
        # Use the less engaged cluster (assumed cluster 0) and calculate Euclidean distance
        less_engaged_centroid = centroids_engagement[0]
        self.data['Engagement Score'] = np.linalg.norm(self.data[columns_to_impute] - less_engaged_centroid, axis=1)

    def calculate_experience_score(self):
        """Assign experience score based on the distance from the worst experience cluster."""
        columns_to_impute = ['Avg RTT DL (ms)', 'Avg Bearer TP DL (kbps)', 'TCP DL Retrans. Vol (Bytes)']
        self.handle_missing_values(columns_to_impute)
        
        # Perform KMeans clustering for experience score
        kmeans_experience = KMeans(n_clusters=3, random_state=0).fit(self.data[columns_to_impute])
        centroids_experience = kmeans_experience.cluster_centers_
        
        worst_experience_centroid = centroids_experience[0]
        self.data['Experience Score'] = np.linalg.norm(self.data[columns_to_impute] - worst_experience_centroid, axis=1)

    def calculate_satisfaction_score(self):
        """Calculate the satisfaction score by combining engagement and experience scores."""
        self.data['Satisfaction Score'] = self.data['Engagement Score'] + self.data['Experience Score']

    def get_top_10_satisfied_customers(self):
        """Return the top 10 customers with the highest satisfaction score."""
        return self.data.nlargest(10, 'Satisfaction Score')[['IMSI', 'Satisfaction Score']]

    def predict_satisfaction_score(self):
        """Predict satisfaction score using some predefined logic (to be defined)."""
        # Placeholder function, implement logic if necessary
        pass

    def run_kmeans_on_scores(self):
        """Run KMeans on engagement and experience scores to classify satisfaction levels."""
        kmeans = KMeans(n_clusters=3, random_state=0).fit(self.data[['Engagement Score', 'Experience Score']])
        self.data['Cluster'] = kmeans.labels_

    def aggregate_per_cluster(self):
        """Aggregate the satisfaction scores per cluster."""
        return self.data.groupby('Cluster')[['Engagement Score', 'Experience Score', 'Satisfaction Score']].mean()

    def plot_cluster_distribution(self):
        """Plot a countplot of the clusters."""
        import seaborn as sns
        plt.figure(figsize=(10, 6))
        sns.countplot(x='Cluster', data=self.data, palette='coolwarm')
        plt.title('Customer Cluster Distribution')
        plt.xlabel('Cluster')
        plt.ylabel('Count')
        plt.show()

    def save_plot(self, filename):
        """Save the cluster plot to a file."""
        import seaborn as sns
        plt.figure(figsize=(10, 6))
        sns.countplot(x='Cluster', data=self.data, palette='coolwarm')
        plt.title('Customer Cluster Distribution')
        plt.xlabel('Cluster')
        plt.ylabel('Count')
        plt.savefig(filename)
