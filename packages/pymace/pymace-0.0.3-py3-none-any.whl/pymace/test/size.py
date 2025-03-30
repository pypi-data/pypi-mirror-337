import sys
from gc import get_referents
from types import FunctionType, ModuleType


def getsize(obj: any) -> int:
    """ Calculates the size of a given python object

    Args:
        obj (any): Python Object

    Raises:
        TypeError: Can't find the size of function and method type

    Returns:
        int: Size in Bytes
    """
    BLACKLIST = type, ModuleType, FunctionType
    if isinstance(obj, BLACKLIST):
        raise TypeError("getsize() does not take argument of type: " + str(type(obj)))
    seen_ids = set()
    size = 0
    objects = [obj]
    while objects:
        need_referents = []
        for obj in objects:
            if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                seen_ids.add(id(obj))
                size += sys.getsizeof(obj)
                need_referents.append(obj)
        objects = get_referents(*need_referents)
    return size
