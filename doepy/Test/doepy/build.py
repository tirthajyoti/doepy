from doepy.doe_functions import build_full_fact, build_frac_fact_res,\
                                build_plackett_burman,build_sukharev,\
                                build_box_behnken, build_central_composite, \
                                build_lhs, build_space_filling_lhs, \
                                build_random_k_means, build_maximin, \
                                build_halton, build_uniform_random

def full_fact(d):
    """
    Builds a full factorial design dataframe from a dictionary of factor/level ranges
    Example of the dictionary which is needed as the input:
    {'Pressure':[50,60,70],'Temperature':[290, 320, 350],'Flow rate':[0.9,1.0]}
    """
    return build_full_fact(d)
    
def frac_fact_res(d,res=None):
    """
    Builds a 2-level fractional factorial design dataframe from a dictionary of factor/level ranges and given resolution.
      
    Parameters
    ----------
    factor_level_ranges : Dictionary of factors and ranges
                         Only min and max values of the range are required.
                         If more than two levels are given, the extreme values will be set to the low/high levels.
                         Example of the dictionary which is needed as the input:
                        {'Pressure':[50,70],'Temperature':[290, 350],'Flow rate':[0.9,1.0]}
    res : int
        Desired design resolution.
        Default: Set to half of the total factor count.
	
	Notes
    -----
    The resolution of a design is defined as the length of the shortest
    word in the defining relation. The resolution describes the level of
    confounding between factors and interaction effects, where higher
    resolution indicates lower degree of confounding.
    For example, consider the 2^4-1-design defined by
        gen = "a b c ab"
    The factor "d" is defined by "ab" with defining relation I="abd", where
    I is the unit vector. In this simple example the shortest word is "abd"
    meaning that this is a resolution III-design.
    In practice resolution III-, IV- and V-designs are most commonly applied.
    * III: Main effects may be confounded with two-factor interactions.
    * IV: Main effects are unconfounded by two-factor interactions, but
          two-factor interactions may be confounded with each other.
    * V: Main effects unconfounded with up to four-factor interactions,
         two-factor interactions unconfounded with up to three-factor
         interactions. Three-factor interactions may be confounded with
         each other.
    Examples
    --------
    ::
        >>> d1 = {'A':[1,5],'B':[0.3,0.7],'C':[10,15],'D':[3,7],'E':[-2,-1]}
        >>> build_frac_fact_res(d1,3)
             A    B     C    D    E
        0  1.0  0.3  10.0  7.0 -1.0
        1  5.0  0.3  10.0  3.0 -2.0
        2  1.0  0.7  10.0  3.0 -1.0
        3  5.0  0.7  10.0  7.0 -2.0
        4  1.0  0.3  15.0  7.0 -2.0
        5  5.0  0.3  15.0  3.0 -1.0
        6  1.0  0.7  15.0  3.0 -2.0
        7  5.0  0.7  15.0  7.0 -1.0
        
        It builds a dataframe with only 8 rows (designs) from a dictionary with 6 factors.
        A full factorial design would have required 2^6 = 64 designs.
        >>> build_frac_fact_res(d1,5)
        Traceback (most recent call last):
        ...
        ValueError: design not possible
    """
    
    return build_frac_fact_res(d,res=res)
    
def plackett_burman(d):
    """
    Builds a Plackett-Burman dataframe from a dictionary of factor/level ranges.
    Only min and max values of the range are required.
    Example of the dictionary which is needed as the input:
    {'Pressure':[50,70],'Temperature':[290, 350],'Flow rate':[0.9,1.0]}
	
	Plackett–Burman designs are experimental designs presented in 1946 by Robin L. Plackett and J. P. Burman while working in the British Ministry of Supply.(Their goal was to find experimental designs for investigating the dependence of some measured quantity on a number of independent variables (factors), each taking L levels, in such a way as to minimize the variance of the estimates of these dependencies using a limited number of experiments. 
	
    Interactions between the factors were considered negligible. The solution to this problem is to find an experimental design where each combination of levels for any pair of factors appears the same number of times, throughout all the experimental runs (refer to table). 
	A complete factorial design would satisfy this criterion, but the idea was to find smaller designs.
	
	These designs are unique in that the number of trial conditions (rows) expands by multiples of four (e.g. 4, 8, 12, etc.). 
	The max number of columns allowed before a design increases the number of rows is always one less than the next higher multiple of four.
    """
    
    return build_plackett_burman(d)

def build_sukharev(d,num_samples=None):
    """
    Builds a Sukharev-grid hypercube design dataframe from a dictionary of factor/level ranges.
    Number of samples raised to the power of (1/dimension), where dimension is the number of variables, must be an integer.
    Only min and max values of the range are required.
    Example of the dictionary which is needed as the input:
    {'Pressure':[50,70],'Temperature':[290, 350],'Flow rate':[0.9,1.0]}
    num_samples: Number of samples to be generated
	
	Special property of this grid is that points are not placed on the boundaries of the hypercube, but at centroids of the  subcells constituted by individual samples. 
	This design offers optimal results for the covering radius regarding distances based on the max-norm.
    """
    
    return build_sukharev(d,num_samples=num_samples)

def box_behnken(d,center=1):
    """
    Builds a Box-Behnken design dataframe from a dictionary of factor/level ranges.
    Note 3 levels of factors are necessary. If not given, the function will automatically create 3 levels by linear mid-section method.
    Example of the dictionary which is needed as the input:
    {'Pressure':[50,60,70],'Temperature':[290, 320, 350],'Flow rate':[0.9,1.0,1.1]}
	
	In statistics, Box–Behnken designs are experimental designs for response surface methodology, devised by George E. P. Box and Donald Behnken in 1960, to achieve the following goals:
		* Each factor, or independent variable, is placed at one of three equally spaced values, usually coded as −1, 0, +1. (At least three levels are needed for the following goal.)
		* The design should be sufficient to fit a quadratic model, that is, one containing squared terms, products of two factors, linear terms and an intercept.
		* The ratio of the number of experimental points to the number of coefficients in the quadratic model should be reasonable (in fact, their designs kept it in the range of 1.5 to 2.6).*estimation variance should more or less depend only on the distance from the centre (this is achieved exactly for the designs with 4 and 7 factors), and should not vary too much inside the smallest (hyper)cube containing the experimental points.
	"""
    
    return build_box_behnken(d,center=center)

def central_composite(d,center=(2,2),alpha='o',face='ccc'):
    """
    Builds a central-composite design dataframe from a dictionary of factor/level ranges.
    Only min and max values of the range are required.
    Example of the dictionary which is needed as the input:
    {'Pressure':[50,70],'Temperature':[290, 350],'Flow rate':[0.9,1.0]}
	
	In statistics, a central composite design is an experimental design, useful in response surface methodology, for building a second order (quadratic) model for the response variable without needing to use a complete three-level factorial experiment.
	The design consists of three distinct sets of experimental runs:
		* A factorial (perhaps fractional) design in the factors studied, each having two levels;
		* A set of center points, experimental runs whose values of each factor are the medians of the values used in the factorial portion. This point is often replicated in order to improve the precision of the experiment;
		* A set of axial points, experimental runs identical to the centre points except for one factor, which will take on values both below and above the median of the two factorial levels, and typically both outside their range. All factors are varied in this way.
    """
    
    return build_central_composite(d,center=center,alpha=alpha,face=face)

def lhs(d, num_samples=None, prob_distribution=None):
    """
    Builds a Latin Hypercube design dataframe from a dictionary of factor/level ranges.
    Only min and max values of the range are required.
    Example of the dictionary which is needed as the input:
    {'Pressure':[50,70],'Temperature':[290, 350],'Flow rate':[0.9,1.0]}
    num_samples: Number of samples to be generated
    prob_distribution: Analytical probability distribution to be applied over the randomized sampling. 
	Accepts one of the following strings: 
    'Normal', 'Poisson', 'Exponential', 'Beta', 'Gamma'

	Latin hypercube sampling (LHS) is a form of stratified sampling that can be applied to multiple variables. The method commonly used to reduce the number or runs necessary for a Monte Carlo simulation to achieve a reasonably accurate random distribution. LHS can be incorporated into an existing Monte Carlo model fairly easily, and work with variables following any analytical probability distribution.
    """
    
    return build_lhs(d, num_samples=num_samples, prob_distribution=prob_distribution)
    
def space_filling_lhs(d, num_samples=None):
    """
    Builds a space-filling Latin Hypercube design dataframe from a dictionary of factor/level ranges.
    Only min and max values of the range are required.
    Example of the dictionary which is needed as the input:
    {'Pressure':[50,70],'Temperature':[290, 350],'Flow rate':[0.9,1.0]}
    num_samples: Number of samples to be generated
    """
    
    return build_space_filling_lhs(d, num_samples=num_samples)

def random_k_means(d, num_samples=None):
    """
    This function aims to produce a centroidal Voronoi tesselation of the unit random hypercube and generate k-means clusters.
    Only min and max values of the range are required.
    Example of the dictionary which is needed as the input:
    {'Pressure':[50,70],'Temperature':[290, 350],'Flow rate':[0.9,1.0]}
    num_samples: Number of samples to be generated
    """
    
    return build_random_k_means(d, num_samples=num_samples)
    
def maximin(d, num_samples=None):
    """
    Builds a maximin reconstructed design dataframe from a dictionary of factor/level ranges.
    Only min and max values of the range are required.
    Example of the dictionary which is needed as the input:
    {'Pressure':[50,70],'Temperature':[290, 350],'Flow rate':[0.9,1.0]}
    num_samples: Number of samples to be generated
	
	This algorithm carries out a user-specified number of iterations to maximize the minimal distance of a point in the set to 
		* other points in the set, 
		* existing (fixed) points, 
		* the boundary of the hypercube.
    """
    
    return build_maximin(d, num_samples=num_samples)
    
def halton(d, num_samples=None):
    """
    Builds a quasirandom dataframe from a dictionary of factor/level ranges using prime numbers as seed.
    Only min and max values of the range are required.
    Example of the dictionary which is needed as the input:
    {'Pressure':[50,70],'Temperature':[290, 350],'Flow rate':[0.9,1.0]}
    num_samples: Number of samples to be generated

    Quasirandom sequence using the default initialization with first n prime numbers equal to the number of factors/variables.
    """
    
    return build_halton(d, num_samples=num_samples)
    
def uniform_random (d, num_samples=None):
    """
    Builds a design dataframe with samples drawn from uniform random distribution based on a dictionary of factor/level ranges.
    Only min and max values of the range are required.
    Example of the dictionary which is needed as the input:
    {'Pressure':[50,70],'Temperature':[290, 350],'Flow rate':[0.9,1.0]}
    num_samples: Number of samples to be generated
    """
    
    return build_uniform_random (d, num_samples=num_samples)