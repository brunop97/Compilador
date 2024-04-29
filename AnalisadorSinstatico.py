class SyntacticAnalyzer:
    def __init__(self, matriz):
        self.matriz = matriz
        self.pos = 0

    def next_token(self):
        global token_atual

        if self.pos < len(self.matriz):
            token_atual= self.matriz[self.pos]
            self.pos += 1
            return token_atual
        else:
            return None  

    def error(self, message):
        print(f"Error: {message}")

    def programa(self):
        self.declaracao()

    def declaracao(self):
        if self.decl_var() or self.comando():
            pass
        else:
            self.error("Declaração inválida.")

    def decl_var(self):
        if self.tipo_var():
            self.lista_var()
            return True
        else:
            return False

    def tipo_var(self):
        if self.next_token()[0] in 'ID_VAR':
            self.next_token()
            return True
        else:
            return False

    def lista_var(self):
        if self.next_token()[0] in 'ID':
            self.next_token()
        elif token_atual and 'DELIM' in token_atual:
            if self.next_token()[0] in 'ID':
                self.next_token()
        else:
            self.error("Falta de identificador na lista de variáveis.")

    def expr(self):
        self.termo()
        if self.next_token()[0] in ['OP_ADD', 'OP_SUB']:
            op = self.next_token()
            self.termo()
        else:
            self.error("Operador inválido.")

    def termo(self):
        self.fator()
        if self.next_token()[0] in ['OP_MUL', 'OP_DIV']:
            op = self.next_token()
            self.fator()
        else:
            self.error("Operador inválido.")

    def fator(self):
        if self.next_token()[0] in ['ID', 'NUM']:
            self.next_token()
        elif self.next_token()[0] in '(':
            self.next_token()
            self.expr()
            if self.next_token()[0] in ')':
                self.next_token()
            else:
                self.error("Falta de ')' no final da expressão.")
        else:
            self.error("Fator inválido.")

    def comando_atribuicao(self):
        if self.next_token()[0] in 'ID':
            self.next_token()
            if self.next_token()[0] in 'OP_ATR':
                self.next_token()
                self.expr()
            else:
                self.error("Falta de '=' no comando de atribuição.")
        else:
            self.error("Identificador não declarado.")

    def comando_repeticao(self):
        if self.next_token()[0] in 'CMD_WHILE':
            self.next_token()
            if self.next_token()[0] in '(':
                self.next_token()
                self.expr()
                if self.next_token()[0] in ')':
                    self.next_token()
                    self.bloco()
                else:
                    self.error("Falta de ')' no final do comando while.")
            else:
                self.error("Falta de '(' no comando while.")

    def comando_condicional(self):
        if self.next_token()[0] in 'CMD_IF':
            self.next_token()
            if self.next_token()[0] in '(':
                self.next_token()
                self.expr()
                if self.next_token()[0] in ')':
                    self.next_token()
                    self.bloco()
                    if self.next_token()[0] in 'CMD_ELSE':
                        self.next_token()
                        self.bloco()
                else:
                    self.error("Falta de ')' no final do comando if.")
            else:
                self.error("Falta de '(' no comando if.")

    def comando(self):
        if self.comando_atribuicao():
            return True
        elif self.comando_repeticao():
            return True
        elif self.comando_condicional():
            return True
        elif self.bloco():
            return True
        else:
            return False

    def bloco(self):
        if self.next_token()[0] in '{':
            self.next_token()
            while self.declaracao():
                pass
            if self.next_token()[0] in '}':
                self.next_token()
            else:
                self.error("Falta de '}' no final do bloco.")

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
    matriz = []
    with open(arquivo, 'r') as arquivo_txt:
        linhas = arquivo_txt.readlines()
        for linha in linhas:
            matriz.append(processar_linha(linha))
    return matriz


arquivo = 'C:/Users/Bruno/Documents/GitHub/Compilador/SaidaAnalisadorLexico.txt'
matriz = ler_arquivo_txt(arquivo)

print(matriz)

syntactic_analyzer = SyntacticAnalyzer(matriz)

def exibe_imprime(programa_status, tokens_analisados):
    """Escreve no arquivo de saída."""
    arquivo_saida = "C:/Users/Bruno/Documents/GitHub/Compilador/SaidaAnalisadorSintatico.txt"
    with open(arquivo_saida, "w") as arq:
        if programa_status:
            arq.write("Análise sintática concluída com sucesso.\n")
        else:
            arq.write("Erros encontrados durante a análise sintática.\n")

        for pos, token in enumerate(tokens_analisados, 1):
            arq.write(f"Posição: {pos}, Token: {token}\n")

# Chamada da função
exibe_imprime(syntactic_analyzer.programa(), iter(syntactic_analyzer.next_token, None))



# if syntactic_analyzer.programa():
#     print("Análise sintática concluída com sucesso.")
# else:
#     print("Erros encontrados durante a análise sintática.")

# for pos, token in enumerate(iter(syntactic_analyzer.next_token, None), 1):
#     print(f"Posição: {pos}, Token: {token}")