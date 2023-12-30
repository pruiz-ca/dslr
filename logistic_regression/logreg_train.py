"""Logistic Regression - Training
"""
import os
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from alive_progress import alive_bar

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dslr_extra.utils import getLRData, parse_input

iterations = 10000
learning_rate = 0.05

c_green = "\033[92m"
c_pink = "\033[95m"
c_red = "\033[91m"
c_grey = "\033[90m"
c_end = "\033[0m"


def sigmoid(x: np.array) -> np.array:
    """Apply the sigmoid function to x

        Parameters:
            x: np.array - input values

        Return:
            np.array: sigmoid(x)
    """
    return 1 / (1 + np.exp(-x))


def prediction(x: np.array, w: np.array, b: np.array) -> np.array:
    """Returns the prediction for x given w and b

        Parameters:
            x: np.array - dependent variables
            w: np.array - weights
            b: np.array - bias

        Return:
            np.array: prediction for x
    """
    z = np.dot(w.T, x) + b
    return sigmoid(z)


def calculate_accuracy(x: np.array, y: np.array, w: np.array,
                       b: np.array) -> float:
    """Returns the accuracy of the model in %

        Parameters:
            x: np.array - dependent variables
            y: np.array - independent variables
            w: np.array - weights
            b: np.array - bias

        Return:
            float: accuracy of the model
    """
    a = (prediction(x, w, b) > 0.5).astype(int)

    return accuracy_score(y[0], a[0]) * 100


def train_model(dataset: str, house: str) -> tuple[np.array, np.array, float]:
    """Model training function

        Parameters:
            dataset: str - path to the dataset
            house: str - house to train the model for

        Return:
            tuple[np.array, np.array, any]: weights, bias, accuracy
    """
    x, y = getLRData(dataset, house)

    m = x.shape[1]
    n = x.shape[0]

    w = np.zeros((n, 1))
    b = np.zeros((1, 1))

    initial_cost = 0
    with alive_bar(iterations,
                   title=f'- {house}',
                   bar='circles',
                   spinner='dots_waves',
                   stats_end=False,
                   title_length=12,
                   spinner_length=3,
                   receipt_text=True) as progress_bar:
        for i in range(1, iterations + 1):
            a = prediction(x, w, b)

            dw = (1 / m) * np.dot(a - y, x.T)
            db = (1 / m) * np.sum(a - y)

            w = w - learning_rate * dw.T
            b = b - learning_rate * db

            if i % (iterations / 100) == 0:
                cost = -(1 / m) * np.sum(y * np.log(a) +
                                         (1 - y) * np.log(1 - a))

                if i <= (iterations / 100):
                    initial_cost = cost

                progress_bar.text(
                    f'| Initial Cost: {initial_cost:.5f}| Cost: {cost:.5f}')

                if np.isnan(cost):
                    raise Exception('Cost function result is NaN.')

            progress_bar()

    accuracy = calculate_accuracy(x, y, w, b)

    return w, b, accuracy


def print_header() -> None:
    """Print initial settings
    """
    print(f'{c_pink}========================================')
    print(f'Iterations: {iterations} | Learning rate: {learning_rate}')
    print(f'========================================\n{c_end}')


def save_results(df: pd.DataFrame, houses: list[str],
                 accuracies: list[float]) -> None:
    """Save results to file and print them

        Parameters:
            df: pd.DataFrame - dataframe containing the weights
            houses: list[str] - list of houses
            accuracies: list[float] - list of accuracies
    """
    path = f'{os.path.dirname(os.path.realpath(__file__))}/results'

    if not os.path.exists(path):
        os.mkdir(path)

    if os.path.exists(f'{path}/weights.csv'):
        os.remove(f'{path}/weights.csv')

    df.to_csv(f'{path}/weights.csv', mode='a', index=0, header=houses)

    print('\n========================================')
    print(
        'Training complete. Results have been saved in logistic_regression/results/weights.csv'
    )
    print('Accuracies:')
    for i, house in enumerate(houses):
        color = c_red
        if accuracies[i] > 98.0:
            color = c_green

        print(f'- {house}: {color}{accuracies[i]}%{c_end}')
    print('========================================')


def main() -> None:
    """Main function
    """
    dataset = parse_input(1, ["dataset.csv"])
    houses = ['Ravenclaw', 'Hufflepuff', 'Gryffindor', 'Slytherin']

    print_header()
    accuracies = []
    df = pd.DataFrame()
    print('Training models:')
    for house in houses:
        w, b, accuracy = train_model(dataset, house)
        w = np.append(b, w)
        accuracies.append(accuracy)
        df[house] = w.tolist()

    save_results(df, houses, accuracies)


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        sys.exit('\nExiting...')
    except Exception as e:
        sys.exit(f'Error. {e}')
