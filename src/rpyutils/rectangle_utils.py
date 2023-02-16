from typing import Union, List

Number = Union[int, float]


def add_two(first: Number, second: Number) -> Number:
    """Adds two numbers together.
    It takes two numbers and return the sum of the two.
    Args:
        first (Number): The first number.
        second (Number): The second number.
    Returns:
        Number: The sum of the two numbers.
    """
    sum_result = first + second
    return sum_result


def sum_number_list(number_list: List[Number]) -> Number:
    """Calculates the sum of all the numbers in a list.
    It takes a list of numbers as input and then adds them two by two. Finally it returns the total sum of the numbers in the list.
    Args:
        number_list (List[Number]): A list of numbers.
    Returns:
        Number: The sum of all the values in the input list.
    """
    total = 0
    for number in number_list:
        total = add_two(number, total)
    return total


def mul_two(first: Number, second: Number) -> Number:
    """Multiply two numbers together.
    It takes two numbers and return the multiplication of the two.
    Args:
        first (Number): The first number.
        second (Number): The second number.
    Returns:
        Number: The multiplication of the two numbers.
    """
    mul_result = first * second
    return mul_result


def mul_number_list(number_list: List[Number]) -> Number:
    """Calculates the multiplication of all the numbers in a list.
    It takes a list of numbers as input and then multiply them two by two. Finally it returns the result of the multiplication of all the numbers in the list.
    Args:
        number_list (List[Number]): A list of numbers.
    Returns:
        Number: The multiplication of all the values in the input list.
    """
    total = 1
    for number in number_list:
        total = mul_two(number, total)
    return total
