import numpy as np
from scipy.constants import c as c_light

def pars_to_dict(pars):
    """Converts a list of parameters into a dictionary of parameter groups.

    This function takes a list of parameters `pars` and groups them into
    dictionaries of three parameters (e.g. Rs, Q, resonant_frequency) each.
    The keys of the resulting dictionary are integers starting from 0,
    and the values are lists containing three consecutive parameters from
    the input list.

    Args:
        pars: A list or array of parameters to be grouped.

    Returns:
        dict: A dictionary where keys are integers and values are
             lists of three parameters.

    Raises:
        ValueError: If the length of `pars` is not a multiple of 3.
    """

    if len(pars) % 3 != 0:
        raise ValueError("Input list length must be a multiple of 3")

    grouped_parameters = {}
    for i in range(0, len(pars), 3):
        grouped_parameters[i // 3] = pars[i : i + 3]

    return grouped_parameters


def compute_fft(data_time, data_wake, fmax=3e9, samples=1001):
    """
    Compute the Fourier transform of a wake and return the frequencies
    and impedance values within a specified frequency range.

    Parameters
    ----------
    data_time : array-like
        Array of time values (in seconds) corresponding to the wake data.
    data_wake : array-like
        Array of wake potential values corresponding to `data_time`.
    fmax : float, optional
        Maximum frequency (in Hz) to include in the output. Defaults to 3e9 Hz (3 GHz).
    samples : int, optional
        Number of samples to determine the resolution of the Fourier transform. Defaults to 1001.

    Returns
    -------
    f : ndarray
        Array of frequency values (in Hz) within the range [0, `fmax`).
    Z : ndarray
        Array of impedance values corresponding to the frequencies in `f`.

    Notes
    -----
    - The time array (`data_time`) is assumed to be evenly spaced.
    - The spatial sampling interval `ds` is computed based on the time step and
      the speed of light in vacuum.
    - The Fourier transform is computed using the `numpy.fft` module, and the
      results are normalized by the sampling interval (`ds`).

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.constants import c
    >>> time = np.linspace(0, 10, 100)  # Time in nanoseconds
    >>> wake = np.sin(2 * np.pi * 1e9 * time * 1e-9)  # Example wake
    >>> f, Z = compute_fft(time, wake, fmax=2e9, samples=500)
    >>> print(f.shape, Z.shape)
    (500, 500)
    """

    ds = (data_time[1] - data_time[0])* c_light
    N = int((c_light/ds)//fmax*samples)
    Z = np.fft.fft(data_wake, n=N)
    f = np.fft.fftfreq(len(Z), ds/c_light)

    # Mask invalid frequencies
    mask  = np.logical_and(f >= 0 , f < fmax)
    Z = Z[mask]*ds
    f = f[mask]

    return f, Z

def compute_deconvolution(data_time, data_wake_potential, sigma, fmax=3e9, samples=1001):

    ds = (data_time[1] - data_time[0])*c_light
    N = int((c_light/ds)//fmax*samples)

    # Analytical gaussian with given sigma
    lambdat = 1/(sigma*np.sqrt(2*np.pi))*np.exp(-(data_time**2)/(2*sigma**2))/c_light

    Z = np.fft.fft(data_wake_potential, n=N)
    lambdaf = np.fft.fft(lambdat, n=N)
    f = np.fft.fftfreq(len(Z), ds/c_light)

    # Mask invalid frequencies
    mask  = np.logical_and(f >= 0 , f < fmax)
    Z = Z[mask] / lambdaf[mask]
    f = f[mask]

    return f, Z

def interpolation_error_abs(func_output, interpolant_output):
    return np.abs(func_output - interpolant_output)

def interpolation_error_rms(func_output, interpolant_output):
    error = interpolant_output - func_output
    squared_error = error**2
    mean_squared_error = np.mean(squared_error, axis=1) # This stage changes the shape from (N, 4) to # (N,)
    rms_error = np.sqrt(mean_squared_error)
    return rms_error

def compute_ineffint(data_freq, data_impedance,
                    times=np.linspace(1e-11, 50e-9, 1000),
                    adaptative=True,
                    interpolation='linear',
                    plane = 'longitudinal',
                    error='Abs'):
    try:
        import neffint
    except:
        raise ImportError('This function uses the python package `neffint` \n \
                           > pip install neffint')
    from scipy.interpolate import interp1d

    if not adaptative:
        wake = neffint.fourier_integral_fixed_sampling(
            times=times,
            frequencies=data_freq,
            func_values=data_impedance,
            pos_inf_correction_term=False,
            neg_inf_correction_term=False,
            interpolation=interpolation # `pchip gives artificial imag. baseline`
        )

    # Using adaptative freq. refining
    if adaptative:
        if error.lower() == 'abs':
            interpolation_error_norm = interpolation_error_abs
        elif error.lower() == 'rms':
            interpolation_error_norm = interpolation_error_rms

        func = interp1d(data_freq, data_impedance,
                        kind='linear', fill_value="extrapolate")

        frequencies, impedance = neffint.improve_frequency_range(
            initial_frequencies=data_freq,
            func=func,
            interpolation_error_norm=interpolation_error_norm,
            absolute_integral_tolerance=1e0, # The absolute tolerance the algorithm tries to get the error below
            step_towards_inf_factor=2, # The multiplicative step size used to scan for higher and lower frequencies to add
            bisection_mode_condition=None, # None (the default) here gives only logarithmic bisection when adding internal points
            max_iterations=10000,
        )

        wake = neffint.fourier_integral_fixed_sampling(
            times=times,
            frequencies=frequencies,
            func_values=impedance,
            pos_inf_correction_term=False,
            neg_inf_correction_term=False,
            interpolation=interpolation
        )

    # Normalize
    wake = np.conjugate(wake)/np.pi

    if plane == "longitudinal":
        pass
    elif plane == "transverse":
        wake *= 1j

    return times, wake.real

def compute_neffint(data_time, data_wake,
                    frequencies=np.linspace(1, 5e9, 1000),
                    adaptative=True,
                    interpolation='linear',
                    plane='longitudinal',
                    error='abs'):
    try:
        import neffint
    except:
        raise ImportError('This function uses the python package `neffint` \n \
                           > pip install neffint')
    from scipy.interpolate import interp1d

    if not adaptative:
        impedance = neffint.fourier_integral_fixed_sampling(
            times=frequencies,
            frequencies=data_time,
            func_values=data_wake,
            pos_inf_correction_term=False,
            neg_inf_correction_term=False,
            interpolation=interpolation # `pchip gives artificial imag. baseline`
        )

    # Using adaptative freq. refining
    if adaptative:
        if error.lower() == 'abs':
            interpolation_error_norm = interpolation_error_abs
        elif error.lower() == 'rms':
            interpolation_error_norm = interpolation_error_rms

        func = interp1d(data_time, data_wake,
                        kind='linear', fill_value="extrapolate")

        times, wake = neffint.improve_frequency_range(
            initial_frequencies=data_time,
            func=func,
            interpolation_error_norm=interpolation_error_norm,
            absolute_integral_tolerance=1e0, # The absolute tolerance the algorithm tries to get the error below
            step_towards_inf_factor=2, # The multiplicative step size used to scan for higher and lower frequencies to add
            bisection_mode_condition=None, # None (the default) here gives only logarithmic bisection when adding internal points
            max_iterations=10000,
        )

        impedance = neffint.fourier_integral_fixed_sampling(
            times=frequencies,
            frequencies=times,
            func_values=wake,
            pos_inf_correction_term=False,
            neg_inf_correction_term=False,
            interpolation=interpolation
        )

    # Normalize
    impedance = np.conjugate(impedance)/np.pi/2

    if plane == "longitudinal":
        pass
    elif plane == "transverse":
        impedance *= 1j

    return frequencies, impedance