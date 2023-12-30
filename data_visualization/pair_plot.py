"""Data visualization - Pair Plot
"""
from os import sys, path
from textwrap import wrap
import matplotlib.pyplot as plt

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from dslr_extra.utils import getVisualData, parse_input


def subplotHistogram(plot, houses_data):
    """Subplot a histogram of the given data

        Parameters:
            plot (matplotlib.pyplot): plot to draw on
            houses_data (list): list of houses data
    """
    colors = ['red', 'green', 'yellow', 'blue']
    labels = ['Gryffindor', 'Slytherin', 'Hufflepuff', 'Ravenclaw']

    plot.hist(houses_data,
              label=labels,
              color=colors,
              alpha=0.6,
              histtype='bar',
              rwidth=0.8)


def subplotScatter(plot, houses_data_1, houses_data_2):
    """Subplot a scatter plot of the given data

        Parameters:
            plot (matplotlib.pyplot): plot to draw on
            houses_data_1 (list): list of houses data
            houses_data_2 (list): list of houses data
    """
    colors = ['red', 'green', 'yellow', 'blue']
    labels = ['Gryffindor', 'Slytherin', 'Hufflepuff', 'Ravenclaw']

    griffindor = houses_data_1[0], houses_data_2[0]
    slytherin = houses_data_1[1], houses_data_2[1]
    hufflepuff = houses_data_1[2], houses_data_2[2]
    ravenclaw = houses_data_1[3], houses_data_2[3]

    plot.scatter(griffindor[0],
                 griffindor[1],
                 label=labels[0],
                 color=colors[0],
                 alpha=0.6,
                 s=0.5)

    plot.scatter(slytherin[0],
                 slytherin[1],
                 label=labels[1],
                 color=colors[1],
                 alpha=0.6,
                 s=0.5)

    plot.scatter(hufflepuff[0],
                 hufflepuff[1],
                 label=labels[2],
                 color=colors[2],
                 alpha=0.6,
                 s=0.5)

    plot.scatter(ravenclaw[0],
                 ravenclaw[1],
                 label=labels[3],
                 color=colors[3],
                 alpha=0.6,
                 s=0.5)


def printPairPlot(houses_raw_data, courses):
    """Generate all the subplots for the pair plot

        Parameters:
            houses_raw_data (list): list of houses data
            courses (list): list of courses
    """
    griffindor = houses_raw_data[0]
    slytherin = houses_raw_data[1]
    hufflepuff = houses_raw_data[2]
    ravenclaw = houses_raw_data[3]

    courses = courses.to_list()
    plots_num = len(courses)
    fig, axs = plt.subplots(plots_num, plots_num, figsize=(10, 10))

    for course_1 in courses:
        x = courses.index(course_1)
        for course_2 in courses:
            y = courses.index(course_2)

            if course_1 == course_2:
                data = [
                    griffindor[course_1], slytherin[course_1],
                    hufflepuff[course_1], ravenclaw[course_1]
                ]

                subplotHistogram(axs[x, y], data)
            else:
                data_1 = [
                    griffindor[course_1], slytherin[course_1],
                    hufflepuff[course_1], ravenclaw[course_1]
                ]

                data_2 = [
                    griffindor[course_2], slytherin[course_2],
                    hufflepuff[course_2], ravenclaw[course_2]
                ]

                subplotScatter(axs[x, y], data_1, data_2)

            axs[x, y].xaxis.set_ticklabels([])
            axs[x, y].yaxis.set_ticklabels([])

            if x == plots_num - 1:
                label = '\n'.join(wrap(course_2, 10))
                axs[x, y].set_xlabel(label, fontsize=7)
            if y == 0:
                label = '\n'.join(wrap(course_1, 10))
                axs[x, y].set_ylabel(label, fontsize=7)

    fig.canvas.manager.set_window_title('Pair Plot')
    plt.tight_layout()
    plt.legend()
    plt.show()


def main():
    """Main function
    """
    dataset = parse_input(1, ["dataset.csv"])
    houses_data, courses = getVisualData(dataset, 0)
    printPairPlot(houses_data, courses)


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        sys.exit('\nExiting...')
    except Exception as e:
        sys.exit(f'Error. {e}')
