def is_positive(n):
    """
    Check if a number is positive.
    
    Args:
        n: A numeric value (int, float)
        
    Returns:
        bool: True if the number is positive, False otherwise
        
    Raises:
        TypeError: If input is not a numeric type
    """
    # Check if input is a numeric type
    if not isinstance(n, (int, float, complex)):
        raise TypeError("Input must be a numeric type (int, float)")
    
    # For complex numbers, raise an error since "positive" isn't well-defined
    if isinstance(n, complex):
        raise TypeError("Complex numbers don't have a well-defined positivity")
        
    # Check if number is positive
    return n > 0