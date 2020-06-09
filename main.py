# author: Julien Klaus

import os
from copy import deepcopy

from compiler.lexer import Lexer
from compiler.parser import Parser, SymbolTable
from compiler.ast import CallBlock, SequenceBlock, CommandBlock, ConditionBlock

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
            results.append(interpret_labyrinth_for_program(labyrinth, int(x)-1, int(y)-1, o, ast, proc_defs))
    return results

def interpret_labyrinth_for_program(labyrinth, start_x, start_y, start_orientation, program, proc_definitions):
    # since we want to insert our position into the labyrinth we copy it.
    cur_lab = deepcopy(labyrinth)
    # insert start position
    x = start_x
    y = start_y
    cur_lab[x][y] = start_orientation
    cur_node = program
    print("Start:", start_x+1, start_y+1, start_orientation)
    lab, x, y, o = interpret_command_and_update_labyrinth(cur_node, cur_lab, proc_definitions, x, y, start_orientation)
    print("Result:", x+1, y+1, o)
    return x+1, y+1, o

def interpret_command_and_update_labyrinth(node, labyrinth, proc_defs, x, y, o):
    node_list = [node]
    while node_list:
        node = node_list.pop(0)
        if isinstance(node, SequenceBlock):
            for n in reversed(node.sequence):
                node_list.insert(0, n)
        elif isinstance(node, CommandBlock):
            if node.name == "m":
                # reset position
                labyrinth[x][y] = "."
                x, y = check_if_move_is_possible(labyrinth, x, y, o)
                # update position
                labyrinth[x][y] = o
                print(labyrinth)
            elif node.name == "l":
                o = update_orientation(o)
                # update orientation
                labyrinth[x][y] = o
                print(labyrinth)
        elif isinstance(node, CallBlock):
            node_list.insert(0, proc_defs.get_program(node.name))
        elif isinstance(node, ConditionBlock):
            if node.name == "i":
                if node.condition == o or check_barrier(labyrinth, x, y, o):
                    node_list.insert(0, node.true_case)
                else:
                    node_list.insert(0, node.false_case)
            elif node.name == "u":
                if node.condition != o and not check_barrier(labyrinth, x, y, o):
                    node_list.insert(0, node)
                    node_list.insert(0, node.true_case)
        elif not node:
            pass
        else:
            raise Exception(f"Node type {node.__class__} not known.")
    return labyrinth, x, y, o

def check_barrier(labyrinth, x, y, o):
    n = len(labyrinth)-1
    m = len(labyrinth[0])-1
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
            if labyrinth[x-1][y] == "#":
                return True
        elif o == "s":
            if labyrinth[x+1][y] == "#":
                return True
        elif o == "e":
            if labyrinth[x][y+1] == "#":
                return True
        elif o == "w":
            if labyrinth[x][y-1] == "#":
                return True

    return False
    #TODO: implement this barrier check
    pass

def update_orientation(o):
    if o == "n":
        o = "w"
    elif o == "s":
        o = "e"
    elif o == "e":
        o = "n"
    elif o == "w":
        o = "s"
    return o

def check_if_move_is_possible(labyrinth, x, y, o):
    n = len(labyrinth)-1
    m = len(labyrinth[0])-1
    if o == "n":
        if x-1 < 0:
            return x, y
        if labyrinth[x-1][y] == ".":
            return x-1, y
    elif o == "s":
        if x+1 > n:
            return x, y
        if labyrinth[x+1][y] == ".":
            return x+1, y
    elif o == "e":
        if y+1 > m:
            return x, y
        if labyrinth[x][y+1] == ".":
            return x, y+1
    elif o == "w":
        if y-1 < 0:
            return x, y
        if labyrinth[x][y-1] == ".":
            return x, y-1
    else:
        raise Exception(f"Orientation {o} not known.")
    return x, y







if __name__ == "__main__":
    test_files = []
    for file in os.listdir("test"):
        if file.endswith("in"):
            test_files.append(file)
            results = parse_test_case_and_get_results(file)
            # check if results are correct
            answers = []
            with open(os.path.join("test", f"{file[:-3]}.ans"), "r") as answer_file:
                answers.append(tuple(answer_file.readline()[:-1].split(" ")))
            for result, answer in zip(results, answers):
                print(result, answer)
                if not (result[0] == int(answer[0]) and result[1] == int(answer[1]) and result[2] == answer[2]):
                    print("Test case not correct.")
            break



