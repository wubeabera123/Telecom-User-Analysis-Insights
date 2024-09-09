import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your analysis class from the utils folder
from app.utils.user_analysis import TelecomUserOverview
from scripts.missing_value_checker import MissingValueChecker

# Cache the data using the updated st.cache_data
@st.cache_data
def load_data():
    try:
        # Adjust the file path to be robust
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "Week1_challenge_data_source(CSV).csv")
        data = pd.read_csv(data_path)
        
        # Create an instance of MissingValueChecker
        missing_checker = MissingValueChecker(data)

        # Check for missing values
        missing_values = missing_checker.check_missing()
        # st.write("Missing Values Before Filling:\n", missing_values)

        # Fill missing values based on datatype (mode for categorical, median for numerical)
        missing_checker.fill_missing_with_mean()

        # Get the cleaned data after handling missing values
        cleaned_data = missing_checker.get_cleaned_data()

        return cleaned_data

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Title for the app
st.title("Telecom Data Analysis and Visualization")

# Sidebar with title and dropdown
st.sidebar.title("User Analysis")
dropdown_value = st.sidebar.selectbox(
    "Select an option",
    ("User overview analysis", "User engagement analysis", "User experience analysis", "User satisfaction analysis")
)

# Load data and initialize the TelecomUserOverview class
cleaned_data = load_data()

# Ensure data is loaded before proceeding
if cleaned_data is not None:
    user_analysis = TelecomUserOverview(cleaned_data)

    # Main section to show selected value from the dropdown
    st.write(f"Selected value from dropdown: {dropdown_value}")

    # Chart based on user selection
    if dropdown_value == "User overview analysis":
        # with st.spinner("Aggregating user data..."):
     # Get aggregated data
        aggregated_user_data = user_analysis.get_user_data_overview()

        # Display aggregated data
        st.write("Aggregated User Data Overview:")
        st.dataframe(aggregated_user_data)

        # Plot for total session duration per user
        st.write("Total Session Duration per User")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='IMSI', y='total_session_duration', data=aggregated_user_data, ax=ax, color='blue')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Plot for total data volume per user
        st.write("Total Data Volume per User")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='IMSI', y='total_data_volume', data=aggregated_user_data, ax=ax, color='green')
        plt.xticks(rotation=45)
        st.pyplot(fig)       

        # Call handset analysis methods
        st.write("Top 10 Handsets Used by Customers")
        top_10_handsets = user_analysis.top_10_handsets()
        st.bar_chart(top_10_handsets)

        st.write("Top 3 Handset Manufacturers")
        top_3_manufacturers = user_analysis.top_3_manufacturers()
        st.write(top_3_manufacturers)

        st.write("Recommendation:")
        recommendation = user_analysis.make_recommendation()
        st.write(recommendation)

    elif dropdown_value == "User engagement analysis":
        st.write("User engagement analysis selected.")

    elif dropdown_value == "User experience analysis":
        st.write("User experience analysis selected.")

    elif dropdown_value == "User satisfaction analysis":
        st.write("User satisfaction analysis selected.")
else:
    st.error("Failed to load data. Please check the data source and try again.")
