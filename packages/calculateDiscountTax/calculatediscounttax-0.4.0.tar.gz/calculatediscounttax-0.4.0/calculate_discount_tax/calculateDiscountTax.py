import numbers
import decimal 
"""
calculate the tax on the amount for the  given tax rate.
    Parameters:
    - data (amount,tax_rate) : The amount on which tax is to be calculated and the tax rate.

    Returns:
    - float: Returns the final amount after the tax rate.

    Raises:
    - ValueError: If the input parameters are not a postive numeric or decimal values.
    - TypeError: If the input parameters contains non-numeric values.
"""
def calculateTax(amount, tax_rate):
    #check if the input parameters are valid, amount and tax rate are positive values.
    if isinstance(amount,(numbers.Number,decimal.Decimal)) and isinstance(tax_rate,(numbers.Number,decimal.Decimal)) and amount > 0 and tax_rate > 0:
        #if the input parameters are valid then calculate the final amount by adding the tax rate to the amount.
        final_amount = amount + amount * tax_rate / 100
        return round(final_amount,2)
    else:
        #if the input parameters are not valid then return an error message.
        return "please check the input parameters the amount must be a postitive value and tax rate must be a postive decimal value "

"""
calculate the discount on the amount for the  given discount rate.
    Parameters:
    - data (amount,discount_percentage) : The amount on which the discount is to be calculated and the discount percentage rate.

    Returns:
    - float: Returns the final amount after the discount is calculated.

    Raises:
    - ValueError: If the input parameters are not a postive numeric or decimal values.
    - TypeError: If the input parameters contains non-numeric values.
"""
# Calculate Discount Function helps us to calculate the discount on the amount for the  given discount rate.  
def calculateDiscount(amount, discount_percentage):
    #check if the input parameters are valid, amount and discount rate are positive values.
    if isinstance(amount,(numbers.Number,decimal.Decimal)) and isinstance(discount_percentage,(numbers.Number,decimal.Decimal)) and amount > 0 and discount_percentage > 0:
        final_amount = amount - amount * discount_percentage / 100
        #if the input parameters are valid then calculate the final amount by subtracting the discount rate from the amount.
        return round(final_amount,2)
    else:
        #if the input parameters are not valid then return an error message.
        return "please check the input parameters the amount must be a postitive value and discount must be a postive decimal value"
    

    
