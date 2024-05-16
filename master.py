from prettytable import PrettyTable
from nltk import Tree
from lexer import Lexer

# Read input from file
with open('input.txt') as file:
    data = file.read()

# Posible Data Type
p_d_t = ['int', 'str', 'float', 'list', 'keyword', 'bool', 'dict', 'tuple', 'set', 'array']

# Lexical Analysis
lexer = Lexer().get_lexer()
tokens = lexer.lex(data)

# Displaying Lexical Analysis output
try:
    table = PrettyTable(["LEXEME", "TOKEN"])
    for token in tokens:
        if token.gettokentype() != "NEWLINE":
            table.add_row([token.getstr(), token.gettokentype()])
    print()
    print("Output source code for Lexical Analysis: ")
    print(table)

except Exception as e:
    print('An error occurred: Unrecognized token name!!')
    print("Error: ", e)

# Symbol Table
x = 0
y = 0
address = {
    "int": 2, "str": 4, "list": 10,
    "float": 4, "keyword": 1, "bool": 1,
    "dict": 16, "tuple": 8, "set": 12,
    "char": 1, "array": None,
}
# list1 = ["int", "b", "str", "c", "float", "a"]  # Assuming this is filled with variable names and types
# list2 = ["b", 2, "c", 5, "a", 7]  # Assuming this is filled with variable names and line numbers
# list3 = []
list1 = ["int", "a", "str", "b", "float", "c"]
list2 = ["a", 2, "b", 5, "c", 7]
list3 = []

# Building symbol table
for j in range(len(list1)):
    if x == len(list1):
        break
    if list1[x] == "int" or list1[x] == 'str' or list1[x] == 'float':
        list3.append([list1[x+1], y, list1[x], 1, list2[x+1], "__"])
        y += address[list1[x]]
        x += 1
    else:
        x += 1

ordered_table = sorted(list3)
unordered_table = list3.copy()

# Displaying symbol table
print()
print("Output symbol table:")
sym_table_table = PrettyTable(["VARIABLE NAME", "OBJ ADDRESS", "DATA TYPE", "DIMENSIONS", "LINE DECLARATION", "LINE REFERENCE"])
for i in ordered_table:
    sym_table_table.add_row(i)
print(sym_table_table)

# Creating symbol table as list of dictionaries
sym_table = []
for i in ordered_table:
    sym_table.append({"Name": i[0], "Address": i[1], "Type": i[2], "Dimensions": i[3], "Line Declared": i[4],
                    "Reference Line": i[5]})

for i in sym_table:
    print(i)
print()

# Parse Table
parse_table1 = {
    'statement_list': {
        'identifier': 'statement ; statement_list',
        'print': 'statement ; statement_list',
        'if': 'statement ; statement_list',
        'while': 'statement ; statement_list',
        ';': 'statement_list',    # grammer is continues to built without new data
        '{': 'statement_list { statement_list } statement_list'
    },
    'statement': {
        'identifier': 'assignment',
        'print': 'print expression ;',
        'if': 'if expression { statement_list }',
        'while': 'while expression { statement_list }'
    },
    'assignment': {
        'identifier': 'identifier = expression ;'
    },
    'print': {
        'print': 'print expression ;'
    },
    'if_statement': {
        'if': 'if expression { statement_list }'
    },
    'while_loop': {
        'while': 'while expression { statement_list }'
    },
    'number': {
        'digit': 'digit'
    },
    'op': {
        '+': '+ term',
        '-': '- term',
        '*': '* term',
        '/': '/ term'
    },
    'string': {
        'identifier': 'identifier',
        'string': 'string'
    },
}

parse_table = {
    'E': {'E': 'E + T', 'T': 'T', 'id': 'T'},
    'T': {'T': 'T * F', 'F': 'F', 'id': 'F'},
    'F': {'id': 'id', '(': '( E )'}
}

# Calculate first
def calculate_first(parse_table):
    first = {}

    for terminal in parse_table.keys():
        first[terminal] = set()
        first[terminal].add(terminal)

    def calculate_first_recursive(symbol):
        if symbol in first:
            return first[symbol]

        first_set = set()

        for production in parse_table[symbol].values():
            production_symbols = production.split()
            for symbol in production_symbols:
                if symbol in first:
                    first_set |= first[symbol]
                    if '' not in first[symbol]:
                        break
                else:
                    first_set |= calculate_first_recursive(symbol)
                    if '' not in first[symbol]:
                        break

        first[symbol] |= first_set
        return first_set

    for non_terminal in parse_table.keys():
        calculate_first_recursive(non_terminal)
    return first

first_sets = calculate_first(parse_table)

print("FIRST sets:")
for symbol, first_set in first_sets.items():
    print(symbol, ":", first_set)
print()

# Calculate follow
def calculate_follow(parse_table, first_sets):
    follow = {non_terminal: set() for non_terminal in parse_table}
    follow[list(parse_table)[0]].add('$')

    def calculate_follow_recursive(symbol, processed=None):
        processed = processed or set()
        if symbol in processed:
            return
        processed.add(symbol)

        for non_terminal, productions in parse_table.items():
            for production in productions.values():
                symbols = production.split()
                if symbol in symbols:
                    idx = symbols.index(symbol)
                    if idx < len(symbols) - 1:
                        next_sym = symbols[idx + 1]
                        follow[symbol] |= set(filter(None, first_sets.get(next_sym, {next_sym})))
                        if '' in first_sets.get(next_sym, {}):
                            calculate_follow_recursive(non_terminal, processed)
                    elif non_terminal != symbol:
                        calculate_follow_recursive(non_terminal, processed)

    for non_term in parse_table:
        calculate_follow_recursive(non_term)
    return follow

follow_sets = calculate_follow(parse_table, first_sets)

print("Follow sets: ")
for sym, follow_set in follow_sets.items():
    print(f"{sym}: {follow_set}")
print()

# Displaying Parse Table
print("Parse Table: ")
for non_terminal, productions in parse_table.items():
    print(f"{non_terminal} ->")
    for terminal, production in productions.items():
        print(f"\t{terminal} -> {production}")

# LL Parser
def ll_parser(input_string, parse_table, follow_sets):
    stack = ['$']
    input_tokens = input_string.split()
    input_tokens.append('$')
    input_index = 0
    stack.append('E')

    while stack:
        top = stack[-1]
        if input_index >= len(input_tokens):
            if top == '$':
                print("Parsing successful!")
                return True
            else:
                print("Parsing error! Current token: $", "Top of stack:", top)
                return False
        current_token = input_tokens[input_index]

        print("Stack:", stack)
        print("Input:", input_tokens[input_index:])

        if top == current_token:
            stack.pop()
            input_index += 1
        elif top in parse_table and current_token in parse_table[top]:
            stack.pop()
            production = parse_table[top][current_token]
            if production != '':
                production_symbols = production.split()[::-1]
                stack.extend(production_symbols)
        elif top in follow_sets and current_token in follow_sets[top]:
            stack.pop()
        else:
            print("Parsing error! Current token:", current_token, "Top of stack:", top)
            return False

    print("Parsing error! Unexpected termination of parsing.")
    return False

input_string = 'id + id * id $'
print()
print("LL parser: ")
success = ll_parser(input_string, parse_table, follow_sets)