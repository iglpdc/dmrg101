# 
# File: increase_number_of_states.py
# Author: Ivan Gonzalez
#
"""A module to increase the number of states in the finite algorithm.
"""
def increase_number_of_states(initial_states, final_states,
		              number_of_sweeps):
    """Increases the number of states linearly during the finite algorithm.
    
    During the finite algoeithm not all the sweeps are performed keeping
    the same number of states. A good way to increase the number of states
    linearly in each half-sweep. The last sweep is always performed at
    final number of states.

    Parameters
    ----------
    initial_states : an int.
        The number of states you are keeping at the beginning of the finite
	algorithm, which is the same as the number of states that you ekpt
	at the end of the infinite algorithm.
    final_states : an int.
        The number of states you will keep at the end of the finite
	algorithm.
    number_of_sweeps : an int.
        The number of (full) sweeps during the finite algorithm.
    
    Returns
    -------
    result : a list of ints.
        A list with the number of states kept at each *half-sweep*.

    Examples
    --------
    >>> from dmrg101.core.increase_number_of_states import
    ... increase_number_of_states
    >>> print increase_number_of_states(20, 100, 5)
    0.9
    """
    half_sweeeps_to_increase = 2 * (number_of_sweeps - 1)
    step = (final_states - initial_states) / half_sweeeps_to_increase
    padding = (final_states - initial_states) % half_sweeeps_to_increase
    result = arange(initial_states+padding, final_states, step)
    result.append([final_states, final_states])
    assert(len(result) == 2 * number_of_sweeps)
    return result
