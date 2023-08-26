import re

def replace_by_regex(text, regex):
    """Replace symbols by regular expressions
    """
    for pattern, repl in regex:
        text = re.sub(pattern, repl, text)

    return text

def letters_full_to_half(text):
    """Convert English full-width letters to half-width
    """
    converted_text = ""
    offset =  0xFF00 - 0x0020
    for char in text:
        if (ord(char) >= 0x0041 and ord(char) <=  0x005a) \
        or (ord(char) >= 0x0061 and ord(char) <= 0x007a):
            converted_char = chr(ord(char) - offset)
        else:
            converted_char = char
        converted_text += converted_char
    return converted_text

def letters_half_to_full(text):
    """Convert English half-width letters to full-width
    """
    converted_text = ""
    offset =  0xFF00 - 0x0020
    for char in text:
        if (ord(char) >= 0x0041 and ord(char) <=  0x005a) \
        or (ord(char) >= 0x0061 and ord(char) <= 0x007a):
            converted_char = chr(ord(char) + offset)
        else:
            converted_char = char
        converted_text += converted_char
    return converted_text 


