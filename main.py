# author: Julien Klaus

import os
from time import time

from compiler.interpreter import Interpreter


if __name__ == "__main__":
    path = "test"
    test_cases = 0
    correct = 0
    print("Start checking test cases ...")
    start = time()
    for file in os.listdir(path):
        if file.endswith("in"):
            i = Interpreter(path, file)
            results = i.get_results()
            # check if results are correct
            answers = []
            with open(os.path.join(path, f"{file[:-3]}.ans"), "r") as answer_file:
                line = answer_file.readline().strip()
                while line:
                    answers.append(tuple(line.split(" ")))
                    line = answer_file.readline().strip()
            for result, answer in zip(results, answers):
                test_cases += 1
                if not (result[0] == int(answer[0]) and result[1] == int(answer[1]) and result[2] == answer[2]):
                    print("Test case[s] not correct in", file)
                else:
                    correct += 1
    print(f"{time()-start}s")
    print(f"... {correct} of {test_cases} done correct.")
