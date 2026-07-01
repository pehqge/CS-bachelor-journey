from dataclasses import dataclass

@dataclass
class SyntaxTree:
    def __init__(self, node_type=None, symbol=None, left=None, right=None):
        self.node_type = node_type # tipo do nó: '|', '.', '*', '?', '+', 'leaf'
        self.symbol = symbol       # símbolo do alfabeto (para folhas)
        self.left = left           # filho esquerdo (para operadores binários)
        self.right = right         # filho direito (para operadores binários)
        
        # atributos semânticos
        self.nullable = False    
        self.firstpos = set()    
        self.lastpos = set()     
        self.position = None         

    def construct_from_regex(self, postfix_er: str):
        stack = []
        position = 1  # contador de posições das folhas

        for token in postfix_er:
            if token not in ['|', '.', '*', '?', '+']:
                # cria folha
                node = SyntaxTree(node_type='leaf', symbol=token)
                node.position = position
                node.firstpos = {position}
                node.lastpos = {position}
                node.nullable = (token == '&')  # epsilon
                position += 1
                stack.append(node)
                
            elif token == '*' or token == '?' or token == '+':
                if not stack:
                    raise ValueError(f"Operador '{token}' sem operando suficiente")
                child = stack.pop()
                node = SyntaxTree(node_type=token, left=child)
                stack.append(node)
                
            else:  # operadores binários: '|', '.'
                if len(stack) < 2:
                    raise ValueError(f"Operador binário '{token}' sem operandos suficientes")
                right = stack.pop()
                left = stack.pop()
                node = SyntaxTree(node_type=token, left=left, right=right)
                stack.append(node)
        
        if len(stack) != 1:
            raise ValueError("Expressão regular inválida - pilha não contém exatamente um elemento")
            
        return stack[0]