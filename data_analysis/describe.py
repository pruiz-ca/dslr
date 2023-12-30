"""Data analysis - Describe
"""

from os import sys, path
from math import nan, sqrt
import pandas as pd

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from dslr_extra.utils import getNumericData, parse_input


def setCount(df: pd.DataFrame, data: pd.DataFrame, col: str) -> None:
    """Count non null values

        Parameters:
            df (pd.DataFrame): dataframe to update
            data (pd.DataFrame): data to count
            col (str): column to count
    """
    df.at['count', col] = data[col].notnull().sum()


def setMean(df: pd.DataFrame, data: pd.DataFrame, col: str) -> None:
    """Calculate the mean

        Parameters:
            df (pd.DataFrame): dataframe to update
            data (pd.DataFrame): data to count
            col (str): column to count
    """
    size = df.at['count', col]
    df.at['mean', col] = data[col].sum() / size if size != 0 else nan


def setStd(df: pd.DataFrame, data: pd.DataFrame, col: str) -> None:
    """Calculate the Std Deviation

        Parameters:
            df (pd.DataFrame): dataframe to update
            data (pd.DataFrame): data to count
            col (str): column to count
    """
    size = df.at['count', col]
    mean = df.at['mean', col]
    numerator = ((data[col] - mean)**2).sum()
    df.at['std', col] = sqrt(numerator / size) if size != 0 else nan


def setMin(df: pd.DataFrame, data: pd.DataFrame, col: str) -> None:
    """Calculate the Minimum value

        Parameters:
            df (pd.DataFrame): dataframe to update
            data (pd.DataFrame): data to count
            col (str): column to count
    """
    df.at['min', col] = data[col].sort_values().iloc[0]


def setMax(df: pd.DataFrame, data: pd.DataFrame, col: str) -> None:
    """Calculate the Maximum value

        Parameters:
            df (pd.DataFrame): dataframe to update
            data (pd.DataFrame): data to count
            col (str): column to count
    """
    size = df.at['count', col]
    df.at['max', col] = data[col].sort_values().iloc[size - 1]


def setPercentile(df: pd.DataFrame, data: pd.DataFrame, col: str,
                  percentile: int) -> None:
    """Calculate the Percentile

        Parameters:
            df (pd.DataFrame): dataframe to update
            data (pd.DataFrame): data to count
            col (str): column to count
            percentile (int): percentile to calculate
    """
    size = df.at['count', col]
    sorted_values = data[col].sort_values()

    rank = percentile / 100 * (size)
    rank_decimal = rank % 1
    rank_rounded = rank - rank_decimal

    lower = sorted_values.iloc[int(rank_rounded)]
    if int(rank_rounded + 1) >= size:
        upper = lower
    else:
        upper = sorted_values.iloc[int(rank_rounded) + 1]

    percentile_value = lower + rank_decimal * (upper - lower)

    df.at[str(percentile) + '%', col] = percentile_value


def main() -> None:
    """Main function
    """
    dataset = parse_input(1, ["dataset.csv"])
    data = getNumericData(dataset)

    describe = pd.DataFrame(
        columns=data.columns.values,
        index=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])

    for col in data:
        setCount(describe, data, col)
        setMean(describe, data, col)
        setStd(describe, data, col)
        setMin(describe, data, col)
        setMax(describe, data, col)
        setPercentile(describe, data, col, 25)
        setPercentile(describe, data, col, 50)
        setPercentile(describe, data, col, 75)

    print(describe)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        sys.exit('\nExiting...')
    except Exception as e:
        sys.exit(f'Error. {e}')
