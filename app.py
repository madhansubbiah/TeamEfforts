import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
excel_file = r'C:\Users\subbiahm\OneDrive - Merck Sharp & Dohme LLC\Desktop\Team Effort\Team Effort Estimation - Copy.xlsx'
df = pd.read_excel(excel_file)

# Trim whitespace from column names
df.columns = df.columns.str.strip()

# Display the title
st.title('Team Effort Estimation Viewer')

# Move filters to the sidebar
unique_applications = df['Application'].unique()
unique_applications = sorted(unique_applications.tolist())
unique_applications.insert(0, 'All')  # Add 'All' option at the beginning
selected_application = st.sidebar.selectbox('Select Application:', unique_applications)

unique_categories = df['Category'].unique()
selected_category = st.sidebar.selectbox('Select Category:', unique_categories)

# Apply filters to the DataFrame
filtered_df = df[
    (df['Application'] == selected_application if selected_application != 'All' else True) &
    (df['Category'] == selected_category)
]

# Calculate total durations for Onshore and Offshore
if not filtered_df.empty:
    total_onshore = filtered_df['Duration in /Hours (Onshore)'].sum()
    total_offshore = filtered_df['Duration in /Hours (Offshore)'].sum()
    
    # Display totals on the same line
    st.write(f"Total Duration (Onshore): {total_onshore} hours    |    Total Duration (Offshore): {total_offshore} hours")

    # Create a bar chart for the totals
    totals = {'Onshore': total_onshore, 'Offshore': total_offshore}
    
    # Use Streamlit's built-in bar chart
    st.bar_chart(totals)

else:
    st.write("No data available for the selected filters.")
