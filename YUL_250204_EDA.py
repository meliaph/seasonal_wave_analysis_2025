import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load data from GitHub
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/meliaph/seasonal_wave_analysis_2025/refs/heads/main/df_analyze_250204.csv"
    df = pd.read_csv(url, parse_dates=['OBS_TIME'])
    df['Month'] = df['OBS_TIME'].dt.month
    df['Year'] = df['OBS_TIME'].dt.year
    return df

df_analyze = load_data()

# Sidebar selections
st.sidebar.header("Options")

# Feature selection
df_features = [col for col in df_analyze.columns if col not in ['OBS_TIME', 'Month', 'Year']]
selected_feature = st.sidebar.selectbox("Select Feature:", df_features)

# Year selection
available_years = sorted(df_analyze['Year'].unique())
selected_years = st.sidebar.multiselect("Select Years:", available_years, default=available_years)

# Filter data
df_filtered = df_analyze[df_analyze['Year'].isin(selected_years)]

# Compute monthly correlation, excluding 'OBS_TIME' and 'Year'
df_corr = df_filtered.drop(columns=['OBS_TIME', 'Year'])
monthly_corr = df_corr.groupby('Month').corr()[selected_feature].unstack()
if selected_feature in monthly_corr.columns:
    monthly_corr.drop(columns=selected_feature, inplace=True)

# Display heatmap
st.subheader(f'Monthly Correlation of {selected_feature} with Other Features')
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(monthly_corr.T, annot=True, cmap='coolwarm', center=0, linewidths=0.5, ax=ax)
plt.xlabel("Month")
plt.ylabel("Features")
plt.xticks(rotation=90)
st.pyplot(fig)

# Display line plot
st.subheader(f'Trend of {selected_feature} Correlation Over Months')
fig, ax = plt.subplots(figsize=(12, 6))
for col in monthly_corr.columns:
    ax.plot(monthly_corr.index, monthly_corr[col], marker='o', label=col)
ax.axhline(0, color='black', linestyle='--', linewidth=0.8)
ax.set_xlabel("Month")
ax.set_ylabel("Correlation")
ax.set_xticks(monthly_corr.index)
ax.set_xticklabels(monthly_corr.index, rotation=90)
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
st.pyplot(fig)
