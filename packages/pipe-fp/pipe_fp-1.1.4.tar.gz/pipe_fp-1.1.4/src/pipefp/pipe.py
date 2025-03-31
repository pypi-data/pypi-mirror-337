from functools import reduce
from typing import Callable


def pipe(*f: Callable) -> Callable:
    """
    ## Description
    Functionally streamlines a series of function calls.

    ## Example
    .. code-block:: python
        def title_case(msg: str) -> list[str]:
            return pipe(
                str.lower,
                str.title,
                str.split
            )(msg)
    
    **Returns**
    >>> title_case('WHY, HELLO THERE! 😊')
    ['Why,', 'Hello', 'There!', '😊']
    """

    return lambda x: reduce(lambda a, f: f(a), f, x)
