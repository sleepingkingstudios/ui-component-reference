from re import split, sub


def _kebab_case_word(word: str) -> str:
    normal = sub(r'[^\w]+', '', word)
    chars = (f'-{char.lower()}' if char.isupper() else char for char in normal)

    return sub(r'^-', '', ''.join(chars))


def kebab_case(string: str) -> str:
    """
    Converts a string to kebab-case.

    First, separates the string into words. Then, for each word:

    - Normalizes the word by removing non-letter, non-digit characters.
    - Replaces any uppercase characters with the lowercase letter
      preceded by a dash.
    - Trims a leading dash, if any.

    Finally, joins the words with dash characters.

    Arguments:
        string (str): The input to process.

    Returns:
        str: The input string in kebab-case.
    """
    words = split(r'[ \-_]', string)
    words = (_kebab_case_word(word) for word in words)

    return '-'.join(words)
