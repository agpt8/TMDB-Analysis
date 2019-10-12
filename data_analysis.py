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


def get_highest_lowest(dataframe, column_name):
    """
    This function calculates highest and lowest values of columns specified in the argument

    Args:
        dataframe: cleaned dataset
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
        dataframe: cleaned dataset
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
        dataframe: cleaned data containing movie runtime for analysis

    """
    # average runtime of all movies
    print('Average runtime of movies is approximately: {}'.format(get_average(dataframe, 'runtime')))

    # gives styles to background
    sns.set_style('darkgrid')
    # changing the label size
    plt.xlabel('Runtime of Movies')
    plt.ylabel('Number of Movies')
    plt.title('Runtime distribution of all the movies')

    # plotting runtime distribution of all movies using a histogram plot
    plt.hist(movie_data['runtime'])
    plt.show()

    # plotting interquartile range of movie runtime using box plot
    sns.boxplot(movie_data['runtime'])
    plt.show()

    # key insights on runtime
    print('Here are some key insights on movie runtime:\n')
    movie_data_cleaned['runtime'].describe()


def profits_each_year(dataframe):
    """
    This function return profits made by movies in each year

    Args:
        dataframe: data containing release year and profits made by movies
    """
    # Since we want to know the profits of movies for every year we need to group all the movies for those years
    profits_per_year = dataframe.groupby('release_year')['profit(US-Dollars)'].sum()

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


def general_statistics(dataframe):
    """
    This function calculates general statistics about the cleaned data frame for exploratory purposes.
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


def get_profit_average(dataframe, column_name):
    """
    This function calculates average of specified column name for most profitable movies

    Args:
        dataframe: data containing most profitable movies
        column_name: column for which average is calculated

    Returns: average of column specified
    """
    return dataframe[column_name].mean()


def get_column_count(dataframe, column_name):
    """
    This function calculate count of specified column elements

    Args:
        dataframe: data in which column is present
        column_name: column containing the elements for which count is calculated
    Returns:
        count of elements
    """
    # will take a column, and separate the string by '|'
    all_data = dataframe[column_name].str.cat(sep='|')

    # giving pandas series and storing the values separately
    all_data = pd.Series(all_data.split('|'))

    count = all_data.value_counts()

    return count


def successful_genre(dataframe):
    """
    This function counts number of movies in a particular genre and plots it in a bar graph

    Args:
        dataframe: data containing the count of movies
    """
    genre_count = get_column_count(dataframe, 'genres')
    print(genre_count.head())

    genre_count.sort_values(ascending=True, inplace=True)

    successful_genre_graph = genre_count.plot.barh(color='#007482', fontsize=15)
    successful_genre_graph.set(title='The Most filmed genres')
    successful_genre_graph.set_xlabel('Number of Movies', fontsize='18')
    successful_genre_graph.figure.set_size_inches(12, 10)
    plt.show()


def highest_movie_month(dataframe):
    """
    This function calculates highest number of movies in a particular month

    Args:
        dataframe: data containing all the months and number of movies
    """
    # grouping all of the months of years and then calculate the profits of those months
    index_release_date = dataframe.set_index('release_date')
    # now we need to group all the data by month, since release date is in form of index, we extract month from it
    group_index = index_release_date.groupby([index_release_date.index.month])

    monthly_movie_count = group_index['profit(US-Dollars)'].count()

    monthly_movie_count = pd.DataFrame(monthly_movie_count)

    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']

    monthly_movie_count_bar = sns.barplot(x=monthly_movie_count.index, y=monthly_movie_count['profit(US-Dollars)'],
                                          data=monthly_movie_count)
    monthly_movie_count_bar.figure.set_size_inches(15, 8)
    monthly_movie_count_bar.axes.set_title('Number of Movies released in each month', fontsize=25, alpha=0.6)
    monthly_movie_count_bar.set_xlabel("Months", fontsize=25)
    monthly_movie_count_bar.set_ylabel("Number of Movies", fontsize=35)
    monthly_movie_count_bar.tick_params(labelsize=15, labelcolor="black")
    monthly_movie_count_bar.set_xticklabels(month_list, rotation=30, size=18)
    plt.show()


def most_profit_month(dataframe):
    """
    This function returns the month which made most profit

    Args:
        dataframe: data containing month and number of movies
    """
    index_release_date = dataframe.set_index('release_date')
    group_index = index_release_date.groupby([index_release_date.index.month])
    monthly_profit = group_index['profit(US-Dollars)'].sum()

    monthly_profit = pd.DataFrame(monthly_profit)

    monthly_profit_bar = sns.barplot(x=monthly_profit.index, y=monthly_profit['profit(US-Dollars)'],
                                     data=monthly_profit)

    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']

    monthly_profit_bar.figure.set_size_inches(15, 8)
    monthly_profit_bar.axes.set_title('Profits made by movies at their released months', fontsize=25, alpha=0.6)
    monthly_profit_bar.set_xlabel("Months", fontsize=25)
    monthly_profit_bar.set_ylabel("Profits", fontsize=35)
    monthly_profit_bar.tick_params(labelsize=15, labelcolor="black")
    monthly_profit_bar.set_xticklabels(month_list, rotation=30, size=18)
    plt.show()


def specific_statistics(dataframe):
    """
    This function calculates specific statistics of most successful movies.

    Args:
        dataframe: cleaned data passed for analysis
    """
    # assigning new dataframe which holds values only of movies having profit $50M or more
    profit_movie_data = dataframe[dataframe['profit(US-Dollars)'] >= 50000000]
    # reindexing new dataframe
    profit_movie_data.index = range(len(profit_movie_data))
    # will initialize dataframe from 1 instead of 0
    profit_movie_data.index += 1

    # average runtime of movies which had profit of >= 50000000
    get_profit_average(dataframe, 'runtime')

    # average budget of movies which had profit of >=50000000
    get_profit_average(dataframe, 'budget(US-Dollars)')

    # average revenue of movies which had profit of >=50000000
    get_profit_average(dataframe, 'revenue(US-Dollars)')

    # count of movies directed by each director
    director_count = get_column_count(dataframe, 'director')
    print(director_count.head())

    # count of cast starring in a particular movie
    cast_count = get_column_count(dataframe, 'cast')
    print(cast_count.head())

    # count of successful movies in a particular genre
    successful_genre(dataframe)

    # count of movies in a month
    highest_movie_month(dataframe)

    # most profitable month
    most_profit_month(dataframe)


def movie_production_trend(dataframe):
    """
    This function analyse the trend movie production has taken over the years

    Args:
        dataframe: data containing movie release years
    """
    # Number of movies produced each year
    movies_per_year = dataframe['release_year'].value_counts().sort_index()
    # Years with maximum and minimum movie production
    print(movies_per_year.idxmax(), movies_per_year.idxmin())
    plt.title('Movie production trend over the years')
    plt.xlabel('Year')
    plt.ylabel('Number of movies released')
    plt.plot(movies_per_year)
    plt.show()


def highest_grossing_movies(dataframe):
    """
    This function gets the top 20 highest grossing movies

    Args:
        dataframe: data containing movies and their revenues
    """
    sorted_revenue = dataframe['revenue(US-Dollars)'].sort_values(ascending=False)[:20]
    high_grossing = pd.DataFrame()
    # List of top 20 highest grossing movies and their revenue
    print(high_grossing)
    titles = []
    revenues = []
    for i in sorted_revenue.index:
        titles.append(dataframe.loc[i, 'original_title'])
        revenues.append(sorted_revenue.loc[i])
    high_grossing['Titles'] = titles
    high_grossing['Revenues'] = revenues
    high_grossing.set_index('Titles', inplace=True)
    high_grossing.plot(kind='bar', figsize=(8, 8))
    plt.title('Top 20 highest grossing movies (1960 - 2015) ')
    plt.ylabel('Revenue in billions ($)')
    plt.show()


def most_expensive_movies(dataframe):
    """
    This function gets top 20 most expensive movies

    Args:
        dataframe: data containing movies and their budget
    """
    sorted_budget = dataframe['budget(US-Dollars)'].sort_values(ascending=False)[:20]
    high_budget = pd.DataFrame()
    # List of top 20 most expensive movies and their revenue
    print(high_budget)
    titles_exp = []
    budgets = []
    for i in sorted_budget.index:
        titles_exp.append(dataframe.loc[i, 'original_title'])
        budgets.append(sorted_budget.loc[i])
    high_budget['Titles'] = titles_exp
    high_budget['Budgets'] = budgets
    high_budget.set_index('Titles', inplace=True)
    high_budget.plot(kind='bar', figsize=(8, 8))
    plt.title('Top 20 most expensive movies (1960 - 2015) ')
    plt.ylabel('Budget in 100\'s of million ($)')
    plt.show()


def budget_revenue_corr(dataframe):
    """
    This function plots correlation between budget and revenue

    Args:
        dataframe: data containing budget and revenue of movies

    """
    dataframe.plot(x='budget(US-Dollars)', y='revenue(US-Dollars)', kind='scatter', figsize=(8, 8))
    plt.title('Budget vs Revenue')
    plt.xlabel('Budget in 100s of million ($)')
    plt.ylabel('Revenue in billions ($)')
    plt.show()
    person_correlation_coeff = dataframe['budget(US-Dollars)'].corr(dataframe['revenue(US-Dollars)'], method='pearson')
    print(person_correlation_coeff)


def genre_runtime(dataframe):
    """
    This function shows what run times are asssociated with genres

    Args:
        dataframe: data containing runtimes and genres

    """
    # Drop rows with null values in genre and director columns
    dataframe.dropna(subset=['genres'], inplace=True)

    # Converting the 'genre' column into a list of genres by splitting at the pipe symbol
    dataframe['genres'] = np.where((dataframe['genres'].str.contains('|')), dataframe['genres'].str.split('|'),
                                   dataframe['genres'])

    # Making sure every row has data as a list, even if only one genre is present
    dataframe.loc[:, 'genres'] = dataframe.genres.apply(np.atleast_1d)

    # Horizontally stacking all the lists from all rows into one big list
    all_genres = np.hstack(dataframe.genres)

    # Repeating the runtime as many times as the length of list genre and merging it all into one list
    all_runtimes = []
    for runtime, genre in dataframe[['runtime', 'genres']].values:
        all_runtimes += [runtime] * len(genre)

    # Assigning the merged lists / arrays to a new dataframe
    a = pd.DataFrame({'genre': all_genres, 'runtime': all_runtimes})

    # Group by genre and find the average of run times sorted in ascending order
    runtime_by_genre = a.sort_values(['runtime']).groupby('genre')['runtime'].mean()
    runtime_by_genre.sort_values().plot(kind='bar')
    plt.title('Average run time for each genre')
    plt.ylabel('Run time (mins)')
    plt.xlabel('Genre')
    plt.show()


def general_analysis(dataframe):
    """
    This function gets general analysis and correlation between various factors

    Args:
        dataframe: cleaned data passed for analysis
    """
    # movie production trend over the years
    movie_production_trend(dataframe)

    # top 20 highest grossing movies
    highest_movie_month(dataframe)

    # top 20 most expensive movies
    most_expensive_movies(dataframe)

    # budget-revenue correlation
    budget_revenue_corr(dataframe)

    # runtime associated with genre
    genre_runtime(dataframe)


if __name__ == '__main__':
    movie_data = pd.read_csv('tmdb-movies.csv')
    movie_data_cleaned = data_cleaning(movie_data)
    general_statistics(movie_data_cleaned)
    specific_statistics(movie_data_cleaned)
    general_analysis(movie_data_cleaned)