def sintatico(tokens):
    var_declaration(tokens)
    statements(tokens)

def var_declaration(tokens):
    #DECLARACAO DO TIPO DAS VARIAVEIS E SEUS NOMES
    if tokens[0][1] == "var":
        tokens.pop(0)
        while(tokens[0][0] in ['ID_VAR']):
            if tokens[0][1] in ['int', 'real']:
                tokens.pop(0)
                #print(tokens[0][0], tokens[1][0])
                while tokens[0][0] in ['ID'] and tokens[1][0] not in ['OP_ATR']:
                    identifier(tokens)
            else:
                raise SyntaxError("Expected 'int' or 'real' after 'var' declaration")
    else:
        raise SyntaxError("Expected 'var' declaration")

    #DECLARACAO DE VALOR DE VARIAVEL
    if tokens[0][0] in ['ID'] and tokens[1][0] in ['OP_ATR']:
        tokens.pop(0) #elimina o identificador
        tokens.pop(0) #elimina o igual
        if tokens [0][0] in ['ID', 'NUM']:
            tokens.pop(0)
        else:
            raise SyntaxError("Expected 'ID' or 'NUM' declaration")

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
        assignment(tokens)

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
                        if tokens[0][0] == "CMD_ELSE":
                            tokens.pop(0)
                            if tokens[0][1] == "{":
                                tokens.pop(0)
                                statements(tokens)
                                if tokens[0][1] == "}":
                                    tokens.pop(0)
                                else:
                                    raise SyntaxError("Expected '}' after statements")
                            else:
                                raise SyntaxError("Expected '{' after else condition")
                        else:
                            return
                    else:
                        raise SyntaxError("Expected '}' after statements")
                else:
                    raise SyntaxError("Expected '{' after if condition")
            else:
                raise SyntaxError("Expected ')' after if condition")
        else:
            raise SyntaxError("Expected '(' after 'if'")

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
                        raise SyntaxError("Expected '}' after statements")
                else:
                    raise SyntaxError("Expected '{' after while condition")
            else:
                raise SyntaxError("Expected ')' after while condition")
        else:
            raise SyntaxError("Expected '(' after 'while'")    

def assignment(tokens):
    identifier(tokens)
    if tokens[0][1] == "=":
        tokens.pop(0)
        math_expression(tokens)
    else:
        raise SyntaxError("Expected '=' after identifier")

def math_expression(tokens):
    if tokens[0][0] == "ID":
        identifier(tokens)
        math_expression(tokens)
    elif tokens[0][0] == "NUM":
        number(tokens)
        math_expression(tokens)
    elif tokens[0][0] == "OP_ARIT":
        op_aritmetico(tokens)
        math_expression(tokens)
    else:
        return

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

#FUNCAO QUE VERIFICA SE HÁ UMA COMPARAÇAO DENTRO DO PARENTESES DAS FUNCOES
def bin_expression(tokens):
    if tokens[0][0] in ["ID"]:
        tokens.pop(0)
        #if tokens[0][0] in ["OP_MOI", "OP_MOE", "OP_DIF", "OP_IGU", "OP_MAI", "OP_MEN", "OP_ATR"]:
        if tokens[0][0] in ["OP_BINARIO"]:
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
        if tokens[0][1] in [',']:
            tokens.pop(0)
    else:
        raise SyntaxError("Invalid identifier")

def number(tokens):
    if tokens[0][0] == "NUM":
        tokens.pop(0)
    else:
        raise SyntaxError("Invalid number")

def op_aritmetico(tokens):
    if tokens[0][0] == "OP_ARIT":
        tokens.pop(0)
    else:
        raise SyntaxError("Invalid Aritmetic Operator")

def exibe_imprime():
    """escreve no arquivo de saida"""
    arq = open("C:/Users/Bruno/Documents/GitHub/Compilador/SaidaAnalisadorSintatico.txt", "w")
    arq.write("Analise Sintatica Concluida Com Sucesso")    
    print("\n\nAnalise Sintatica Concluida Com Sucesso\n\n")
    arq.close()

def processar_linha(linha):
    linha = linha.replace('[', '').replace(']', '')  # Remove os colchetes
    tokens = []
    dentro_aspas_simples = False
    token_atual = ''
    for char in linha:
        if char == "'" and not dentro_aspas_simples:
            dentro_aspas_simples = True
        elif char == "'" and dentro_aspas_simples:
            dentro_aspas_simples = False
        elif char == ',' and not dentro_aspas_simples:
            tokens.append(token_atual.strip())  # Adiciona o token atual à lista de tokens
            token_atual = ''
        else:
            token_atual += char
    tokens.append(token_atual.strip())  # Adiciona o último token após a última vírgula
    return tokens

def ler_arquivo_txt(arquivo):
    tokens = []
    with open(arquivo, 'r') as arquivo_txt:
        linhas = arquivo_txt.readlines()
        for linha in linhas:
            tokens.append(processar_linha(linha))
    return tokens


arquivo = 'C:/Users/Bruno/Documents/GitHub/Compilador/SaidaAnalisadorLexico.txt'

# Input Automatico dos Tokens pelo arquivo TXT
tokens = ler_arquivo_txt(arquivo)

# Input Manual dos Tokens sem arquivo TXT
# tokens = [
#     ['ID_VAR', 'var'],
#     ['ID_VAR', 'int'],
#     ['ID', 'cont'],
#     ['DELIM', ','],
#     ['ID', 'num'],
#     ['ID_VAR', 'real'],
#     ['ID', 'cont2'],
#     ['ID', 'num'],
#     ['OP_ATR', '='],
#     ['NUM', '0'],
#     ['CMD_WHILE', 'while'],
#     ['DELIM', '('],
#     ['ID', 'cont'],
#     ['OP_BINARIO', '<'],
#     ['NUM', '10'],
#     ['DELIM', ')'],
#     ['DELIM', '{'],
#     ['ID', 'cont2'],
#     ['OP_ATR', '='],
#     ['NUM', '3.1415'],
#     ['OP_ARIT', '*'],
#     ['ID', 'contador'],
#     ['NUM', '2'],
#     ['CMD_IF', 'if'],
#     ['DELIM', '('],
#     ['ID', 'cont'],
#     ['OP_BINARIO', '<'],
#     ['NUM', '5'],
#     ['DELIM', ')'],
#     ['DELIM', '{'],
#     ['ID', 'num'],
#     ['OP_ATR', '='],
#     ['ID', 'num'],
#     ['OP_ARIT', '+'],
#     ['ID', 'cont2'],
#     ['DELIM', '}'],
#     ['CMD_ELSE', 'else'],
#     ['DELIM', '{'],
#     ['ID', 'cont'],
#     ['OP_ATR', '='],
#     ['NUM', '0'],
#     ['DELIM', '}'],
#     ['ID', 'cont'],
#     ['OP_ATR', '='],
#     ['ID', 'cont'],
#     ['OP_ARIT', '+'],
#     ['NUM', '1'],
#     ['DELIM', '}'],
# ]

#print(tokens)

sintatico(tokens)
exibe_imprime()

