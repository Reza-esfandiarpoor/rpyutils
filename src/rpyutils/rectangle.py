"""Defines the rectangle class.

This file contains the defintion of the rectangle class.
The rectangle class contains the height and width of a rectangle.
It also provides methods to calculate the area and perimeter of the rectangle.
"""

from . import rectangle_utils


class Rectangle(object):
    """Providing the necessary tools to work with a rectangle.

    This class stores the width and height of a rectangle. It also provides methods for calculating the area and perimeter of the rectangle.

    Args:
        width (Number): The width of the rectangle.
        height (Number): The height of the rectangle.
    """

    def __init__(
        self, width: rectangle_utils.Number, height: rectangle_utils.Number
    ) -> None:
        self.width = width
        self.height = height

    def get_area(self) -> rectangle_utils.Number:
        """Returns the area of the rectangle.

        It calculates the area of the rectangle by multiplying the width and height of the rectangle.

        Returns:
            Number: The area of the rectangle.
        """
        area = rectangle_utils.mul_two(self.width, self.height)
        return area

    def get_perimeter(self) -> rectangle_utils.Number:
        """Returns the perimeter of the rectangle.

        It calculates the perimeter of the rectangle by adding the width and height of the rectangle and multiplying it by two.

        Returns:
            Number: The perimeter of the rectangle.
        """
        half_perimeter = rectangle_utils.add_two(self.width, self.height)
        perimeter = rectangle_utils.mul_two(half_perimeter, 2)
        return perimeter
