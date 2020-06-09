# author: Julien Klaus

import os

from compiler.lexer import Lexer
from compiler.parser import Parser, SymbolTable

def parse_test_case_and_get_results(test_case):
    results = []
    # we know exactly the structure of the document
    with open(os.path.join("test", test_case), "r") as file:
        # first line are dimensions and number of definitions and programs
        r, c, d, e = file.readline().split(" ")
        # read the labyrinth
        labyrinth = []
        for i in range(int(r)):
            # -1 removes the ending \n
            labyrinth.append(list(file.readline())[:-1])
        # create symbol table and save procedure definitions
        proc_defs = SymbolTable()
        for i in range(int(d)):
            p = Parser(file.readline()[:-1])
            name, program = p.proc_def()
            proc_defs.add_definition(name, program)
        # run and interpret different programs
        for i in range(int(e)):
            x, y, o = file.readline()[:-1].split(" ")
            p = Parser(file.readline()[:-1])
            ast = p.program()
            results.append(interpret_labyrinth_for_program(labyrinth, x, y, o, program, proc_defs))
    return results






if __name__ == "__main__":
    test_files = []
    for file in os.listdir("test"):
        if file.endswith("in"):
            test_files.append(file)

    results = parse_test_case_and_get_results(test_files[0])


