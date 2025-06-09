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
# Add filter for Application Type first, defaulting to 'Legacy'
unique_application_types = df['Application Type'].unique()
unique_application_types = sorted(unique_application_types.tolist())
# Set default value to 'Legacy'
default_application_type = 'Legacy' if 'Legacy' in unique_application_types else unique_application_types[0]
selected_application_type = st.sidebar.selectbox('Select Application Type:', unique_application_types, index=unique_application_types.index(default_application_type))

# Add filter for Category
unique_categories = df['Category'].unique()
unique_categories = sorted(unique_categories.tolist())

# Conditional logic for Category filter
if selected_application_type == 'Legacy':
    # If Application Type is 'Legacy', only show 'Operations'
    selected_category = 'Operations'
else:
    # Otherwise, allow selection from all categories
    selected_category = st.sidebar.selectbox('Select Category:', unique_categories)

# Apply filters to the main DataFrame
filtered_df = df[
    (df['Application Type'] == selected_application_type) &
    (df['Category'] == selected_category)
]

# Exclude "Ad-Hoc" entries from the filtered DataFrame
filtered_df = filtered_df[filtered_df['Daily/Weekly/Monthly'] != 'Ad-Hoc']

# Initialize variables for sums
sum1_onshore = sum1_offshore = 0
sum2_onshore = sum2_offshore = 0
sum3_onshore = sum3_offshore = 0

# Calculate total durations for Onshore and Offshore directly from the specified columns
if not filtered_df.empty:
    # Additional information for Application Type: ZG
    if selected_application_type == 'ZG':
        # Handle all applications under ZG
        sum1_onshore = filtered_df.loc[filtered_df['Application'] == 'DIAL', 'Duration in /Hours/Per Day (Onshore)'].sum()
        sum1_offshore = filtered_df.loc[filtered_df['Application'] == 'DIAL', 'Duration in /Hours/Per Day (Offshore)'].sum()

        sum2_onshore = filtered_df.loc[filtered_df['Application'] == 'OTID', 'Duration in /Hours/Per Day (Onshore)'].sum()
        sum2_offshore = filtered_df.loc[filtered_df['Application'] == 'OTID', 'Duration in /Hours/Per Day (Offshore)'].sum()

        sum3_onshore = filtered_df.loc[filtered_df['Application'] == 'CRDR', 'Duration in /Hours/Per Day (Onshore)'].sum()
        sum3_offshore = filtered_df.loc[filtered_df['Application'] == 'CRDR', 'Duration in /Hours/Per Day (Offshore)'].sum()
        
        # Calculate total FTE
        total_fte = (sum1_onshore + sum1_offshore) / 8 + (sum2_onshore + sum2_offshore) / 8 + (sum3_onshore + sum3_offshore) / 8
        
        # Prepare data for the table
        current_values = {
            "DIAL": f"{((sum1_onshore + sum1_offshore) / 8):.2f}",
            "OTID": f"{((sum2_onshore + sum2_offshore) / 8):.2f}",
            "CRDR": f"{((sum3_onshore + sum3_offshore) / 8):.2f}",
            "Total": f"{total_fte:.2f}"
        }
        
        contract_values = {
            "DIAL": "2",
            "OTID": "1",
            "CRDR": "1",
            "Total": "4"
        }

        # Create a DataFrame for the table
        table_data = {
            "Description": ["Current FTE", "Contract FTE"],
            "DIAL": [current_values["DIAL"], contract_values["DIAL"]],
            "OTID": [current_values["OTID"], contract_values["OTID"]],
            "CRDR": [current_values["CRDR"], contract_values["CRDR"]],
            "Total": [current_values["Total"], contract_values["Total"]]
        }

        # Create a DataFrame for the combined row
        table_df = pd.DataFrame(table_data)

        # Display the combined row in a table without the index using HTML for left alignment
        st.markdown(
            table_df.to_html(index=False, justify='left'), 
            unsafe_allow_html=True
        )

    # Additional information for Application Type: Legacy
    elif selected_application_type == 'Legacy':
        # Define actual contract totals
        actual_contract_total = 7.77 + 6.63 + 4.91  # Given values

        # Calculate sums based on application categories
        sum1_onshore = filtered_df.loc[filtered_df['Application'].isin(['CORE', 'SMART', 'SPRDR', 'Spectrum I2S', 'SPECTRUM-MUL']),
                                        'Duration in /Hours/Per Day (Onshore)'].sum()
        sum1_offshore = filtered_df.loc[filtered_df['Application'].isin(['CORE', 'SMART', 'SPRDR', 'Spectrum I2S', 'SPECTRUM-MUL']),
                                         'Duration in /Hours/Per Day (Offshore)'].sum()
        
        sum2_onshore = filtered_df.loc[filtered_df['Application'] == 'E2E',
                                        'Duration in /Hours/Per Day (Onshore)'].sum()
        sum2_offshore = filtered_df.loc[filtered_df['Application'] == 'E2E',
                                         'Duration in /Hours/Per Day (Offshore)'].sum()
        
        sum3_onshore = filtered_df.loc[filtered_df['Application'] == 'SPECTRUM',
                                        'Duration in /Hours/Per Day (Onshore)'].sum()
        sum3_offshore = filtered_df.loc[filtered_df['Application'] == 'SPECTRUM',
                                         'Duration in /Hours/Per Day (Offshore)'].sum()
        
        # Calculate total FTE
        total_fte = (sum1_onshore + sum1_offshore + sum2_onshore + sum2_offshore + sum3_onshore + sum3_offshore) / 8
        
        # Prepare data for the table
        current_values = {
            "SPECTRUM": (sum3_onshore + sum3_offshore) / 8,
            "SPRDR": (sum1_onshore + sum1_offshore) / 8,
            "E2E": (sum2_onshore + sum2_offshore) / 8,
            "Total": total_fte
        }
        
        contract_values = {
            "SPECTRUM": 7.77,
            "SPRDR": 6.63,
            "E2E": 4.91,
            "Total": actual_contract_total
        }
        
        # Create a DataFrame for the table
        table_data = {
            "Description": ["Current FTE", "Contract FTE"],
            "SPECTRUM": [current_values["SPECTRUM"], contract_values["SPECTRUM"]],
            "SPRDR": [current_values["SPRDR"], contract_values["SPRDR"]],
            "E2E": [current_values["E2E"], contract_values["E2E"]],
            "Total": [current_values["Total"], contract_values["Total"]]
        }

        # Create a DataFrame for the combined row
        table_df = pd.DataFrame(table_data)

        # Display the combined row in a table without the index using HTML for left alignment
        st.markdown(
            table_df.to_html(index=False, justify='left'), 
            unsafe_allow_html=True
        )

    # Create a bar chart for the totals with adjusted height
    totals = {
        'Onshore': sum1_onshore + sum2_onshore + sum3_onshore,  # Total hours for onshore
        'Offshore': sum1_offshore + sum2_offshore + sum3_offshore  # Total hours for offshore
    }

    # Use Streamlit's built-in bar chart with specified height
    st.bar_chart(totals, height=300)  # Adjust height as needed

else:
    st.write("No data available for the selected filters.")

# Option to view the "Team Efforts" worksheet
if st.sidebar.checkbox('View Team Efforts Data'):
    st.subheader('Team Efforts Data')
    
    # Display the DataFrame without filters
    st.dataframe(df)  # Display the entire DataFrame in a table format
