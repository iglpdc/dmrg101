"""Gets tge real part of a complex number as a double.
"""
def get_real(real_or_complex_number):
    """Gets the real part of a complex number as a double.
    
    If the argument is already a real number does nothing.  It works only with
    numbers, not with other user defined types, such as numpy arrays.

    Parameters
    ----------
    real_or_complex_number : a real or complex number.
        The number you want to get real.
    Returns
    -------
    result : a double
        The real part of `real_or_complex_number`.
    """
    result = real_or_complex_number
    if isinstance(real_or_complex_number, complex):
        result = double(real_or_complex_number.real)
    return result
