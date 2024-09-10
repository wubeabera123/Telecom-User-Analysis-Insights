import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

# Import the TelecomUserOverview and UserEngagementAnalysis classes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.user_analysis import TelecomUserOverview
from app.utils.engagement_analysis import UserEngagementAnalysis
from app.utils.experience_anlysis import UserExperienceAnalysis
from app.utils.satisfaction_analysis import UserSatisfactionAnalysis

# Initialize Streamlit app

st.title("Telecom Data Overview Dashboard")

# Sidebar to select analysis type
st.sidebar.title("Select Analysis")
dropdown_value = st.sidebar.selectbox(
    "Choose an option",
    ("User overview", "User engagement analysis", "User experience analysis", "User satisfaction analysis")
)

# Load the dataset
data_path = os.path.join(os.path.dirname(__file__), "..", "data", "Week1_challenge_data_source(CSV).csv")
data = pd.read_csv(data_path)

# Initialize user analysis class
if data is not None:
    user_analysis = TelecomUserOverview(data)
    engagement_analysis = UserEngagementAnalysis(data)
    user_experience = UserExperienceAnalysis(data)

    # Main section to show selected value from the dropdown
    st.write(f"Selected option: {dropdown_value}")

    if dropdown_value == "User overview":
        # Display the key metrics for user data aggregation
        st.subheader("Aggregated User Data")
        aggregated_user_data = user_analysis.aggregate_user_data()

        # Show a preview of the aggregated data
        st.write("User Overview (Total Session Duration and Data Volume):")
        st.dataframe(aggregated_user_data.head(10))  # Displaying only the first 10 rows

        # Plot total session duration per user
        st.write("Total Session Duration per User")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x='IMSI', y='total_session_duration', data=aggregated_user_data, ax=ax, color='blue')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Plot total data volume per user
        st.write("Total Data Volume per User")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x='IMSI', y='total_data_volume', data=aggregated_user_data, ax=ax, color='green')
        plt.xticks(rotation=45)
        st.pyplot(fig)

    elif dropdown_value == "User engagement analysis":
        # Perform user engagement analysis
        st.subheader("User Engagement Analysis")
        aggregated_engagement_data = engagement_analysis.aggregate_metrics_per_customer()

        # Show the top 10 users for session frequency, session duration, and total traffic
        st.write("Top 10 Users by Engagement Metrics:")
        top_customers = engagement_analysis.top_10_customers_per_metric(aggregated_engagement_data)
        
        for metric, top_data in top_customers.items():
            st.write(f"Top 10 Users by {metric.capitalize()}:")
            st.dataframe(top_data)

        # Normalize and run clustering
        st.write("Clustering of Users Based on Engagement Metrics")
        clustered_data, kmeans_model = engagement_analysis.normalize_and_cluster(aggregated_engagement_data)

        # Display cluster statistics
        st.write("Cluster Statistics")
        cluster_stats = engagement_analysis.compute_cluster_statistics(clustered_data)
        st.dataframe(cluster_stats)

        # Display a plot for clustering result
        st.write("Cluster Distribution of Users")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.countplot(x='cluster', data=clustered_data, ax=ax, palette='coolwarm')
        st.pyplot(fig)

        # Optional: Use the elbow method to suggest optimal clusters
        st.write("Elbow Method for Optimal Clusters")
        # engagement_analysis.elbow_method(aggregated_engagement_data)

    elif dropdown_value == "User experience analysis":
        st.subheader("User Experience Analysis")
        st.write("Aggregate Customer Information (Network Parameters)")
        aggregated_customer_info = user_experience.aggregate_customer_info()
        st.dataframe(aggregated_customer_info.head(10))

        # Throughput distribution per handset
        st.write("Throughput Distribution per Handset")
        user_experience.throughput_distribution_per_handset()

        # TCP retransmission per handset
        st.write("Average TCP Retransmission per Handset")
        user_experience.average_tcp_per_handset()

        # K-means clustering analysis
        st.write("K-means Clustering")
        clustered_data, cluster_description = user_experience.kmeans_clustering()
        st.write(cluster_description)

    elif dropdown_value == "User satisfaction analysis":
        # Create an instance of UserSatisfactionAnalysis
        satisfaction_analysis = UserSatisfactionAnalysis(data, cluster_labels=None, experience_labels=None)

        # Perform the analysis
        satisfaction_analysis.calculate_engagement_score()
        satisfaction_analysis.calculate_experience_score()
        satisfaction_analysis.calculate_satisfaction_score()

        # Get the top 10 satisfied customers
        top_10_satisfied_customers = satisfaction_analysis.get_top_10_satisfied_customers()
        print("Top 10 Satisfied Customers:")
        print(top_10_satisfied_customers)

        # Predict satisfaction scores (this is a placeholder for further implementation)
        satisfaction_analysis.predict_satisfaction_score()

        # Run KMeans on engagement and experience scores
        satisfaction_analysis.run_kmeans_on_scores()

        # Aggregate results per cluster
        aggregated_scores = satisfaction_analysis.aggregate_per_cluster()
        print("\nAggregated Scores per Cluster:")
        print(aggregated_scores)

        # Plot cluster distribution
        satisfaction_analysis.plot_cluster_distribution()

    else:
        st.error("Failed to load data. Please check the data source.")
