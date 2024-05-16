from rply import LexerGenerator

#######################################
# TOKENS
#######################################

TT_INT          = 'INTEGER'
TT_FLOAT        = 'FLOAT'
TT_BOOLEAN      = 'BOOLEAN'
TT_IDENTIFIER   = 'IDENTIFIER'
TT_PLUS         = 'PLUS'
TT_EQ           = 'EQUALS'
TT_NEQ          = 'NOTEQUALS'
TT_LT           = 'LT'
TT_GT           = 'GT'
TT_LTE          = 'LTE'
TT_GTE          = 'GTE'
TT_ASSIGN       = 'ASSIGN'
TT_LSQUARE      = 'LSQUARE'
TT_RSQUARE      = 'RSQUARE'
TT_RCURLY       = 'RCURLY'
TT_LCURLY       = 'LCURLY'
TT_PIPE         = 'PIPE'
TT_DOT          = 'DOT'
TT_COLON        = 'COLON'
TT_MUL          = 'MUL'
TT_MINUS        = 'MINUS'
TT_DIV          = 'DIV'
TT_MOD          = 'MODE'
TT_POW          = 'POW'
TT_COMMA        = 'COMMA'
TT_LPAREN       = 'LPAREN'
TT_RPAREN       = 'RPAREN'
TT_NEWLINE      = 'NEWLINE'
TT_STRING       = 'STRING'
TT_COMMENT      = 'COMMENT',


KEYWORDS = {
    'TT_IF': 'IF',
    'TT_ELIF': 'ELIF',
    'TT_ELSE': 'ELSE',
    'TT_END':'END',
    'TT_AND': 'AND',
    'TT_OR': 'OR',
    'TT_NOT': 'NOT',
    'TT_LET': 'LET',
    'TT_FOR': 'FOR',
    'TT_WHILE': 'WHILE',
    'TT_BREAK': 'BREAK',
    'TT_CONTINUE': 'CONTINUE',
    'TT_MATCH': 'MATCH',
    'TT_ENUM': 'ENUM',
    'TT_NEW': 'NEW',
    'TT_RETURN': 'RETURN',
    'TT_TYPE': 'TYPE',
    'TT_ARRAY': 'ARRAY',
    'TT_DICT': 'DICT',
    'TT_INTGER': 'INTGER',
    'TT_STRING': 'STRING',
    'TT_FLOUT': 'FLOUT',
    'TT_CHAR': 'CHAR',
    'TT_LONG': 'LONG',
    'TT_DOUBLE': 'DOUBLE',
    'TT_RECORD': 'RECORD',
    'TT_FUNC': 'FUNCTION',
    'TT_PRIVATE': 'PRIVATE',
    'TT_MODULE': 'MODULE',
    'TT_TRAIT': 'TRAIT',
    'TT_IMPLEMENT': 'IMPLEMENT',
    'TT_IMPORT': 'IMPORT',
    'TT_SEND': 'SEND',
    'TT_RECEIVE': 'RECEIVE',
}

class Lexer:
    def __init__(self):
        self.lexer = self._build_lexer()
        self.symbol_table = {}

    def _build_lexer(self):
        tokens = LexerGenerator()

        # Define tokens and their corresponding regular expressions
        tokens.add(TT_FLOAT, r'-?\d+\.\d+')
        tokens.add(TT_INT, r'-?\d+')
        tokens.add(TT_BOOLEAN, r"true(?!\w)|false(?!\w)")
        # Keywords
        tokens.add(KEYWORDS['TT_IF'], r'if(?!\w)')
        tokens.add(KEYWORDS['TT_ELIF'], r'elif(?!\w)')
        tokens.add(KEYWORDS['TT_ELSE'], r'else(?!\w)')
        tokens.add(KEYWORDS['TT_END'], r'end(?!\w)')
        tokens.add(KEYWORDS['TT_AND'], r"and(?!\w)")
        tokens.add(KEYWORDS['TT_OR'], r"or(?!\w)")
        tokens.add(KEYWORDS['TT_NOT'], r"not(?!\w)")
        tokens.add(KEYWORDS['TT_LET'], r'let(?!\w)')
        tokens.add(KEYWORDS['TT_FOR'], r'for(?!\w)')
        tokens.add(KEYWORDS['TT_WHILE'], r'while(?!\w)')
        tokens.add(KEYWORDS['TT_BREAK'], r'break(?!\w)')
        tokens.add(KEYWORDS['TT_CONTINUE'], r'continue(?!\w)')
        tokens.add(KEYWORDS['TT_MATCH'], r'match(?!\w)')
        tokens.add(KEYWORDS['TT_ENUM'], r'enum(?!\w)')
        tokens.add(KEYWORDS['TT_NEW'], r'new(?!\w)')
        tokens.add(KEYWORDS['TT_RETURN'], r'return(?!\w)')
        tokens.add(KEYWORDS['TT_TYPE'], r'type(?!\w)')
        tokens.add(KEYWORDS['TT_ARRAY'], r'array(?!\w)')
        tokens.add(KEYWORDS['TT_DICT'], r'dict(?!\w)')
        tokens.add(KEYWORDS['TT_INTGER'], r'int(?!\w)')
        tokens.add(KEYWORDS['TT_STRING'], r'str(?!\w)')
        tokens.add(KEYWORDS['TT_FLOUT'], r'float(?!\w)')
        tokens.add(KEYWORDS['TT_CHAR'], r'char(?!\w)')
        tokens.add(KEYWORDS['TT_LONG'], r'long(?!\w)')
        tokens.add(KEYWORDS['TT_DOUBLE'], r'double(?!\w)')
        tokens.add(KEYWORDS['TT_RECORD'], r'record(?!\w)')
        tokens.add(KEYWORDS['TT_FUNC'], r'func(?!\w)')
        tokens.add(KEYWORDS['TT_PRIVATE'], r'priv(?!\w)')
        tokens.add(KEYWORDS['TT_MODULE'], r'mod(?!\w)')
        tokens.add(KEYWORDS['TT_TRAIT'], r'trait(?!\w)')
        tokens.add(KEYWORDS['TT_IMPLEMENT'], r'impl(?!\w)')
        tokens.add(KEYWORDS['TT_IMPORT'], r'import(?!\w)')
        tokens.add(KEYWORDS['TT_SEND'], r'send(?!\w)')
        tokens.add(KEYWORDS['TT_RECEIVE'], r'receive(?!\w)')
        # Identifier token
        tokens.add(TT_IDENTIFIER, r"[a-zA-Z_][a-zA-Z0-9_]*")
        # Operators
        tokens.add(TT_PLUS, r'\+')
        tokens.add(TT_EQ, r'==')
        tokens.add(TT_NEQ, r'!=')
        tokens.add(TT_GTE, r'>=')
        tokens.add(TT_LTE, r'<=')
        tokens.add(TT_GT, r'>')
        tokens.add(TT_LT, r'<')
        tokens.add(TT_ASSIGN, r'=')
        tokens.add(TT_LSQUARE, r'\[')
        tokens.add(TT_RSQUARE, r'\]')
        tokens.add(TT_LCURLY, r'\{')
        tokens.add(TT_RCURLY, r'\}')
        tokens.add(TT_PIPE, r'\|')
        tokens.add(TT_COMMA, r',')
        tokens.add(TT_DOT, r'\.')
        tokens.add(TT_COLON, r':')
        tokens.add(TT_MINUS, r'-')
        tokens.add(TT_MUL, r'\*')
        tokens.add(TT_DIV, r'/')
        tokens.add(TT_POW, r'^')
        tokens.add(TT_MOD, r'%')
        tokens.add(TT_LPAREN, r'\(')
        tokens.add(TT_RPAREN, r'\)')
        tokens.add(TT_STRING, r'"([^"\\]|\\.)*"')
        # tokens.add(TT_COMMENT, r'#.*(?:\n|\Z)')

        # Newline token
        tokens.add(TT_NEWLINE, r"\n+ *\n*")

        # Ignore comments and space
        tokens.ignore(r'#.*(?:\n|\Z)')
        tokens.ignore(r'[ \t\r\f\v]+')

        return tokens.build()

    def get_lexer(self):
        return self.lexer