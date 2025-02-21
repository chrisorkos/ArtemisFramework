import numpy as np
from scipy.optimize import curve_fit

def linear_func_to_fit(x, a, b):
    """
    Linear function to fit the transformed data.

    Parameters:
    - x: Independent variable (log-transformed x-values).
    - a: Intercept parameter of the linear fit.
    - b: Slope parameter of the linear fit.

    Returns:
    - Linear model output based on the given parameters.
    """
    return b * x + a

def power_law_curve_fit(degree_distribution_list):
    """
    Fits a power law to the given degree distribution list.

    Parameters:
    - degree_distribution_list: List of frequencies [freq. k=0, freq. k=1, ..., freq. k=k_max].

    Returns:
    - List containing:
        - fit_success: 1 if fit is successful, 0 otherwise.
        - a: Exponential of the intercept from the fit (scaling factor in the power law).
        - b: Slope of the linear fit (exponent in the power law).
        - start_x: Index of the first non-zero element in the distribution.
        - opt_para_covariance: Covariance matrix of the fit parameters.
    """
    # Default values in case of failure
    found_non_zero = False
    start_x = 0
    a, b = 0, 0
    opt_para_covariance = np.zeros((2, 2))
    fit_success = 0

    # Identify the first non-zero element in the degree distribution
    for x_possible in range(len(degree_distribution_list)):
        if degree_distribution_list[x_possible] > 0:
            start_x = x_possible
            found_non_zero = True
            break

    if found_non_zero:
        # Slice the degree distribution to start from the first non-zero element
        non_zero_distribution = np.array(degree_distribution_list[start_x:])
        x0 = np.arange(len(non_zero_distribution))
        x1 = x0 + 0.1  # Shift x-values slightly to avoid log(0) issues
        x2 = np.log(x1)

        # Shift y-values to ensure all are positive and take their logarithm
        y0 = non_zero_distribution
        y1 = y0 + np.abs(np.min(y0)) + 0.1
        y2 = np.log(y1)

        # Attempt to fit a linear model to the log-transformed data
        try:
            optimal_parameters, opt_para_covariance = curve_fit(linear_func_to_fit, x2, y2, p0=[5, -2.5])
            a, b = np.exp(optimal_parameters[0]), optimal_parameters[1]
            fit_success = 1
        except (RuntimeError, TypeError) as e:
            # Handle cases where the fit fails
            print(f"Fit failed with error: {e}")

    return [fit_success, a, b, start_x, opt_para_covariance]

