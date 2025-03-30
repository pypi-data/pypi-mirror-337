# x23286873_cpp_class_library

# Calculate Discount Tax 
A simple Python library used to calculate the final amount for the given tax rate or discount rate.

## Features

- Calculate Discount Amount
- Calculate Tax Amount

## Installation

You can install the library using pip:

```bash
pip install .

## Usage
from calculate_discount_tax import calculateTax,calculateDiscount
print("Tax Amount:", calculateTax(amount,tax_rate)) #100,5.0 - will return 105
print("Discount Amount ", calculateDiscount(amount,discount_rate)) #100,10 - will return 90
