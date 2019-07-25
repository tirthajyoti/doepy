import re
import numpy as np
from itertools import dropwhile, combinations, islice
import string
from scipy.special import binom


# __all__ = ['np', 'fullfact_corrected', 'ff2n_corrected', 'fracfact']


def fullfact_corrected(levels):
    """
    Create a general full-factorial design
    
    Parameters
    ----------
    levels : array-like
        An array of integers that indicate the number of levels of each input
        design factor.
    
    Returns
    -------
    mat : 2d-array
        The design matrix with coded levels 0 to k-1 for a k-level factor
    
    Example
    -------
    ::
    
        >>> fullfact([2, 4, 3])
        array([[ 0.,  0.,  0.],
               [ 1.,  0.,  0.],
               [ 0.,  1.,  0.],
               [ 1.,  1.,  0.],
               [ 0.,  2.,  0.],
               [ 1.,  2.,  0.],
               [ 0.,  3.,  0.],
               [ 1.,  3.,  0.],
               [ 0.,  0.,  1.],
               [ 1.,  0.,  1.],
               [ 0.,  1.,  1.],
               [ 1.,  1.,  1.],
               [ 0.,  2.,  1.],
               [ 1.,  2.,  1.],
               [ 0.,  3.,  1.],
               [ 1.,  3.,  1.],
               [ 0.,  0.,  2.],
               [ 1.,  0.,  2.],
               [ 0.,  1.,  2.],
               [ 1.,  1.,  2.],
               [ 0.,  2.,  2.],
               [ 1.,  2.,  2.],
               [ 0.,  3.,  2.],
               [ 1.,  3.,  2.]])
               
    """
    n = len(levels)  # number of factors
    nb_lines = np.prod(levels)  # number of trial conditions
    H = np.zeros((nb_lines, n))

    level_repeat = 1
    range_repeat = np.prod(levels)
    for i in range(n):
        range_repeat //= levels[i]
        lvl = []
        for j in range(levels[i]):
            lvl += [j] * level_repeat
        rng = lvl * range_repeat
        level_repeat *= levels[i]
        H[:, i] = rng

    return H


################################################################################


def ff2n_corrected(n):
    """
    Create a 2-Level full-factorial design
    
    Parameters
    ----------
    n : int
        The number of factors in the design.
    
    Returns
    -------
    mat : 2d-array
        The design matrix with coded levels -1 and 1
    
    Example
    -------
    ::
    
        >>> ff2n(3)
        array([[-1., -1., -1.],
               [ 1., -1., -1.],
               [-1.,  1., -1.],
               [ 1.,  1., -1.],
               [-1., -1.,  1.],
               [ 1., -1.,  1.],
               [-1.,  1.,  1.],
               [ 1.,  1.,  1.]])
       
    """
    return 2 * fullfact_corrected([2] * n) - 1


def ff2n(levels):
    return 2 * fullfact_corrected([2] * levels) - 1


################################################################################


def fracfact_corrected(gen):
    """
    Create a 2-level fractional-factorial design with a generator string.
    
    Parameters
    ----------
    gen : str
        A string, consisting of lowercase, uppercase letters or operators "-"
        and "+", indicating the factors of the experiment
    
    Returns
    -------
    H : 2d-array
        A m-by-n matrix, the fractional factorial design. m is 2^k, where k
        is the number of letters in ``gen``, and n is the total number of
        entries in ``gen``.
    
    Notes
    -----
    In ``gen`` we define the main factors of the experiment and the factors
    whose levels are the products of the main factors. For example, if
    
        gen = "a b ab"
    
    then "a" and "b" are the main factors, while the 3rd factor is the product
    of the first two. If we input uppercase letters in ``gen``, we get the same
    result. We can also use the operators "+" and "-" in ``gen``.
    
    For example, if
    
        gen = "a b -ab"
    
    then the 3rd factor is the opposite of the product of "a" and "b".
    
    The output matrix includes the two level full factorial design, built by
    the main factors of ``gen``, and the products of the main factors. The
    columns of ``H`` follow the sequence of ``gen``.
    
    For example, if
    
        gen = "a b ab c"
    
    then columns H[:, 0], H[:, 1], and H[:, 3] include the two level full
    factorial design and H[:, 2] includes the products of the main factors.
    
    Examples
    --------
    ::
    
        >>> fracfact("a b ab")
        array([[-1., -1.,  1.],
               [ 1., -1., -1.],
               [-1.,  1., -1.],
               [ 1.,  1.,  1.]])
       
        >>> fracfact("A B AB")
        array([[-1., -1.,  1.],
               [ 1., -1., -1.],
               [-1.,  1., -1.],
               [ 1.,  1.,  1.]])
        
        >>> fracfact("a b -ab c +abc")
        array([[-1., -1., -1., -1., -1.],
               [ 1., -1.,  1., -1.,  1.],
               [-1.,  1.,  1., -1.,  1.],
               [ 1.,  1., -1., -1., -1.],
               [-1., -1., -1.,  1.,  1.],
               [ 1., -1.,  1.,  1., -1.],
               [-1.,  1.,  1.,  1., -1.],
               [ 1.,  1., -1.,  1.,  1.]])
       
    """
    # Recognize letters and combinations
    A = [item for item in re.split("\-|\s|\+", gen) if item]  # remove empty strings
    C = [len(item) for item in A]

    # Indices of single letters (main factors)
    I = [i for i, item in enumerate(C) if item == 1]

    # Indices of letter combinations (we need them to fill out H2 properly).
    J = [i for i, item in enumerate(C) if item != 1]

    # Check if there are "-" or "+" operators in gen
    U = [item for item in gen.split(" ") if item]  # remove empty strings

    # If R1 is either None or not, the result is not changed, since it is a
    # multiplication of 1.
    R1 = _grep(U, "+")
    R2 = _grep(U, "-")

    # Fill in design with two level factorial design
    H1 = ff2n(len(I))
    H = np.zeros((H1.shape[0], len(C)))
    H[:, I] = H1

    # Recognize combinations and fill in the rest of matrix H2 with the proper
    # products
    for k in J:
        # For lowercase letters
        xx = np.array([ord(c) for c in A[k]]) - 97

        # For uppercase letters
        if np.any(xx < 0):
            xx = np.array([ord(c) for c in A[k]]) - 65

        H[:, k] = np.prod(H1[:, xx], axis=1)

    # Update design if gen includes "-" operator
    if R2:
        H[:, R2] *= -1

    # Return the fractional factorial design
    return H


def _grep(haystack, needle):
    try:
        haystack[0]
    except (TypeError, AttributeError):
        return [0] if needle in haystack else []
    else:
        locs = []
        for idx, item in enumerate(haystack):
            if needle in item:
                locs += [idx]
        return locs


def _n_fac_at_res(n, res):
    """ Calculate number of possible factors for fractional factorial
    design with `n` base factors at resolution `res`.
    """
    return sum(binom(n, r) for r in range(res - 1, n)) + n


# __all__ = ['bbdesign_corrected']


def fracfact_by_res(n, res):
    """
    Create a 2-level fractional factorial design with `n` factors
    and resolution `res`.
    Parameters
    ----------
    n : int
        The number of factors in the design.
    res : int
        Desired design resolution
    Returns
    -------
    H : 2d-array
        A m-by-`n` matrix, the fractional factorial design. m is the
        minimal amount of rows possible for creating a fractional
        factorial design matrix at resolution `res`
    Raises
    ------
    ValueError
        If the current design is not possible to construct.
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
        >>> fracfact_by_res(6, 3)
        array([[-1., -1., -1.,  1.,  1.,  1.],
               [ 1., -1., -1., -1., -1.,  1.],
               [-1.,  1., -1., -1.,  1., -1.],
               [ 1.,  1., -1.,  1., -1., -1.],
               [-1., -1.,  1.,  1., -1., -1.],
               [ 1., -1.,  1., -1.,  1., -1.],
               [-1.,  1.,  1., -1., -1.,  1.],
               [ 1.,  1.,  1.,  1.,  1.,  1.]])
        >>> fracfact_by_res(5, 5)
        Traceback (most recent call last):
        ...
        ValueError: design not possible
    """
    # Determine minimum required number of base-factors.
    min_fac = next(
        dropwhile(lambda n_: _n_fac_at_res(n_, res) < n, range(res - 1, n)), None
    )

    if min_fac is None:
        raise ValueError("design not possible")
    elif min_fac > len(string.ascii_lowercase):
        # This check needs to be done to make sure that the number
        # of available are enough since `fracfact` parses design generator
        # characters. In practice, this is highly theoretical and it is
        # much more likely to run into memory-issues.
        raise ValueError("design requires too many base-factors.")

    # Get base factors.
    factors = list(string.ascii_lowercase[:min_fac])

    # Fill out with factor combinations until `n` factors.
    factor_combs = (
        "".join(c)
        for r in range(res - 1, len(factors))
        for c in combinations(factors, r)
    )
    extra_factors = list(islice(factor_combs, n - len(factors)))

    # Concatenate `gen` string for `fracfact`.
    gen = " ".join(factors + extra_factors)
    return fracfact_corrected(gen)


def bbdesign_corrected(n, center=None):
    """
    Create a Box-Behnken design
    
    Parameters
    ----------
    n : int
        The number of factors in the design
    
    Optional
    --------
    center : int
        The number of center points to include (default = 1).
    
    Returns
    -------
    mat : 2d-array
        The design matrix
    
    Example
    -------
    ::
    
        >>> bbdesign(3)
        array([[-1., -1.,  0.],
               [ 1., -1.,  0.],
               [-1.,  1.,  0.],
               [ 1.,  1.,  0.],
               [-1.,  0., -1.],
               [ 1.,  0., -1.],
               [-1.,  0.,  1.],
               [ 1.,  0.,  1.],
               [ 0., -1., -1.],
               [ 0.,  1., -1.],
               [ 0., -1.,  1.],
               [ 0.,  1.,  1.],
               [ 0.,  0.,  0.],
               [ 0.,  0.,  0.],
               [ 0.,  0.,  0.]])
        
    """
    assert n >= 3, "Number of variables must be at least 3"

    # First, compute a factorial DOE with 2 parameters
    H_fact = ff2n_corrected(2)
    # Now we populate the real DOE with this DOE

    # We made a factorial design on each pair of dimensions
    # - So, we created a factorial design with two factors
    # - Make two loops
    Index = 0
    nb_lines = int((0.5 * n * (n - 1)) * H_fact.shape[0])
    H = repeat_center(n, nb_lines)

    for i in range(n - 1):
        for j in range(i + 1, n):
            Index = Index + 1
            H[
                max([0, (Index - 1) * H_fact.shape[0]]) : Index * H_fact.shape[0], i
            ] = H_fact[:, 0]
            H[
                max([0, (Index - 1) * H_fact.shape[0]]) : Index * H_fact.shape[0], j
            ] = H_fact[:, 1]

    if center is None:
        if n <= 16:
            points = [0, 0, 0, 3, 3, 6, 6, 6, 8, 9, 10, 12, 12, 13, 14, 15, 16]
            center = points[n]
        else:
            center = n

    H = np.c_[H.T, repeat_center(n, center).T].T

    return H


import numpy as np

# from pyDOE.doe_factorial import ff2n
from pyDOE.doe_star import star
from pyDOE.doe_union import union
from pyDOE.doe_repeat_center import repeat_center

__all__ = ["ccdesign"]


def ccdesign_corrected(n, center=(4, 4), alpha="orthogonal", face="circumscribed"):
    """
    Central composite design
    
    Parameters
    ----------
    n : int
        The number of factors in the design.
    
    Optional
    --------
    center : int array
        A 1-by-2 array of integers, the number of center points in each block
        of the design. (Default: (4, 4)).
    alpha : str
        A string describing the effect of alpha has on the variance. ``alpha``
        can take on the following values:
        
        1. 'orthogonal' or 'o' (Default)
        
        2. 'rotatable' or 'r'
        
    face : str
        The relation between the start points and the corner (factorial) points.
        There are three options for this input:
        
        1. 'circumscribed' or 'ccc': This is the original form of the central
           composite design. The star points are at some distance ``alpha``
           from the center, based on the properties desired for the design.
           The start points establish new extremes for the low and high
           settings for all factors. These designs have circular, spherical,
           or hyperspherical symmetry and require 5 levels for each factor.
           Augmenting an existing factorial or resolution V fractional 
           factorial design with star points can produce this design.
        
        2. 'inscribed' or 'cci': For those situations in which the limits
           specified for factor settings are truly limits, the CCI design
           uses the factors settings as the star points and creates a factorial
           or fractional factorial design within those limits (in other words,
           a CCI design is a scaled down CCC design with each factor level of
           the CCC design divided by ``alpha`` to generate the CCI design).
           This design also requires 5 levels of each factor.
        
        3. 'faced' or 'ccf': In this design, the star points are at the center
           of each face of the factorial space, so ``alpha`` = 1. This 
           variety requires 3 levels of each factor. Augmenting an existing 
           factorial or resolution V design with appropriate star points can 
           also produce this design.
    
    Notes
    -----
    - Fractional factorial designs are not (yet) available here.
    - 'ccc' and 'cci' can be rotatable design, but 'ccf' cannot.
    - If ``face`` is specified, while ``alpha`` is not, then the default value
      of ``alpha`` is 'orthogonal'.
        
    Returns
    -------
    mat : 2d-array
        The design matrix with coded levels -1 and 1
    
    Example
    -------
    ::
    
        >>> ccdesign(3)
        array([[-1.        , -1.        , -1.        ],
               [ 1.        , -1.        , -1.        ],
               [-1.        ,  1.        , -1.        ],
               [ 1.        ,  1.        , -1.        ],
               [-1.        , -1.        ,  1.        ],
               [ 1.        , -1.        ,  1.        ],
               [-1.        ,  1.        ,  1.        ],
               [ 1.        ,  1.        ,  1.        ],
               [ 0.        ,  0.        ,  0.        ],
               [ 0.        ,  0.        ,  0.        ],
               [ 0.        ,  0.        ,  0.        ],
               [ 0.        ,  0.        ,  0.        ],
               [-1.82574186,  0.        ,  0.        ],
               [ 1.82574186,  0.        ,  0.        ],
               [ 0.        , -1.82574186,  0.        ],
               [ 0.        ,  1.82574186,  0.        ],
               [ 0.        ,  0.        , -1.82574186],
               [ 0.        ,  0.        ,  1.82574186],
               [ 0.        ,  0.        ,  0.        ],
               [ 0.        ,  0.        ,  0.        ],
               [ 0.        ,  0.        ,  0.        ],
               [ 0.        ,  0.        ,  0.        ]])
        
       
    """
    # Check inputs
    assert isinstance(n, int) and n > 1, '"n" must be an integer greater than 1.'
    assert alpha.lower() in (
        "orthogonal",
        "o",
        "rotatable",
        "r",
    ), 'Invalid value for "alpha": {:}'.format(alpha)
    assert face.lower() in (
        "circumscribed",
        "ccc",
        "inscribed",
        "cci",
        "faced",
        "ccf",
    ), 'Invalid value for "face": {:}'.format(face)

    try:
        nc = len(center)
    except:
        raise TypeError(
            'Invalid value for "center": {:}. Expected a 1-by-2 array.'.format(center)
        )
    else:
        if nc != 2:
            raise ValueError(
                'Invalid number of values for "center" (expected 2, but got {:})'.format(
                    nc
                )
            )

    # Orthogonal Design
    if alpha.lower() in ("orthogonal", "o"):
        H2, a = star(n, alpha="orthogonal", center=center)

    # Rotatable Design
    if alpha.lower() in ("rotatable", "r"):
        H2, a = star(n, alpha="rotatable")

    # Inscribed CCD
    if face.lower() in ("inscribed", "cci"):
        H1 = ff2n_corrected(n)
        H1 = H1 / a  # Scale down the factorial points
        H2, a = star(n)

    # Faced CCD
    if face.lower() in ("faced", "ccf"):
        H2, a = star(n)  # Value of alpha is always 1 in Faced CCD
        H1 = ff2n_corrected(n)

    # Circumscribed CCD
    if face.lower() in ("circumscribed", "ccc"):
        H1 = ff2n_corrected(n)

    C1 = repeat_center(n, center[0])
    C2 = repeat_center(n, center[1])

    H1 = union(H1, C1)
    H2 = union(H2, C2)
    H = union(H1, H2)

    return H


def repeat_center(n, repeat):
    """
    Create the center-point portion of a design matrix
    
    Parameters
    ----------
    n : int
        The number of factors in the original design
    repeat : int
        The number of center points to repeat
    
    Returns
    -------
    mat : 2d-array
        The center-point portion of a design matrix (elements all zero).
    
    Example
    -------
    ::
    
        >>> repeat_center(3, 2)
        array([[ 0.,  0.,  0.],
               [ 0.,  0.,  0.]])
       
    """
    return np.zeros((repeat, n))
