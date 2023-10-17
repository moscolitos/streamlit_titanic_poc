# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 13:53:17 2023

@author: Mosco
"""

import pandas as pd

class DataManager:
    def __init__(self, data_path: str):
        self.data = pd.read_csv(data_path)

    def get_survival_count(self):
        return self.data.groupby('Survived').size()

    def get_class_distribution(self):
        return self.data.groupby('Pclass').size()
