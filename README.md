# FranceLab 3 - Kordel K. France

This project was constructed for the Foundations of Algorithms course, 605.621 section 83, instructed by Dr. Eleanor Chlan at Johns
Hopkins University. The project performs recognition of patterns in a binary signal.

**Quick Look**
- Correctness runs are evaluated first in program execution, including the required project input. Cost runs are evaluated after.
#
- 5 different signals `S` of lengths  n = 50, 100, 500, 1000, and 1500 are processed for the detection of `X` and `Y` patterns
of different sizes. The size of the detection pattern is referred to as `m` such that a `3-pattern` signal is an `X` or `Y`
signal containing only 3 elements, i.e. `[0,1,1]`. So `S` will be detecting an `X` or `Y` of size `m`.
#
- Each of 3 different signal types are evaluated: signals that contain only an `X` signal pattern, signals that contain 
only a `Y` signal pattern, and signals that contain both `X` and `Y` patterns.
#
- Each of 5 different values of `n` are analyzed over each of the 3 file types for four different values of `m` resulting 
in 60 different cost runs that are evaluated.
#
- The file `Metric.py` contains an object that stores details and performance characteristics about each run. Think of
one `Metric` object as one run.
#
- The file `file_manager.py` contains functions that generate all of the data files automatically.
#
- The file `constants.py` contains all of the sorting parameters - file sizes (signal lengths), pattern lengths of `X`
and `Y`, and data types as defined in the assignment requirements.
#
- Each of the sorting algorithms contains its own file. Each of the sorting algorithms uses recursion, not iteration.
#
- `algorithm.py` contains the state machine that runs the detection algorithm and scans the transmission signal.
#

***Note to Graders:*** For the required output files, I figured it was easier to open and read a `.csv` file of the data run
instead of analyzing it from the console. Files are named as `{algorithm_name}-{date_type}-{n}count.csv` such that the
50-count transmission signal `S` being scanned for a 5-count `X` and `Y` pattern is named as `5-pattern_x and y__50count.csv`. 
Hopefully this is easier; reading from the console seemed like a nightmare.

Required input files are hard coded in `constants.py` and saved as `{algorithm_name}-{data_type}-50count.csv`.


## Running FranceLab3
1. **Ensure Python 3.7 is installed on your computer.**

2. **Navigate to the Lab3 directory.** For example, `cd User\Documents\PythonProjects\Lab3`.
Do NOT `cd` into the `Lab3` module.

3. **Run the program as a module: `python -m Lab3 -h`.** This will print the help message.

4. **Run the program as a module (with no inputs): `python -m Lab3`.** All data is automatically generated; there is no 
need to pass in any inputs / arguments.

5. **Monitor the program as it performs the analysis.** The program will output a status and metrics to the screen as 
computation is performed.

6. **Plots of all of the data runs will appear.** Once calculation is completed, the program displays the cost
 and trajectory of each algorithm through line graphs. Do dismiss the plot and move to the next plot, simply 
 enter any key into the command prompt. One plot for each of the 3 data types will appear.

7. **View the Summary Table and Output Files.** A summary table illustrating the performance of all cost runs is presented
on the screen. An output file of each run can be found in the `output_files` directory. Each of these files 
contains the following details: 
        1) signal type
        2) signal length
        3) the pattern type
        4) number of operations performed
        5) ending index of the last detected pattern 
        6) an equation that plots the trajectory of the number of operations made by the algorithm over this data type as
     `n` scales along with the correlation coefficient between the equation and the observed data.
        7)  an equation that plots the trajectory of the ending index seen by the algorithm over this data type as
     `n` scales along with the correlation coefficient between the equation and the observed data.
        8) the initial transmission signal `S` to be analyzed
        9) the `X` pattern signal
        10) the `Y` pattern signal
        11) the execution time (in seconds) for the algorithm to detect the patterns if found
        12) the signal to noise ratio of the signal
        
8. **Open `output_files/FINAL_ANALYSIS.csv`.** This file contains a direct copy of the `Summary` table in the output but
as an archived `.csv` file.

### FranceLab3 Usage

```commandline
usage: python -m Lab3

positional arguments:
  none

optional arguments:
  none
```
Copy the output below and paste into the command line as a quick start:
```buildoutcfg
python -m Lab3
```

### Project Layout

Here is how the project is structured and organized.

* FranceLab3: `The parent folder of the project. This should be the last subdirectory you navigate to to run the
project.`
    * README.md:
      `A guide on what the project does, how to run the project.`
      
    * Lab3: 
      `This is the module of the entire program package. It is not a directory. Do not navigate into it.`
      
      * __init__.py 
        `As the name suggests, this file initializes the program and gives access to the algorithms capabilities
        to other programs.`
        
      * __main__.py 
        `This file contains the driver code for the signal detection  program. All other files may be viewed 
        as helpers that are pooled together here for use.`
        
      * **algorithm.py** 
        `This file contains the detection algorithm and several global properties used to diagnose performance of the
        algorithm and whether or not the X and Y patterns were detected in the transmission signal S.`
        
      * **file_manager.py** 
        `This file provides public-accessible functions to auto-generate data for cost runs and read input data. 
        Each function returns an array of it's designated distribution. Let it be emphasized that all data is 
        automatically generated.`

      * **constants.py**
        `This file contains the specification for which file sizes, file types, and pattern sizes should be used for
        analysis. These act as hyperparameters that may be edited to add / delete an analysis parameter.`

      * **graph_data.py**
        `This file provides functions to categorize, filter, graph, and save analyzed cost data.
        The data is first categorized by data type and algorithm, then graphed and saved, and finally summarized.
`
      * **Metric.py**
        `This file specifies an object used to illustrate the performance of the detection algorithm.`

###Enhancements
   There are several enhancements for this project. The analysis document has a more comprehensive list, but here are
   highlights for a few:
   
   * Time Delays - processing is paused briefly throughout the program to allow the user time to read and interpret the
   output. This creates for a much better user experience.
   
   
   * Execution time is tracked and monitored for each  algorithm.
   
   * Each run is graphed in a `.csv` file. Files are named as `{algorithm_name}-{date_type}-{n}count.csv` such that the
    50-count transmission signal `S` being scanned for a 5-count `X` and `Y` pattern is named as `5-pattern_x and y_50count.csv`.
    Each file is located in the `output_files` directory and contains the following 
    properties:
    
        1) signal type
        2) signal length
        3) the pattern type
        4) number of operations performed
        5) ending index of the last detected pattern 
        6) an equation that plots the trajectory of the number of operations made by the algorithm over this data type as
     `n` scales along with the correlation coefficient between the equation and the observed data.
        7)  an equation that plots the trajectory of the ending index seen by the algorithm over this data type as
     `n` scales along with the correlation coefficient between the equation and the observed data.
        8) the initial transmission signal `S` to be analyzed
        9) the X pattern signal
        10) the Y pattern signal
        11) the execution time (in seconds) for the algorithm to detect the patterns if found
        12) the signal to noise ratio of the signal
    
   * A `Summary Table` is provided at the very end of the program that shows the performance of each algorithm over 
   different data distributions. A `FINAL_ANALYSIS.csv` file is a direct copy of the `Summary Table`, but in a `.csv`
   file that shows performance over all cost runs.
   
   * Equations for trajectory curves were calculated to extrapolate the number of comparisons \ exchanges  that would be 
   theoretically needed for very large `n` as the algorithm scales. This was accomplished by calculating coefficients of 
   power regression  to define the trajectory path based on the data gathered for similar algorithms.
   If one opens `Metric.py` where the regression algorithms are located, they will notice the regression curve is 
   computed from scratch with no "packages" - the regression equation is derived from low-level statistics functions.
   The `numpy` package is only used to cast an array type to one of a type easier to manipulate with these statistics
   functions.
   
   * Correlation values are calculated (again from scratch and without any use of packages) to show how well the above
   regression curve fits the empirically gathered data in our analysis. More details on this reside in the 
   `FranceLab3_Analysis.docx` document.
   
   * A status is communicated to the user as a % complete in the `__main__.py` file while the data is being processed.
   This allows for a more appealing user interface and lets the user have an idea of where the program is at
   in its execution steps.
   
   * Plots of all of the data runs for each algorithm are shown and allowed for easy comparison against other algorithms. 
   This makes it simple for the user to spot analytical trends and spot which algorithms out-perform others on certain
   datasets.
   
   
   
###References
The following items were used as references for the construction of this project. 
1)	Cormen, T. H., & Leiserson, C. E. (2009). Introduction to Algorithms, 3rd edition.
 
2)	Miller, B. N., & Ranum, D. L. (2014). Problem solving with algorithms and data structures using Python (2nd ed.). Decorah, IA: Brad Miller, David Ranum

3)	Artificial Intelligence: A Modern Approach. Third Edition. Russel, Stuart J.; Norvig, Peter. 2015, Pearson India Education Services Pvt. Ltd. p 961-962.

4)	Deep Learning. Goodfellow, Ian; Bengio, Yoshua; Courville, Aaron. 2016, Massachusetts Institute of Technology. p 147 -149, 525 – 527.

5)	Garey, M. R., & Johnson, D. S. (2003). Computers and Intractability: A Guide to the Theory of NP - Completeness. W.H. Freeman and Co. 

6)	Kleinberg, J., & Tardos, É. (2014). Algorithm Design. Pearson India Education Services Pvt Ltd.
