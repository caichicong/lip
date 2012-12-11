# LL(1) Recursive-Descent Lexer

class Token:
    def __init__(self, type, text):
        self.type = type
        self.text = text

    def __str__(self):
        return "<'%s', %s>" % (self.text, ListLexer.tokenNames[self.type])

class Lexer:

    @staticmethod
    def init(lexer, input):
        lexer.input = input
        lexer.p = 0
        # lookahead char
        lexer.c = lexer.input[0]

    @staticmethod
    def consume(lexer):
        lexer.p += 1
        if lexer.p >= len(lexer.input):
            lexer.c = lexer.EOF
        else:
            lexer.c = lexer.input[lexer.p]

    @staticmethod
    def match(lexer, x):
        if lexer.c == x:
            lexer.consume()
        else:
            raise Exception('expecting ' + x + '; found ' + lexer.c)

class ListLexer(Lexer):

    tokenNames = ["n/a", "<EOF>", "NAME", "COMMA", "LBRACK", "RBRACK"]
    EOF_TYPE = 1
    NAME = 2
    COMMA = 3
    LBRACK = 4
    RBRACK = 5
    EOF = -1

    def __init__(self, input):
        Lexer.init(self, input)

    def isLetter(self):
        return (self.c >= 'a' and self.c <= 'z') or \
                (self.c >= 'A' and self.c <= 'Z')

    def consume(self):
        Lexer.consume(self)

    #match is not use
    def match(self, x):
        Lexer.match(self, x)

    def nextToken(self):
        while self.c != self.EOF :
            if self.c in (' ', '\t','\n', '\r'):
                self.whitespace()
            elif self.c == ',':
                self.consume()
                return Token(ListLexer.COMMA, ",")
            elif self.c == '[':
                self.consume()
                return Token(ListLexer.LBRACK, "[")
            elif self.c == ']':
                self.consume()
                return Token(ListLexer.RBRACK, "]")
            else:
                if self.isLetter():
                    return self.name()
                else:
                    raise Exception("invalid character: " + self.c)
        return Token(ListLexer.EOF_TYPE, "<EOF>")

    def getTokenName(self, x):
        return self.tokenNames[x]

    def whitespace(self):
        while self.c in (' ', '\t','\n', '\r'):
            self.consume()

    def name(self):
        buf = ''
        while True:
            buf += self.c 
            self.consume()
            if not self.isLetter():
                break
        return Token(ListLexer.NAME, buf)

lexer = ListLexer('[sdfs, sdfs , sfds]')

t = lexer.nextToken()

while t.type != 1:
    print t
    t = lexer.nextToken()

print t

#  wrong_lexer = ListLexer('[1s, sdfs , sfds]')
#  
#  t = wrong_lexer.nextToken()
#  while t.type != 1:
#      print t
#      t = wrong_lexer.nextToken()
#  
#  print t


class Parser:
    @staticmethod
    def init(parser, input):
        parser.input = input
        Parser.consume(parser)

    @staticmethod
    def consume(parser):
        parser.lookahead = parser.input.nextToken()

    @staticmethod
    def match(parser, x):
        if parser.lookahead.type == x:
            Parser.consume(parser)
        else:
            raise Exception("expecting: " + parser.input.getTokenName(x) + "; found " + str(parser.lookahead))

class ListParser(Parser):

    def __init__(self, input):
        Parser.init(self, input)

    def list(self):
        Parser.match(self, ListLexer.LBRACK)
        self.elements()
        Parser.match(self, ListLexer.RBRACK)

    def elements(self):
        self.element()
        while True:
            if self.lookahead.type == ListLexer.COMMA:
                Parser.match(self, ListLexer.COMMA)
                self.element()
            else:
                break

    def element(self):
        if self.lookahead.type == ListLexer.NAME:
            Parser.match(self, ListLexer.NAME)
        elif self.lookahead.type == ListLexer.LBRACK:
            self.list()
        else:
            raise Exception("expecting name of list ; found " + str(self.lookahead))

lexer = ListLexer('[dfs, ]')
parser = ListParser(lexer)
parser.list()
