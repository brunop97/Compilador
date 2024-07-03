import re

declared_id = []

def match(word, vector):
    return any(word == item for item in vector)

def lexico(input_string):
    tokens = []

    # Regular expressions for matching different token types
    token_patterns = [
        (r'if\b', 'CMD_IF'),
        (r'else\b', 'CMD_ELSE'),
        (r'while\b', 'CMD_WHILE'),
        (r'(var|int|float|char|real)\b', 'ID_VAR'),
        (r'\d+(\.\d+)?', 'NUM'),
        (r'[A-Za-z_][A-Za-z0-9_]*', 'ID'),
        (r'[+\-*/^]', 'OP_ARITMETICO'),
        (r'[><]=?|<>|==', 'OP_RELACIONAL'),
        (r'=', 'OP_ATRIBUICAO'),
        (r'[;[\](){}.,]', 'DELIMITADOR')
    ]

    # Tokenize the input string
    while input_string:
        match = None
        for token_pattern, token_type in token_patterns:
            regex = re.compile(token_pattern)
            match = regex.match(input_string)
            if match:
                tokens.append([token_type, match.group(0)])
                input_string = input_string[match.end():]
                break
        if not match:
            #undefined characters
            input_string = input_string[1:]

    return tokens

def generate_C3E(tokens):
    temp_count = 0
    label_count = 0

    def new_temp():
        nonlocal temp_count
        temp_name = f"T{temp_count}"
        temp_count += 1
        return temp_name

    def new_label():
        nonlocal label_count
        label_name = f"L{label_count}"
        label_count += 1
        return label_name

    C3E_code = []

    def var_declaration(tokens):
        if tokens and tokens[0][1] == "var":
            tokens.pop(0)
            C3E_code.append(f"var")
            while tokens and tokens[0][0] in ['ID_VAR']:
                if tokens and tokens[0][0] in ['ID_VAR']:
                    type_token = tokens.pop(0)
                    while tokens and tokens[0][0] in ['ID'] and tokens[1][0] not in ['OP_ATRIBUICAO']:
                        identifier = tokens.pop(0)
                        declared_id.append(identifier[1])  # Add to declared identifiers
                        C3E_code.append(f"{type_token[1]} {identifier[1]}")
                        if tokens and tokens[0][1] == ',':
                            tokens.pop(0)
                else:
                    raise SyntaxError("Expected 'ID_VAR' after 'var' declaration")
        else:
            raise SyntaxError("Expected 'var' declaration")

    def statements(tokens):
        while tokens:
            if tokens and tokens[0][1] == "}":
                return
            else:
                statement(tokens)

    def statement(tokens):
        if tokens and tokens[0][0] == "CMD_IF":
            verify_if(tokens)
        elif tokens[0][0] == "CMD_WHILE":
            verify_while(tokens)
        else:
            if match(tokens[0][1], declared_id):
                assignment(tokens)
            else:
                raise SyntaxError(f"Identifier '{tokens[0][1]}' not declared")

    def verify_if(tokens):
        if tokens and tokens[0][0] == "CMD_IF":
            tokens.pop(0)
            if tokens and tokens[0][1] == "(":
                tokens.pop(0)
                cond_expr = bin_expression(tokens, invert=False)
                if tokens and tokens[0][1] == ")":
                    tokens.pop(0)
                    true_label = new_label()
                    false_label = new_label()
                    C3E_code.append(f"if {cond_expr} goto {true_label}")
                    C3E_code.append(f"goto {false_label}")
                    C3E_code.append(f"{true_label}:")
                    if tokens and tokens[0][1] == "{":
                        tokens.pop(0)
                        statements(tokens)
                        if tokens and tokens[0][1] == "}":
                            tokens.pop(0)
                            if tokens and tokens[0][0] == "CMD_ELSE":
                                end_label = new_label()
                                C3E_code.append(f"goto {end_label}")
                                C3E_code.append(f"{false_label}:")
                                tokens.pop(0)
                                if tokens and tokens[0][1] == "{":
                                    tokens.pop(0)
                                    statements(tokens)
                                    if tokens and tokens[0][1] == "}":
                                        tokens.pop(0)
                                        C3E_code.append(f"{end_label}:")
                                    else:
                                        raise SyntaxError("Expected '}' to end else statements")
                                else:
                                    raise SyntaxError("Expected '{' to initiate else statements")
                            else:
                                C3E_code.append(f"{false_label}:")
                        else:
                            raise SyntaxError("Expected '}' to end if statements")
                    else:
                        raise SyntaxError("Expected '{' to initiate if statements")
                else:
                    raise SyntaxError("Expected ')' to end if conditions")
            else:
                raise SyntaxError("Expected '(' to initiate if conditions")

    def verify_while(tokens):
        if tokens and tokens[0][0] == "CMD_WHILE":
            tokens.pop(0)
            if tokens and tokens[0][1] == "(":
                tokens.pop(0)
                cond_expr = bin_expression(tokens, invert=True)
                if tokens and tokens[0][1] == ")":
                    tokens.pop(0)
                    begin_label = new_label()
                    end_label = new_label()
                    C3E_code.append(f"{begin_label}:")
                    C3E_code.append(f"if {cond_expr} goto {end_label}")
                    if tokens and tokens[0][1] == "{":
                        tokens.pop(0)
                        statements(tokens)
                        C3E_code.append(f"goto {begin_label}")
                        if tokens and tokens[0][1] == "}":
                            tokens.pop(0)
                            C3E_code.append(f"{end_label}:")
                        else:
                            raise SyntaxError("Expected '}' to end while statements")
                    else:
                        raise SyntaxError("Expected '{' to initiate while statements")
                else:
                    raise SyntaxError("Expected ')' to end while conditions")
            else:
                raise SyntaxError("Expected '(' to initiate while conditions")

    def assignment(tokens):
        identifier = tokens.pop(0)[1]
        if tokens and tokens[0][0] == "OP_ATRIBUICAO":
            tokens.pop(0)
            expr = expression(tokens)
            C3E_code.append(f"{identifier} = {expr}")
        else:
            raise SyntaxError("Expected '=' after identifier")

    def expression(tokens):
        left = term(tokens)
        while tokens and tokens[0][0] == "OP_ARITMETICO":
            op = tokens.pop(0)[1]
            right = term(tokens)
            temp = new_temp()
            C3E_code.append(f"{temp} = {left} {op} {right}")
            left = temp
        return left

    def term(tokens):
        left = fator(tokens)
        while tokens and tokens[0][0] == "OP_ARITMETICO" and tokens[0][1] in "*/":
            op = tokens.pop(0)[1]
            right = fator(tokens)
            temp = new_temp()
            C3E_code.append(f"{temp} = {left} {op} {right}")
            left = temp
        return left

    def fator(tokens):
        if tokens[0][1] == "(":
            tokens.pop(0)
            expr = expression(tokens)
            if tokens[0][1] == ")":
                tokens.pop(0)
                return expr
            else:
                raise SyntaxError("Expected ')' after expression")
        elif tokens[0][0] == "ID":
            if match(tokens[0][1], declared_id):
                return tokens.pop(0)[1]
            else:
                raise SyntaxError(f"Identifier '{tokens[0][1]}' not declared")
        elif tokens[0][0] == "NUM":
            return tokens.pop(0)[1]
        else:
            raise SyntaxError("Invalid factor")

    def bin_expression(tokens, invert=False):
        left = term(tokens)
        if tokens and tokens[0][0] in ["OP_RELACIONAL"]:
            op = tokens.pop(0)[1]
            right = term(tokens)
            if invert:
                if op == ">":
                    op = "<="
                elif op == "<":
                    op = ">="
                elif op == ">=":
                    op = "<"
                elif op == "<=":
                    op = ">"
            return f"{left} {op} {right}"
        else:
            raise SyntaxError("Expected a relational operator")

    var_declaration(tokens)
    statements(tokens)

    return C3E_code

input_string = '''
var
   int cont, num, contador
   real cont2

   num = 0
while(cont < 10) {
   cont2 = 3.1415 * contador ^ 2
   if (cont < 5) {
      num = num + cont2
   }
   else {
      cont = 0
   }
      cont = cont + 1
}
'''

tokenC3E = lexico(input_string)

try:
    declared_id = []
    C3E_code = generate_C3E(tokenC3E)
    print("\n\nDDS C3E do Programa:\n")
    for line in C3E_code:
        print(line)

except SyntaxError as e:
    print(f"Erro de sintaxe: {e}")