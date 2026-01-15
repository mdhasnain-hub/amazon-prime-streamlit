# ---------------------------------------
# Import required libraries
# ---------------------------------------
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import os

print("Current working directory:", os.getcwd())

# ---------------------------------------
# App Configuration
# ---------------------------------------
st.set_page_config(
    page_title="Amazon Prime Data Analysis",
    layout="wide"
)

# ---------------------------------------
# Title & Description
# ---------------------------------------
st.title("📊 Amazon Prime Content Analysis Dashboard")
st.markdown(
    """
    This dashboard provides insights into **Amazon Prime TV Shows and Movies**
    using ratings, popularity, genres, release trends, and participation data.
    """
)

# ---------------------------------------
# Load Data
# ---------------------------------------
@st.cache_data
def load_data():
    # Load main dataset
    df = pd.read_csv("data/titles.csv")

    # Load credits dataset
    df_credits = pd.read_csv("data/credits.csv")

    return df, df_credits

df, df_credits = load_data()

# ---------------------------------------
# Sidebar Navigation
# ---------------------------------------
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to",
    [
        "Dataset Overview",
        "Genre Analysis",
        "Content Type Distribution",
        "Release Year Analysis",
        "Ratings & Popularity",
        "Correlation Analysis",
        "Actors & Directors",
        "Conclusion"
    ]
)

# ---------------------------------------
# Dataset Overview
# ---------------------------------------
if section == "Dataset Overview":
    st.header("📁 Dataset Overview")

    # Display dataset shape
    st.write("**Dataset Shape:**", df.shape)

    # Show first few rows
    st.dataframe(df.head())

    # Show column information
    st.subheader("Column Information")
    st.write(df.dtypes)

# ---------------------------------------
# Genre Analysis
# ---------------------------------------
elif section == "Genre Analysis":
    st.header("🎭 Genre Analysis")

    # Remove missing genres
    genre_df = df[df['primary_genre'].notna()]

    # Count genres
    genre_counts = genre_df['primary_genre'].value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Count']

    # Bar chart for genre distribution
    fig = px.bar(
        genre_counts,
        x='Genre',
        y='Count',
        title='Content Distribution by Primary Genre'
    )

    fig.update_layout(
        title_x=0.5,
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------
# Content Type Distribution
# ---------------------------------------
elif section == "Content Type Distribution":
    st.header("🎬 Movies vs TV Shows")

    type_counts = df['type'].value_counts().reset_index()
    type_counts.columns = ['Type', 'Count']

    fig = px.bar(
        type_counts,
        x='Type',
        y='Count',
        title='Movies vs TV Shows Distribution'
    )

    fig.update_layout(title_x=0.5)

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------
# Release Year Analysis
# ---------------------------------------
elif section == "Release Year Analysis":
    st.header("📆 Release Year Trends")

    fig = px.histogram(
        df,
        x='release_year',
        nbins=30,
        title='Distribution of Content by Release Year'
    )

    fig.update_layout(title_x=0.5)

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------
# Ratings & Popularity
# ---------------------------------------
elif section == "Ratings & Popularity":
    st.header("⭐ Ratings & Popularity Analysis")

    col1, col2 = st.columns(2)

    # IMDb Votes vs IMDb Score
    with col1:
        fig1 = px.scatter(
            df,
            x='imdb_votes',
            y='imdb_score',
            title='IMDb Votes vs IMDb Score',
            opacity=0.6
        )
        fig1.update_xaxes(type='log')
        fig1.update_layout(title_x=0.5)
        st.plotly_chart(fig1, use_container_width=True)

    # TMDB Popularity vs TMDB Score
    with col2:
        fig2 = px.scatter(
            df,
            x='tmdb_popularity',
            y='tmdb_score',
            title='TMDB Popularity vs TMDB Score',
            opacity=0.6
        )
        fig2.update_xaxes(type='log')
        fig2.update_layout(title_x=0.5)
        st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------
# Correlation Analysis
# ---------------------------------------
elif section == "Correlation Analysis":
    st.header("🔗 Correlation Heatmap")

    numeric_df = df[
        ['imdb_score', 'imdb_votes', 'tmdb_score', 'tmdb_popularity']
    ].dropna()

    corr_matrix = numeric_df.corr()

    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale='RdBu',
        title='Correlation Heatmap of Ratings & Popularity'
    )

    fig.update_layout(title_x=0.5)

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------
# Actor & Director Participation
# ---------------------------------------
elif section == "Actors & Directors":
    st.header("🎥 Actor & Director Participation")

    role = st.selectbox(
        "Select Role",
        ["ACTOR", "DIRECTOR"]
    )

    filtered_df = df_credits[df_credits['role'] == role]

    counts = (
        filtered_df['name']
        .value_counts()
        .head(20)
        .reset_index()
    )

    counts.columns = ['Name', 'Count']

    fig = px.bar(
        counts,
        x='Count',
        y='Name',
        orientation='h',
        title=f'Top 20 {role}s by Participation Volume'
    )

    fig.update_layout(
        title_x=0.5,
        yaxis=dict(autorange='reversed')
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------
# Conclusion
# ---------------------------------------
elif section == "Conclusion":
    st.header("📌 Project Conclusion")

    st.markdown(
        """
        This analysis provided valuable insights into Amazon Prime’s content
        strategy by examining genre dominance, release trends, regional patterns,
        and the relationship between popularity and ratings.

        The findings highlight the importance of balancing **high-performing
        mainstream content** with **diverse regional and genre offerings**.
        Leveraging both popularity and quality metrics can help improve
        recommendations, user satisfaction, and long-term platform growth.
        """
    )

# ---------------------------------------
# Footer
# ---------------------------------------
st.markdown("---")
st.markdown("**Amazon Prime Data Analysis | Built with Streamlit** 🚀")
