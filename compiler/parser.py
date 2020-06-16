from compiler.scanner import Scanner, ALPHA
from compiler.ast import ConditionBlock, CommandBlock, CallBlock, SequenceBlock

"""
GRAMMAR
<program> := "" | <command> <program>
<command> := "m" | "l" | <proc-call> | "i" <condition> "(" <program> ")(" <program> ")" | "u" <condition> "(" <program> ")"
<condition> := "b" | "n" | "s" | "e" | "w"
<proc-call> := <uppercase-letter>
<proc-def> := <uppercase-letter> "=" <program>
"""

class Parser():
    def __init__(self, input_string):
        self.input_string = input_string
        self.lexer = Scanner(input_string)
        self.desc = None
        self.value = None
        self.next_desc_and_value()

    def next_desc_and_value(self):
         self.desc, self.value = self.lexer.next()

    def program(self):
        if self.desc in ["command", "alpha"]:
            sequence = SequenceBlock()
            command_block = self.command()
            if command_block:
                sequence.add_program(command_block)
            command_block = self.program()
            if command_block:
                sequence.add_program(command_block)
            return sequence

    def command(self):
        node = None
        if self.desc == "command":
            if self.value in ["m", "l"]:
                node = CommandBlock(self.value)
                self.next_desc_and_value()
            elif self.value == "i":
                node = ConditionBlock(self.value)
                self.next_desc_and_value()
                node.set_condition(self.condition())
                # if case
                if self.desc == "lpar":
                    self.next_desc_and_value()
                    node.set_true_case(self.program())
                    if self.desc == "rpar":
                        self.next_desc_and_value()
                        # else case
                        if self.desc == "lpar":
                            self.next_desc_and_value()
                            node.set_false_case(self.program())
                            if self.desc == "rpar":
                                self.next_desc_and_value()
                            else:
                                raise Exception("Expected ) of else case.")
                        else:
                            raise Exception("Expected ( of else case.")
                    else:
                        raise Exception("Expected ) of if case.")
                else:
                    raise Exception("Expected ( of if case.")
            elif self.value == "u":
                node = ConditionBlock(self.value)
                self.next_desc_and_value()
                node.set_condition(self.condition())
                if self.desc == "lpar":
                    self.next_desc_and_value()
                    node.set_true_case(self.program())
                    if self.desc == "rpar":
                        self.next_desc_and_value()
                    else:
                        raise Exception("Expected ) of until case.")
                else:
                    raise Exception("Expected ( of if case.")
            else:
                raise Exception(f"Error, not known command found: ({self.desc}, {self.value}).")
        elif self.desc == "alpha":
            node = self.proc_call()
        else:
            raise Exception(f"Command or program call required. Found: ({self.desc}, {self.value}).")
        return node

    def condition(self):
        if self.desc == "condition":
            condition = self.value
            self.next_desc_and_value()
            return condition
        else:
            raise Exception(f"Expected conditon, found ({self.desc}, {self.value}).")

    def proc_call(self):
        node = CallBlock(self.value)
        self.next_desc_and_value()
        return node

    def proc_def(self):
        if self.desc == "alpha":
            program_name = self.value
            self.next_desc_and_value()
            if self.desc == "equal":
                self.next_desc_and_value()
                return program_name, self.program()
            else:
                raise Exception(f"Error, assumed =, found ({self.desc}, {self.value}).from ")

class SymbolTable():
    def __init__(self):
        self.table = {}

    def add_definition(self, name, program):
        self.table[name] = program

    def get_program(self, name):
        if self.has_program(name):
            return self.table[name]
        else:
            return None

    def has_program(self, name):
        return name in self.table.keys()

    def __str__(self):
        representation = ""
        for name, definition in self.table.items():
            representation += f"{name}: {definition}\n"
        return representation