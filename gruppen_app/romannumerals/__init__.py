
"""
Utilities to handle variable naming with roman numerals.
We will only accept uppercase characters.
"""

from __future__ import unicode_literals

# int2roman taken from Frescobaldi

def is_roman_letter(c, strict_upper = True):
    """
    Checks if c is one of the roman letters.
    If strict_upper == True (default)
    only uppercase letters are accepted.
    """
    if not strict_upper:
        c = c.upper()
    if c in _roman_letters:
        return True
    else:
        return False

def is_roman_letters(inp, strict_upper = True):
    """
    Checks if inp is a roman numeral,
    i.e. a string composed only of roman letters
    (no validity check performed at this stage)
    If strict_upper == True (default)
    only uppercase letters are accepted.
    """
    for c in inp:
        if not is_roman_letter(c, strict_upper):
            return False
    return True

def romansuffix2int(varname):
    """
    Return an integer representing a
    roman numeral suffix to the given varname.
    
    A varname 'testXI' will return 11 (for the 'XI').
    If there is no roman suffix it returns 0.
    If there is an invalid suffix (a string of 
    roman numeral letters that doesn't form a valid number)
    it returns -1.    
    """
    roman = ''
    while len(varname):
        # collect roman numerals from the end of the input string
        c = varname[-1]
        if is_roman_letter(c):
            roman = c + roman
            varname = varname[:-1]
        else:
            break
    return varname, roman2int(roman)


# Thanks: http://billmill.org/python_roman.html
_roman_numerals = (("M", 1000), ("CM", 900), ("D", 500), ("CD", 400),
("C", 100),("XC", 90),("L", 50),("XL", 40), ("X", 10), ("IX", 9), ("V", 5),
("IV", 4), ("I", 1))

def int2roman(n):
    if n < 1:
        return ''
    roman = []
    for ltr, num in _roman_numerals:
        k, n = divmod(n, num)
        roman.append(ltr * k)
    return "".join(roman)

_roman_letters = {'M': 1000, 
                  'D': 500, 
                  'C': 100, 
                  'L': 50, 
                  'X': 10, 
                  'V': 5, 
                  'I': 1}


# Basic conversion routine taken from:
## {{{ http://code.activestate.com/recipes/81611/ (r2)
## and adapted by Urs Liska

def roman2int(inp, strict_upper = True):
   """
   Convert a roman numeral to an integer.
   If strict_upper = True (default)
   only uppercase letters are accepted.
   Returns an integer value or
   -1 if input is invalid
   """
   if not is_roman_letters(inp, strict_upper):
       return -1
   places = []
   for i in range(len(inp)):
      c = inp[i]
      value = _roman_letters[c]
      # If the next place holds a larger number, this value is negative.
      try:
         nextvalue = _roman_letters[inp[i+1]]
         if nextvalue > value:
            value *= -1
      except IndexError:
         # there is no next place.
         pass
      places.append(value)
   sum = 0
   for n in places: sum += n
   # Easiest test for validity...
   if int2roman(sum) == inp.upper():
      return sum
   else:
      return -1
## end of http://code.activestate.com/recipes/81611/ }}}
