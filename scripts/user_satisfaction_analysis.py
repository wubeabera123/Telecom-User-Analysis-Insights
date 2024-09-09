import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.metrics import euclidean_distances
import numpy as np

class UserSatisfactionAnalysis:
    def __init__(self, data, cluster_labels, experience_labels):
        self.data = data
        self.cluster_labels = cluster_labels
        self.experience_labels = experience_labels

    def calculate_engagement_score(self):
        """Task 4.1: Assign engagement score based on the distance from the less engaged cluster."""
        # Extract cluster centroids for engagement clusters
        kmeans_engagement = KMeans(n_clusters=3, random_state=0).fit(self.data[['Avg RTT DL (ms)', 'Avg Bearer TP DL (kbps)', 'TCP DL Retrans. Vol (Bytes)']])
        centroids_engagement = kmeans_engagement.cluster_centers_
        
        # Use the less engaged cluster (assumed cluster 0) and calculate Euclidean distance
        less_engaged_centroid = centroids_engagement[0]
        self.data['Engagement Score'] = np.linalg.norm(self.data[['Avg RTT DL (ms)', 'Avg Bearer TP DL (kbps)', 'TCP DL Retrans. Vol (Bytes)']] - less_engaged_centroid, axis=1)
    
    def calculate_experience_score(self):
        """Task 4.1: Assign experience score based on distance from the worst experience cluster."""
        # Extract experience cluster centroids
        kmeans_experience = KMeans(n_clusters=3, random_state=0).fit(self.data[['Avg RTT DL (ms)', 'Avg Bearer TP DL (kbps)', 'TCP DL Retrans. Vol (Bytes)']])
        centroids_experience = kmeans_experience.cluster_centers_
        
        # Use the worst experience cluster (assumed cluster 0) and calculate Euclidean distance
        worst_experience_centroid = centroids_experience[0]
        self.data['Experience Score'] = np.linalg.norm(self.data[['Avg RTT DL (ms)', 'Avg Bearer TP DL (kbps)', 'TCP DL Retrans. Vol (Bytes)']] - worst_experience_centroid, axis=1)
    
    def calculate_satisfaction_score(self):
        """Task 4.2: Calculate satisfaction score as the average of engagement and experience scores."""
        self.data['Satisfaction Score'] = (self.data['Engagement Score'] + self.data['Experience Score']) / 2
    
    def get_top_10_satisfied_customers(self):
        """Task 4.2: Return the top 10 satisfied customers based on the satisfaction score."""
        top_10_satisfied = self.data.nlargest(10, 'Satisfaction Score')
        return top_10_satisfied[['IMSI', 'Satisfaction Score']]
    
    def predict_satisfaction_score(self):
        """Task 4.3: Build a regression model to predict satisfaction score."""
        X = self.data[['Avg RTT DL (ms)', 'Avg Bearer TP DL (kbps)', 'TCP DL Retrans. Vol (Bytes)', 'Engagement Score', 'Experience Score']]
        y = self.data['Satisfaction Score']
        
        reg = LinearRegression()
        reg.fit(X, y)
        
        # Predict satisfaction score for the dataset
        self.data['Predicted Satisfaction Score'] = reg.predict(X)
    
    def run_kmeans_on_scores(self):
        """Task 4.4: Perform k-means (k=2) on engagement and experience scores."""
        score_data = self.data[['Engagement Score', 'Experience Score']]
        kmeans = KMeans(n_clusters=2, random_state=0)
        self.data['Satisfaction Cluster'] = kmeans.fit_predict(score_data)
    
    def aggregate_per_cluster(self):
        """Task 4.5: Aggregate average satisfaction and experience scores per cluster."""
        aggregated_scores = self.data.groupby('Satisfaction Cluster').agg({
            'Satisfaction Score': 'mean',
            'Experience Score': 'mean'
        }).reset_index()
        
        return aggregated_scores
