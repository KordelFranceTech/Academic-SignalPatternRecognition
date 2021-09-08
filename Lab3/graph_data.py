# graph_data.py
# Kordel France
########################################################################################################################
# This file provides functions to categorize, filter, graph, and save analyzed data.
# The data is first categorized by data type and algorithm, then graphed and saved, and finally summarized.
########################################################################################################################

# used as an interface to build a graph and plot with data
import matplotlib.pyplot as plt
# used to write performance data to .csv files
import csv
from Lab3.Metric import Metric as m
from Lab3.constants import file_sizes, file_types, pattern_sizes

final_metrics = []

def stratify_data(metrics):
	"""
	Categorizes (stratifies) the data according to the data's initial distribution.
	;param metrics: An array of metrics evaluated from the data that will be categorized here.
	"""
	x_metrics = []
	y_metrics = []
	xy_metrics = []
	for i in range(0, len(metrics)):
		met = metrics[i]
		m0 = m(met.n, met.pattern, met.m, met.comps, met.exs, met.predata, met.x_signal, met.y_signal, '', '', met.time, met.snr)
		if m0.pattern == 'x':
			x_metrics.append(m0)
		elif m0.pattern == 'y':
			y_metrics.append(m0)
		elif m0.pattern == 'x and y':
			xy_metrics.append(m0)
	stratify_data_algos(x_metrics, y_metrics, xy_metrics)


def stratify_data_algos(x_metrics, y_metrics, xy_metrics):
	"""
	Categorizes (stratifies) the data according to the data's algorithm.
	After this categorization procedure, all Metric objects will be grouped primarily by type and secondarily
		by algorithm. This helps with outputting data to the screen in a clean, logical manner.
	After categorization, the data is sent to be graphed.
	;param x_metrics: An array of metrics evaluated from initially x data that will be categorized here.
	;param y_metrics: An array of metrics evaluated from initially y data that will be categorized here.
	;param xy_metrics: An array of metrics evaluated from initially x and y data that will be categorized here.
	"""
	# initialize arrays for population
	data_3p = []
	data_5p = []
	data_10p = []
	data_20p = []
	data_50p = []
	data_100p = []
	data_150p = []

	# traverse through metrics and classify by algorithm
	for i in range(0, len(x_metrics)):
		met = x_metrics[i]
		s = m(met.n, met.pattern, met.m, met.comps, met.exs, met.predata, met.x_signal, met.y_signal, '', '', met.time, met.snr)
		if s.m == 3:
			data_3p.append(s)
		elif s.m == 5:
			data_5p.append(s)
		elif s.m == 10:
			data_10p.append(s)
		elif s.m == 20:
			data_20p.append(s)
		elif s.m == 50:
			data_50p.append(s)
		elif s.m == 100:
			data_100p.append(s)
		elif s.m == 150:
			data_150p.append(s)

	# metrics categorized - prepare them for graphing
	graph_exchanges('Signal with Only X', data_3p, data_5p, data_10p,  data_20p, data_50p, data_100p, data_150p)
	# re-init the data for next category
	data_3p.clear()
	data_5p.clear()
	data_10p.clear()
	data_20p.clear()
	data_50p.clear()
	data_100p.clear()
	data_150p.clear()

	# traverse through y-only pattern metrics and classify by algorithm
	for i in range(0, len(y_metrics)):
		met = y_metrics[i]
		s = m(met.n, met.pattern, met.m, met.comps, met.exs, met.predata, met.x_signal, met.y_signal, '', '', met.time, met.snr)
		if s.m == 3:
			data_3p.append(s)
		elif s.m == 5:
			data_5p.append(s)
		elif s.m == 10:
			data_10p.append(s)
		elif s.m == 20:
			data_20p.append(s)
		elif s.m == 50:
			data_50p.append(s)
		elif s.m == 100:
			data_100p.append(s)
		elif s.m == 150:
			data_150p.append(s)

	# metrics categorized - prepare them for graphing
	graph_exchanges('Signal with Only Y', data_3p, data_5p, data_10p, data_20p, data_50p, data_100p, data_150p)
	# re-init the data for next category
	data_3p.clear()
	data_5p.clear()
	data_10p.clear()
	data_20p.clear()
	data_50p.clear()
	data_100p.clear()
	data_150p.clear()

	# traverse through x and y pattern metrics and classify by algorithm
	for i in range(0, len(xy_metrics)):
		met = xy_metrics[i]
		s = m(met.n, met.pattern, met.m, met.comps, met.exs, met.predata, met.x_signal, met.y_signal, '', '', met.time, met.snr)
		if s.m == 3:
			data_3p.append(s)
		elif s.m == 5:
			data_5p.append(s)
		elif s.m == 10:
			data_10p.append(s)
		elif s.m == 20:
			data_20p.append(s)
		elif s.m == 50:
			data_50p.append(s)
		elif s.m == 100:
			data_100p.append(s)
		elif s.m == 150:
			data_150p.append(s)

	# metrics categorized - prepare them for graphing
	graph_exchanges('Signal with Both X and Y', data_3p, data_5p, data_10p, data_20p, data_50p, data_100p, data_150p)


def graph_exchanges(title, data_3p, data_5p, data_10p, data_20p, data_50p, data_100p, data_150p):
	"""
	Graphs the  data in accordance to each category - x-pattern only, y-pattern only, or x and y patterns together..
	All runs of similar categories and algorithms are graphed together, as long as they belong to the same category.
	This function is called 3 times - (1 x only pattern data, 2) y only pattern data, 3) x and y interwoven pattern data
	;param title: a string of one of the three data categories being graphed and the title of our graph.
	;param data_3p: an array of Metric objects representing a 3-pattern detected in the signal.
	;param data_5p: an array of Metric objects representing a 5-pattern detected in the signal.
	;param data_10p: an array of Metric objects representing a 10-pattern detected in the signal.
	;param data_20p: an array of Metric objects representing a 20-pattern detected in the signal.
	"""
	global final_metrics
	p3_x_vals = []
	p3_comp_vals = []
	p3_ex_vals = []
	p5_x_vals = []
	p5_comp_vals = []
	p5_ex_vals = []
	p10_x_vals = []
	p10_comp_vals = []
	p10_ex_vals = []
	p20_x_vals = []
	p20_comp_vals = []
	p20_ex_vals = []
	p50_x_vals = []
	p50_comp_vals = []
	p50_ex_vals = []
	p100_x_vals = []
	p100_comp_vals = []
	p100_ex_vals = []
	p150_x_vals = []
	p150_comp_vals = []
	p150_ex_vals = []

	# iterate through all 3-pattern  objects to extract costs for graphing
	for metric in data_3p:
		met = metric
		m0 = m(met.n, met.pattern, met.m, met.comps, met.exs, met.predata, met.x_signal, met.y_signal, '', '', met.time, met.snr)
		p3_x_vals.append(m0.n)
		p3_ex_vals.append(m0.exs)
		p3_comp_vals.append(m0.comps)

	# iterate through all 5-pattern  objects to extract costs for graphing
	for metric in data_5p:
		met = metric
		m0 = m(met.n, met.pattern, met.m, met.comps, met.exs, met.predata, met.x_signal, met.y_signal, '', '', met.time, met.snr)
		p5_x_vals.append(m0.n)
		p5_ex_vals.append(m0.exs)
		p5_comp_vals.append(m0.comps)

	# iterate through all 10-pattern  objects to extract costs for graphing
	for metric in data_10p:
		met = metric
		m0 = m(met.n, met.pattern, met.m, met.comps, met.exs, met.predata, met.x_signal, met.y_signal, '', '', met.time, met.snr)
		p10_x_vals.append(m0.n)
		p10_ex_vals.append(m0.exs)
		p10_comp_vals.append(m0.comps)

	# iterate through all 20-pattern  objects to extract costs for graphing
	for metric in data_20p:
		met = metric
		m0 = m(met.n, met.pattern, met.m, met.comps, met.exs, met.predata, met.x_signal, met.y_signal, '', '', met.time, met.snr)
		p20_x_vals.append(m0.n)
		p20_ex_vals.append(m0.exs)
		p20_comp_vals.append(m0.comps)

	# iterate through all 50-pattern  objects to extract costs for graphing
	for metric in data_50p:
		met = metric
		m0 = m(met.n, met.pattern, met.m, met.comps, met.exs, met.predata, met.x_signal, met.y_signal, '', '', met.time, met.snr)
		p50_x_vals.append(m0.n)
		p50_ex_vals.append(m0.exs)
		p50_comp_vals.append(m0.comps)

	# iterate through all 100-pattern  objects to extract costs for graphing
	for metric in data_100p:
		met = metric
		m0 = m(met.n, met.pattern, met.m, met.comps, met.exs, met.predata, met.x_signal, met.y_signal, '', '', met.time, met.snr)
		p100_x_vals.append(m0.n)
		p100_ex_vals.append(m0.exs)
		p100_comp_vals.append(m0.comps)

	# iterate through all 150-pattern  objects to extract costs for graphing
	for metric in data_150p:
		met = metric
		m0 = m(met.n, met.pattern, met.m, met.comps, met.exs, met.predata, met.x_signal, met.y_signal, '', '', met.time, met.snr)
		p150_x_vals.append(m0.n)
		p150_ex_vals.append(m0.exs)
		p150_comp_vals.append(m0.comps)

	# iterate through all 3pattern objects to compute the fitted exponential regression curves for trajectory
	#		of # comparisons and # exchanges as n scales larger.
	# also write to file
	for qs in data_3p:
		qs.comp_eq = qs.fitPowerRegressionCurveComparisons(p3_x_vals, p3_comp_vals)
		qs.ex_eq = qs.fitPowerRegressionCurveExchanges(p3_x_vals, p3_ex_vals)
		write_data_to_file(qs)
		final_metrics.append(qs)

	# iterate through all 5pattern  objects to compute the fitted exponential regression curves for trajectory
	#		of # comparisons and # exchanges as n scales larger.
	# also write to file
	for qsr in data_5p:
		qsr.comp_eq = qsr.fitPowerRegressionCurveComparisons(p5_x_vals, p5_comp_vals)
		qsr.ex_eq = qsr.fitPowerRegressionCurveExchanges(p5_x_vals, p5_ex_vals)
		write_data_to_file(qsr)
		final_metrics.append(qsr)

	# iterate through all 10pattern objects to compute the fitted exponential regression curves for trajectory
	#		of # comparisons and # exchanges as n scales larger.
	# also write to file
	for p10 in data_10p:
		p10.comp_eq = p10.fitPowerRegressionCurveComparisons(p10_x_vals, p10_comp_vals)
		p10.ex_eq = p10.fitPowerRegressionCurveExchanges(p10_x_vals, p10_ex_vals)
		write_data_to_file(p10)
		final_metrics.append(p10)

	# iterate through all 20pattern objects to compute the fitted exponential regression curves for trajectory
	#		of # comparisons and # exchanges as n scales larger.
	# also write to file
	for m1 in data_20p:
		m1.comp_eq = m1.fitPowerRegressionCurveComparisons(p20_x_vals, p20_comp_vals)
		m1.ex_eq = m1.fitPowerRegressionCurveExchanges(p20_x_vals, p20_ex_vals)
		write_data_to_file(m1)
		final_metrics.append(m1)

	# iterate through all 50pattern objects to compute the fitted exponential regression curves for trajectory
	#		of # comparisons and # exchanges as n scales larger.
	# also write to file
	for m2 in data_50p:
		m2.comp_eq = m2.fitPowerRegressionCurveComparisons(p50_x_vals, p50_comp_vals)
		m2.ex_eq = m2.fitPowerRegressionCurveExchanges(p50_x_vals, p50_ex_vals)
		write_data_to_file(m2)
		final_metrics.append(m2)

	# iterate through all 100pattern objects to compute the fitted exponential regression curves for trajectory
	#		of # comparisons and # exchanges as n scales larger.
	# also write to file
	for m3 in data_100p:
		m3.comp_eq = m3.fitPowerRegressionCurveComparisons(p100_x_vals, p100_comp_vals)
		m3.ex_eq = m3.fitPowerRegressionCurveExchanges(p100_x_vals, p100_ex_vals)
		write_data_to_file(m3)
		final_metrics.append(m3)

	# iterate through all 150pattern objects to compute the fitted exponential regression curves for trajectory
	#		of # comparisons and # exchanges as n scales larger.
	# also write to file
	for h in data_150p:
		h.comp_eq = h.fitPowerRegressionCurveComparisons(p150_x_vals, p150_comp_vals)
		h.ex_eq = h.fitPowerRegressionCurveExchanges(p150_x_vals, p150_ex_vals)
		write_data_to_file(h)
		final_metrics.append(h)

	# create scatter plots of all the data
	plt.scatter(p3_x_vals, p3_comp_vals, color='black')
	plt.scatter(p5_x_vals, p5_comp_vals, color='black')
	plt.scatter(p10_x_vals, p10_comp_vals, color='black')
	plt.scatter(p20_x_vals, p20_comp_vals, color='black')
	plt.scatter(p50_x_vals, p50_comp_vals, color='black')

	# overlay line graphs of # comparisons per algorithm
	plt.plot(p3_x_vals, p3_comp_vals, label='(operations) 3-pattern', color='red')
	plt.plot(p5_x_vals, p5_comp_vals, label='(operations)  5-pattern', color='blue')
	plt.plot(p10_x_vals, p10_comp_vals, label='(operations)  10-pattern', color='purple')
	plt.plot(p20_x_vals, p20_comp_vals, label='(operations)  20-pattern', color='green')
	plt.plot(p50_x_vals, p50_comp_vals, label='(operations)  50-pattern', color='black')

	plt.title(f'Algorithm Performance Over {title} Data')
	plt.xlabel('number of files (n)')
	plt.ylabel('number of cost operations')
	plt.xlim(0, max(file_sizes) * 1.05)
	plt.legend()
	plt.show(block=False)
	print('\n\n\n\n\n')
	print('_________________________________________________________________________________________')
	print('_________________________________________________________________________________________')
	print(f'Now displaying algorithmic performance over {title} data.')
	print('\nType any key to dismiss current plot and view next plot...')
	# the user simply taps a key in order to dismiss the plot and move to the next one
	if input() != None:
		# reset plot for redraw on new data
		plt.clf()
		plt.cla()
	print('_________________________________________________________________________________________')
	print('_________________________________________________________________________________________')


def write_data_to_file(data):
	"""
	This function writes data to a .csv file for interpretation by user after program termination.
	Each possible scenario gets its own .csv file.
	Files are named {algorithm_name}-{date_type}-{n} count.csv such as '3-way_merge_random_1000count.csv'.
	All files are output to the 'output_Files' folder.
	The 'csv' library is used to write the data to each respective report.
	;param data: an array of Metric objects used to build .csv file
	"""
	metric = m(data.n, data.pattern, data.m, data.comps, data.exs, data.predata, data.x_signal, data.y_signal, '', '', data.time, data.snr)
	if metric.m == 3:
		metric.m = '3-pattern'
	elif metric.m == 5:
		metric.m = '5-pattern'
	elif metric.m == 10:
		metric.m = '10-pattern'
	elif metric.m == 20:
		metric.m = '20-pattern'
	elif metric.m == 50:
		metric.m = '50-pattern'
	elif metric.m == 100:
		metric.m = '100-pattern'
	elif metric.m == 120:
		metric.m = '120-pattern'
	elif metric.m == 150:
		metric.m = '150-pattern'
	else:
		metric.m = '300-pattern'

	with open(f'output_files/{metric.m}_{metric.pattern}_{metric.n}count.csv', 'w', newline='') as csv_file:
			title_names = ['title']
			comp_names = ['comparisons', 'equation', 'time']
			ex_names = ['exchanges', 'equation']
			col_names = ['count', 'incoming signal', 'x signal', 'y signal']
			title_writer = csv.DictWriter(csv_file, fieldnames=title_names)
			title_writer.writerow({'title': f'Analysis data for {metric.m}-pattern algorithm on {metric.pattern} signals for n = {metric.n}'})
			comp_writer = csv.DictWriter(csv_file, fieldnames=comp_names)
			comp_writer.writerow({'comparisons': f'# of comparisons: {str(metric.comps)}',
								  'equation': f' regression equation: {str(metric.comp_eq)}',
								  'time': f'execution time: {str(metric.time)} s'})
			ex_writer = csv.DictWriter(csv_file, fieldnames=ex_names)
			ex_writer.writerow({'exchanges': f'# of exchanges: {str(metric.exs)}',
								'equation': f' regression equation: {str(metric.ex_eq)}'})
			csv_writer = csv.DictWriter(csv_file, fieldnames=col_names)
			csv_writer.writeheader()
			count = 0
			for i in range(0, max(len(metric.predata), len(metric.x_signal), len(metric.y_signal))):
				s = ''
				x = ''
				y = ''
				if i < len(metric.predata):
					s += str(metric.predata[i])
				if i < len(metric.x_signal):
					x += str(metric.x_signal[i])
				if i < len(metric.y_signal):
					y += str(metric.y_signal[i])

				csv_writer.writerow({'count': str(count),
									 'incoming signal': s,
									 'x signal': x,
									 'y signal': y})
				count += 1


def present_and_save_summary():
	"""
	This function presents a final summary of performance statistics for each sorting run analyzed.
	A summary table is printed to the console and a copy of that summary table is written to a .csv file.
	The summary .csv file is named FINAL_ANALYSIS.csv and may be found in the 'output_files' folder of this module.
	"""
	global final_metrics
	metrics = final_metrics

	with open(f'output_files/FINAL_ANALYSIS.csv', 'w', newline='') as csv_file:
			title_names = ['title']
			col_names = ['#',
						'data_type',
						'n',
						'm-pattern',
						'operations',
						'end index',
						'SNR',
						'operations trajectory equation',
						'end index trajectory equation',
						'time']
			title_writer = csv.DictWriter(csv_file, fieldnames=title_names)
			title_writer.writerow({'title': f'Summary of all {len(file_types) * len(file_sizes) * len(pattern_sizes)} analyzed sorting runs'})
			csv_writer = csv.DictWriter(csv_file, fieldnames=col_names)
			csv_writer.writeheader()

			print('#\t|data type\t|n\t|m-pattern\t|operations\t|end index\t|SNR\t|time\t\t|operations trajectory eqn\t\t\t |end index trajectory eqn')
			print('____________________________________________________________________________________________'
				  '____________________________________________________________________________________________')

			count = 0
			# print(f'metrics:')
			for i in range(0, len(metrics)):
				count += 1
				metric = metrics[i]
				# print(metric.algo)
				if metric.m == 3:
					metric.m = '3-pattern'
				elif metric.m == 5:
					metric.m = '5-pattern'
				elif metric.m == 10:
					metric.m = '10-pattern'
				elif metric.m == 20:
					metric.m = '20-pattern'
				elif metric.m == 50:
					metric.m = '50-pattern'
				elif metric.m == 100:
					metric.m = '100-pattern'
				elif metric.m == 120:
					metric.m = '120-pattern'
				elif metric.m == 150:
					metric.m = '150-pattern'
				else:
					metric.m = '300-pattern'

				if metric.m == 'reverse_sorted':
					metric.m = 'reverse'
				else:
					metric.m = f'{metric.m}\t'

				if metric.pattern == 'x and y':
					print(f'{count}\t|{metric.pattern}\t|{metric.n}\t|{metric.m}|{metric.comps}\t\t|\t{metric.exs}\t|{round(metric.snr, 2)}\t|{metric.time} s\t|  {metric.comp_eq}  |  {metric.ex_eq}')
				else:
					print(f'{count}\t|{metric.pattern} detected\t|{metric.n}\t|{metric.m}|{metric.comps}\t\t|\t{metric.exs}\t|{round(metric.snr, 2)}\t|{metric.time} s\t|  {metric.comp_eq}  |  {metric.ex_eq}')
				csv_writer.writerow({'#':f'{count}',
									 'data_type':f'{metric.pattern} detected',
									 'n':f'{metric.n}',
									 'm-pattern':f'{metric.m}',
									 'operations':f'{metric.comps}',
									 'end index':f'{metric.exs}',
									 'SNR':f'{metric.snr}',
									 'operations trajectory equation':f'{metric.comp_eq}',
									 'end index trajectory equation':f'{metric.ex_eq}',
									 'time':f'execution time: {metric.time} s'})










