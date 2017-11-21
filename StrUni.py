# -----------------------------------------------------------------------------
# isThisStringUnicode
#
# Returns true if String is Unicode
#
def isThisStringUnicode(s):
    """
    Determines if a string is Unicode (return True) or not (returns False)
    to allow correct print operations.

    Used by StrUnicodeOut function.
    Example:
        niceprint('Checking file:[{!s}]...'.format(
                                 file.encode('utf-8') \
                                 if isThisStringUnicode(file) \
                                 else file))

    >>> isThisStringUnicode('No Unicode string')
    False
    >>> isThisStringUnicode(u'Unicode string')
    True
    >>> isThisStringUnicode(2)
    False                                 
    """
    if isinstance(s, unicode):
        return True
    elif isinstance(s, str):
        return False
    else:
        return False


# -----------------------------------------------------------------------------
# StrUnicodeOut
#
# Returns true if String is Unicode
#
def StrUnicodeOut(s):
    """
    Outputs s.encode('utf-8') if isThisStringUnicode(s) esle s
        niceprint('Checking file:[{!s}]...'.format(StrUnicodeOut(file))
    """
    if s is not None:
        return s.encode('utf-8') if isThisStringUnicode(s) else s
    else:
        return ''.encode('utf-8') if isThisStringUnicode('') else ''

