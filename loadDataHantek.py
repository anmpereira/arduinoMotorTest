"""
This script can be used to load data from a hantek 6022BE save file into numpy arrays
"""
import numpy as np


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
    with open(r'testData\a.txt') as f:
        line_array = f.readlines()

        empty_lines = np.argwhere([i == '\n' for i in line_array]).flatten()
        header = line_array[:empty_lines[0]]
        size = int(header[2][6:-1])
        clock = convertToSeconds(header[1][7:-1])
        step = stepFromClock(clock)

        if len(line_array) > 2*size:
            # Two channels
            limits = empty_lines[0:2]
            ch1_y = np.array([float(i[:-1]) for i in line_array[limits[0]+1:limits[1]]])
            ch1_x = np.linspace(0, size*step, size)
        else:
            # Single channel
            pass


if __name__ == '__main__':
    loadFile(r'testData\a.txt')
