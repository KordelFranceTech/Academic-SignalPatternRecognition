# file_manager.py
# Kordel France
########################################################################################################################
# This file provides public-accessible functions to generate trace runs and import data.
# Let it be emphasized that all data is automatically generated.
########################################################################################################################

import random
from Lab3.config import DEBUG_MODE
from Lab3.constants import acceptable_chars


def generate_single_signal_trace_run(x_length, s_length) -> [int]:
    """
    Generates an array of binary values of s_length with a pattern of x_legnth interwoven.
    :param x_length: the length of the pattern X array to generate.
    :param s_length: the length of the signal to generate.
    :return x_array, s_array: a signal s_array with its encoded pattern x_array
    """
    # intialize signal and pattern signal
    x_arr = []
    s_arr = []
    # determine random index to insert pattern signal into
    delta_length = s_length - x_length - 1
    # determine how much noise should be in S
    index_0 = random.randint(0, delta_length)

    if DEBUG_MODE:
        print(f'delta length: {delta_length}, index 0: {index_0}, index 1: {index_1}')

    # build the pattern signal
    for i in range(0, x_length):
        x_arr.append(random.randint(0, 1))
    # fill the master signal with noise until we encounter index to insert patten signal
    for i in range(0, index_0):
        s_arr.append(random.randint(0, 1))
    # insert pattern signal
    for i in range(index_0, index_0 + x_length):
        s_arr.append(x_arr[i - index_0])
    # fill the rest of the master signal with noise
    for i in range(index_0 + x_length, s_length):
        s_arr.append(random.randint(0,1))

    if DEBUG_MODE:
        print(f'\tx: {x_arr}\n\ts: {s_arr}')
        print(f'array length: {len(s_arr)}')

    # metric for operational cost
    op_count = x_length + index_0

    # return constructed arrays
    return x_arr, s_arr, op_count


def generate_dual_signal_trace_run(x_length, y_length, s_length) -> [int]:
    """
    Generates an array of binary values of s_length with a pattern of x_legnth interwoven.
    :param x_length: the length of the pattern X array to generate.
    :param y_length: the length of the pattern Y array to generate.
    :param s_length: the length of the signal to generate.
    :return x_array, y_array, s_array: a signal s_array with its encoded pattern x_array and y_array
    """
    # randomly determine which pattern gets inserted into S first - x or y
    seed = random.randint(0,1)
    # intialize signal and pattern signal
    x_arr = []
    y_arr = []
    s_arr = []
    # determine how much noise should be in S
    delta_length = s_length - x_length - y_length - 1

    # insert x first
    if seed == 0:
        # determine random index to insert pattern signal into
        index_0 = random.randint(0, delta_length)
        index_1 = random.randint(index_0, delta_length) + x_length
        if DEBUG_MODE:
            print(f'delta length: {delta_length}, index 0: {index_0}, index 1: {index_1}')
        # build the pattern signals
        for i in range(0, x_length):
            x_arr.append(random.randint(0, 1))
        for i in range(0, y_length):
            y_arr.append(random.randint(0, 1))
        # fill the master signal with noise until we encounter index to insert patten signal
        for i in range(0, index_0):
            s_arr.append(random.randint(0, 1))
        # insert x pattern signal
        for i in range(index_0, index_0 + x_length):
            s_arr.append(x_arr[i - index_0])
        # fill the master signal with noise until we encounter index to insert patten signal
        for i in range(index_0 + x_length, index_1):
            s_arr.append(random.randint(0, 1))
        # insert y pattern signal
        for i in range(index_1, index_1 + y_length):
            s_arr.append(y_arr[i - index_1])
        # fill the rest of the master signal with noise
        for i in range(index_1 + y_length, s_length):
            s_arr.append(random.randint(0, 1))
    # insert y first
    else:
        # determine random index to insert pattern signal into
        index_0 = random.randint(0, delta_length)
        index_1 = random.randint(index_0, delta_length) + y_length
        if DEBUG_MODE:
            print(f'delta length: {delta_length}, index 0: {index_0}, index 1: {index_1}')
        # build the pattern signals
        for i in range(0, x_length):
            x_arr.append(random.randint(0, 1))
        for i in range(0, y_length):
            y_arr.append(random.randint(0, 1))
        # fill the master signal with noise until we encounter index to insert patten signal
        for i in range(0, index_0):
            s_arr.append(random.randint(0, 1))
        # insert y pattern signal
        for i in range(index_0, index_0 + y_length):
            s_arr.append(y_arr[i - index_0])
        # fill the master signal with noise until we encounter index to insert patten signal
        for i in range(index_0 + y_length, index_1):
            s_arr.append(random.randint(0, 1))
        # insert x pattern signal
        for i in range(index_1, index_1 + x_length):
            s_arr.append(x_arr[i - index_1])
        # fill the rest of the master signal with noise
        for i in range(index_1 + x_length, s_length):
            s_arr.append(random.randint(0, 1))

    if DEBUG_MODE:
        print(f'\tx: {x_arr}\n\ty: {y_arr}\n\ts: {s_arr}')
        print(f'array length: {len(s_arr)}')

    # metric for operational cost
    op_count = index_1 + s_length

    # return constructed arrays
    return x_arr, y_arr, s_arr, op_count


def process_file_data(input_text_file):
    """
    Reads in and parses input files into the format of Tape object to be read by a DTM object.
    :param input_text_file: the name of the file to read in and process of type str
    :returns left_file_array: a list object containing the left-hand side of binary equation
    :returns right_file_array: a list object containing the right-hand side of binary equation
    """
    input_file = open(str(input_text_file), 'r')
    last_char = ''
    x_series = []
    y_series = []
    s_series = []
    x_seq = []
    y_seq = []
    s_seq = []
    x_filled = False
    y_filled = False
    s_filled = False

    # read the entire file into an array so it can be cleaned
    # clean the data as it is read
    while 1:
        # read in one character at a time as specified by Programming Assignment Guidelines
        single_char = input_file.read(1)
        # a bit of error handling - only accept certain values
        if single_char in acceptable_chars:
        # if single_char != '%':
            if not x_filled:
                x_seq.append(int(single_char))
            elif x_filled and not y_filled:
                y_seq.append(int(single_char))
            elif x_filled and y_filled and not s_filled:
                s_seq.append(int(single_char))

        # this indicates the separator between left and right sides of equation
        elif single_char == '\n':
            if not x_filled:
                x_filled = True
                x_series.append(x_seq)
                x_seq = []
            elif not y_filled:
                y_filled = True
                y_series.append(y_seq)
                y_seq = []
            elif not s_filled:
                # s_filled = True
                x_filled = False
                y_filled = False
                s_filled = False
                s_series.append(s_seq)
                s_seq = []
            else:
                continue
            continue
        # EOF found
        elif not single_char:
            x_series.append(x_seq)
            y_series.append(y_seq)
            s_series.append(s_seq)
            break
        # EOF found
        elif last_char == '\n' and single_char == '\n':
            x_series.append(x_seq)
            y_series.append(y_seq)
            s_series.append(s_seq)
            break
        else:
            continue
        last_char = single_char

    # close the processed file
    input_file.close()
    return x_series, y_series, s_series

