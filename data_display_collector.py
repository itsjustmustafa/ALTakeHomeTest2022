import displays.ASCII_display, displays.HTML_display


def get_displays():
    """
    Returns a list of python modules that are able to display Pandas DataFrames

    :return: list of modules that are able to display DataFrames
    :rtype: list of python modules
    """
    return [displays.ASCII_display, displays.HTML_display]


if __name__ == "__main__":
    print(get_displays())
