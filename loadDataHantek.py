"""
This script can be used to load data from a hantek 6022BE save file into numpy arrays
"""
import numpy as np
import matplotlib.pyplot as plt


class FigureGridRegistry:
    fig_nr = 0

    def __init__(self):
        self._grid_on = {}

    def addFigure(self, fig_index):
        if fig_index in self._grid_on:
            pass
        else:
            self._grid_on[fig_index] = False

    def activateGrid(self, fig_index):
        self._grid_on[fig_index] = True

    def checkActiveGrid(self, fig_index):
        return self._grid_on[fig_index]


figure_registry = FigureGridRegistry()


def stepFromClock(clock: float) -> float:
    """
    Returns the time in seconds between samples, given a clock value in seconds
    The formula is 1/T, where T is the sampling frequency in Hz
    :param clock: clock value of the channel in seconds
    :return: float
    """

    if clock < 3e-6:  # from 1 to 2e-6 clock
        return 1/48e6
    elif clock < 7e-6:  # 5e-6 only
        return 1/16e6
    elif clock < 12e-6:  # 10e-6 only
        return 1/8e6
    elif clock < 22e-6:  # 20e-6 only
        return 1/4e6
    elif clock < 102e-3:  # 50e-6 to 100e-3
        return 1/1e6
    elif clock < 202e-3:  # 200e-3
        return 1/500e3
    elif clock < 502e-3:  # 500e-3
        return 1/200e3
    else:
        return 1/100e3


def convertToSeconds(string: str) -> float:
    number = float(''.join([i for i in string if not i.isalpha()]))
    prefix = ''.join([i for i in string if i.isalpha()])[0]

    if prefix.upper() == 'S':
        return number
    elif prefix.upper() == 'M':
        return number / 1e3
    elif prefix.upper() == 'U':
        return number / 1e6
    elif prefix.upper() == 'N':
        return number / 1e9


def loadFile(path: str):
    with open(path) as f:
        line_array = f.readlines()

        empty_lines = np.argwhere([i == '\n' for i in line_array]).flatten()
        header = line_array[:empty_lines[0]]
        size = int(header[2][6:-1])
        clock = convertToSeconds(header[1][7:-1])
        step = stepFromClock(clock)

        limits = empty_lines[0:2]
        ch1_y = np.array([float(i[:-1]) for i in line_array[limits[0]+1:limits[1]]])
        # noinspection PyUnresolvedReferences
        ch1_x = np.linspace(0, size*step, size)

        if len(line_array) > 2*size:
            # Two channels
            limits2 = empty_lines[3:5]
            ch2_y = np.array([float(i[:-1]) for i in line_array[limits2[0]+1:limits2[1]]])
            return (ch1_x, ch1_y), (ch1_x, ch2_y)

        else:
            # Single channel
            return (ch1_x, ch1_y),


def scopePlot(x: np.ndarray, y: np.ndarray, fig=-1, **kwargs):
    if fig == -1:
        fig = figure_registry.fig_nr
        figure_registry.fig_nr += 1
    else:
        pass
    plt.figure(fig)
    figure_registry.addFigure(fig)

    # noinspection PyTypeChecker
    xlabel = kwargs.setdefault('xlabel', None)
    ylabel = kwargs.setdefault('ylabel', None)
    label = kwargs.setdefault('label', None)
    title = kwargs.setdefault('title', None)

    plt.plot(x, y, label=label)

    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if title is not None:
        plt.title(title)

    if figure_registry.checkActiveGrid(fig):
        pass
    else:
        plt.grid()
        figure_registry.activateGrid(fig)

    plt.legend()
    plt.draw()


if __name__ == '__main__':
    ch1, ch2 = loadFile(r'testData\c.txt')

    scopePlot(ch1[0], ch1[1], 0, xlabel='Time (seconds)', ylabel='Reading (Volt)', label='Channel 1', title='DSO')
    scopePlot(ch2[0], ch2[1], 0, label='Channel 2')

    scopePlot(ch2[0], ch2[1]*ch1[1], 1, label='Multiplication', title='Power')

    scopePlot(ch1[1], ch2[1], 2, label='XY', title='XY plot')
