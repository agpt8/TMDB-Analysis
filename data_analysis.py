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

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from data_clean import data_cleaning

movie_data = pd.read_csv('tmdb-movies.csv')


def get_highest_lowest(dataframe, column_name):
    """
    This function calculates highest and lowest values of columns specified in the argument

    Args:
        dataframe: dataframe from which values are taken
        column_name: column name for which highest and values are to be calculated
    Returns:
        concatenated data frame containing highest and lowest calculated values
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

    Args:
        dataframe: dataframe from which values are taken
        column_name: column name for which average is calculated
    Returns:
        average value of the column
    """
    return dataframe[column_name].mean()


def get_runtime(dataframe):
    """
    This function gets runtime average of all movies including graphs for runtime distribution, swarmplot and box plot
    for deeper insights

    Args:
        dataframe: data containing runtime for analysis
    """
    # average runtime of all movies
    print(get_average(dataframe, 'runtime'))

    # gives styles to background
    sns.set_style('darkgrid')
    # changing the label size
    plt.rc('xtick', labelsize=10)
    plt.rc('ytick', labelsize=10)
    plt.figure(figsize=(9, 6), dpi=100)
    plt.xlabel('Runtime of Movies', fontsize=15)
    plt.ylabel('Number of Movies', fontsize=15)
    plt.title('Runtime distribution of all the movies', fontsize=18)

    # plotting runtime distribution of all movies using a histogram plot
    plt.hist(movie_data['runtime'], rwidth=0.9, bins=31)
    # displays the plot
    plt.show()

    # plotting interquartile range of movie runtime using box plot
    plt.figure(figsize=(9, 7), dpi=105)
    sns.boxplot(movie_data['runtime'], linewidth=3)
    plt.show()

    # plotting swarmplot showing all the data points
    plt.figure(figsize=(10, 5), dpi=105)
    sns.swarmplot(data=movie_data['runtime'], color='red')
    plt.show()

    # key insights on runtime
    movie_data_cleaned['runtime'].describe()


def profits_each_year(dataframe):
    """
    This function return profits made by movies in each year

    Args:
        dataframe: data containing release year and profits made by movies
    """
    # Since we want to know the profits of movies for every year we need to group all the movies for those years
    profits_per_year = movie_data.groupby('release_year')['profit_(in_US_Dollars)'].sum()

    # giving the figure size(width, height)
    plt.figure(figsize=(12, 6), dpi=130)
    plt.xlabel('Release Year of Movies', fontsize=12)
    plt.ylabel('Total Profits made by Movies', fontsize=12)
    plt.title('Calculating Total Profits made by all movies in year which it released.')
    # using a line plot
    plt.plot(profits_per_year)
    plt.show()

    # shows which year made the highest profit
    profits_per_year.idxmax()

    # using a dataFrame just to get a clean and better visual output
    profits_per_year = pd.DataFrame(profits_per_year)
    profits_per_year.tail()


def get_statistics(dataframe):
    """
    This function infer various statistics about the cleaned data frame for exploratory purposes.
    See README.md for more details

    Args:
        dataframe: cleaned data passed for analysis
    """
    # assigning a new column which will hold the profit values of each movie
    dataframe.insert(2, 'profit(US-Dollars)', dataframe['revenue(US-Dollars)'] - dataframe['budget(US-Dollars)'])
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
    get_runtime(dataframe)

    # profits made by movies in each year
    profits_each_year(dataframe)


if __name__ == '__main__':
    movie_data_cleaned = data_cleaning(movie_data)
    get_statistics(movie_data_cleaned)
