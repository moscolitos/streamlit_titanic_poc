# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 14:09:53 2023

@author: Mosco
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from data_manager import DataManager

# Load data
DATA_PATH = 'data/titanic.csv'
data_manager = DataManager(DATA_PATH)

def set_css():
    st.markdown("""
        <style>
            body {
                color: #fff;
                background-color: #4F4F4F;
            }
            .sidebar .sidebar-content {
                background-image: linear-gradient(#2e7bcf,#2e7bcf);
                color: #ffffff;
            }
            .Widget > label {
                color: black !important;
                font-weight: bold !important;
            }
            /* Change the font color of Streamlit widgets to black */

            /* Change the font color of the dropdown selections to black */
            .st-cg {
                color: black !important;
            }
            
            /* Change the font color of the slider values to black */
            .st-ey {
                color: black !important;
            }

            .stButton>button {
                color: #4F4F4F;
            }
            
        </style>
        """, unsafe_allow_html=True)



def main():
    set_css()

    st.title("Titanic Dataset Analysis")
    st.markdown("""
    ### Introduction
    The Titanic dataset captures information about passengers on the RMS Titanic, which infamously sank on its maiden voyage in 1912.
    This application allows you to explore various aspects of the dataset through visualizations and filters. Dive in to uncover patterns 
    related to survival rates, fare, age, and more.
    """)


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
    
    # Calculate survival rates
    survival_rate = filtered_data.groupby('Sex')['Survived'].mean().reset_index()
    survival_rate_class_gender = filtered_data.groupby(['Pclass', 'Sex'])['Survived'].mean().reset_index()
    corr = filtered_data[['Survived', 'Pclass', 'Age', 'SibSp', 'Parch', 'Fare']].corr()

    st.write(f"Data Filtered By: Gender: {gender}, Class: {pclass}, Age: {age_range}, Embarked: {embarked}")
    
    palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    if nav == "Survival Count":
        fig = px.bar(filtered_data, 
                     x=filtered_data['Survived'].map({0: 'Not Survived', 1: 'Survived'}),
                     color=filtered_data['Survived'].map({0: 'Not Survived', 1: 'Survived'}),
                     color_discrete_map={'Not Survived': palette[3], 'Survived': palette[2]},
                     title='Survival Count', hover_data=['Survived', 'Sex', 'Pclass', 'Age'])
        st.plotly_chart(fig)
    elif nav == "Survival Rate by Gender":
        fig = px.bar(survival_rate, x='Sex', y='Survived', 
                     color='Sex',
                     color_discrete_map={'male': palette[0], 'female': palette[1]},
                     title='Survival Rate by Gender', hover_data=['Sex', 'Survived'])
        st.plotly_chart(fig)
    elif nav == "Survival Rate by Class and Gender":
        fig = px.bar(survival_rate_class_gender, x='Pclass', y='Survived', color='Sex',
                     color_discrete_map={'male': palette[0], 'female': palette[1]},
                     title='Survival Rate by Class and Gender', labels={'Pclass': 'Class'}, 
                     hover_data=['Pclass', 'Sex', 'Survived'])
        st.plotly_chart(fig)
    elif nav == "Age Distribution":
        fig = px.histogram(filtered_data, x='Age', nbins=30, color='Sex',
                           color_discrete_map={'male': palette[0], 'female': palette[1]},
                           title='Age Distribution', hover_data=['Age', 'Sex'])
        st.plotly_chart(fig)
    elif nav == "Fare Distribution":
        fig = px.histogram(filtered_data, x='Fare', nbins=30, color='Pclass',
                           color_discrete_sequence=palette[:3],
                           title='Fare Distribution', hover_data=['Fare', 'Pclass'])
        st.plotly_chart(fig)
    elif nav == "Correlation Heatmap":
        fig = px.imshow(corr, title='Correlation Heatmap', color_continuous_scale=px.colors.sequential.Viridis)
        st.plotly_chart(fig)

    # Expandable section for raw data
    if st.checkbox("Show Raw Data"):
        st.subheader("Raw Data")
        st.write(filtered_data)

    # Display some dynamic statistics based on filtered data
    st.subheader("Summary Statistics")
    st.write(filtered_data.describe())

if __name__ == "__main__":
    main()
