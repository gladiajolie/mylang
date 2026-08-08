class Number:
    def __init__(self, value):
        self.value = value

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Let:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Print:
    def __init__(self, value):
        self.value = value

class If:
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class FuncDef:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class FuncCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Return:
    def __init__(self, value):
        self.value = value

class String:
    def __init__(self, value):
        self.value = value

class Name:
    def __init__(self, name):
        self.name = name

class List:
    def __init__(self, elements):
        self.elements = elements

class Index:
    def __init__(self, list, index):
        self.list = list
        self.index = index 


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        if self.i < len(self.tokens):
            return self.tokens[self.i]
        return None

    def eat(self, kind):
        token = self.peek()
        if token is None or token[0] != kind:
            raise SyntaxError(f"Expected {kind} but got {token}")
        self.i += 1
        return token

    def parse_primary(self):
        token = self.peek()
        if token is None:
            raise SyntaxError("Unexpected end of input")
        if token[0] == "MINUS":
            self.eat("MINUS")
            operand = self.parse_primary()
            return BinOp(Number(0), "-", operand)
        if token[0] == "NUMBER":
            self.eat("NUMBER")
            return Number(int(token[1]))
        if token[0] == "STRING":
            self.eat("STRING")
            return String(token[1][1:-1])
        if token[0] == "NAME":
            self.eat("NAME")
            if self.peek() and self.peek()[0] == "LBRACKET":
                self.eat("LBRACKET")
                index = self.parse_expr()
                self.eat("RBRACKET")
                return Index(Name(token[1]), index)
            if self.peek() and self.peek()[0] in ("NUMBER", "STRING", "NAME"):
                args = []
                while self.peek() and self.peek()[0] in ("NUMBER", "STRING", "NAME"):
                    args.append(self.parse_primary())
                return FuncCall(token[1], args)
            return Name(token[1])
        if token[0] == "LBRACKET":
            self.eat("LBRACKET")
            elements = []
            while self.peek() and self.peek()[0] != "RBRACKET":
                elements.append(self.parse_expr())
                if self.peek() and self.peek()[0] == "COMMA":
                    self.eat("COMMA")
            self.eat("RBRACKET")
            return List(elements)
        raise SyntaxError(f"Unexpected token: {token}")

    def parse_term(self):
        # handles * and / (high priority)
        left = self.parse_primary()
        while self.peek() and self.peek()[0] in ("STAR", "SLASH"):
           op = self.eat(self.peek()[0])
           right = self.parse_primary()
           left = BinOp(left, op[1], right)
        return left

    def parse_expr(self):
        # handles + and - (low priority)
        # calls parse_term for each side, so * and / always bind first
        left = self.parse_term()
        while self.peek() and self.peek()[0] in ("PLUS", "MINUS"):
            op = self.eat(self.peek()[0])
            right = self.parse_term()
            left = BinOp(left, op[1], right)
        return left
    
    def parse_comparison(self):
        # handles a single comparison: expr op expr
        left = self.parse_expr()
        if self.peek() and self.peek()[0] in ("GT", "LT", "EQEQ", "NOTEQ", "GTE", "LTE"):
            op = self.eat(self.peek()[0])
            right = self.parse_expr()
            return (left, op[1], right)
        return (left, None, None)

    def parse_condition(self):
        # handles: comparison (and/or comparison)*
        left = self.parse_comparison()
        while self.peek() and self.peek()[0] in ("AND", "OR"):
            op = self.eat(self.peek()[0])
            right = self.parse_comparison()
            left = (left, op[1], right)
        return left
    
    def parse_block(self):
        self.eat("LBRACE")
        statements = []
        while self.peek() and self.peek()[0] != "RBRACE":
            statements.append(self.parse_statement())
        self.eat("RBRACE")
        return statements

    def parse_statement(self):
        token = self.peek()
        if token is None:
            raise SyntaxError("Unexpected end of input")

        if token[0] == "PRINT":
            self.eat("PRINT")
            value = self.parse_expr()
            return Print(value)

        elif token[0] == "IF":
            self.eat("IF")
            condition = self.parse_condition()
            body = self.parse_block()
            else_body = None
            if self.peek() and self.peek()[0] == "ELSE":
                self.eat("ELSE")
                else_body = self.parse_block()
            return If(condition, body, else_body)

        elif token[0] == "WHILE":
            self.eat("WHILE")
            condition = self.parse_condition()
            body = self.parse_block()
            return While(condition, body)

        elif token[0] == "FUNC":
            self.eat("FUNC")
            name = self.eat("NAME")
            params = []
            while self.peek() and self.peek()[0] == "NAME":
                params.append(self.eat("NAME")[1])
            body = self.parse_block()
            return FuncDef(name[1], params, body)

        elif token[0] == "RETURN":
            self.eat("RETURN")
            value = self.parse_expr()
            return Return(value)

        else:
            self.eat("LET")
            name = self.eat("NAME")
            self.eat("EQUALS")
            value = self.parse_expr()
            return Let(name[1], value)

    def parse(self):
        statements = []
        while self.peek() is not None:
            statements.append(self.parse_statement())
        return statements