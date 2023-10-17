# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 14:09:53 2023

@author: Mosco
"""

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from data_manager_v1 import DataManager

# Load data
DATA_PATH = 'data/titanic.csv'
data_manager = DataManager(DATA_PATH)

def main():
    st.title("Titanic Dataset Analysis")
    st.write("Explore various visualizations and filters based on the Titanic dataset.")

    # Navigation bar
    nav = st.sidebar.radio("Choose a Visualization:", ["Survival Count", "Survival Rate by Gender",
                                                       "Survival Rate by Class and Gender", "Age Distribution",
                                                       "Fare Distribution", "Correlation Heatmap"])

    # Filters
    gender = st.sidebar.radio("Filter by Gender:", ["All", "male", "female"])
    pclass = st.sidebar.radio("Filter by Class:", ["All", 1, 2, 3])
    age_range = st.sidebar.slider("Filter by Age Range:", 0, 80, (0, 80))
    embarked = st.sidebar.radio("Filter by Embarked Location:", ["All", "C", "Q", "S"])

    # Apply filters
    filtered_data = data_manager.filter_data(gender if gender != "All" else None,
                                             pclass if pclass != "All" else None,
                                             age_range,
                                             embarked if embarked != "All" else None)
    if nav == "Survival Count":
        st.header("Survival Count")
        survival_count = filtered_data.groupby('Survived').size()
        fig, ax = plt.subplots()
        survival_count.plot(kind='bar', ax=ax)
        st.pyplot(fig)
    elif nav == "Survival Rate by Gender":
        st.header("Survival Rate by Gender")
        fig, ax = plt.subplots()
        sns.barplot(x=filtered_data['Sex'].unique(), y=filtered_data.groupby('Sex')['Survived'].mean().values, ax=ax)
        st.pyplot(fig)
    elif nav == "Survival Rate by Class and Gender":
        st.header("Survival Rate by Class and Gender")
        fig, ax = plt.subplots()
        sns.barplot(x='Pclass', y='Survived', hue='Sex', data=filtered_data, ax=ax)
        st.pyplot(fig)
    elif nav == "Age Distribution":
        st.header("Age Distribution of Passengers")
        fig, ax = plt.subplots()
        sns.histplot(filtered_data['Age'], bins=30, kde=True, ax=ax)
        st.pyplot(fig)
    elif nav == "Fare Distribution":
        st.header("Fare Distribution")
        fig, ax = plt.subplots()
        sns.histplot(filtered_data['Fare'], bins=30, kde=True, ax=ax)
        st.pyplot(fig)
    elif nav == "Correlation Heatmap":
        st.header("Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(10, 8))
        corr = filtered_data.corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

if __name__ == "__main__":
    main()
