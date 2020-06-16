import os
from copy import deepcopy

from compiler.parser import Parser, SymbolTable
from compiler.ast import CallBlock, SequenceBlock, CommandBlock, ConditionBlock, simplify

class Interpreter:
    def __init__(self, path, file):
        # collect all results
        results = []
        # we know exactly the structure of the document
        with open(os.path.join(path, file), "r") as file:
            # first line are dimensions and number of definitions and programs
            self.rows, self.cols, self.d, self.e = file.readline().split(" ")
            self.rows = int(self.rows)
            self.cols = int(self.cols)

            # read the labyrinth
            labyrinth = []
            for i in range(int(self.rows)):
                # -1 removes the ending \n
                labyrinth.append(list(file.readline().rstrip()))
            self.labyrinth = labyrinth

            # create symbol table and save procedure definitions
            proc_defs = SymbolTable()
            for i in range(int(self.d)):
                p = Parser(file.readline().rstrip())
                name, program = p.proc_def()
                simplify(program)
                proc_defs.add_definition(name, program)

            # run and interpret different programs
            for i in range(int(self.e)):
                x, y, o = file.readline().rstrip().split(" ")
                p = Parser(file.readline().rstrip())
                ast = p.program()
                simplify(ast)
                # -1 since the indexes start at 1
                results.append(self.interpret_labyrinth_for_program(labyrinth, int(x) - 1, int(y) - 1, o, ast, proc_defs))
        self.results = results

    def get_results(self):
        return self.results

    def interpret_labyrinth_for_program(self, labyrinth, start_x, start_y, start_orientation, ast, proc_definitions):
        # since we want to insert our position into the labyrinth we copy it.
        cur_lab = deepcopy(labyrinth)
        # insert start position
        x = start_x
        y = start_y
        cur_lab[x][y] = start_orientation
        lab, x, y, o = self.interpret_command_and_update_labyrinth(ast, cur_lab, proc_definitions, x, y, start_orientation)
        # index adjustment
        return x + 1, y + 1, o

    def interpret_command_and_update_labyrinth(self, ast, labyrinth, proc_defs, x, y, o):
        node_list = [ast]
        while node_list:
            ast = node_list.pop(0)
            if isinstance(ast, SequenceBlock):
                for n in reversed(ast.sequence):
                    node_list.insert(0, n)
            elif isinstance(ast, CommandBlock):
                if ast.name == "m":
                    # reset position
                    labyrinth[x][y] = "."
                    x, y = self._check_if_move_is_possible(labyrinth, x, y, o)
                    # update position
                    labyrinth[x][y] = o
                elif ast.name == "l":
                    o = self._update_orientation(o)
                    # update orientation
                    labyrinth[x][y] = o
            elif isinstance(ast, CallBlock):
                node_list.insert(0, proc_defs.get_program(ast.name))
            elif isinstance(ast, ConditionBlock):
                if ast.name == "i":
                    if ast.condition == o or (self._check_barrier(labyrinth, x, y, o) and ast.condition == "b"):
                        node_list.insert(0, ast.true_case)
                    else:
                        node_list.insert(0, ast.false_case)
                elif ast.name == "u":
                    if (ast.condition != o and ast.condition != "b") or (
                            ast.condition == "b" and not self._check_barrier(labyrinth, x, y, o)):
                        node_list.insert(0, ast)
                        node_list.insert(0, ast.true_case)
            elif not ast:
                pass
            else:
                raise Exception(f"Node type {ast.__class__} not known.")
        return labyrinth, x, y, o

    def _check_barrier(self, labyrinth, x, y, o):
        n = self.rows - 1
        m = self.cols - 1
        # check four different boarders
        if x == 0 and o == "n":
            return True
        elif x == n and o == "s":
            return True
        elif y == 0 and o == "w":
            return True
        elif y == m and o == "e":
            return True
        # check if next field in labyrinth is barrier
        else:
            if o == "n":
                if labyrinth[x - 1][y] == "#":
                    return True
            elif o == "s":
                if labyrinth[x + 1][y] == "#":
                    return True
            elif o == "e":
                if labyrinth[x][y + 1] == "#":
                    return True
            elif o == "w":
                if labyrinth[x][y - 1] == "#":
                    return True
        return False

    def _update_orientation(self, o):
        if o == "n":
            o = "w"
        elif o == "s":
            o = "e"
        elif o == "e":
            o = "n"
        elif o == "w":
            o = "s"
        return o

    def _check_if_move_is_possible(self, labyrinth, x, y, o):
        n = self.rows - 1
        m = self.cols - 1
        if o == "n":
            if x - 1 < 0:
                return x, y
            if labyrinth[x - 1][y] == ".":
                return x - 1, y
        elif o == "s":
            if x + 1 > n:
                return x, y
            if labyrinth[x + 1][y] == ".":
                return x + 1, y
        elif o == "e":
            if y + 1 > m:
                return x, y
            if labyrinth[x][y + 1] == ".":
                return x, y + 1
        elif o == "w":
            if y - 1 < 0:
                return x, y
            if labyrinth[x][y - 1] == ".":
                return x, y - 1
        else:
            raise Exception(f"Orientation {o} not known.")
        return x, y