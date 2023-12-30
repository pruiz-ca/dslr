"""Utility functions
"""
import os
import sys
import pandas as pd
import numpy as np


def parse_input(argc: int, args: list[str]) -> str | tuple[str]:
    """Parse input and return the dataset path

        Return:
            str: path to the dataset
    """
    if len(sys.argv[1:]) != argc:
        file = sys.argv[0].rsplit("/", maxsplit=1)[-1]
        msg = f'Usage: {file} {" ".join([f"<{arg}>" for arg in args])}'
        sys.exit(msg)

    for arg in sys.argv[1:]:
        if not arg.endswith('.csv'):
            sys.exit('Error. Invalid dataset')

        if not os.path.isfile(arg):
            sys.exit('Error. Dataset not found')

    if argc == 1:
        return sys.argv[1]
    return [sys.argv[1], sys.argv[2]]


def normalizeData(data: pd.DataFrame) -> pd.DataFrame:
    """Convert data to a range between 0 and 1

        Parameters:
            data (pd.DataFrame): data to normalize

        Returns:
            pd.DataFrame: normalized data
    """
    data_norm = (data - data.min()) / (data.max() - data.min())
    return data_norm


def ask_user_for_courses(columns: list, input_count: int) -> tuple:
    """Ask user for #input_count courses and return a tuple with the
    selected ones

        Parameters:
            columns (list): list of column names
            input_count (int): number of courses to select

        Returns:
            tuple: tuple of selected courses
    """
    try:
        courses = []
        print('Please select courses:')

        for count in range(input_count):
            for i, column_value in enumerate(columns):
                print(str(i + 1) + ') ' + column_value)

            choice = input(f'> Course {count + 1}: ')

            idx = int(choice) - 1
            if idx not in range(len(columns)):
                raise Exception('Error. Input is out of range')

            courses.append(columns[idx])

        return courses

    except ValueError:
        sys.exit('Error. Input is not a number.')

    except KeyboardInterrupt:
        sys.exit('\nExiting...')

    except Exception as e:
        sys.exit(f'Error. {e}')


def getNumericData(dataset: str) -> pd.DataFrame:
    """"Get data for data_analysis script

        Returns:
            pd.DataFrame: numeric data for data_analysis script
    """
    raw_data = pd.read_csv(dataset, index_col=0)
    return raw_data.select_dtypes(include=['number'])


def getVisualData(dataset: str, input_count: int) -> tuple:
    """Get data for data_visualization scripts

        Parameters:
            dataset (str): path to the dataset
            input_count (int): number of courses to select

        Returns:
            tuple: tuple of houses data and selected courses
    """

    raw_data = pd.read_csv(dataset, index_col=0)
    numeric_data = raw_data.select_dtypes(include=['number'])

    griffindor = raw_data.query("`Hogwarts House` == 'Gryffindor'")
    slytherin = raw_data.query("`Hogwarts House` == 'Slytherin'")
    hufflepuff = raw_data.query("`Hogwarts House` == 'Hufflepuff'")
    ravenclaw = raw_data.query("`Hogwarts House` == 'Ravenclaw'")

    if input_count == 0:
        courses = numeric_data.columns
        houses_data = [griffindor, slytherin, hufflepuff, ravenclaw]
        return houses_data, courses

    courses = ask_user_for_courses(numeric_data.columns, input_count)

    houses_data = []
    for course in courses:
        houses_data.append([
            griffindor[course], slytherin[course], hufflepuff[course],
            ravenclaw[course]
        ])

    return houses_data, courses


def getLRData(dataset: str, house: str) -> tuple[np.array]:
    """Get data for logistic_regression scripts

        Parameters:
            dataset (str): path to the dataset
            input_count (int): number of courses to select

        Returns:
            tuple[np.array]: x and y data ready for lr
    """
    data = pd.read_csv(dataset, index_col=0)
    X = normalizeData(data.select_dtypes(include=['number']).fillna(0))
    Y = data['Hogwarts House'].apply(lambda x: 1 if x == house else 0)

    x_array = X.values
    y_array = Y.values

    x = x_array.T
    y = y_array.reshape(1, x.shape[1])

    return x, y
