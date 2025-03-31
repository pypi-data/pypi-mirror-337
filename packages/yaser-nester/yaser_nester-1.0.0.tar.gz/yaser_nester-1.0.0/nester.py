'''
A module for printing nested lists.
This module provides a function to recursively print all items in a nested list,
including any sublists.
'''

def print_lol(the_list):
    
    """
    Prints each item in a nested list recursively.

    Args:
        the_list (list): A list that may contain nested lists.

    Returns:
        None

    Examples:
        >>> print_lol([1, 2, [3, 4]])
        1
        2
        3
        4
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
            

