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
    def __init__(self, name):
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

def get_nodes(ast):
    nodes = [ast]
    node_list = []
    while nodes:
        node = nodes.pop(0)
        node_list.append(node)
        if isinstance(node, CallBlock):
            pass
        elif isinstance(node, CommandBlock):
            pass
        elif isinstance(node, ConditionBlock):
            if node.true_case:
                nodes.append(node.true_case)
            if node.false_case:
                nodes.append(node.false_case)
        elif isinstance(node, SequenceBlock):
            for seq_node in node.sequence:
                nodes.append(seq_node)
    return node_list


def simplify(ast):
    for node in get_nodes(ast):
        if isinstance(node, ConditionBlock):
            if node.true_case:
                if isinstance(node.true_case, SequenceBlock):
                    if len(node.true_case.sequence) == 1:
                        node.true_case = node.true_case.sequence[0]
            elif node.false_case:
                if isinstance(node.false_case, SequenceBlock):
                    if len(node.false_case.sequence) == 1:
                        node.false_case = node.false_case.sequence[0]
        if isinstance(node, SequenceBlock):
            for index, seq_node in enumerate(node.sequence):
                if isinstance(seq_node, SequenceBlock):
                    if len(seq_node.sequence) == 1:
                        node.sequence[index] = seq_node.sequence[0]
    return ast