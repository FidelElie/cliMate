"""
"""
import sys
import regex
import itertools
import PyInquirer

class IntValidator(PyInquirer.Validator):
    def validate(self, document):
        ok = regex.match("^\d+$", document.text)
        if not ok:
            raise PyInquirer.ValidationError(
                message="Please Enter A Valid Number",
                cursor_position=len(document.text)
            )

class FloatValidator(PyInquirer.Validator):
    def validate(self, document):
        ok = regex.match(
            "^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$", document.text)
        if not ok:
            raise PyInquirer.ValidationError(
                message="Please Enter A Valid Number",
                cursor_position=len(document.text)
            )

def prompt(questions, style=None):
    """Wrapper for Pyinquirer prompt, includes app exit functionality

    Parameters
    ----------
    question: dict, list
        Iterator containing dictionaries of questions
    style: dict
        Style information for styling the command prompt text

    Returns
    -------
    value: dict
        Chosen value(s) for the question(s).
    """
    if style != None:
        if not isinstance(style, dict):
            raise TypeError("Style Data Can Only Be A Dictionary")

    while True:
        if isinstance(questions, dict):
            questions = [questions]
        elif isinstance(questions, list):
            for question in questions:
                if not isinstance(question, dict):
                    raise TypeError("Must Be List Of Dictionaries")
        else:
            message = "Invalid Datatype, Supports Dictionaries or List of Dictionaries"
            raise Exception(message)

        if style is not None:
            value = PyInquirer.prompt(questions, style=style)
        else:
            value = PyInquirer.prompt(questions)

        if len(value) != len(questions):
            dictionary_length = len(value)
            current_question = questions[dictionary_length]
            if current_question["message"] == "Exit Application":
                print("Exiting Application")
                sys.exit()
            exit_prompt = inquirer_confirm("Exit Application", True)
            if exit_prompt:
                print("Exiting Application")
                sys.exit()
        else:
            break

    return value

def inquirer_list(choices = None, message = None, lambda_filter = None):
    """Creates value for Pyinquirer list prompt.

    Parameters
    ---------
    choices: list
        Containing choices for the prompt.
    message: str
        Message that is disaplyed upon the start of the prompt.
    lambda_filter: object
        Lambda function to convert the returned input to a preferable input.

    Returns
    -------
    list_input: value
        Chosen value chosen from the Pyinquirer prompt.

    Example
    -------
    >>> choice_list = ["First Choice", "Second Choice", "Third Choice"]

    >>> message = "Pick Your Choices"

    >>> value = inquirer_list(choice_list, message)

    >>> # dictionary is returned, 'value' key returns choice.
    """
    inq_list = {
        "name": "value",
        "type": "list",
        "choices":  choices if choices is not None else [],
        "message": message if message is not None else ""
    }

    if lambda_filter is not None:
        inq_list["filter"] = lambda_filter

    return prompt(inq_list)["value"]

def inquirer_input(message = None, validator = None, lambda_filter = None,                          default = None):
    """Creates input value from Pyinquirer input prompt.

    Parameters
    ----------
    message: str
        Message that is displayed upon the start of the prompt.
    validator: object
        Validation class to validate input.
    lambda_filter: object
        Lambda function to convert the returned input to a preferable input.
    default: bool
        Default value which is chosen when no value is given.

    Returns
    -------
    inq_input: value
        Output value used for Pyinquirer prompt.

    Example
    -------
    >>> message = "Please Input What You Like"

    >>> int_con = lambda x: int(x)

    >>> int_value = inquirer_input(message=message, lambda_filter=int_con)
    """
    inq_input = {
        "name": "value",
        "type": "input",
        "message": message if message is not None else ""
    }
    if validator is not None:
        inq_input["validate"] = validator

    if lambda_filter is not None:
        inq_input["filter"] = lambda_filter

    if default is not None:
        if isinstance(default, bool):
            inq_input["default"] = default
        else:
            raise TypeError("Inquirer Input Default Argument Expected Boolean")

    return prompt(inq_input)["value"]

def inquirer_checkbox(message = None, choices = None) -> dict:
    """Creates checkbox values from Pyinquirer checkbox prompt.

    Parameters
    ----------
    message: str
        Message that is displayed upon the start of the prompt.
    choices: list
        Containing choices for the prompt.

    Returns
    -------
    inq_checkbox: dict
        Checkbox dictionary used for Pyinquirer prompt.

    Example
    -------
    >>> prompt_message = "This is a checkbox prompt"

    >>> prompt_options = ["Pizza", "Pie", "Chicken"]

    >>> answers = inquirer_checkbox(prompt_message, prompt_options)

    >>> returned_values = answers["value"]
    """
    inq_checkbox = {
        "name": "value",
        "type": "checkbox",
        "choices": [] if choices is not None else choices
    }

    return prompt(inq_checkbox)["value"]

def inquirer_confirm(message = None, default = None) -> bool:
    """Creates value for Pyqinquirer confirmation prompt.

    Parameters
    ----------
    message: str
        Message that is displayed upon the start of the prompt.
    default: bool
        Default value which is chosen when no value is given.

    Returns
    -------
    inq_confirm: dict
        Confirm value used for Pyinquirer prompt.

    Example
    -------
    >>> message = "Confirmation Example"

    >>> default = False

    >>> answer = inquirer_confirm(message, default)["value"]
    """
    inq_confirm = {
        "name": "value",
        "type": "confirm",
        "message": message if message is not None else ""
    }
    if default is not None:
        if isinstance(default, bool):
            inq_confirm["default"] = default
        else:
            raise TypeError("Inquirer Input Default Argument Expected Boolean")

    return prompt(inq_confirm)["value"]

def list_creation(message = None) -> list:
    """Creates a list or array argument with specified datatype(s).

    Parameters
    ----------
    message: str
        Message to be shown before the creation process starts.

    Returns
    -------
    value_list: list
        List containing the specified values for the argument.
    """
    if message != None:
        print("{}\n".format(message))

    int_func, int_args = get_inquirer("int")
    int_args["message"] = "Enter Number Of Values To Add To List"
    number_of_values = int_func(**int_args)

    choice_func, choice_args = get_inquirer("choices")
    choice_args["message"] = "Create List Or Array"
    choice_args["choices"] = ["List", "Array"]
    desired_choice = choice_func(**choice_args)

    if desired_choice == "Array":
        desired_datatype = get_datatype()

    value_list = []
    for i in range(number_of_values):
        if desired_choice == "List":
            desired_datatype = get_datatype()

        value_func, value_args = get_inquirer(desired_datatype)
        datatype_title = DATATYPE_NAMES[DATATYPE_KEYS.index(desired_datatype)]
        value_args["message"] = "{}. {} Value".format(i + 1, datatype_title)
        desired_value = value_func(**value_args)
        value_list.append(desired_value)

    return value_list

def get_datatype() -> str:
    """Returns a user specified datatype to be used elsewhere.

    Returns
    -------
    desired_datatype: str
        User specified datatype from list.
    """
    data_func, data_args = get_inquirer("choices")
    data_args["choices"] = DATATYPE_NAMES
    datatype_call = data_func(**data_args)
    desired_datatype = DATATYPE_KEYS[DATATYPE_NAMES.index(datatype_call)]

    return desired_datatype

def get_inquirer(inquirer_key) -> (object, dict):
    """Returns inquirer information based off of datatype.

    Parameters
    ----------
    inquirer_key: str
        Dictionary key of desired datatype to call from INQUIRER_TABLE.

    Returns
    -------
    inquirer_function: object
        Function taken from inquirer table to call inquirer function.
    inquirer_args: dict
        Arguments to be passed to the inquirer function.
    """
    try:
        inquirer = INQUIRER_TABLE[inquirer_key]
        inquirer_function = inquirer["function"]
        inquirer_args = dict(
            itertools.islice(inquirer.items(), 2, len(inquirer.items())))
    except KeyError:
        raise KeyError(f"Key was not found in the INQUIRER_TABLE got '{key}'")

    return inquirer_function, inquirer_args

INQUIRER_TABLE = {
    "str": {
        "name": "String",
        "function": inquirer_input
    },
    "list": {
        "name": "List",
        "function": list_creation
    },
    "choices": {
        "name": "Choices",
        "function": inquirer_list
        # choices
        # lambda_filter
    },
    "int": {
        "name": "Integer",
        "function": inquirer_input,
        "validator": IntValidator,
        "lambda_filter": lambda x: int(x)
    },
    "float": {
        "name": "Float",
        "function": inquirer_input,
        "validator": FloatValidator,
        "lambda_filter": lambda x: float(x)
    },
    "bool": {
        "name": "Boolean",
        "function": inquirer_list,
        "choices": ["True", "False"],
        "lambda_filter": lambda x: True if x is "True" else False
    }
}

DATATYPE_KEYS = [key for key in INQUIRER_TABLE]

DATATYPE_NAMES = [
    INQUIRER_TABLE[key]["name"] for key in INQUIRER_TABLE if key is not "choices"]

