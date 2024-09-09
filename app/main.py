import streamlit as st
import pandas as pd
import numpy as np

# Title for the app
st.title("Telecom Data Analysis and Visualization")

# Sidebar with title and dropdown
st.sidebar.title("User Analysis")
dropdown_value = st.sidebar.selectbox(
    "Select an option",
    ("User overview analysis", "User engagement analysis", "User experience analysis", "User satisfaction analysis")
)

# Main section to show selected value from the dropdown
st.write(f"Selected value from dropdown: {dropdown_value}")


# Chart based on user selection
if dropdown_value == "User overview analysis":
    print("User overview analysis")
elif dropdown_value == "User engagement analysis":
    print("User overview analysis")
elif dropdown_value == "User experience analysis":
    print("User overview analysis")
elif dropdown_value == "User satisfaction analysis":
    print("User overview analysis")
else:
    st.write("")
