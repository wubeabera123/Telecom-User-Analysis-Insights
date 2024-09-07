import streamlit as st
import pandas as pd
import numpy as np

# Title for the app
st.title("Interactive Streamlit App with Sidebar")

# Sidebar
st.sidebar.header("Sidebar Features")

# Slider in the sidebar
x = st.sidebar.slider("Select a value for x", 0, 100, 50)
st.sidebar.write(f"Selected value: {x}")

# Checkbox for showing the chart in the sidebar
show_chart = st.sidebar.checkbox("Show Line Chart")

# Radio button for selecting a chart type
chart_type = st.sidebar.radio(
    "Select Chart Type", 
    ("Line Chart", "Bar Chart")
)

# Main section
st.write(f"Selected value from slider: {x}")

# Generating random data
data = pd.DataFrame({
    'x': np.arange(1, 101),
    'y': np.random.randn(100).cumsum()
})

# Displaying chart based on user input
if show_chart:
    if chart_type == "Line Chart":
        st.line_chart(data)
    elif chart_type == "Bar Chart":
        st.bar_chart(data)

# Sidebar multiselect for customizing columns to display
selected_columns = st.sidebar.multiselect(
    "Select columns to display from the data",
    data.columns
)

# Display selected columns
if selected_columns:
    st.write("Selected Data:", data[selected_columns])
