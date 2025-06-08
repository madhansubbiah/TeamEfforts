import streamlit as st
import pandas as pd

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

# Exclude "Ad-Hoc" entries from the filtered DataFrame
filtered_df = filtered_df[filtered_df['Daily/Weekly/Monthly'] != 'Ad-Hoc']

# Calculate total durations for Onshore and Offshore directly from the specified columns
if not filtered_df.empty:
    total_onshore = filtered_df['Duration in /Hours/Per Day (Onshore)'].sum()
    total_offshore = filtered_df['Duration in /Hours/Per Day (Offshore)'].sum()
    
    # Calculate FTE values
    onsite_fte = total_onshore / 8  # Assuming 8 hours workday
    offshore_fte = total_offshore / 8  # Assuming 8 hours workday
    
    # Calculate total FTE
    total_fte = onsite_fte + offshore_fte
    
    # Display onsite and offshore FTEs and daily hours
    st.write(f"Onsite: {onsite_fte:.2f}(FTE) Daily Hours: {total_onshore:.2f} | Offshore: {offshore_fte:.2f}(FTE) Daily Hours: {total_offshore:.2f}")
    
    # Display Total FTE
    st.write(f"Total FTE: {total_fte:.2f}")

    # Additional information for Application Type: ZG
    if selected_application_type == 'ZG':
        actual_contract_total = 4  # Given actual/contract total
        increase = ((total_fte - actual_contract_total) / actual_contract_total) * 100 if actual_contract_total > 0 else 0
        
        # Display additional information with the specified format
        st.write(f"Actual/Contract Total: {actual_contract_total} | ODM&E2E+OTID+CRRDR(2+1+1) => Increase: **{increase:.2f}%**")

    # Additional information for Application Type: Legacy
    elif selected_application_type == 'Legacy':
        total_value = 14.4  # Given total FTE value
        spectrum = 7.77  # Example value for Spectrum
        sprdr = 6.63  # Example value for SPRDR
        
        # Calculate percentage reduction
        reduction = ((total_value - total_fte) / total_value) * 100 if total_value > 0 else 0
        
        # Display additional information with the specified format
        st.write(f"Actual/Contract Total: {total_value} | Spectrum: {spectrum} | SPRDR: {sprdr} => Reduction: **{reduction:.2f}%**")

    # Create a bar chart for the totals with adjusted height
    totals = {'Onshore': total_onshore, 'Offshore': total_offshore}
    
    # Use Streamlit's built-in bar chart with specified height
    st.bar_chart(totals, height=300)  # Adjust height as needed

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
