import re

TOKEN_PATTERNS = [
    ("NUMBER",  r"\d+"),
    ("PLUS",    r"\+"),
    ("MINUS",   r"-"),
    ("STAR",    r"\*"),
    ("SLASH",   r"/"),
    ("EQEQ",    r"=="),
    ("NOTEQ",   r"!="),
    ("GTE",     r">="),
    ("LTE",     r"<="),
    ("EQUALS",  r"="),
    ("LBRACE",  r"\{"),
    ("RBRACE",  r"\}"),
    ("LBRACKET",r"\["),
    ("RBRACKET",r"\]"),
    ("COMMA",   r","),
    ("LET",     r"let\b"),
    ("PRINT",   r"print\b"),
    ("IF",      r"if\b"),
    ("WHILE",   r"while\b"),
    ("ELSE",    r"else\b"),
    ("AND",     r"and\b"),
    ("OR",      r"or\b"),
    ("NOT",     r"not\b"),
    ("FUNC",    r"func\b"),
    ("RETURN",  r"return\b"),
    ("GT",      r">"),
    ("LT",      r"<"),
    ("STRING",  r'"[^"]*"'),
    ("NAME",    r"[a-zA-Z_]\w*"),
    ("COMMENT", r"#[^\n]*"),
    ("SKIP",    r"[ \t\n]+"),
]

def lex(source):
    tokens = []
    i = 0
    while i < len(source):
        for kind, pattern in TOKEN_PATTERNS:
            match = re.match(pattern, source[i:])
            if match:
                if kind != "SKIP" and kind != "COMMENT":
                    tokens.append((kind, match.group()))
                i += len(match.group())
                break
        else:
            raise SyntaxError(f"Unexpected character: {source[i]!r}")
    return tokens