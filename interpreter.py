class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self):
        self.variables = {}

    def eval(self, node):
        if node.__class__.__name__ == "Number":
            return node.value

        if node.__class__.__name__ == "String":
            return node.value

        if node.__class__.__name__ == "Name":
            name = node.name
            if name not in self.variables:
                raise NameError(f"Undefined variable: {name}")
            return self.variables[name]
        
        if node.__class__.__name__ == "List":
            return [self.eval(element) for element in node.elements]
        
        if node.__class__.__name__ == "Index":
            list_val = self.eval(node.list)
            index_val = self.eval(node.index)
            return list_val[index_val]
        if node.__class__.__name__ == "Print":
            value = self.eval(node.value)
            print(value)
            return value
        
        if node.__class__.__name__ == "If":
            if self.eval_condition(node.condition):
                return self.eval_block(node.body)
            elif node.else_body is not None:
                return self.eval_block(node.else_body)
            return None

        if node.__class__.__name__ == "While":
            while self.eval_condition(node.condition):
                self.eval_block(node.body)
            return None
        
        if node.__class__.__name__ == "Forloop":
            iterable_val = self.eval(node.iterable)
            for item in iterable_val:
                self.variables[node.var_name] = item
                self.eval_block(node.body)
            return None

        if node.__class__.__name__ == "FuncDef":
            self.variables[node.name] = node
            return None

        if node.__class__.__name__ == "FuncCall":
            func = self.variables[node.name]
            old_vars = self.variables
            new_vars = old_vars.copy()
            for param, arg in zip(func.params, node.args):
                new_vars[param] = self.eval(arg)
            self.variables = new_vars
            try:
                result = self.eval_block(func.body)
            except ReturnException as r:
                result = r.value
            self.variables = old_vars
            return result

        if node.__class__.__name__ == "Return":
            value = self.eval(node.value)
            raise ReturnException(value)

        if node.__class__.__name__ == "BinOp":
            left = self.eval(node.left)
            right = self.eval(node.right)
            if node.op == "+": return left + right
            if node.op == "-": return left - right
            if node.op == "*": return left * right
            if node.op == "/": return left / right

        if node.__class__.__name__ == "Let":
            value = self.eval(node.value)
            self.variables[node.name] = value
            return value
        
    def eval_condition(self, condition):
        left, op, right = condition

        # if op is "and" or "or", left and right are themselves conditions
        if op == "and":
            return self.eval_condition(left) and self.eval_condition(right)
        if op == "or":
            return self.eval_condition(left) or self.eval_condition(right)

        # otherwise it's a simple comparison -- left and right are AST nodes
        left_val = self.eval(left)
        right_val = self.eval(right)
        if op == ">":  return left_val > right_val
        if op == "<":  return left_val < right_val
        if op == "==": return left_val == right_val
        if op == "!=": return left_val != right_val
        if op == ">=": return left_val >= right_val
        if op == "<=": return left_val <= right_val

    def eval_block(self, statements):
        result = None
        for statement in statements:
            result = self.eval(statement)
        return result

    def run(self, statements):
        for statement in statements:
            self.eval(statement)
        print(f"Variables: {self.variables}")