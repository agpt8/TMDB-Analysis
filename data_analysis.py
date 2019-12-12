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
        dataframe: cleaned dataset containing movie runtime for analysis

    """
    # average runtime of all movies
    print('\nAverage runtime of movies is approximately: {}'.format(get_average(dataframe, 'runtime')))

    # gives styles to background
    sns.set_style('darkgrid')
    plt.xlabel('Runtime of Movies')
    plt.ylabel('Number of Movies')
    plt.title('Runtime distribution of all the movies')

    # plotting runtime distribution of all movies using a histogram plot
    plt.hist(dataframe['runtime'])
    plt.show()

    # plotting interquartile range of movie runtime using box plot
    sns.boxplot(dataframe['runtime'])
    plt.show()

    # key insights on runtime
    print('\nHere are some key insights on movie runtime: ')
    print(dataframe['runtime'].describe())


def profits_each_year(dataframe):
    """
    This function return profits made by movies in each year

    Args:
        dataframe: cleaned dataset containing release year and profits made by movies

    """
    # Since we want to know the profits of movies for every year we need to group all the movies for those years
    profits_per_year = dataframe.groupby('release_year')['profit(US-Dollars)'].sum()

    # giving the figure size(width, height)
    plt.xlabel('Release Year of Movies')
    plt.ylabel('Total Profits made by Movies')
    plt.title('Total Profits Made by Movies')
    # using a line plot
    plt.plot(profits_per_year)
    plt.show()

    # shows which year made the highest profit
    print('\nThe year which made most profit is: {}'.format(profits_per_year.idxmax()))

    # using a dataFrame just to get a clean and better visual output
    profits_per_year = pd.DataFrame(profits_per_year)
    print('\nProfits made by movies in the last 5 years: ')
    print(profits_per_year.tail())


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
    print('Movies that earned most and least profit: ')
    print(get_highest_lowest(dataframe, 'profit(US-Dollars)'))

    # movies with longest and shortest runtime
    print('\nMovies which have longest and shortest runtime: ')
    print(get_highest_lowest(dataframe, 'runtime'))

    # movies with largest and smallest budget
    print('\nMovies that had largest and smallest budget: ')
    print(get_highest_lowest(dataframe, 'budget(US-Dollars)'))

    # movies with largest and smallest revenue
    print('\nMovies which had generated largest and smallest revenue: ')
    print(get_highest_lowest(dataframe, 'revenue(US-Dollars)'))

    # average runtime of all movies
    get_runtime(dataframe)

    # profits made by movies in each year
    profits_each_year(dataframe)


def get_column_count(dataframe, column_name):
    """
    This function calculate count of specified column elements

    Args:
        dataframe: cleaned dataset
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
        dataframe: cleaned dataset

    """
    genre_count = get_column_count(dataframe, 'genres')
    print('\nNumber of movies in each genre: ')
    print(genre_count.head())

    genre_count.sort_values(ascending=True, inplace=True)

    successful_genre_graph = genre_count.plot.barh(color='#007482')
    successful_genre_graph.set(title='Most Filmed Genres')
    successful_genre_graph.set_xlabel('Number of Movies')
    plt.show()


def highest_movie_month(dataframe):
    """
    This function calculates highest number of movies in a particular month

    Args:
        dataframe: cleaned dataset

    """
    # grouping all of the months of years and then calculate the profits of those months
    index_release_date = dataframe.set_index('release_date')
    # now we need to group all the data by month, since release date is in form of index, we extract month from it
    group_index = index_release_date.groupby([index_release_date.index.month])

    monthly_movie_count = group_index['profit(US-Dollars)'].count()

    monthly_movie_count = pd.DataFrame(monthly_movie_count)
    print('\nNumber of movies released in each month: ')
    print(monthly_movie_count)

    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']

    monthly_movie_count_bar = sns.barplot(x=monthly_movie_count.index, y=monthly_movie_count['profit(US-Dollars)'],
                                          data=monthly_movie_count)
    monthly_movie_count_bar.axes.set_title('Number of Movies Released in Each Month', alpha=0.6)
    monthly_movie_count_bar.set_xlabel("Months")
    monthly_movie_count_bar.set_ylabel("Number of Movies")
    monthly_movie_count_bar.set_xticklabels(month_list, rotation=30)
    plt.show()


def most_profit_month(dataframe):
    """
    This function returns the month which made most profit

    Args:
        dataframe: cleaned dataset

    """
    index_release_date = dataframe.set_index('release_date')
    group_index = index_release_date.groupby([index_release_date.index.month])
    monthly_profit = group_index['profit(US-Dollars)'].sum()

    monthly_profit = pd.DataFrame(monthly_profit)
    print('\nProfits made by movies in their release month: ')
    print(monthly_profit)

    monthly_profit_bar = sns.barplot(x=monthly_profit.index, y=monthly_profit['profit(US-Dollars)'],
                                     data=monthly_profit)

    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']

    monthly_profit_bar.axes.set_title('Profits Made by Movies in their Release Month', alpha=0.6)
    monthly_profit_bar.set_xlabel("Months")
    monthly_profit_bar.set_ylabel("Profits")
    monthly_profit_bar.set_xticklabels(month_list, rotation=30)
    plt.show()


def specific_statistics(dataframe):
    """
    This function calculates statistics, specifically for most successful movies.

    Args:
        dataframe: cleaned data passed for analysis

    """
    # assigning new dataframe which holds values only of movies having profit $50M or more
    profit_movie_data = dataframe[dataframe['profit(US-Dollars)'] >= 50000000]
    # reindexing new dataframe
    profit_movie_data.index = range(len(profit_movie_data))
    # will initialize dataframe from 1 instead of 0
    profit_movie_data.index += 1

    # average runtime of movies
    print('\nAverage runtime of movies: {} min(s)'.format(get_average(profit_movie_data, 'runtime')))

    # average budget of movies
    print('Average budget of movies: ${}'.format(get_average(profit_movie_data, 'budget(US-Dollars)')))

    # average revenue of movies
    print('Average revenue of movies: ${}'.format(get_average(profit_movie_data, 'revenue(US-Dollars)')))

    # average profit of movies
    print('Average profit of movies: ${}'.format(get_average(profit_movie_data, 'profit(US-Dollars)')))

    # count of movies directed by each director
    director_count = get_column_count(profit_movie_data, 'director')
    print('\nCount of movies directed by each directed: ')
    print(director_count.head())

    # count of cast starring in a particular movie
    cast_count = get_column_count(profit_movie_data, 'cast')
    print('\nCount of cast starring in a particular movie: ')
    print(cast_count.head())

    # count of successful movies in a particular genre
    successful_genre(profit_movie_data)

    # count of movies in a month
    highest_movie_month(profit_movie_data)

    # most profitable month
    most_profit_month(profit_movie_data)


def movie_production_trend(dataframe):
    """
    This function analyse the trend movie production has taken over the years

    Args:
        dataframe: cleaned dataset

    """
    # Number of movies produced each year
    movies_per_year = dataframe['release_year'].value_counts().sort_index()
    # Years with maximum and minimum movie production
    print('\nYear with lowest movie production: {}'.format(movies_per_year.idxmin()))
    print('Year with highest movie production: {}'.format(movies_per_year.idxmax()))
    plt.title('Movie Production Trend over the Years')
    plt.xlabel('Year')
    plt.ylabel('Number of movies released')
    plt.plot(movies_per_year)
    plt.show()


def highest_grossing_movies(dataframe):
    """
    This function gets the top 20 highest grossing movies

    Args:
        dataframe: cleaned dataset

    """
    sorted_revenue = dataframe['revenue(US-Dollars)'].sort_values(ascending=False)[:20]
    high_grossing = pd.DataFrame(sorted_revenue)

    titles = []
    revenues = []
    for i in sorted_revenue.index:
        titles.append(dataframe.loc[i, 'original_title'])
        revenues.append(sorted_revenue.loc[i])

    high_grossing['Titles'] = titles
    # high_grossing['Revenues'] = revenues

    high_grossing.set_index('Titles', inplace=True)
    high_grossing.plot(kind='bar')
    plt.title('Top 20 highest grossing movies (1960 - 2015) ')
    plt.ylabel('Revenue in billions ($)')
    plt.show()

    # List of top 20 highest grossing movies and their revenue
    print('\nTop 20 highest grossing movies: ')
    print(high_grossing)


def most_expensive_movies(dataframe):
    """
    This function gets top 20 most expensive movies

    Args:
        dataframe: cleaned dataset

    """
    sorted_budget = dataframe['budget(US-Dollars)'].sort_values(ascending=False)[:20]
    high_budget = pd.DataFrame(sorted_budget)
    titles_exp = []
    budgets = []
    for i in sorted_budget.index:
        titles_exp.append(dataframe.loc[i, 'original_title'])
        budgets.append(sorted_budget.loc[i])

    high_budget['Titles'] = titles_exp
    # high_budget['Budgets'] = budgets

    high_budget.set_index('Titles', inplace=True)
    high_budget.plot(kind='bar')
    plt.title('Top 20 most expensive movies (1960 - 2015)')
    plt.ylabel('Budget in 100\'s of million ($)')
    plt.show()

    # List of top 20 most expensive movies and their revenue
    print('\nTop 20 most expensive movies of all time: ')
    print(high_budget)


def budget_revenue_corr(dataframe):
    """
    This function plots correlation between budget and revenue

    Args:
        dataframe: cleaned dataset

    """
    dataframe.plot(x='budget(US-Dollars)', y='revenue(US-Dollars)', kind='scatter')
    plt.title('Budget vs Revenue')
    plt.xlabel('Budget in 100s of million ($)')
    plt.ylabel('Revenue in billions ($)')
    plt.show()
    person_correlation_coeff = dataframe['budget(US-Dollars)'].corr(dataframe['revenue(US-Dollars)'], method='pearson')
    print('\nCorrelation between budget and revenue: {}'.format(person_correlation_coeff))


def genre_runtime(dataframe):
    """
    This function shows what run times are associated with genres

    Args:
        dataframe: cleaned dataset

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
    genre_runtime_combined = pd.DataFrame({'genre': all_genres, 'runtime': all_runtimes})

    # Group by genre and find the average of run times sorted in ascending order
    runtime_by_genre = genre_runtime_combined.sort_values(['runtime']).groupby('genre')['runtime'].mean()
    runtime_by_genre.sort_values().plot(kind='bar')
    plt.title('Average Run Time for Each Genre')
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
    highest_grossing_movies(dataframe)

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
