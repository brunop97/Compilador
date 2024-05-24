- Bruno Peroni

# Analisador
Analisador Lexico e Sintático


# Sobre o Analisador Léxico
Este analisador apresenta uma implementação simples de analisador léxico e analisador sintático. O mesmo está escrito em python 3.10.7. 

O Analisador Léxico reconhece os seguintes padrões:

- Delimitadores: ';', '[', ']', ')', '(', ')', '{', '}', ',', '.'; desconsiderando brancos e sinais de tabulação;
- Números: [0-9]+;
- Identificadores: palavras formadas por Letras maiúsculas, minúsculas e números [a-zA-Z][a-zA-Z0-9_]*;
- Operadores aritméticos binários: '+', '-', '*', '/', '^';
- Operadores relacionais binários: '>', '>=', '<', '<=', '<>', '==';
- Comando de atribuição: '=';
- Comando de desvio: 'if', ‘else’;
- Comando de repetição : 'while';

# Sobre o Analisador Sintático

O Analisador Sintático reconhece os seguintes padrões:

- Expressões aritméticas binárias: x + y, x – y, x / y, x * y, x ^ y, etc.
- Expressões aritméticas com parênteses balanceados: (x + y), x * (y+z), (x / (y-z)), etc.
- Expressões relacionais: (x > y), x <= (y+z), (x <> (y-z)), etc.
- Declaração de variáveis: int x, y | real s | etc.
- Comando de Atribuição simples: a = b, a = expr + 78.
- Comando de Repetição: while ( a > b ) { comandos }.
- Comando de Fluxo de controle: if ( a > b ) { comandos } else {comandos}.
- Exibir mensagem de erro adequada ao contexto quando a sentença de entrada não estiver de acordo com a gramática.

Símbolos Terminais:

- ID: Identificador (variável)
- ID_VAR: Identificador de tipo de variável (inteiro, real, etc.)
- NUM: Número (inteiro ou real)
- OP_ATRIBUICAO: Operador de atribuição (=)
- OP_ARITMETICO: Operador aritmetico (+ - * / ^)
- OP_RELACIONAL: Operador binario (>= <= <> == > <)
- DELIMITADOR: Delimitador (; [ ] ) ( { } , .)
- CMD_WHILE: Comando while
- CMD_IF: Comando if
- CMD_ELSE: Comando else

------------------

Regras de Produção:

- Sintatico -> var_declaration statements
- var_declaration -> 'var' ID_VAR (',' ID_VAR) | ε
- statements -> statement statements | ε
- statement -> assignment | verify_if | verify_while
- assignment -> identifier OP_ATRIBUICAO expression
- expression -> math_expression | '(' bin_expression ')'
- math_expression -> identifier | NUM | OP_ARITMETICO math_expression
- bin_expression -> identifier OP_RELACIONAL (identifier | NUM) | '(' expression OP_RELACIONAL expression ')'
- verify_if -> CMD_IF '(' expression ')' '{' statements '}' (CMD_ELSE '{' statements '}' | ε)
- verify_while -> CMD_WHILE '(' expression ')' '{' statements '}'
- identifier -> ID (',' ID)

# Como Executar

Para executar o analisador em um ambiente Linux ou Windows é necessario possuir o python 3.10.7 instalado. Com o python instalado abra o terminal e siga os passos abaixo.
Neste caso o arquivo de teste a ser carregado é o DadosEntradaAnalisador.txt

> python Analisador.py
