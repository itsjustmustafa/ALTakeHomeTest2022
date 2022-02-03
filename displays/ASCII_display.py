"""
ASCII_display

A simple ASCII display of the DataFrame
"""

import pandas as pd


def display(dataframe, output_stream=print):
    """
    Pass the string version of `dataframe` through the `output_method`

    :param dataframe: the Pandas DataFrame to display
    :param output_stream: Function to pass the string version of `dataframe`
    :type dataframe: Pandas DataFrame
    :type output_stream: function that takes in a string
    """
    output_stream(dataframe.to_string())
