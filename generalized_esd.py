import numpy as np
from scipy.stats import t

def g_esd(data, percentage, alpha = 0.05, *kwargs):
   
	'''
	Function implements generalized-ESD for outlier-detection, as described here:
	http://www.itl.nist.gov/div898/handbook/eda/section3/eda35h3.htm

	data: one dimensional array with values
	percentage: percentage points expected to be outliers in the data
	alpha: threshold for p-value

	Returns: a list containing indicies of the outliers
	'''
 
	y = list(data)
	n = len(y)
    
	max_outliers = int(percentage*n/100) 

	test_stats = []
	lambdas = []
	indices = []

	for i in xrange(max_outliers):
    
		mu = np.nanmean(y)
		sigma = np.nanstd(y)
		diff = np.abs(y - mu)

		index = np.nanargmax(diff)
		indices.append(index)
		test_stats.append(diff[index]/sigma)

		y[index] = np.nan

		j = i+1
		p = 1 - alpha/( 2*(n-j+1) )  
		t_p_nu = t.ppf(p, n-j+1)
		lambdas.append(  (n-j)*t_p_nu / np.sqrt( (n-j-1+t_p_nu**2) * (n-j+1) )  )
        
	for i in xrange(max_outliers-1, -1, -1):
		if test_stats[i] > lambdas[i]:
			break

	print "Found %d outliers. Returning indices..." % (i+1)
	return indices[:i+1]
