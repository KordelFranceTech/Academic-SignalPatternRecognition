# algorithm.py
# Kordel France
########################################################################################################################
# This file contains the specification for the signal processing algorithm along with some helper methods. Primarily,
# this file facilitates the construction of a state machine that detects desired patterns in a transmission signal.
########################################################################################################################

import time

from Lab3.constants import acceptable_chars as acceptable_chars
from Lab3.config import DEBUG_MODE


# global counters that keep track of performance and some detection operations
X_START = False
X_INDEX = 0
X_MAX = 0
X_SCAN = True
X_OUT = []
X_FOUND = False

Y_START = False
Y_INDEX = 0
Y_MAX = 0
Y_SCAN = True
Y_OUT = []
Y_FOUND = False

INDEX = 0

def reset_counts_for_detection_metrics():
    """
    Resets the global counters used for metrics and pattern recognition within the
    detection algorithm.
    :return: null
    """
    global X_START
    global X_INDEX
    global X_MAX
    global X_SCAN
    global X_CAN_END
    global X_END
    global X_OUT
    global X_TERMINATE
    global X_FOUND

    global Y_START
    global Y_INDEX
    global Y_MAX
    global Y_SCAN
    global Y_CAN_END
    global Y_END
    global Y_OUT
    global Y_TERMINATE
    global Y_FOUND
    global INDEX

    X_START = False
    X_INDEX = 0
    X_MAX = 0
    X_SCAN = True
    X_CAN_END = False
    X_END = False
    X_OUT = []
    X_TERMINATE = True
    X_FOUND = False

    Y_START = False
    Y_INDEX = 0
    Y_MAX = 0
    Y_SCAN = True
    Y_CAN_END = False
    Y_END = False
    Y_OUT = []
    Y_TERMINATE = True
    Y_FOUND = False

    INDEX = 0


def signal_detection_driver(x_seq, y_seq, s_seq):
    """
    Constructs the pattern detection algorithm and feeds data as needed. Also monitors metrics on
    performance..
    :param x_seq: the X pattern to detect within the signal S.
    :param y_seq: the Y pattern to detect within the signal S.
    :param s_seq: the signal S to analyze for patterns X and Y.
    :return x_found, y_found, end_index, op_count, time: metrics revealing the success of the algorithm and its cost.
    """
    # init timer
    start_time = time.time()
    # declare flags to indicate if x and y patterns found
    global X_FOUND
    global Y_FOUND

    # indicates when to stop searching
    s_max = len(s_seq)
    # local variable indicating if X found
    x_found = False
    # local variable indicating if y found
    y_found = False
    # holds metrics for ending index
    indices = []
    # holds metrics for cost counters
    counters = []
    # final ending index
    end_index = 0
    # final cost count
    op_count = 0
    both = False

    # flag indicating excessive noise in signal
    NOISE_FLAG = False

    # check for excessive noise
    noise_counter = 0
    for i in range(1, s_max):
        if s_seq[i] == 0 and s_seq[i - 1] == 0:
            noise_counter += 1
        else:
            noise_counter = 0

    # if excessive noise encountered, set the flag
    if noise_counter > X_MAX or noise_counter > Y_MAX:
        NOISE_FLAG = True

    # traverse through the signal and begin detection
    for i in range(0, s_max):
        # feed the signal to the pattern recognition algorithm and receive metrics
        x0, y0, index0, counter0 = build_dtm_to_recognize_dual_pattern(x_seq, y_seq, s_seq[i:])
        # x and y patterns both found, stop searching
        if x0 and y0 and not both:
            both = True
            x_found = True
            y_found = True
            break

        # x found, set the flag
        if not x_found:
            x_found = x0

        # y found, set the flag
        if not y_found:
            y_found = y0

        # add the metrics
        indices.append(index0)
        counters.append(counter0)

        # feed the reverse signal to the pattern recognition algorithm and receive metrics
        y1, x1, index1, counter1 = build_dtm_to_recognize_dual_pattern(y_seq, x_seq, s_seq[i:])
        # x and y patterns both found, stop searching
        if x1 and y1 and not both:
            both = True
            x_found = True
            y_found = True
            break

        # x found, set the flag
        if not x_found:
            x_found = x1

        # y found, set the flag
        if not y_found:
            y_found = y1
        if x_found and y_found:
            break

        # add the metrics
        indices.append(index1)
        counters.append(counter1)

    if DEBUG_MODE:
        if both:
            print(f'x and y found together')
        if x_found:
            print(f'x found')
        if y_found:
            print(f'y found')

    # stop the timer and calculate delta
    end_time = time.time()
    delta_time = end_time - start_time

    # final costs are maximium of acquired costs
    end_index += max(indices) + 1 if len(indices) > 0 else len(x_seq) + len(y_seq)
    op_count += max(counters) + 1 if len(counters) > 0 else len(x_seq) + len(y_seq)

    # return the results
    return x_found, y_found, end_index, op_count, "{:.6f}".format(delta_time), NOISE_FLAG


def build_dtm_to_recognize_single_pattern(x_seq, s_seq):

    global X_INDEX
    global X_MAX
    global X_SCAN
    global X_OUT
    global X_FOUND
    global INDEX

    X_INDEX = 0
    X_MAX = 0
    X_SCAN = True
    X_OUT = []

    STATE = 0
    X0_FOUND = False
    X_MAX = len(x_seq)
    COUNTER = 0
    INDEX = 0

    for i in range(0, len(s_seq)):
        if s_seq[i] == x_seq[X_INDEX] and X_SCAN and X_INDEX < X_MAX and Y_SCAN and STATE == 0:
            # print('block 1')
            STATE = 10
            X_OUT.append(x_seq[X_INDEX])
            if X_INDEX < X_MAX - 1:
                X_INDEX += 1
        elif s_seq[i] == x_seq[X_INDEX] and X_SCAN and X_INDEX < X_MAX and STATE == 10:
            # print('block 2')
            X_OUT.append(x_seq[X_INDEX])
            if X_INDEX < X_MAX - 1:
                X_INDEX += 1
        elif s_seq[i] == x_seq[X_INDEX] and X_SCAN and X_INDEX < X_MAX and STATE == 20:
            # print('block 5')
            X_OUT.append(x_seq[X_INDEX])
            if X_INDEX < X_MAX - 1:
                X_INDEX += 1
        elif s_seq[i] == x_seq[X_INDEX] and X_SCAN and Y_SCAN and Y_INDEX < Y_MAX and STATE == 20:
            # print('block 7')
            STATE = 10
            X_OUT.append(x_seq[X_INDEX])
            if X_INDEX < X_MAX - 1:
                X_INDEX += 1
        else:
            # print('block 12')
            STATE = 0
            X_INDEX = 0
            X_OUT = []
            COUNTER = 0

        INDEX = i
        if STATE != 0:
            COUNTER += 1

        X_SCAN = check_for_termination(X_OUT, x_seq)

        if DEBUG_MODE:
            print(f'\n\niteration {i}, state: {STATE}')
            print(f'\tfull s sequence: {s_seq}\n\t\tcurrent s value: {s_seq[i]}')
            print(f'\t\tfull x sequence: {x_seq}')
            print(f'\t\tx index: {X_INDEX}')
            print(f'\t\tread-in x values: {X_OUT}')

        if not X_SCAN:
            if DEBUG_MODE:
                print('###########FOUND BOTH')
                print(f'\n\nfound x:\n\tX_OUT: {X_OUT}')
                print(f'\n\nfound y:\n\tY_OUT: {Y_OUT}')
            X_FOUND = True if not X_FOUND else False
            return True, i, COUNTER

    return X0_FOUND, Y0_FOUND, INDEX, COUNTER


def build_dtm_to_recognize_dual_pattern(x_seq, y_seq, s_seq):
    """
    Constructs the pattern detection algorithm and feeds data as needed. Also monitors metrics on
    performance..
    :param x_seq: the X pattern to detect within the signal S.
    :param y_seq: the Y pattern to detect within the signal S.
    :param s_seq: the signal S to analyze for patterns X and Y.
    :return x_found, y_found, end_index, op_count: metrics revealing the success of the algorithm and its cost.
    """
    # declare global parameters that hold cost, index, and performance data
    global X_INDEX
    global X_MAX
    global X_SCAN
    global X_OUT
    global X_FOUND

    global Y_INDEX
    global Y_MAX
    global Y_SCAN
    global Y_OUT
    global Y_FOUND
    global INDEX

    # reset the global properties to allow for new algorithmic run
    # tracks which index of X has been satisfied
    X_INDEX = 0
    X_MAX = 0
    # tracks whether scanning for detection has started
    X_SCAN = True
    # holds detected x values as a sequence
    X_OUT = []

    # tracks which index of Y has been satisfied
    Y_INDEX = 0
    Y_MAX = 0
    # tracks whether scanning for detection has started
    Y_SCAN = True
    # holds detected y values as a sequence
    Y_OUT = []

    # declare flags to indicate if x and y patterns found
    # maintains state of the DTM
    STATE = 0
    # local flag for X pattern found
    X0_FOUND = False
    # local flag for Y pattern found
    Y0_FOUND = False
    # max length of X pattern
    X_MAX = len(x_seq)
    # max length of Y pattern
    Y_MAX = len(y_seq)
    # cost counter
    COUNTER = 0
    # ending index
    INDEX = 0

    # iterate through transmission signal S
    for i in range(0, len(s_seq)):

        # define each state with its "rules"
        if s_seq[i] == x_seq[X_INDEX] and X_SCAN and X_INDEX < X_MAX and Y_SCAN and STATE == 0:
            # print('block 1')
            STATE = 10
            X_OUT.append(x_seq[X_INDEX])
            if X_INDEX < X_MAX - 1:
                X_INDEX += 1
        elif s_seq[i] == x_seq[X_INDEX] and X_SCAN and X_INDEX < X_MAX and STATE == 10:
            # print('block 2')
            X_OUT.append(x_seq[X_INDEX])
            if X_INDEX < X_MAX - 1:
                X_INDEX += 1
        elif s_seq[i] == y_seq[Y_INDEX] and Y_SCAN and Y_INDEX < Y_MAX and STATE == 10:
            # print('block 3')
            STATE = 20
            Y_OUT.append(y_seq[Y_INDEX])
            if Y_INDEX < Y_MAX - 1:
                Y_INDEX += 1
        elif s_seq[i] == y_seq[Y_INDEX] and Y_SCAN and Y_INDEX < Y_MAX and STATE == 20:
            # print('block 4')
            Y_OUT.append(y_seq[Y_INDEX])
            if Y_INDEX < Y_MAX - 1:
                Y_INDEX += 1
        elif s_seq[i] == x_seq[X_INDEX] and X_SCAN and X_INDEX < X_MAX and STATE == 20:
            # print('block 5')
            X_OUT.append(x_seq[X_INDEX])
            if X_INDEX < X_MAX - 1:
                X_INDEX += 1
        elif s_seq[i] == y_seq[Y_INDEX] and Y_SCAN and Y_INDEX < Y_MAX and STATE == 20:
            # print('block 6')
            STATE = 20
            X_OUT.append(x_seq[X_INDEX])
            if Y_INDEX < Y_MAX - 1:
                Y_INDEX += 1
        elif s_seq[i] == x_seq[X_INDEX] and X_SCAN and Y_SCAN and Y_INDEX < Y_MAX and STATE == 20:
            # print('block 7')
            STATE = 10
            X_OUT.append(x_seq[X_INDEX])
            if X_INDEX < X_MAX - 1:
                X_INDEX += 1
        elif s_seq[i] == y_seq[Y_INDEX] and not X_SCAN and Y_INDEX < Y_MAX and STATE == 10:
            # print('block 8')
            STATE = 20
            Y_OUT.append(y_seq[Y_INDEX])
            if Y_INDEX < Y_MAX - 1:
                Y_INDEX += 1
        elif s_seq[i] == y_seq[Y_INDEX] and not X_SCAN and Y_INDEX < Y_MAX:
            # print('block 9')
            STATE = 20
            Y_OUT.append(y_seq[Y_INDEX])
            if Y_INDEX < Y_MAX - 1:
                Y_INDEX += 1
        elif not X_SCAN:
            # print('block 10')
            STATE = 0
            Y_INDEX = 0
            Y_OUT = []
        elif not Y_SCAN:
            # print('block 11')
            STATE = 0
            X_INDEX = 0
            X_OUT = []
        else:
            # print('block 12')
            STATE = 0
            X_INDEX = 0
            Y_INDEX = 0
            X_OUT = []
            Y_OUT = []

        # set ending index for performance metric
        INDEX = i
        # increment the cost counter if value is not noise
        if STATE != 0:
            COUNTER += 1

        # check if the full X pattern has been found
        X_SCAN = check_for_termination(X_OUT, x_seq)
        # check if the full Y pattern has been found
        Y_SCAN = check_for_termination(Y_OUT, y_seq)

        if DEBUG_MODE:
            print(f'\n\niteration {i}, state: {STATE}')
            print(f'\tfull s sequence: {s_seq}\n\t\tcurrent s value: {s_seq[i]}')
            print(f'\t\tfull x sequence: {x_seq}')
            print(f'\t\tx index: {X_INDEX}')
            print(f'\t\tread-in x values: {X_OUT}')
            print(f'\tfull y sequence: {y_seq}')
            print(f'\t\ty index: {Y_INDEX}')
            print(f'\t\tread-in y values: {Y_OUT}')

        # we are no longer scanning for x nor y since they were both found
        # set properties and return
        if not X_SCAN and not Y_SCAN:
            if DEBUG_MODE:
                print('###########FOUND BOTH')
                print(f'\n\nfound x:\n\tX_OUT: {X_OUT}')
                print(f'\n\nfound y:\n\tY_OUT: {Y_OUT}')
            X_FOUND = True if not X_FOUND else False
            Y_FOUND = True if not Y_FOUND else False
            return True, True, i, COUNTER

        # haven't found x pattern yet, still scanning for it
        elif not X_SCAN:
            if DEBUG_MODE:
                print(f'\n\nfound x:\n\tX_OUT: {X_OUT}')
            X0_FOUND = True
            # break

        # haven't found y pattern yet, still scanning for it
        elif not Y_SCAN:
            if DEBUG_MODE:
                print(f'\n\nfound y:\n\tY_OUT: {Y_OUT}')
            Y0_FOUND = True
            # break

    # return if x or y were found, the ending index of detection, and the cost counter
    return X0_FOUND, Y0_FOUND, INDEX, COUNTER



def check_for_termination(base_signal, comp_signal) -> bool:
    """
    Checks to see if a given array is equal to another array.
    :param base_signal: the signal to compare to.
    :param comp_signal: the signal to compare against the base_signal for equality.
    :return terminate: whether or not the detection algorithm should terminate because the
    signals are equal, so the pattern was found.
    """
    # if signals aren't of same length, they aren't equal
    if len(base_signal) != len(comp_signal):
        return True

    # otherwise check each value of the signal against the other
    for i in range(0, len(comp_signal)):
        if base_signal[i] != comp_signal[i]:
            return True
    return False


def process_file_data(input_text_file):
    """
    Reads in and parses input files into the format of Tape object to be read by a DTM object.
    :param input_text_file: the name of the file to read in and process of type str
    :return x_seq, y_seq, s_seq: a signal S with its encoded patterns X and Y
    """
    input_file = open(str(input_text_file), 'r')
    last_char = ''
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
        print(single_char)

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
            elif not y_filled:
                y_filled = True
            elif not s_filled:
                s_filled = True
            else:
                continue
            continue
        # EOF found
        elif not single_char:
            break
        # EOF found
        elif last_char == '\n' and single_char == '\n':
            break
        else:
            continue
        last_char = single_char

    # close the processed file
    input_file.close()
    return x_seq, y_seq, s_seq


# x_seq, y_seq, s_seq = process_file_data('RequiredInputProj3.txt')
# recognize_pattern_v8(x_seq, y_seq, s_seq)

# signal_detection_driver(x_seq, y_seq, s_seq)
