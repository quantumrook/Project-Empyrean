"""A series of helper functions to format text or lists of text.
"""
__TAB_SPACING = '        '

def format_text_as_wrapped(string_to_wrap: str, add_tab: bool = False, number_of_characters_per_line: int = 80) -> str:
    """Takes a string and returns a formatted string with line breaks 
    according to the desired number of characters per line. Will start
    a new line early if the current word will not fit.

    Args:
        string_to_wrap (str): The string that is too long to be displayed properly.
        add_tab (bool, optional): Adds whitespace to the wrapped string to simulate
        paragraph indenting. Defaults to False.
        number_of_characters_per_line (int, optional): Number of characters to fit
        to each line. Defaults to 80.

    Returns:
        str: The formatted string.
    """
    words = string_to_wrap.split(' ')

    characters_per_row = number_of_characters_per_line

    word_count = 0
    word_to_save = ''
    rows = [ ]

    row = __TAB_SPACING
    if not add_tab:
        row = ''

    row_length = len(row)

    for word in words:
        if row_length == 0 and word_to_save != '':
            row += word_to_save
            row_length = len(word_to_save)
            word_to_save = ''

        if (row_length + len(word)) <= characters_per_row:
            row_length += 1 + len(word)
            row += ' ' + word
        elif (row_length + len(word)) > characters_per_row:
            word_to_save = word
            row_length = 0
            rows.append(row + "\n")
            row = ''

        word_count += 1
        if word_count >= len(words):
            rows.append(row)

    wrapped_text = ''
    for row in rows: #TODO use .join instead
        wrapped_text += row

    return wrapped_text

def format_list_as_line_with_breaks(list_to_compress: list[str], add_tab_spacing: bool = False) -> str:
    """Converts a list of strings into one string with new lines.

    Args:
        list_to_compress (list[str]): The list of strings.
        add_tab (bool, optional): Adds whitespace to the wrapped string to simulate
        paragraph indenting. Defaults to False.

    Returns:
        str: _description_
    """
    list_as_single_string = ''

    spacing = __TAB_SPACING

    if not add_tab_spacing:
        spacing = ''

    for line_number in range(0, len(list_to_compress)): #TODO refactor?
        list_as_single_string += spacing + list_to_compress[line_number]
        if line_number + 1 < len(list_to_compress):
            list_as_single_string += '\n'

    return list_as_single_string
