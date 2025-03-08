import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

all_data = pd.read_csv("main-bike-sharing.csv")

def create_total_penyewa():
    all_data['dteday'] = pd.to_datetime(all_data['dteday'])  
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    all_data['season'] = all_data['season'].map(season_mapping)  
    all_data['time_category'] = all_data['hr'].apply(lambda x: 'Morning' if 6 <= x < 12 else 'Afternoon' if 12 <= x < 18 else 'Evening' if 18 <= x < 24 else 'Night')
    return all_data

def filter_data(df, season_filter, time_filter):
    if not season_filter and not time_filter:
        return 0, pd.DataFrame(columns=df.columns)
    filtered_df = df.copy()
    
    if season_filter:
        filtered_df = filtered_df[filtered_df['season'].isin(season_filter)]
    
    if time_filter:
        filtered_df = filtered_df[filtered_df['time_category'].isin(time_filter)]
    
    if filtered_df.empty:
        return 0, pd.DataFrame()  
    
    total_orders = filtered_df['cnt'].sum()
    return total_orders, filtered_df


def create_byseason_chart(filtered_df, df):
    if filtered_df.empty:
        season_avg = df.groupby('season')['cnt'].mean().sort_values(ascending=False)
    else:
        season_avg = filtered_df.groupby('season')['cnt'].mean().sort_values(ascending=False)
    
    plt.figure(figsize=(8, 5))
    sns.barplot(hue=season_avg.index, y=season_avg.values, palette='coolwarm')
    plt.xlabel("Musim")
    plt.ylabel("Rata-rata Penyewaan Sepeda")
    plt.title("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
    st.pyplot(plt)

def create_byhour_chart(filtered_df, df):
    if filtered_df.empty:
        hour_avg = df.groupby('hr')['cnt'].mean().sort_index()
    else:
        hour_avg = filtered_df.groupby('hr')['cnt'].mean().sort_index()
    
    plt.figure(figsize=(10, 5))
    sns.barplot(hue=hour_avg.index, y=hour_avg.values,palette='viridis')
    plt.xlabel("Jam")
    plt.ylabel("Rata-rata Penyewaan Sepeda")
    plt.title("Jumlah Peminjaman Sepeda Berdasarkan Jam")
    st.pyplot(plt)

all_data = create_total_penyewa()

with st.sidebar:
    st.header('Bike Sharing Dataset')
    season_filter = st.multiselect(
        label="Filter berdasarkan Musim:",
        options=['Spring', 'Summer', 'Fall', 'Winter'],
        default=['Spring','Summer','Fall','Winter']
    )
    
    time_filter = st.multiselect(
        label="Filter berdasarkan Waktu:",
        options=['Morning', 'Afternoon', 'Evening', 'Night'],
        default=['Morning', 'Afternoon', 'Evening', 'Night']
    )
    
st.title('Dashboard Bike Share :sparkles:')

total_orders, filtered_df = filter_data(all_data, season_filter, time_filter)
    
st.header("Total Penyewaan:")
st.subheader(f"{total_orders} orang")

st.header(" Penyewaan Berdasarkan Musim")
create_byseason_chart(filtered_df,all_data)
    

st.header("Penyewaan Berdasarkan jam")
create_byhour_chart(filtered_df,all_data)

st.caption('Copyright (c) andry septian syahputra tumaruk 2025')
    


