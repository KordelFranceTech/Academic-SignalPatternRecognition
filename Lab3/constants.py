# constants.py
# Kordel France
########################################################################################################################
# This file contains the specification for which file sizes, file types, and detection algorithms should be used for
#    analysis. These act as hyperparameters that may be edited to add / delete an analysis parameter.
########################################################################################################################

#characters that are acceptable as operands for the evaluation.
acceptable_chars = ['0','1']

# sorting file size
file_sizes = [50, 100, 500, 1000, 1500]
# pattern types
file_types = ['x', 'y', 'x and y']
# pattern sizes
pattern_sizes = [3, 5, 10, 20]
# notes
notes = ['required input',
         'required input',
         'required input',
         'required input',
         'required input',
         'excessive noise at beginning and end of S',
         'excessive noise at beginning of S',
         'excessive noise at end of S',
         'short sequence',
         'short sequence'
         ]
