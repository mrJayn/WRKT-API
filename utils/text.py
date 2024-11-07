import re
import unicodedata

from django.utils.text import camel_case_to_spaces as _camel_case_to_spaces
from django.utils.regex_helper import _lazy_re_compile


re_camel_case = _lazy_re_compile(r"(?:-|_|\s)([A-Za-z])")
re_title_case = _lazy_re_compile(r"(?:^|-|_|\s)([A-Za-z]+)")


# re_camel_case = _lazy_re_compile( r"(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))")


"""
Text Case Types:
 - camelCase 
 - snake_case 
 - kebab-case 
 - PascalCase 
 - MACRO_CASE 
 - Train-Case
"""


def camel_case(s):
    """Return a copy of a cased string converted to camel case."""
    if s.isupper():
        s = str(s).lower()
    elif s[0].isupper():
        s = s[0].lower() + s[1:]

    def upper_repl(matchobj):
        return matchobj.group(1).upper()

    s = re.sub(r"(?:-|_|\s)([A-Za-z])", upper_repl, s)

    return s.strip()


# ====


def snake_to_camel(value):
    """
    Convert `snake_case` to `camelCase`. Strip surrounding whitespace.
    """
    res = "".join(x.capitalize() for x in value.split("_"))
    return (res[0].lower() + res[1:]).strip()


def camel_to_snake(value):
    """
    Convert `camelCase` to `snake_case`. Strip surrounding whitespace.
    """
    return _camel_case_to_spaces(value)


def as_title(s):

    def title_repl(matchobj):
        return " " + matchobj.group(1).title()

    return re_title_case.sub(title_repl, s).strip()
