"""
HTML_display

Open the DataFrame as a HTML table in the default browser, and in a new tab if possible
"""

import webbrowser
from os import mkdir, path
import datetime


def display(dataframe, output_stream=print):
    """
    Open `dataframe` as a HTML Table in the current browser

    :param dataframe: the Pandas DataFrame to display
    :param output_stream: Function to pass the string version of `dataframe`
    :type dataframe: Pandas DataFrame
    :type output_stream: function that takes in a string
    """
    output_dir = "output_displays"

    try:
        if not path.exists(output_dir):
            mkdir(output_dir)
        filename = path.join(
            output_dir,
            "datafile_display_"
            + datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            + ".html",
        )

        try:
            dataframe.to_html(filename)
            output_stream("Opening {} in browser...".format(filename))
            try:
                webbrowser.open(path.abspath(filename), new=2)
            except Exception as e:
                output_stream(str(e))
                output_stream("There was a problem opening the HTML file")
        except Exception as e:
            output_stream(str(e))
            output_stream("There was a problem creating the HTML file")
    except Exception as e:
        output_stream(str(e))
        output_stream("There was a problem creating the output directory")
