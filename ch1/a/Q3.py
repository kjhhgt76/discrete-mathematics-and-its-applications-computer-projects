# Question: Give a compound proposition, determine whether it is satisfiable by checking its truth value for all positive assignments of truth values to its propositional variables.

# Input: Compound proposition as a string
# Output: A truth table and the satisfiability.

# Explanation: first, parse the proposition to a tree structure. Store the nodes with atomic variables to a dictionary.
# loop through range(0, 2^(the number of entries in dictionary)). The index is used to assign the truth value to the atomic variables.
# Get the truth value of the whole tree recursively.
# Works for propositions which contains &, |, !, T, F, (, )
# cannot mix & and | in one layer.

class Node:
    def __init__(self, parent=None):
        self.leafs = []
        self.parent = parent
        self.expr = None
        self.truth_value = None

def gen_truth_table(prop):
    satisfiable = False
    print("Proposition: {0}".format(prop))
    root, atomic_vars = proposition_parser(prop)
    for key in atomic_vars:
        print("{0}   ".format(key), end='')
    print("output")
    for i in range(0, 2**len(atomic_vars)):
        len_at = 2**len(atomic_vars) >> 1
        for key in atomic_vars:
            if i & len_at == 0:
                print("0   ", end='')
                atomic_vars[key].truth_value = False
            else:
                print("1   ", end='')
                atomic_vars[key].truth_value = True
            len_at = len_at >> 1
        output = get_truth_value(root)
        if output:
            satisfiable = True
            print("1   ", end='')
        else:
            print("0   ", end='')
        print()
    print("Satisfiable? {0}".format(satisfiable))
    print()
    return satisfiable
def get_truth_value(node):
    if (len(node.leafs) > 0):
        if (node.expr == "&"):
            result = True
            for leaf in node.leafs:
                result = result and get_truth_value(leaf)
            node.truth_value = result
            return node.truth_value
        elif (node.expr == "|"):
            result = False
            for leaf in node.leafs:
                result = result or get_truth_value(leaf)
            node.truth_value = result
            return node.truth_value
        elif (node.expr == '!'):
            result = get_truth_value(node.leafs[0])
            node.truth_value = not result
            return node.truth_value
        elif (node.expr == None):
            result = get_truth_value(node.leafs[0])
            node.truth_value = result
            return node.truth_value
    else:
        return node.truth_value
def proposition_parser(prop):
    root = Node()
    current_node = root
    atomic_vars = {}
    for char in prop:
        if char == ' ':
            continue
        elif char == '(':
            temp_node = Node(current_node)
            current_node.leafs.append(temp_node)
            current_node = temp_node
        elif char == ')':
            current_node = current_node.parent
            if current_node.expr == '!':
                current_node = current_node.parent
        elif char == '!':
            temp_node = Node(current_node)
            temp_node.expr = '!'
            current_node.leafs.append(temp_node)
            current_node = temp_node
        elif char in ['&', '|']:
            if current_node.expr is not None and char != current_node.expr:
                raise ValueError("Detect different connectives in the same depth!")
            current_node.expr = char
        else:
            if char in atomic_vars:
                temp_node = atomic_vars[char]
            elif char == 'F':
                temp_node = Node()
                temp_node.truth_value = False
            elif char == 'T':
                temp_node = Node()
                temp_node.truth_value = True
            else:
                temp_node = Node()
                temp_node.expr = char
                atomic_vars[char] = temp_node

            current_node.leafs.append(temp_node)
            if current_node.expr == '!':
                current_node = current_node.parent

    return root, atomic_vars



if __name__ == "__main__":
    satisfiable_props = [ "T",
                          "p | T",
                          "q | F",
                          "p & q",
                          "p | q",
                          "(p | q)",
                          "!(p | q)",
                          "!p | !q",
                          "!(p & !p)",
                          "(p & q) | r",
                          "!(p & q) | r",
                          "(p & p) | p",
                          "!((p & p) | p)",
                          "(p & !p) | p",
                          "(p & !p) | q",
                          "((!(( p & q ) | (!p & !q)) & ( r | s )) | q)",
                          "((!r | s) & p) | (r & !(!p | !r)",
                          "(p & q) | (!p & !q)"
                          ]
    for prop in satisfiable_props:
        gen_truth_table(prop)
    unsatisfiable_props = ["F",
                           "p & !p",
                           "(p & !p) | (q & !q)",
                         "(!p & p) | ((!s & s) & (p | q | r) & T) | (T & ( (r & !r) | (q & !q)))"
                         ]
    for prop in unsatisfiable_props:
        gen_truth_table(prop)