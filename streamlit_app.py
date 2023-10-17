# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 13:59:06 2023

@author: Mosco
"""

import streamlit as st
import seaborn as sns
from data_manager import DataManager

# Load data
DATA_PATH = 'data/titanic.csv'
data_manager = DataManager(DATA_PATH)

def main():
    st.title("Titanic Dataset Analysis")

    # Navigation bar
    nav = st.sidebar.radio("Choose a Visualization:", ["Survival Count", "Class Distribution"])

    if nav == "Survival Count":
        st.header("Survival Count")
        survival_count = data_manager.get_survival_count()
        st.bar_chart(survival_count)
    elif nav == "Class Distribution":
        st.header("Class Distribution")
        class_distribution = data_manager.get_class_distribution()
        st.bar_chart(class_distribution)

if __name__ == "__main__":
    main()
