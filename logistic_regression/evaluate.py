"""
Put these files in the same folder as `houses.csv` and `dataset_truth.csv`.

Usage:
    $ python evaluate.py
"""
import csv
import sys
import os.path

color_d = "\033[0m"
color_g = "\033[92m"
color_r = "\033[91m"


def load_csv(filename):
    """Load a CSV file and return a list with datas (corresponding to truths or
    predictions).
    """
    datas = []
    with open(filename, 'r', encoding='utf-8') as opened_csv:
        read_csv = csv.reader(opened_csv, delimiter=',')
        for line in read_csv:
            datas.append(line[1])
    # Clean the header cell
    datas.remove("Hogwarts House")
    return datas


if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))

    if os.path.isfile(f"{path}/results/dataset_truth.csv"):
        truths = load_csv(f"{path}/results/dataset_truth.csv")
    else:
        sys.exit("Error: missing dataset_truth.csv in the current directory.")
    if os.path.isfile(f"{path}/results/houses.csv"):
        predictions = load_csv(f"{path}/results/houses.csv")
    else:
        sys.exit("Error: missing houses.csv in the current directory.")

    count = 0
    if len(truths) == len(predictions):
        for i, truth in enumerate(truths):
            if truth == predictions[i]:
                count += 1
    score = float(count) / len(truths) * 100

    if score >= 98:
        print(f"{color_g}Your score on test set: {score:.2f}%")
        print(f"Good job! Mc Gonagall congratulates you {color_d}")
    else:
        print(f"{color_r}Your score on test set: {score:.2f}%")
        print(f"Too bad, Mc Gonagall flunked you.{color_d}")
