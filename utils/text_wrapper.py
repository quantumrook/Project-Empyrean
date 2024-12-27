__tab_spacing = '        '

def format_text_as_wrapped(string_to_wrap: str, add_tab: bool = False, number_of_characters_per_line: int = 80) -> str:
    words = string_to_wrap.split(' ')

    characters_per_row = number_of_characters_per_line
    
    word_count = 0
    word_to_save = ''
    rows = [ ]

    row = __tab_spacing
    if add_tab == False:
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
    for row in rows:
        wrapped_text += row
    
    return wrapped_text

def format_list_as_line_with_breaks(list_to_compress: list[str], add_tab_spacing: bool = False) -> str:
    list_as_single_string = ''

    spacing = __tab_spacing

    if add_tab_spacing == False:
        spacing = ''
    
    for line_number in range(0, len(list_to_compress)):
        list_as_single_string += spacing + list_to_compress[line_number]
        if line_number + 1 < len(list_to_compress):
            list_as_single_string += '\n'


    return list_as_single_string