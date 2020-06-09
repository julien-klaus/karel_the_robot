# author: Julien Klaus

class ConditionBlock():
    def __init__(self, name, condition=None):
        self.name = name
        self.condition = condition
        self.true_case = None
        self.false_case = None

    def set_condition(self, condition):
        self.condition = condition

    def set_true_case(self, true_case):
        self.true_case = true_case

    def set_false_case(self, false_case):
        self.false_case = false_case

    def __str__(self):
        return f"{self.name}{self.condition}?({str(self.true_case)})" \
               + (f":({str(self.false_case)})" if self.name == "i" else "")

class CommandBlock():
    def __init__(self, name, successor=None):
        self.name = name

    def __str__(self):
        return f"{self.name}"

class CallBlock():
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name}"

class SequenceBlock():
    def __init__(self):
        self.sequence = []

    def add_program(self, program):
        self.sequence.append(program)

    def __str__(self):
        return f"{','.join([str(seq) for seq in self.sequence])}"

