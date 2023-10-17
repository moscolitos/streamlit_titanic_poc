# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 14:09:22 2023

@author: Mosco
"""

import pandas as pd
import streamlit as st

class DataManager:
    def __init__(self, data_path: str):
#        self.data = self.load_data(data_path)
        self.data = pd.read_csv(data_path)

        self.preprocess_data()

    @st.cache
    def load_data(self, data_path):
        return pd.read_csv(data_path)


    def preprocess_data(self):
        # Handle missing values (basic handling for simplicity)
        self.data['Age'].fillna(self.data['Age'].median(), inplace=True)
        self.data['Embarked'].fillna(self.data['Embarked'].mode()[0], inplace=True)

    def get_survival_count(self):
        return self.data.groupby('Survived').size()

    def get_class_distribution(self):
        return self.data.groupby('Pclass').size()

    def get_survival_by_gender(self):
        return self.data.groupby('Sex')['Survived'].mean()

    def get_survival_by_class_gender(self):
        return self.data.groupby(['Pclass', 'Sex'])['Survived'].mean().unstack()

    def get_age_distribution(self):
        return self.data['Age']

    def get_fare_distribution(self):
        return self.data['Fare']

    def filter_data(self, gender=None, pclass=None, age_range=None, embarked=None):
        filtered_data = self.data
        if gender:
            filtered_data = filtered_data[filtered_data['Sex'] == gender]
        if pclass:
            filtered_data = filtered_data[filtered_data['Pclass'] == pclass]
        if age_range:
            min_age, max_age = age_range
            filtered_data = filtered_data[(filtered_data['Age'] >= min_age) & (filtered_data['Age'] <= max_age)]
        if embarked:
            filtered_data = filtered_data[filtered_data['Embarked'] == embarked]
        return filtered_data
