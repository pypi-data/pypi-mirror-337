"""
Calcluate Discount Tax - A library that is used to calculate the final price of the amount after calculating the discount or tax.
- Calculate Tax Rate for the amount
- Calculate the discount rate for the amount
"""

from .calculateDiscountTax import calculateTax, calculateDiscount

__all__ = ['calculateTax', 'calculateDiscount']

def __version__():
    """Return the version of the calculate discount tax package."""
    return "0.0.1"

def describe():
   
    description = (
        """This Package is used to calculate the discount and tax for the final amount.\n
        Developer: Nidhi Anandan\n
        college: National College of Ireland, Ireland\n
        Project: Cloud Platform Programming\n
        """
        "Version: {}\n"
        "Provides basic tax and discount calculations including:\n"
        "  - Calculate Tax Rate for the amount\n"
        "  - Calculate the discount rate for the amount\n"
    ).format(__version__())
    print(description)