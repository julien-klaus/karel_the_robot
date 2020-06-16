import string

SYMBOLS = {
    "m": "command", # move, no effect at barrier
    "l": "command", # turn left 90 degree
    "i": "command", # if <condition> (<program>) (<program>)
    "u": "command", # until <condition> (<program>)
    "b": "condition", # TRUE if next is barrier
    "n": "condition", # TRUE current heading is north
    "s": "condition", # TRUE current heading is south
    "e": "condition", # TRUE current heading is east
    "w": "condition", # TRUE current heading is west
    "(": "lpar",
    ")": "rpar",
    ".": "dot",
    "#": "hash",
    "=": "equal"
}

NUMBER = list([str(i) for i in range(0, 10)])
ALPHA = list(string.ascii_uppercase)


class Scanner():
    def __init__(self, input_string):
        self.input_string = list(input_string)
        self.index = 0
        self.length = len(self.input_string)
        # TODO: add row and column tracker

    def _get_next_character(self):
        if self.index < self.length:
            cur_char = self.input_string[self.index]
            self.index += 1
            return cur_char

    def has_next_character(self):
        return self.index < self.length

    def next(self):
        # returns a description, value pair
        cur_char = self._get_next_character()
        while cur_char in [" "]:
            cur_char = self._get_next_character()
        if cur_char in NUMBER:
            return ("number", cur_char)
        elif cur_char in ALPHA:
            return ("alpha", cur_char)
        elif cur_char in SYMBOLS.keys():
            return (SYMBOLS[cur_char], cur_char)
        elif cur_char == "\n":
            return ("newline", cur_char)
        elif cur_char is None:
            return (None, None)
        else:
            raise Exception(f"Character {cur_char} not known.")