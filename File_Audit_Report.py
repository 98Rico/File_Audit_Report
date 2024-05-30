from datetime import datetime
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

# Streamlit page configuration
st.set_page_config(layout="wide")

st.image("https://i.redd.it/9t73bdrpg7891.jpg", use_column_width=False, width=150)

# Write directly to the app
st.title('File Audit Report')

# Data
data = {
    "File Name": ["file1.txt", "file2.docx", "file3.xlsx", "file4.jpg", "file5.pdf", "file6.png", "file7.pptx", "file8.txt", "file9.csv", "file10.docx",
                  "file11.pdf", "file12.txt", "file13.xlsx", "file14.docx", "file15.pdf", "file16.jpg", "file17.txt", "file18.csv", "file19.jpg", "file20.xlsx"],
    "File Location": ["/path/to/file1", "/path/to/file2", "/path/to/file3", "/path/to/file4", "/path/to/file5", "/path/to/file6", "/path/to/file7",
                      "/path/to/file8", "/path/to/file9", "/path/to/file10", "/path/to/file11", "/path/to/file12", "/path/to/file13", "/path/to/file14",
                      "/path/to/file15", "/path/to/file16", "/path/to/file17", "/path/to/file18", "/path/to/file19", "/path/to/file20"],
    "Date Created": [datetime(2023, 5, 10), datetime(2023, 6, 15), datetime(2023, 7, 20), datetime(2023, 8, 25), datetime(2023, 9, 30), datetime(2023, 10, 5),
                     datetime(2023, 11, 10), datetime(2023, 12, 15), datetime(2023, 1, 20), datetime(2023, 2, 25), datetime(2023, 3, 30), datetime(2023, 4, 5),
                     datetime(2023, 5, 10), datetime(2023, 6, 15), datetime(2023, 7, 20), datetime(2023, 8, 25), datetime(2023, 9, 30), datetime(2023, 10, 5),
                     datetime(2023, 11, 10), datetime(2023, 12, 15)],
    "Date Modified": [datetime(2023, 5, 12), datetime(2023, 6, 17), datetime(2023, 7, 22), datetime(2023, 8, 27), datetime(2023, 10, 2), datetime(2023, 10, 7),
                      datetime(2023, 11, 12), datetime(2023, 12, 17), datetime(2023, 1, 22), datetime(2023, 2, 27), datetime(2023, 4, 1), datetime(2023, 4, 7),
                      datetime(2023, 5, 12), datetime(2023, 6, 17), datetime(2023, 7, 22), datetime(2023, 8, 27), datetime(2023, 10, 2), datetime(2023, 10, 7),
                      datetime(2023, 11, 12), datetime(2023, 12, 17)],
    "Owner": ["Alice", "Bob", "Alice", "Charlie", "Bob", "Alice", "Charlie", "Bob", "Alice", "Bob",
              "Charlie", "Alice", "Bob", "Alice", "Charlie", "Bob", "Alice", "Bob", "Charlie", "Alice"],
    "File Type": ["txt", "docx", "xlsx", "jpg", "pdf", "png", "pptx", "txt", "csv", "docx",
                  "pdf", "txt", "xlsx", "docx", "pdf", "jpg", "txt", "csv", "jpg", "xlsx"],
    "File Size (KB)": [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
                       1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000],
    "Notes": ["Note1", "Note2", "Note3", "Note4", "Note5", "Note6", "Note7", "Note8", "Note9", "Note10",
              "Note11", "Note12", "Note13", "Note14", "Note15", "Note16", "Note17", "Note18", "Note19", "Note20"],
    "Upload Status": ["Success", "Success", "Success", "Failed", "Success", "Success", "Success", "Success", "Failed", "Success",
                      "Success", "Failed", "Success", "Success", "Failed", "Success", "Success", "Failed", "Success", "Success"],
    "Failure Reason": ["", "", "", "Connection error", "", "", "", "", "Invalid format", "",
                       "", "Disk full", "", "", "Timeout", "", "", "Invalid file", "", ""],
    "PRIORITY": [1, 2, 1, 3, 2, 1, 3, 2, 1, 2,
                 3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
    "DEPARTMENT": ["IT", "Finance", "HR", "IT", "Finance", "HR", "IT", "Finance", "HR", "IT",
                   "Finance", "HR", "IT", "Finance", "HR", "IT", "Finance", "HR", "IT", "Finance"]
}

# Create DataFrame
df = pd.DataFrame(data)





# Columns for user selection
columns = ['DEPARTMENT', 'File Name', 'Upload Status', 'PRIORITY', 'File Type']

selected_criteria = {}


with st.sidebar: #place filter buttons on the sidebar
    st.header('Filter Options')
    
    
    for col in columns:
        selected_criteria[col] = st.selectbox(f'Select {col}:', ['All'] + list(df[col].unique()), index=0)
    
    
    if st.button('Clear All'):
        selected_criteria = {col: 'All' for col in columns}


    
filtered_df = df.copy()
for col, value in selected_criteria.items():
    if value != 'All':
        filtered_df = filtered_df[filtered_df[col] == value]


tabs = st.tabs(["Main", "History"]) #One tab for overall and the second one for historucal dfata

with tabs[0]:

    
    st.write('## Successful Upload Progress') #progress bar at the top
    success_count = filtered_df[filtered_df['Upload Status'] == 'Success'].shape[0]
    total_count = filtered_df.shape[0]
   



    progress_percent = (success_count / total_count) * 100 if total_count > 0 else 0

    st.progress(progress_percent / 100.0)
    st.write(f'{success_count} out of {total_count} files successfully uploaded ({progress_percent:.2f}%)')

    col1, col2 = st.columns(2)

    with col1:
        
        st.write('## File Audit Data')
        st.dataframe(filtered_df)
    with col2:
        
        st.write('## Summary Table')
        summary = filtered_df.groupby('DEPARTMENT').agg(
            Total_Files=('File Name', 'count'),
            Successful_Uploads=('Upload Status', lambda x: (x == 'Success').sum()),
            Failed_Uploads=('Upload Status', lambda x: (x == 'Failed').sum()),
            Average_File_Size=('File Size (KB)', 'mean')
        ).reset_index()
        st.dataframe(summary)

    selected_column = st.selectbox('Select a column for histogram:', filtered_df.columns)
    st.subheader(f'Histogram of {selected_column}')
    st.bar_chart(filtered_df[selected_column].value_counts(), color='#012A53')

   
    col1, col2 = st.columns(2) #split grapjh in two columns to make it less verticA;

    with col1: # Bar graph labeled with priority
        
        st.write('## File Distribution by Priority')
        bar_chart = alt.Chart(filtered_df).mark_bar().encode(
            x=alt.X('File Type:N', title='File Type'),
            y=alt.Y('count()', title='Count'),
            color=alt.Color('PRIORITY:N', scale=alt.Scale(range=["#E6ED23", "#E15A3C", "#ED0707"]), legend=alt.Legend(title='Priority')),
            tooltip=['File Type', 'count()', 'PRIORITY']
        ).interactive()
        st.altair_chart(bar_chart, use_container_width=True)

    with col2:  # Heatmap of upload status by users
       
        st.write('## Upload Status by Owner')
        heatmap_data = filtered_df.groupby(['Owner', 'Upload Status']).size().reset_index(name='count')
        heatmap = alt.Chart(heatmap_data).mark_rect().encode(
            x=alt.X('Upload Status:N', title='Upload Status'),
            y=alt.Y('Owner:N', title='Owner'),
            color=alt.Color('count:Q', scale=alt.Scale(scheme='bluegreen'), legend=alt.Legend(title='Count')),
            tooltip=['Owner', 'Upload Status', 'count']
        ).interactive()
        st.altair_chart(heatmap, use_container_width=True)

with tabs[1]:
    # History Tab
    st.write('## Historical Data')
   
   # Date filter for history
    start_date = st.date_input('Start Date', value=datetime(2023, 1, 1))
    end_date = st.date_input('End Date', value=datetime(2023, 12, 31))

    # Filter the DataFrame based on date range
    history_df = df[(df['Date Created'] >= pd.to_datetime(start_date)) & (df['Date Created'] <= pd.to_datetime(end_date))]

    # Apply sidebar filters to history_df
    for col, value in selected_criteria.items():
        if value != 'All':
            history_df = history_df[history_df[col] == value]

    # KPIs
    kpis = {
        'Total Successful Uploads': (history_df['Upload Status'] == 'Success').sum(),
        'Total Failed Uploads': (history_df['Upload Status'] == 'Failed').sum(),
        'Unique Users': history_df['Owner'].nunique()
    }

    st.write('### Key Performance Indicators')
    kpi1, kpi2, kpi3 = st.columns(3)

    kpi1.metric('Count of Successful Uploads', kpis['Total Successful Uploads'])
    kpi2.metric('Count of Failed Uploads', kpis['Total Failed Uploads'])
    kpi3.metric('Count of Users who Uploaded', kpis['Unique Users'])

    # Line graph of successful and unsuccessful uploads over time
    st.write('### Upload History')
    history_df['Date Created'] = pd.to_datetime(history_df['Date Created']).dt.date
    upload_history = history_df.groupby(['Date Created', 'Upload Status']).size().reset_index(name='count')

    line_chart = alt.Chart(upload_history).mark_line().encode(
        x=alt.X('Date Created:T', title='Date'),
        y=alt.Y('count:Q', title='Count'),
        color=alt.Color('Upload Status:N', title='Upload Status', scale=alt.Scale(domain=['Success', 'Failed'], range=['green', 'red'])),
        tooltip=['Date Created', 'Upload Status', 'count']
    ).interactive()

    st.altair_chart(line_chart, use_container_width=True)
