# Metric.py
# Kordel France
########################################################################################################################
# This file provides the protocol for the Metric class. The Metric class is an object that maintains information and
#   performance statistics about each algorithm run.
########################################################################################################################

# numpy is imported to allow for the casting of an array to an easier mutable np.array
# numpy is used to form the np.arrays but not to compute the actual regression and correlations metrics.
import numpy as np
np.seterr(all='ignore')

class Metric:
    def __init__(self,
                 n,
                 pattern,
                 m,
                 comps,
                 exs,
                 predata,
                 x_signal,
                 y_signal,
                 comp_eq,
                 ex_eq,
                 time,
                 snr):
        """
        The Metric class consolidates all information needed about an algorithm's run in order to determine performance statistics.
        :param n: The length of the array that the metric relates to.
        ;param pattern: The type of detection being made: x only, y only, x and y together..
        ;param m: The length of the pattern to find.
        ;param comps: The number of comparisons made by the algorithm.
        ;param exs: The number of exchanges made by the algorithm.
        ;param predata: The data as it arrives before being passed through the detection algorithm.
        ;param x_signal: The array of data to detect within the predata - the X pattern to detect of m length.
        ;param y_signal: The array of data to detect within the predata - the Y pattern to detect of m length..
        ;param comp_eq: The exponential regression equation that predicts the trajectory of the # of comparisons.
        ;param ex_eq: The exponential regression equation that predicts the trajectory of the # of exchanges.
        ;param time: The time it takes for the algorithm to sort the file.
        ;param snr: Signal-to-noise ratio.
        """
        self.n = n
        self.pattern = pattern
        self.m = m
        self.comps = comps
        self.exs = exs
        self.predata = predata
        self.x_signal = x_signal
        self.y_signal = y_signal
        self.comp_eq = comp_eq
        self.ex_eq = ex_eq
        self.time = time
        self.snr = snr


    def print_metric(self):
        """
        Prints each parameter in the metric.
        This is useful in debugging and quality sampling algorithms.
        """
        print(f'\n\n{self.sort} metric of size {self.n}')
        print(f'algorithm: {self.m}-pattern')
        print(f'number of comparisons: {self.comps}')
        print(f'number of exchanges: {self.exs}')
        print(f'regression equation for comparisons: {self.comp_eq}')
        print(f'regression equation for exchanges: {self.ex_eq}')
        print(f'presorted data: {self.predata}')
        print(f'x signal data: {self.x_signal}')
        print(f'y signal data: {self.y_signal}')


    def fitPowerRegressionCurveComparisons(self, xVals0, yVals0):
        """
        Fits a power regression curve to plot a trajectory for the number of comparisons a specific
            algorithm will perform as it scales with larger n.
        Notice the regression curve is computed from scratch with no "packages;" numpy is only used to
            cast an array of calculated type to an array of type easier to manipulate through math.
        ;param xVals0: The explanatory variable to use for regression.
        ;param yVals0: The response variable to use for regression.
        :returns: The computed exponential regression equation in the form Ax^B + C as a string.
        """
        xValCount = 0
        yValCount = 0
        if len(xVals0) > 2:
            xValCount += int(len(xVals0) / 2) - 1
            yValCount += int(len(xVals0) / 2) - 1
        else:
            return "regression error", 0.0
        xVals = []
        yVals = []
        xValIndex = xValCount + 1
        yValIndex = yValCount + 1
        for i in range(xValIndex, len(xVals0)):
            xVals.append(xVals0[i])
        for i in range(yValIndex, len(xVals0)):
            yVals.append(yVals0[i])
        n = len(xVals)
        sumLnxLny = 0.0
        sumLnx = 0.0
        sumLny = 0.0
        sumLnx2 = 0.0
        sumLny2 = 0.0
        for i in range(0, n - 1):
            lnx = np.log(xVals[i])
            lny = np.log(yVals[i])
            sumLnxLny += (lnx * lny)
        for i in range(0, n - 1):
            lnx = np.log(xVals[i])
            sumLnx += lnx
        for i in range(0, n - 1):
            lny = np.log(yVals[i])
            sumLny += lny
        for i in range(0, n - 1):
            lny = np.log(yVals[i])
            sumLny2 += (lny * lny)
        for i in range(0, n - 1):
            lnx = np.log(xVals[i])
            sumLnx2 += (lnx * lnx)
        lnxBar = sumLnx / n
        lnyBar = sumLny / n
        sxx = sumLnx2 - (n * (lnxBar ** 2))
        syy = sumLny2 - (n * (lnyBar ** 2))
        sxy = sumLnxLny - (n * lnxBar * lnyBar)
        b = sxy / sxx
        a = pow(np.e, lnyBar - (b * lnxBar))
        r = sxy / (np.sqrt(sxx) * np.sqrt(syy))
        xx = np.array(xVals)
        yy = np.array(yVals)
        def power_law(xx, a, b):
            return a * np.power(xx, b)
        yHats = []
        for xPrime in xx:
            yHats.append(power_law(xPrime, a, b))
        eq = str(f' y = {str(round(a, 4))} (x) ^ {str(round(b, 4))} w/ correlation {str(round(100.0000 * r, 1))} %')
        if 'nan' in eq:
            eq_nan = 'could not calculate regression\t\t'
            self.eq = eq_nan
            return eq_nan
        else:
            self.ex_eq = eq
            return eq


    def fitPowerRegressionCurveExchanges(self, xVals0, yVals0):
        """
        Fits a power regression curve to plot a trajectory for the number of comparisons a specific sorting
            algorithm will perform as it scales with larger n.
        Notice the regression curve is computed from scratch with no "packages;" numpy is only used to
            cast an array of calculated type to an array of type easier to manipulate through math.
        ;param xVals0: The explanatory variable to use for regression.
        ;param yVals0: The response variable to use for regression.
        :returns: The computed exponential regression equation in the form Ax^B + C as a string.
        """
        xValCount = 0
        yValCount = 0
        if len(xVals0) > 2:
            xValCount += int(len(xVals0) / 2) - 1
            yValCount += int(len(xVals0) / 2) - 1
        else:
            return "regression error", 0.0
        xVals = []
        yVals = []
        xValIndex = xValCount + 1
        yValIndex = yValCount + 1
        for i in range(xValIndex, len(xVals0)):
            xVals.append(xVals0[i])
        for i in range(yValIndex, len(xVals0)):
            yVals.append(yVals0[i])
        n = len(xVals)
        sumLnxLny = 0.0
        sumLnx = 0.0
        sumLny = 0.0
        sumLnx2 = 0.0
        sumLny2 = 0.0
        for i in range(0, n - 1):
            lnx = np.log(xVals[i])
            lny = np.log(yVals[i])
            sumLnxLny += (lnx * lny)
        for i in range(0, n - 1):
            lnx = np.log(xVals[i])
            sumLnx += lnx
        for i in range(0, n - 1):
            lny = np.log(yVals[i])
            sumLny += lny
        for i in range(0, n - 1):
            lny = np.log(yVals[i])
            sumLny2 += (lny * lny)
        for i in range(0, n - 1):
            lnx = np.log(xVals[i])
            sumLnx2 += (lnx * lnx)
        lnxBar = sumLnx / n
        lnyBar = sumLny / n
        sxx = sumLnx2 - (n * (lnxBar ** 2))
        syy = sumLny2 - (n * (lnyBar ** 2))
        sxy = sumLnxLny - (n * lnxBar * lnyBar)
        b = sxy / sxx
        a = pow(np.e, lnyBar - (b * lnxBar))
        r = sxy / (np.sqrt(sxx) * np.sqrt(syy))
        xx = np.array(xVals)
        yy = np.array(yVals)
        def power_law(xx, a, b):
            return a * np.power(xx, b)
        yHats = []
        for xPrime in xx:
            yHats.append(power_law(xPrime, a, b))
        eq = str(f' y = {str(round(a, 4))} (x) ^ {str(round(b, 4))} w/ correlation {str(round(100.0000 * r, 1))} %')
        if 'nan' in eq:
            eq_nan = 'could not calculate regression\t\t'
            self.eq = eq_nan
            return eq_nan
        else:
            self.ex_eq = eq
            return eq
