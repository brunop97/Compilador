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

def sintatico(tokens):
    var_declaration(tokens)
    statements(tokens)

def var_declaration(tokens):
    # DECLARACAO DO TIPO DAS VARIAVEIS E SEUS NOMES
    if tokens[0][1] == "var":
        tokens.pop(0)
        while tokens and tokens[0][0] in ['ID_VAR']:
            if tokens[0][0] in ['ID_VAR']:
                tokens.pop(0)
                while tokens and tokens[0][0] in ['ID'] and tokens[1][0] not in ['OP_ATRIBUICAO']:
                    declared_id.append(tokens[0][1])  # Add to declared identifiers
                    identifier(tokens)
            else:
                raise SyntaxError("Expected 'ID_VAR' after 'var' declaration")
    else:
        raise SyntaxError("Expected 'var' declaration")

    # Declaracao de valores
    if tokens and tokens[0][1] not in ['if', 'else', 'while']:
        if match(tokens[0][1], declared_id):
            assignment(tokens)
        else:
            raise SyntaxError(f"Identifier '{tokens[0][1]}' not declared OR expected an OP_ARITMETICO")
            

def statements(tokens):
    while tokens:
        if tokens[0][1] == "}":
            return
        else:
            statement(tokens)

def statement(tokens):
    if tokens[0][0] == "CMD_IF":
        verify_if(tokens)
    elif tokens[0][0] == "CMD_WHILE":
        verify_while(tokens)
    else:
        if match(tokens[0][1], declared_id):
            assignment(tokens)
        else:
            raise SyntaxError(f"Identifier '{tokens[0][1]}' not declared")

def verify_if(tokens):
    if tokens[0][0] == "CMD_IF":
        tokens.pop(0)
        if tokens[0][1] == "(":
            tokens.pop(0)
            bin_expression(tokens)
            if tokens[0][1] == ")":
                tokens.pop(0)
                if tokens[0][1] == "{":
                    tokens.pop(0)
                    statements(tokens)
                    if tokens[0][1] == "}":
                        tokens.pop(0)
                        if tokens and tokens[0][0] == "CMD_ELSE":
                            tokens.pop(0)
                            if tokens[0][1] == "{":
                                tokens.pop(0)
                                statements(tokens)
                                if tokens[0][1] == "}":
                                    tokens.pop(0)
                                else:
                                    raise SyntaxError("Expected '}' to end else statements")
                            else:
                                raise SyntaxError("Expected '{' to initiate else statements")
                        else:
                            return
                    else:
                        raise SyntaxError("Expected '}' to end if statements")
                else:
                    raise SyntaxError("Expected '{' to initiate if statements")
            else:
                raise SyntaxError("Expected ')' to end if conditions")
        else:
            raise SyntaxError("Expected '(' to initiate if conditions")

def verify_while(tokens):
    if tokens[0][0] == "CMD_WHILE":
        tokens.pop(0)
        if tokens[0][1] == "(":
            tokens.pop(0)
            bin_expression(tokens)
            if tokens[0][1] == ")":
                tokens.pop(0)
                if tokens[0][1] == "{":
                    tokens.pop(0)
                    statements(tokens)
                    if tokens[0][1] == "}":
                        tokens.pop(0)
                    else:
                        raise SyntaxError("Expected '}' to end while statements")
                else:
                    raise SyntaxError("Expected '{' to initiate while statements")
            else:
                raise SyntaxError("Expected ')' to end while conditions")
        else:
            raise SyntaxError("Expected '(' to initiate while conditions")

def assignment(tokens):
    identifier(tokens)
    if not tokens:
        raise SyntaxError("Expected '=' after identifier, but tokens are empty")
    if tokens[0][0] == "OP_ATRIBUICAO":
        tokens.pop(0)
        math_expression(tokens)
    else:
        raise SyntaxError("Expected '=' after identifier")

def math_expression(tokens):
    term(tokens)
    while tokens and tokens[0][0] == "OP_ARITMETICO":
        op_aritmetico(tokens)
        term(tokens)

def term(tokens):
    if tokens[0][0] == "ID":
        if match(tokens[0][1], declared_id):
            identifier(tokens)
        else:
            raise SyntaxError(f"Identifier '{tokens[0][1]}' not declared")
    elif tokens[0][0] == "NUM":
        number(tokens)
    elif tokens[0][1] == "(":
        tokens.pop(0)
        math_expression(tokens)
        if not tokens:
            raise SyntaxError(f"Expected ')' to end math expression, but tokens are empty")
        if tokens[0][1] == ")":
            tokens.pop(0)
        else:
            raise SyntaxError("Expected ')' to end math expression")
    else:
        raise SyntaxError("Expected identifier or number")

def expression(tokens):
    if tokens[0][1] == "(":
        tokens.pop(0)
        bin_expression(tokens)
        if tokens[0][1] == ")":
            return
        else:
            raise SyntaxError("Expected ')' after expression")
    else:
        raise SyntaxError("Invalid expression")

# FUNCÃO QUE VERIFICA SE HÁ UMA COMPARAÇÃO DENTRO DO PARENTESES DAS FUNCOES
def bin_expression(tokens):
    if tokens[0][0] in ["ID"]:
        tokens.pop(0)
        if tokens[0][0] in ["OP_RELACIONAL"]:
            tokens.pop(0)
        else:
            raise SyntaxError("Expected an 'Operador Binario' after an identifier")

        if tokens[0][0] in ["ID", "NUM"]:
            tokens.pop(0)
            bin_expression(tokens)
        else:
            raise SyntaxError("Expected an 'identifier or Number' after Operador Binario")
    else:
        return

def identifier(tokens):
    if tokens[0][0] in ["ID"]:
        tokens.pop(0)
        if tokens and tokens[0][1] in [',']:
            tokens.pop(0)
    else:
        raise SyntaxError("Invalid identifier")

def number(tokens):
    if tokens[0][0] == "NUM":
        tokens.pop(0)
    else:
        raise SyntaxError("Invalid number")

def op_aritmetico(tokens):
    if tokens[0][0] == "OP_ARITMETICO":
        tokens.pop(0)
    else:
        raise SyntaxError("Invalid Aritmetic Operator")


input_string = '''
var
    int b, x, y, h, ah, z

    b  3.14 + x - ((y * h / ah) ^ z)


'''

tokens = lexico(input_string)

try:
    sintatico(tokens)
    print("\n\nAnalise Lexica e Sintatica Concluida Com Sucesso\n\n")
except SyntaxError as e:
    print(f"Erro de sintaxe: {e}")