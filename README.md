- Bruno Peroni

# Analisador
Analisador Lexico e Sintático


# Sobre o Analisador Léxico
Este analisador apresenta uma implementação simples de analisador léxico e analisador sintático. O mesmo está escrito em python 3.10.7. 

O Analisador Léxico reconhece os seguintes padrões:

- Delimitadores: ';', '[', ']', ')', '(', ')', '{', '}', ',', '.'; desconsiderando brancos e sinais de tabulação;
- Números: [0-9];
- Letras maiúsculas: [A-Z];
- Letras minúsculas: [a-z];
- Identificadores: palavras formadas por Letras maiúsculas e minúsculas;
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
- OP_ATR: Operador de atribuição (=)
- OP_ARIT: Operador aritmetico (+ - * / ^)
- OP_BINARIO: Operador binario (>= <= <> == > <)
- DELIM: Delimitador (; [ ] ) ( { } , .)
- CMD_WHILE: Comando while
- CMD_IF: Comando if
- CMD_ELSE: Comando else

------------------

Regras de Produção:

Sintatico -> statements
statements -> statement | statement , statements
statement -> assignment | verify_if | verify_while
assignment -> identifier OP_ATR expression
expression -> math_expression | '(' bin_expression ')'
math_expression -> identifier | number | OP_ARIT math_expression
bin_expression -> identifier OP_BINARIO identifier | '(' expression OP_BINARIO expression ')'
verify_if -> CMD_IF '(' expression ')' '{' statements '}' (CMD_ELSE '{' statements '}')
verify_while -> CMD_WHILE '(' expression ')' '{' statements '}'
identifier -> ID (',' ID)*
number -> NUM

# Como Executar

Para executar o analisador em um ambiente Linux ou Windows é necessario possuir o python 3.10.7 instalado. Com o python instalado abra o terminal e siga os passos abaixo.
Neste caso o arquivo de teste a ser carregado é o DadosEntradaAnalisador.txt

> python AnalisadorLexico.py
- Em seguida:
> python AnalisadorSintatico.py

# Arquivos de Saida
Ao executar o analisador será gerado um arquivo:
- Arquivo com os tokens gerados do analisador Léxico. (SaidaAnalisadorLexico.txt)
- Arquivo com os tokens gerados do analisador Sintático. (SaidaAnalisadorSintatico.txt)