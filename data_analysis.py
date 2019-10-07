# Copyright 2019 Ayush Gupta
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import pandas as pd

from data_clean import data_cleaning

movie_data = pd.read_csv('tmdb-movies.csv')


def get_highest_lowest(dataframe, column_name):
    """
    This function calculates highest and lowest values of columns specified in the argument

    :param dataframe: dataframe from which values are taken
    :param column_name: column name for which highest and values are to be calculated
    :return: concatenated data frame containing highest and lowest calculated values
    """
    # taking the index value of the highest number in profit column
    highest_id = dataframe[column_name].idxmax()
    # calling by index number, storing that row info in a variable
    highest_value = pd.DataFrame(dataframe.loc[highest_id])

    # taking the index value of the lowest number in profit column
    lowest_id = dataframe[column_name].idxmin()
    # calling by index number, storing that row info in a variable
    lowest_value = pd.DataFrame(dataframe.loc[lowest_id])

    # concatenating two values in a single data frame
    combined_values = pd.concat([highest_value, lowest_value], axis=1)

    return combined_values


def get_average(dataframe, column_name):
    """
    This function calculates and returns average of the column specified

    :param dataframe: dataframe from which values are taken
    :param column_name: column name for which average is calculated
    :return: average value of the column
    """
    return dataframe[column_name].mean()


def get_statistics(dataframe):
    """
    This function infer various statistics about the cleaned data frame for exploratory purposes.
    See README.md for more details

    :param dataframe: cleaned data passed for analysis
    """
    # assigning a new column which will hold the profit values of each movie
    dataframe.insert(2, 'profit(US-Dollars)', dataframe['revenue(US-Dollars)'] - dataframe['budget('
                                                                                           'US-Dollars)'])
    # changing the data type of the column to float for consistency
    dataframe['profit(US-Dollars)'] = dataframe['profit(US-Dollars)'].apply(np.float64)

    # movie with most and least earned profit
    print(get_highest_lowest(dataframe, 'profit(US-Dollars)'))

    # movies with longest and shortest runtime
    print(get_highest_lowest(dataframe, 'runtime'))

    # movies with largest and smallest budget
    print(get_highest_lowest(dataframe, 'budget(US-Dollars)'))

    # movies with largest and smallest revenue
    print(get_highest_lowest(dataframe, 'revenue(US-Dollars)'))

    # average runtime of all movies
    print(get_average(dataframe, 'runtime'))


if __name__ == '__main__':
    movie_data_cleaned = data_cleaning(movie_data)
    get_statistics(movie_data_cleaned)
