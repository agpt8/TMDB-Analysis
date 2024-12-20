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


def data_info(dataframe):
    """
    Provides general information about the dataframe like shape, data types of the columns, mean, standard deviation,
    inter quartile ranges, minimum, maximum. etc.

    Args:
        dataframe: data passed for assessment

    """
    # general info about the dataframe
    info = dataframe.info()
    # description of the data
    description = dataframe.describe()
    # data type of columns
    data_type = dataframe.dtypes
    # view first five rows of the dataframe
    data_view = dataframe.head()
    # shape of the dataframe before cleaning
    rows, col = dataframe.shape

    print(info)
    print(description)
    print(data_type)
    print(data_view)
    # since 'rows' includes count of a header, we need to remove its count.
    print('We have {} total entries of movies and {} columns/features of it.\n'.format(rows - 1, col))


def data_cleaning(dataframe):
    """
    This function cleans the data for further analysis. Cleaning includes
    removing duplicates, removing null values and deleting unnecessary columns.

    Args:
        dataframe: data passed for cleaning

    Returns:
        cleaned dataframe

    """
    # getting information about the data before cleaning
    print('Here is the information on the data before we clean it: \n')
    data_info(dataframe)

    # list of columns that needs to be deleted
    del_col = ['id', 'imdb_id', 'popularity', 'budget_adj', 'revenue_adj', 'homepage', 'keywords', 'overview',
               'production_companies', 'vote_count', 'vote_average']
    # deleting the columns from the database
    dataframe = dataframe.drop(del_col, axis=1)

    # dropping duplicate rows but will keep the first one
    dataframe = dataframe.drop_duplicates()

    # list of column names that needs to be checked for 0
    check_row = ['budget', 'revenue']
    # this will replace the value of '0' to NaN of columns given in the list
    dataframe[check_row] = dataframe[check_row].replace(0, np.NaN)
    # now we will drop any row which has NaN values in any of the column of the list (check_row)
    dataframe = dataframe.dropna(subset=check_row)

    # replacing 0 with NaN of runtime column of the dataframe
    dataframe['runtime'] = dataframe['runtime'].replace(0, np.NaN)

    # changing data type of `release_date` column from string to datetime
    dataframe['release_date'] = pd.to_datetime(dataframe['release_date'])

    # renaming `budget` and `revenue` columns to include currency (assuming US dollars)
    dataframe.rename(columns={'budget': 'budget(US-Dollars)', 'revenue': 'revenue(US-Dollars)'}, inplace=True)

    # getting information about the data after cleaning
    print('Here is the information on the data after we clean it: \n')
    data_info(dataframe)

    return dataframe
