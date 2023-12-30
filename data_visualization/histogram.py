"""Data visualization - Histogram
"""
from os import sys, path
import matplotlib.pyplot as plt

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from dslr_extra.utils import getVisualData, parse_input


def printHistogram(houses_data: list, course: list) -> None:
    """Show a histogram of the selected course

        Parameters:
            houses_data (list): list of houses data
            course (list): list of courses
    """
    course_1 = course[0]
    houses_data_1 = houses_data[0]
    colors = ['red', 'green', 'yellow', 'blue']
    labels = ['Gryffindor', 'Slytherin', 'Hufflepuff', 'Ravenclaw']

    plt.figure(num='Histogram')
    plt.title(course_1)

    plt.hist(houses_data_1,
             label=labels,
             color=colors,
             alpha=0.6,
             histtype='bar',
             rwidth=0.8)

    plt.grid(alpha=0.2)
    plt.xlabel('Grade')
    plt.ylabel('# of Students')
    plt.legend()
    plt.show()


def main():
    """Main function
    """
    dataset = parse_input(1, ["dataset.csv"])
    houses_data, course = getVisualData(dataset, 1)
    printHistogram(houses_data, course)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        sys.exit('\nExiting...')
    except Exception as e:
        sys.exit(f'Error. {e}')
