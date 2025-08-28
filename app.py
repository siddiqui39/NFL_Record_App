import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('NFL Football Stats (Rushing) Explorer')

st.markdown("""
This app performs simple webscraping of NFL Football player stats data (focusing on Rushing)!
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Data source:** [pro-football-reference.com](https://www.pro-football-reference.com/).
""")

# Sidebar-Year Selection
st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1990,2025))))

# Load data
@st.cache_data
def load_data(year):
    url = f"https://www.pro-football-reference.com/years/{year}/rushing.htm"
    html = pd.read_html(url, header=1)
    df = html[0]
    # Remove repeating headers inside the table
    df = df[df.Age != 'Age']
    df = df.fillna(0)
    df = df.drop(['Rk'], axis=1)
    return df

# Load player statistics
player_stats = load_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(
    [str(team) for team in player_stats['Team'].unique() if str(team) != "0"]
)
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar-Position selection
unique_pos = sorted(
    [str(pos) for pos in player_stats['Pos'].unique() if str(pos) != "0"]
)
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filter data
df_selected_team = player_stats[
    (player_stats['Team'].astype(str).isin(selected_team)) &
    (player_stats['Pos'].astype(str).isin(selected_pos))
]

# Display filtered data
st.header('Display Player Stats of Selected Team(s)')
st.write(f'Data Dimension: {df_selected_team.shape[0]} rows and {df_selected_team.shape[1]} columns.')
st.dataframe(df_selected_team)

# CSV download
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="player_stats.csv">Download CSV File</a>'

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)
