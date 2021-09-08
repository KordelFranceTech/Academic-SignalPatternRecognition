#__main__.py
# Kordel France
########################################################################################################################
# This file contains the driver code for the signal detection program.
# All other files may be viewed as helpers that are pooled together here for use.
########################################################################################################################

from Lab3.constants import file_sizes, file_types, pattern_sizes, notes
from Lab3.file_manager import generate_single_signal_trace_run, generate_dual_signal_trace_run, process_file_data
from Lab3 import graph_data as graph
from Lab3.algorithm import signal_detection_driver, reset_counts_for_detection_metrics
from Lab3.Metric import Metric as m
import time
import sys

sys.setrecursionlimit(10**7)

data_metrics = []
status = len(file_sizes) * len(file_types)
status_count = 0
# print a header for UI aesthetics
print('_________________________________________________________________________________________')
print('_________________________________________________________________________________________')
print('_________________________________________________________________________________________')
print('\t\t\t\t\tWelcome')
print('*****************************************************************************************')
print('*****************************************************************************************')


# briefly pause processing so the user can read the feedback given to them in the command prompt
time.sleep(2.0)
print('*****************************************************************************************')
print('\t\t\tStarting Signal Detection Program\n')
print('_________________________________________________________________________________________')
time.sleep(2.0)
print('\t\t\tAnalyzing required correction runs\n')

# import the project required input data for correctness runs
x_series, y_series, s_series = process_file_data('Lab3/RequiredInputProj3.txt')

# iterate over the data to set up detection of the signal
for i in range(0, len(s_series)):
    print('_________________________________________________________________________________________')
    x_signal = x_series[i]      # the X sub-signal to find within S
    y_signal = y_series[i]      # the Y sub-signal to find within S
    s_signal = s_series[i]      # the transmission signal to analyze

    # start the detection algorithm
    detect_x, detect_y, comps, exs, dt, noise_flag = signal_detection_driver(x_signal, y_signal, s_signal)
    print(f'\n{i + 1}  Performing correctness run for purpose: {notes[i]}')
    print(f'\tThe following signal is being scanned: {s_signal}')
    print(f'\tThe signal is being scanned for the following patterns X and Y:')
    print(f'\t\tpattern X: {x_signal}')
    print(f'\t\tpattern Y: {y_signal}')
    time.sleep(0.5)
    print('\t\tperforming scan...')
    time.sleep(0.5)

    # if there isn't excessive noise
    if not noise_flag:
        # if one of the signal patterns were found, tell the user
        if detect_x:
            print(f'\t\t\tX signal was detected within the transmission signal')
        if detect_y:
            print(f'\t\t\tY signal was detected within the transmission signal')
        if detect_x or detect_y:
            print(f'\t\t\t{exs} operations were performed in order to detect both signals')
            print(f'\t\t\tsignal to noise ratio (SNR) = {(len(x_signal) + len(y_signal)) / len(s_signal)}')
    else:
        print('\t***********excessive noise detected in signal**********')
        # if one of the signal patterns were found, tell the user
        if detect_x:
            print(f'\t\t\tX signal was detected within the transmission signal')
        if detect_y:
            print(f'\t\t\tY signal was detected within the transmission signal')
        if detect_x or detect_y:
            print(f'\t\t\t{exs} operations were performed in order to detect both signals')
            print(f'\t\tsignal to noise ratio (SNR) = {(len(x_signal) + len(y_signal)) / len(s_signal)}')

    # otherwise let the user know that no signal patterns were found
    if not detect_x and not detect_y:
        print(f'\t\t\tNeither pattern X nor pattern Y could be detected within the transmission signal')
    time.sleep(2.0)


# correctness runs are complete, now start generating cost runs
print('_________________________________________________________________________________________')
print('_________________________________________________________________________________________')
print('Now trace runs will be generated and analyzed')
time.sleep(2.0)
# inform the user of what will be accomplished by and presented in this program
print(f'A total of {len(file_types) * len(file_sizes) * len(pattern_sizes)} different analyses will be performed on '
      f'different sorting scenarios.')
print(f'\t{len(pattern_sizes)} different sizes of sub-sequences for X and Y will be compared: {[pattern for pattern in pattern_sizes]}.')
print(f'\t{len(file_sizes)} different file sizes will be compared for each sort: {[size for size in file_sizes]}.')
print(f'\t{len(file_types)} different signals will be analyzed - signals only containing X, signals only containing Y, '
      f'signals containing both X and Y: {[type for type in file_types]}.')

# briefly pause processing so the user can read the feedback given to them in the command prompt
time.sleep(7.0)
print(f'\n\nBeginning trace runs now.')
time.sleep(2.0)
print('_________________________________________________________________________________________')

# begin automatically generating and distributing the data to its respective algorithm
for size in file_sizes:
    # iterate through file sizes (n)
    for file_type in file_types:
        # iterate through file types
        for pattern in pattern_sizes:
            # check for file type
            if file_type == 'x':
                # the pattern of interest cannot exceed size of S
                if pattern < size:
                    # get an auto generated signal containing X pattern of length m
                    x_signal_3p, y_signal_3p, signal_3p, op_count = generate_dual_signal_trace_run(pattern, 1, size)
                    # run the detection algorithm on the generated data and receive the metrics
                    detect_x3p, detect_y3p, comps_3p, exs_3p, dt_3p, noise = signal_detection_driver(x_signal_3p, y_signal_3p, signal_3p)
                    # create a metric object
                    metric_3p = m(n=int(size),
                                  pattern=str(file_type),
                                  m=pattern,
                                  comps=op_count,
                                  exs=exs_3p,
                                  predata=signal_3p,
                                  x_signal=x_signal_3p,
                                  y_signal=y_signal_3p,
                                  comp_eq='',
                                  ex_eq='',
                                  time=str(dt_3p),
                                  snr=(len(x_signal_3p) + len(y_signal_3p)) / len(signal_3p))
                    data_metrics.append(metric_3p)
                    # reset the global counters
                    reset_counts_for_detection_metrics()

            # check for file type
            elif file_type == 'y':
                # the pattern of interest cannot exceed size of S
                if pattern < size:
                    # get an auto generated signal containing X pattern of length m
                    x_signal_3p, y_signal_3p, signal_3p, op_count = generate_dual_signal_trace_run(1, pattern, size)
                    # run the detection algorithm on the generated data and receive the metrics
                    detect_x3p, detect_y3p, comps_3p, exs_3p, dt_3p, noise = signal_detection_driver(x_signal_3p, y_signal_3p, signal_3p)
                    # create a metric object
                    metric_3p = m(n=int(size),
                                  pattern=str(file_type),
                                  m=pattern,
                                  comps=op_count,
                                  exs=exs_3p,
                                  predata=signal_3p,
                                  x_signal=x_signal_3p,
                                  y_signal=y_signal_3p,
                                  comp_eq='',
                                  ex_eq='',
                                  time=str(dt_3p),
                                  snr=(len(x_signal_3p) + len(y_signal_3p)) / len(signal_3p))
                    data_metrics.append(metric_3p)
                    # reset the global counters
                    reset_counts_for_detection_metrics()

            # check for file type
            elif file_type == 'x and y':
                # the pattern of interest cannot exceed size of S                                                   # check for sorted file type
                if (2 * pattern) < size:
                    # get an auto generated signal containing X pattern of length m
                    x_signal_3p, y_signal_3p, signal_3p, op_count = generate_dual_signal_trace_run(pattern, pattern, size)
                    # run the detection algorithm on the generated data and receive the metrics
                    detect_x3p, detect_y3p, comps_3p, exs_3p, dt_3p, noise = signal_detection_driver(x_signal_3p, y_signal_3p, signal_3p)
                    # create a metric object
                    metric_3p = m(n=int(size),
                                  pattern=str(file_type),
                                  m=pattern,
                                  comps=op_count,
                                  exs=exs_3p,
                                  predata=signal_3p,
                                  x_signal=x_signal_3p,
                                  y_signal=y_signal_3p,
                                  comp_eq='',
                                  ex_eq='',
                                  time=str(dt_3p),
                                  snr=(len(x_signal_3p) + len(y_signal_3p)) / len(signal_3p))
                    data_metrics.append(metric_3p)
                    # reset the global counters
                    reset_counts_for_detection_metrics()

        # logic for presenting status of trace run build back to user
        status_count += 1                                                             # print status as % completion
        print(f'{str(round(100.00 * float(status_count / status), 2))} % complete.\t\t\t'
              f'Finished analysis of {file_type} data for size {size}.')
        time.sleep(0.1)                                                               # briefly pause for visual effect
print('_________________________________________________________________________________________')

# all trace runs are complete
# now present the results and performance metrics to the user
# inform them of what is to come
print(f'\n\nPresenting results of analysis now.\nA final summary will follow a series of performance graphs.')
time.sleep(5.0)

# process data for graphing, saving, and printing
graph.stratify_data(data_metrics)
print('*****************************************************************************************')
print('*****************************************************************************************')

# graphing complete, now build and write the performance summary
print(f'\nSummary of all {len(file_types) * len(file_sizes) * len(pattern_sizes)} analyzed sorting runs:')
print('_________________________________________________________________________________________')
graph.present_and_save_summary()

# inform user to check 'output_files' folder for a thorough archive of the analysis
print(f'\nA copy of the table above along with individual .csv files for each of the '
      f'{len(file_types) * len(file_sizes) * len(pattern_sizes)} trace runs may be found in the `output_files` folder.')
print('____________________________________________________________________________________________'
      '____________________________________________________________________________________________\n\n')




