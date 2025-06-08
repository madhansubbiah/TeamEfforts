import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
excel_file = 'TeamEffortEstimation.xlsx'
df = pd.read_excel(excel_file, sheet_name='Team Efforts')  # Load the specific worksheet

# Trim whitespace from column names
df.columns = df.columns.str.strip()

# Display the title
st.title('Team Effort Estimation Viewer')

# Move filters to the sidebar for main data
# Add filter for Application Type first
unique_application_types = df['Application Type'].unique()
unique_application_types = sorted(unique_application_types.tolist())
unique_application_types.insert(0, 'All')  # Add 'All' option at the beginning
selected_application_type = st.sidebar.selectbox('Select Application Type:', unique_application_types)

# Then add filter for Application
unique_applications = df['Application'].unique()
unique_applications = sorted(unique_applications.tolist())
unique_applications.insert(0, 'All')  # Add 'All' option at the beginning
selected_application = st.sidebar.selectbox('Select Application:', unique_applications)

unique_categories = df['Category'].unique()
selected_category = st.sidebar.selectbox('Select Category:', unique_categories)

# Apply filters to the main DataFrame
filtered_df = df[
    (df['Application'] == selected_application if selected_application != 'All' else True) &
    (df['Application Type'] == selected_application_type if selected_application_type != 'All' else True) &
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

# Option to view the "Team Efforts" worksheet
if st.sidebar.checkbox('View Team Efforts Data'):
    st.subheader('Team Efforts Data')
    
    # Add filtering options for the displayed Team Efforts data
    # Add filter for Application Type first
    unique_application_types_team_efforts = df['Application Type'].unique()
    unique_application_types_team_efforts = sorted(unique_application_types_team_efforts.tolist())
    unique_application_types_team_efforts.insert(0, 'All')  # Add 'All' option at the beginning
    selected_application_type_team_efforts = st.selectbox('Filter by Application Type:', unique_application_types_team_efforts)

    # Then add filter for Application
    unique_applications_team_efforts = df['Application'].unique()
    unique_applications_team_efforts = sorted(unique_applications_team_efforts.tolist())
    unique_applications_team_efforts.insert(0, 'All')  # Add 'All' option at the beginning
    selected_application_team_efforts = st.selectbox('Filter by Application:', unique_applications_team_efforts)

    unique_categories_team_efforts = df['Category'].unique()
    selected_category_team_efforts = st.selectbox('Filter by Category:', unique_categories_team_efforts)

    # Apply filters to the Team Efforts DataFrame
    filtered_team_efforts_df = df[
        (df['Application'] == selected_application_team_efforts if selected_application_team_efforts != 'All' else True) &
        (df['Application Type'] == selected_application_type_team_efforts if selected_application_type_team_efforts != 'All' else True) &
        (df['Category'] == selected_category_team_efforts)
    ]

    # Display the filtered DataFrame
    st.dataframe(filtered_team_efforts_df)  # Display the DataFrame in a table format
