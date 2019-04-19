# -*- coding: utf-8 -*-

import pandas as pd

#Function to read only the first N columns of a dataframe
def front(self, n):
	return self.iloc[:, :n]

pd.DataFrame.front = front
