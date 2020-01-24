"""
"""
def map_int(to_int) -> int:
    """Maps value to integer from a string.

    Parameters
    ----------
    to_int: various (usually str)
        Value to be converted to integer

    Returns
    -------
    mapped_int: int
        Value mapped to integer.

    Examples
    --------
    >>> number_one = "1"

    >>> error_value = "will cause error"

    >>> one_to_float = map_int(number_one) # will convert to 1

    >>> error_to_float = map_int(error_value) # will cause exception
    """
    try:
        mapped_int = int(to_int)
    except ValueError:
        raise ValueError("Integer Value Expected Got '{}'".format(to_int))

    return mapped_int

def map_float(to_float) -> float:
    """Maps value to float from a string.

    Parameters
    ----------
    to_float: various (usually str)
        Value to be converted to float.

    Returns
    -------
    mapped_float: float
        Value mapped to float.

    Examples
    --------
    >>> number_one = "1"

    >>> error_value = "will cause error"

    >>> one_to_float = map_float(number_one) # will convert to 1.0

    >>> error_to_float = map_float(error_value) # will cause exception
    """
    try:
        mapped_float = float(to_float)
    except ValueError:
        raise ValueError("Float Value Expected Got '{}'".format(to_float))

    return mapped_float

def map_bool(to_bool) -> bool:
    """Maps value to boolean from a string.

    Parameters
    ----------
    to_bool: str
        Value to be converted to boolean.

    Returns
    -------
    mapped_bool: bool
        Boolean value converted from string.

    Example
    -------
    >>> boolean_string = "True" # can also be lower case

    >>> boolean_value = map_bool(boolean_string)
    """
    try:
        boolean_map = {"true": True, "false": False}
        mapped_bool = boolean_map[to_bool.lower()]
    except KeyError:
        raise KeyError("Boolean Value Expected got '{}'".format(to_bool))

    return mapped_bool

def map_list(to_list, type_table) -> list:
    """Maps list values with specific data types.

    Parameters
    ----------
    to_list: str
        String containing a list for conversion.
    type_table: list, tuple
        Contains the data type strings corresponding to CONVERSION_TABLE.

    Returns
    -------
    mapped_list: list
        List converted from string.

    Example
    -------
    >>> list_string = ["1", "3", "True", "5"]

    >>> conversion_table = ["int", "float", "bool", "float"]

    >>> mapped_list = map_list(list_string, conversion_table)
    """
    try:
        brackets = ["[", "]", "(", ")", "{", "}"]
        translation_dict = {bracket:"" for bracket in brackets}
        translated_list = to_list.translate(str.maketrans(translation_dict))
        mapped_list = [value.strip() for value in translated_list.split(",")]

        if len(mapped_list) != len(type_table):
            raise ValueError("Values Do Not Match Number Of Conversions")

        for i in range(len(mapped_list)):
            mapped_list[i] = CONVERSION_TABLE[type_table[i]](mapped_list[i])

    except KeyError:
        raise KeyError("Type Given Was Not Found In Conversion Table Got {}".format(type_table[i]))

    return mapped_list

def map_choice(value) -> str:
    """

    Parameters
    ----------
    value: str

    Returns
    -------
    value: str
        Value that was chosen.
    """
    return value

CONVERSION_TABLE = {
    "str": str,
    "int": map_int,
    "bool": map_bool,
    "list": map_list,
    "float": map_float,
    "choices": map_choice
}
