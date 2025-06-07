import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
excel_file = 'TeamEffortEstimation.xlsx'
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
    
    # Calculate FTE values
    onsite_fte = total_onshore / 8
    offshore_fte = total_offshore / 8
    
    # Display totals in the desired format
    st.write(f"Onsite: {onsite_fte:.2f}(FTE) Hours: {total_onshore} | Offshore: {offshore_fte:.2f}(FTE) Hours: {total_offshore}")

    # Create a bar chart for the totals
    totals = {'Onshore': total_onshore, 'Offshore': total_offshore}
    
    # Use Streamlit's built-in bar chart
    st.bar_chart(totals)

else:
    st.write("No data available for the selected filters.")
