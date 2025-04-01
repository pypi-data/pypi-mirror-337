# tests/test_example.py
import sys
import os

# Add the my_library directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'my_library')))

from example import some_function  # Import the function from the example.py file

def test_some_function():
    """
    This test checks if the some_function returns the expected result.
    """
    result = some_function()  # Call the function
    assert result == "Expected Result"  # Compare the result with the expected value
