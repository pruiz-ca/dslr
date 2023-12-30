"""Data Visualization - Scatter Plot
"""
from os import sys, path
import matplotlib.pyplot as plt

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from dslr_extra.utils import getVisualData, parse_input


def printScatter(houses_data, courses):
    """Print a scatter plot of the two selected courses

        Parameters:
            houses_data (list): list of houses data
            courses (list): list of courses
    """
    colors = ['red', 'green', 'yellow', 'blue']
    labels = ['Gryffindor', 'Slytherin', 'Hufflepuff', 'Ravenclaw']
    houses_data_1, houses_data_2 = houses_data

    plt.figure(num='Scatter Plot')
    plt.title(courses[0] + ' vs ' + courses[1])

    griffindor = houses_data_1[0], houses_data_2[0]
    slytherin = houses_data_1[1], houses_data_2[1]
    hufflepuff = houses_data_1[2], houses_data_2[2]
    ravenclaw = houses_data_1[3], houses_data_2[3]

    plt.scatter(griffindor[0],
                griffindor[1],
                label=labels[0],
                color=colors[0],
                alpha=0.6)

    plt.scatter(slytherin[0],
                slytherin[1],
                label=labels[1],
                color=colors[1],
                alpha=0.6)

    plt.scatter(hufflepuff[0],
                hufflepuff[1],
                label=labels[2],
                color=colors[2],
                alpha=0.6)

    plt.scatter(ravenclaw[0],
                ravenclaw[1],
                label=labels[3],
                color=colors[3],
                alpha=0.6)

    plt.grid(alpha=0.2)
    plt.xlabel(courses[0])
    plt.ylabel(courses[1])
    plt.legend()
    plt.show()


def main():
    """"Main function
    """
    dataset = parse_input(1, ['dataset.csv'])
    houses_data, courses = getVisualData(dataset, 2)
    printScatter(houses_data, courses)


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        sys.exit('\nExiting...')
    except Exception as e:
        sys.exit(f'Error. {e}')
