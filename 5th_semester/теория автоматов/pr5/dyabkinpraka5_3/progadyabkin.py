"""
Лексер и Парсер для практической 5 задания 3.
"""
NEG_SIGN    = 'NEG'    # ~
MUL_SIGN    = 'MUL'    # &
ADD_SIGN    = 'ADD'    # |
ASSIGN_SIGN = 'ASSIGN' # =
LPAR_SIGN   = 'LPAR'   # (
RPAR_SIGN   = 'RPAR'   # )
SEMI_SIGN   = 'SEMI'   # ;
ID_SIGN     = 'ID'     # идентификатор (1–2 буквы)
CONST_SIGN  = 'CONST'  # константа (10/2/16)
EOP         = 'EOP'    # конец ввода
UNDEF       = 'UNDEF'  # неизвестное



#ID, CONST, '~', '&', '|', '=', '(', ')', ';', EOP
#LIST      -> ASSIGN LIST_TAIL
#LIST_TAIL -> ';' ASSIGN LIST_TAIL | ε
#ASSIGN      -> EXPR ASSIGN_TAIL
#ASSIGN_TAIL -> '=' ASSIGN | ε
#EXPR -> NEXT_EXPR ADD
#ADD  -> '|' NEXT_EXPR ADD | ε
#NEXT_EXPR -> UNARY MUL
#MUL       -> '&' UNARY MUL | ε
#UNARY -> '~' UNARY | PRIMARY
#PRIMARY -> ID | CONST | '(' EXPR ')'
#CONST      -> '0' CONST_TAIL | NZDIGIT DIGIT_TAIL
#CONST_TAIL -> 'b' BINARY | 'B' BINARY | 'x' HEX | 'X' HEX | DIGIT_TAIL
#BINARY     -> BIT BIT_TAIL
#BIT_TAIL   -> BIT BIT_TAIL | ε
#BIT        -> '0' | '1'
#HEX        -> HEXDIGIT HEX_TAIL
#HEX_TAIL   -> HEXDIGIT HEX_TAIL | ε
#HEXDIGIT   -> DIGIT | 'a' | 'b' | 'c' | 'd' | 'e' | 'f'
#                        | 'A' | 'B' | 'C' | 'D' | 'E' | 'F'
#DIGIT_TAIL -> DIGIT DIGIT_TAIL | ε
#NZDIGIT    -> '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
#DIGIT      -> NZDIGIT | '0'
# CONST -> 0 CONST_TAIL | NZDIGIT DIGIT_TAIL
# CONST_TAIL -> 'b' BINARY | 'x' HEX | DIGIT_TAIL
# BINARY -> BIT BIT_TAIL
# BIT_TAIL -> BIT BIT_TAIL | ε
# BIT -> '0' | '1'
# HEX -> HEXDIGIT HEX_TAIL
# HEX_TAIL -> HEXDIGIT HEX_TAIL | ε
# HEXDIGIT -> DIGIT | a..f
# DIGIT_TAIL -> DIGIT DIGIT_TAIL | ε
# NZDIGIT -> 1..9
# DIGIT -> NZDIGIT | 0

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def skip_spaces(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def get_token(self):
        self.skip_spaces()
        if self.pos >= len(self.text):
            return (EOP, '')

        ch = self.text[self.pos]

        # одиночные символы операций и скобок
        if ch == '~': self.pos += 1; return (NEG_SIGN, '~')
        if ch == '&': self.pos += 1; return (MUL_SIGN, '&')
        if ch == '|': self.pos += 1; return (ADD_SIGN, '|')
        if ch == '=': self.pos += 1; return (ASSIGN_SIGN, '=')
        if ch == '(': self.pos += 1; return (LPAR_SIGN, '(')
        if ch == ')': self.pos += 1; return (RPAR_SIGN, ')')
        if ch == ';': self.pos += 1; return (SEMI_SIGN, ';')

        # ID: ONE_SYM SEC_SYM, где ONE_SYM — буква a..z
        if ch.isalpha():
            start = self.pos
            self.pos += 1
            if self.pos < len(self.text) and self.text[self.pos].isalpha():
                self.pos += 1           # допускаем 2‑символьный ID
            return (ID_SIGN, self.text[start:self.pos])

        # CONST: начинаем с цифры, затем буквы/цифры (0, 0b..., 0x..., десятичное)
        if ch.isdigit():
            start = self.pos
            self.pos += 1
            while self.pos < len(self.text) and self.text[self.pos].isalnum():
                self.pos += 1
            return (CONST_SIGN, self.text[start:self.pos])

        self.pos += 1
        return (UNDEF, ch)

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.tok, self.lexeme = lexer.get_token()  # текущий токен

    def error(self):
        raise ParseError()

    def eat(self, token_type):
        if self.tok == token_type:
            self.tok, self.lexeme = self.lexer.get_token()
        else:
            self.error()

    # LIST -> ASSIGN LIST_TAIL
    def LIST(self):
        self.ASSIGN()
        self.LIST_TAIL()

    # LIST_TAIL -> ';' ASSIGN LIST_TAIL | ε
    def LIST_TAIL(self):
        if self.tok == SEMI_SIGN:
            self.eat(SEMI_SIGN)
            self.ASSIGN()
            self.LIST_TAIL()

    # ASSIGN -> EXPR ASSIGN_TAIL
    def ASSIGN(self):
        self.EXPR()
        self.ASSIGN_TAIL()

    # ASSIGN_TAIL -> '=' ASSIGN | ε
    def ASSIGN_TAIL(self):
        if self.tok == ASSIGN_SIGN:
            self.eat(ASSIGN_SIGN)
            self.ASSIGN()

    # EXPR -> NEXT_EXPR ADD
    def EXPR(self):
        self.NEXT_EXPR()
        self.ADD()

    # ADD -> '|' NEXT_EXPR ADD | ε
    def ADD(self):
        if self.tok == ADD_SIGN:
            self.eat(ADD_SIGN)
            self.NEXT_EXPR()
            self.ADD()

    # NEXT_EXPR -> UNARY MUL
    def NEXT_EXPR(self):
        self.UNARY()
        self.MUL()

    # MUL -> '&' UNARY MUL | ε
    def MUL(self):
        if self.tok == MUL_SIGN:
            self.eat(MUL_SIGN)
            self.UNARY()
            self.MUL()

    # UNARY -> '~' UNARY | PRIMARY
    def UNARY(self):
        if self.tok == NEG_SIGN:
            self.eat(NEG_SIGN)
            self.UNARY()
        else:
            self.PRIMARY()

    # PRIMARY -> ID | CONST | '(' EXPR ')'
    def PRIMARY(self):
        if self.tok == ID_SIGN:
            self.eat(ID_SIGN)
        elif self.tok == CONST_SIGN:
            self.parse_const_grammar(self.lexeme)
            self.eat(CONST_SIGN)
        elif self.tok == LPAR_SIGN:
            self.eat(LPAR_SIGN)
            self.EXPR()
            self.eat(RPAR_SIGN)
        else:
            self.error()



    def parse_const_grammar(self, s: str):
        self.c_pos = 0
        try:
            self.CONST_RULE(s)
            if self.c_pos != len(s):
                self.error()
        finally:
            del self.c_pos

    def c_peek(self, s: str):
        return s[self.c_pos] if self.c_pos < len(s) else None

    def c_eat(self, s: str, allowed: str):
        ch = self.c_peek(s)
        if ch is None or ch not in allowed:
            self.error()
        self.c_pos += 1
        return ch

    # CONST -> 0 CONST_TAIL | NZDIGIT DIGIT_TAIL
    def CONST_RULE(self, s: str):
        ch = self.c_peek(s)
        if ch == '0':
            self.c_pos += 1
            self.CONST_TAIL_RULE(s)
        elif ch is not None and ch in "123456789":
            self.c_pos += 1
            self.DIGIT_TAIL_RULE(s)
        else:
            self.error()

    # CONST_TAIL -> 'b' BINARY | 'x' HEX | DIGIT_TAIL
    def CONST_TAIL_RULE(self, s: str):
        ch = self.c_peek(s)
        if ch in ('b', 'B'):
            self.c_pos += 1
            self.BINARY_RULE(s)
        elif ch in ('x', 'X'):
            self.c_pos += 1
            self.HEX_RULE(s)
        else:
            self.DIGIT_TAIL_RULE(s)

    # BINARY -> BIT BIT_TAIL
    def BINARY_RULE(self, s: str):
        self.BIT_RULE(s)
        self.BIT_TAIL_RULE(s)

    # BIT_TAIL -> BIT BIT_TAIL | ε
    def BIT_TAIL_RULE(self, s: str):
        ch = self.c_peek(s)
        if ch in ('0', '1'):
            self.BIT_RULE(s)
            self.BIT_TAIL_RULE(s)

    # BIT -> 0 | 1
    def BIT_RULE(self, s: str):
        self.c_eat(s, "01")

    # HEX -> HEXDIGIT HEX_TAIL
    def HEX_RULE(self, s: str):
        self.HEXDIGIT_RULE(s)
        self.HEX_TAIL_RULE(s)

    # HEX_TAIL -> HEXDIGIT HEX_TAIL | ε
    def HEX_TAIL_RULE(self, s: str):
        ch = self.c_peek(s)
        if ch is not None and (ch.isdigit() or ch.lower() in "abcdef"):
            self.HEXDIGIT_RULE(s)
            self.HEX_TAIL_RULE(s)

    # HEXDIGIT -> DIGIT | a..f
    def HEXDIGIT_RULE(self, s: str):
        ch = self.c_peek(s)
        if ch is None:
            self.error()
        if ch.isdigit() or ch.lower() in "abcdef":
            self.c_pos += 1
        else:
            self.error()

    # DIGIT_TAIL -> DIGIT DIGIT_TAIL | ε
    def DIGIT_TAIL_RULE(self, s: str):
        ch = self.c_peek(s)
        if ch is not None and ch.isdigit():
            self.c_pos += 1
            self.DIGIT_TAIL_RULE(s)


def check_line(line: str) -> bool:
    lexer = Lexer(line)
    parser = Parser(lexer)
    try:
        parser.LIST()
        return parser.tok == EOP
    except ParseError:
        return False

def main():
    while True:
        try:
            line = input("Введите текст: ")
        except EOFError:
            break

        if line == "":
            break

        if check_line(line):
            print("Accepted")
        else:
            print("Rejected")

if __name__ == "__main__":
    main()
