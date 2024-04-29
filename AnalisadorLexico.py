import sys
import re

token = ""
numerico = ""
relacional = ""
estado = 0
separadores = [';', '[', ']', ')', '(', ')', '{', '}', ',', '.']
operadores = ['-', '+', '/', '*']
token_geral = []
linha = 0
coluna = 0

def verifica_erro(elemento, token_geral, linha, coluna):
    """Se não encontrar um erro retorna 1"""
    if not re.match("[\w]", elemento):
        if elemento not in separadores:
            if elemento not in operadores:
                if elemento != '=':
                    if not re.search(r"\s", elemento):
                        token_geral.append("[Token Inválido]")
                    return 0
    return 1

def exibe_imprime(lista):
    """escreve no arquivo de saida"""
    arq = open("C:/Users/Bruno/Documents/GitHub/Compilador/SaidaAnalisadorLexico.txt", "w")
    if(len(lista) == 0):
        arq.write("Lista vazia\n")
    for i in lista:
        print (i)
        arq.write(str(i) + "\n")

    arq.close()

def add_linha_coluna(token, linha, coluna):
    """Adiciona linha e coluna"""
    p_inicio = coluna - len(token)
    return "L:" + str(linha) + " C:(" + str(p_inicio) + "," + str(coluna) + ")"

def ver_iden(elemento):
    """ Verifica se o elemento é um separador dos numeros """
    if(re.match(r"[\w]", elemento)):
        return 0
    else:
        return 1

def ver_num(elemento):
    """Verifica se o elemento pertence ao grupo das constantes numericas"""
    if(re.match(r"[\d.]", elemento)):
        return 0
    else:
        """Se ele não pertence retorna 1"""
        return 1

def ver_rel(elemento):
    """ Verifica se o elemento é um separador dos numeros """
    if(re.match(r"[\s]", elemento)):
        return 1
    else:
        return 0

def verifica_reservada(token):
    """ Verifica se determinado token é reservado e retorna um código para o mesmo """
    reservada_list = ['if', 'else', 'while', 'int', 'float', 'real', 'char']
    cont = 0
    for i in reservada_list:
        cont = cont + 1
        if (token == i):
            return cont

def verifica_relacional(token):
    """ Verifica se determinado token é reservado e retorna um código para o mesmo """
    reservada_list = ['>=', '<=', '<>', '==']
    cont = 0
    for i in reservada_list:
        cont = cont + 1
        if (token == i):
            return cont

def open_file():
    """Abre o arquivo de entrada"""
    try:
        arquivo = open("C:/Users/Bruno/Documents/GitHub/Compilador/DadosEntradaAnalisador.txt", "r")
    except Exception as e:
        print ("Erro ao abrir o arquivo!!")
    return arquivo

arquivo = open_file()
for i in arquivo:
    linha = linha + 1
    coluna = 0
    for k in i:
        coluna = coluna + 1
        if estado == 0:
            """ Pesquisa por identificadores validos """
            if re.match(r"([A-Za-z_])", k) and estado == 0:              
                estado = 1  # Identificador   
            """ Pesquisa por Constante Numérica """
            if re.match(r"[0-9]", k) and estado == 0:
                estado = 2  # Constante Numérica        
            """ Pesquisa por Operadores Aritméticos """
            if re.match(r"[+\-*/]", k) and estado == 0:
                estado = 3
            """ Pesquisa por Operadores Relacionais """
            if re.match(r"[<>=]", k) and estado == 0:
                estado = 4
            if re.match(r"[()[\]{}]", k) and estado == 0:
                estado = 5

        if estado == 1:
            """ Valida Identificador """
            """ \w = Corresponde a caracteres de palavras Unicode """
            if re.match(r"([\w])", k):
                token = token + k
            if ver_iden(k):
                """Lista com separadores"""
                estado = 0
                if verifica_reservada(token):
                    """ Verifica se é IF """
                    if verifica_reservada(token) == 1:
                        token_geral.append(["CMD_IF", token])

                    if verifica_reservada(token) == 2:
                        token_geral.append(["CMD_ELSE", token])

                    if verifica_reservada(token) == 3:
                        token_geral.append(["CMD_WHILE", token])

                    if verifica_reservada(token) > 3 and verifica_reservada(token) < 8:
                        token_geral.append(["ID_VAR", token])

                    if k != " ":
                        if k in operadores:
                            estado = 3
                        elif k == '=':
                            token_geral.append(["OP_ATR", k])
                        elif k in separadores:
                            estado = 5
                        elif verifica_erro(k, token_geral, linha, coluna):
                            token_geral.append([k])
                    token = ""

                else:
                    token_geral.append(["ID", token])

                    if ver_iden(k):
                        #Vai inserir o k como separador
                        if k != re.match(r"\s", k):                            
                            estado = 0
                            if k in separadores:
                                estado = 5
                            elif k == '=':
                                token_geral.append(["OP_ATR", k])
                            elif k in operadores:
                                estado = 3
                            elif verifica_erro(k, token_geral, linha, coluna):
                                token_geral.append([k])
                    token = ""
        
        if estado == 2:
            """Estado de indentificacao de constante numerica"""
            if re.match(r"[\w.]", k):
                numerico = numerico + k
            if ver_num(k):                
                estado = 0
                if(re.match(r"(^[0-9]*$|[0-9]+.[0-9]+)", numerico)):
                    valor = re.match(r"(^[0-9]*$|[0-9]+.[0-9]+)", numerico)
                    if valor != None:
                        token_geral.append(["NUM", valor.group()])
                        if k != " ":
                            if k in operadores:
                                estado = 3
                            elif k == '=':
                                token_geral.append(["OP_ATR", k])
                            elif k in separadores:
                                estado = 5
                            elif verifica_erro(k, token_geral, linha, coluna):
                                token_geral.append([k])
                        numerico = ""
                else:
                    if k in separadores:
                        estado = 5
                    elif k == '=':
                        token_geral.append(["OP_ATR", k])
                    elif k in operadores:
                        estado = 3
                    elif re.match(r"\s", k):
                        """Identifica o token inválido"""
                        token_geral.append("[Token Inválido]")
                        estado = 0
                        numerico = ""
            else:
                if ver_num(k):
                    "Armazena token de separadores"
                    if k != " ":
                        estado = 0
                        if k in operadores:
                            estado = 3
                        elif k == '=':
                            token_geral.append(["OP_ATR", k])
                        elif k in separadores:
                            estado = 5
                        elif verifica_erro(k, token_geral, linha, coluna):
                            token_geral.append([k])

        if estado == 3:
            """ Estado de indentificacao de operador aritmetico """
            if (k) == '+':
                token_geral.append(["OP_ADD", k])             
            if (k) == '-':
                token_geral.append(["OP_SUB", k])  
            if (k) == '*':
                token_geral.append(["OP_MUL", k])
            if (k) == '/':
                token_geral.append(["OP_DIV", k])
            if (k) == '^':
                token_geral.append(["OP_POW", k])
            estado = 0

        if estado == 4:
            if (re.match(r"[<>=]", k)):
                relacional = relacional + k
            if ver_rel(k):
                estado = 0
                if verifica_relacional(relacional):
                    if verifica_relacional(relacional) == 1:
                        token_geral.append(["OP_MOI", relacional])

                    if verifica_relacional(relacional) == 2:
                        token_geral.append(["OP_MOE", relacional])
                    
                    if verifica_relacional(relacional) == 3:
                        token_geral.append(["OP_DIF", relacional])
                    
                    if verifica_relacional(relacional) == 4:
                        token_geral.append(["OP_IGU", relacional])

                    if k != " ":
                        if verifica_erro(k, token_geral, linha, coluna):
                            token_geral.append([k])
                    relacional = ""

                else:

                    if (relacional) == '>':
                        token_geral.append(["OP_MAI", relacional])
                    
                    if (relacional) == '<':
                        token_geral.append(["OP_MEN", relacional])
                    
                    if (relacional) == '=':
                        token_geral.append(["OP_ATR", relacional])
                    
                    estado = 0
                    relacional = ""

        if estado == 5:
            if (k) in separadores:
                token_geral.append(["DELIM", k])
            estado = 0
            
if __name__ == '__main__':
    exibe_imprime(token_geral)