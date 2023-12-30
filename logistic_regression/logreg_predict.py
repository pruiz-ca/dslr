"""Logistic Regression - Predict
"""
import os
import sys
import numpy as np
import pandas as pd
from logreg_train import prediction

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dslr_extra.utils import parse_input, normalizeData


def main() -> None:
    """Main function
    """
    datasets = parse_input(2, ['dataset.csv', 'weights.csv'])
    houses = ['Gryffindor', 'Slytherin', 'Ravenclaw', 'Hufflepuff']

    data = pd.read_csv(datasets[0], index_col=0).drop('Hogwarts House', axis=1)
    weights = pd.read_csv(datasets[1])

    X = normalizeData(data.select_dtypes(include=['number']).fillna(0))
    x = X.values.T

    results = pd.DataFrame(np.zeros((x.shape[1], 0)))
    results['Hogwarts House'] = 'None'

    for house in houses:
        w = weights[house][1:].values
        b = np.array(weights[house][0])

        predicts = prediction(x, w, b) > 0.5
        predicts = pd.DataFrame(predicts, columns=['Hogwarts House'])
        predicts = predicts['Hogwarts House'].apply(lambda x: house
                                                    if x else 'None')

        results = results.where(results['Hogwarts House'] != 'None',
                                predicts,
                                axis=0)

    results.to_csv('logistic_regression/results/houses.csv',
                   index=True,
                   index_label='Index')

    print(
        'Sorting hat predictions saved to logistic_regression/results/houses.csv'
    )


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        sys.exit('\nExiting...')
    except Exception as e:
        sys.exit(f'Error. {e}')
