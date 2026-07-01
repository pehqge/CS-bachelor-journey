from dataclasses import dataclass
from .regular_expression import RegularExpression
from ..automata.automaton import Automaton
from typing import Dict, List, Set
import re

@dataclass
class Token:
    type: str
    lexeme: str

class Converter:

    def __init__(self, initial_expressions: list = None):
        self.definitions: dict[str, str] = {}
        self.raw_expressions: dict[str, str] = {}
        self.automata: dict[str, Automaton] = {}
        self.token_final_pos: dict[str, int] = {}
        self.final_state_to_token: dict[str, str] = {}  # Mapeia estados do autômato final para tokens
        
        # Mapeamento para tratar caracteres especiais
        # Usa caracteres unicode para representar operadores especiais
        self.escape_map = {
            '+': '\uE000',
            '*': '\uE001',
            '.': '\uE002',
            '|': '\uE003',
            '(': '\uE004',
            ')': '\uE005',
            '?': '\uE006',
            '[': '\uE007',
            ']': '\uE008',
            '-': '\uE009',
            '\\': '\uE00A',
            '{': '\uE00B',
            '}': '\uE00C'
        }
        self.reverse_escape_map = {v: k for k, v in self.escape_map.items()}

        if initial_expressions:
            for expr in initial_expressions:
                self.process_expression(expr)

    def process_expression(self, expression: str) -> None:
        if ':' not in expression:
            raise ValueError("Toda expressão deve ser nomeada. Ex: num: [0-9]+")

        parts = expression.split(':', 1)
        name = parts[0].strip()
        er_string = parts[1].strip()
        
        # Trata casos onde o nome do token começa com ':' (ex: ":: :", ":=: :=")
        if not name:
            if ':' in er_string:
                parts2 = er_string.split(':', 1)
                name = ':' + parts2[0].strip()
                er_string = parts2[1].strip()
            else:
                name = ":"
            
        self.raw_expressions[name] = er_string

        # Expande referências a outras ER já definidas -> digits: digit.digit+
        processed_er = self._process_er_with_definitions(er_string)
        
        # Transforma em ER pós-fixada com concatenação explícita
        final_er = self._extract_er(processed_er)

        # Guarda a ER expandida
        self.definitions[name] = final_er

        # Constroi o AFD individual
        automaton = self._build_automaton(final_er, token_name=name)
        self.automata[name] = automaton

    def _process_er_with_definitions(self, er_string: str) -> str:
        result = er_string
        # Ordena por comprimento para evitar substituições parciais incorretas
        for name in sorted(self.raw_expressions.keys(), key=len, reverse=True):
            escaped_name = re.escape(name)
            
            is_alphanum = name.replace('_', '').isalnum()
            if is_alphanum:
                # Para identificadores, usa fronteiras de palavra para evitar substituições dentro de outras palavras
                pattern = f"(?<!\\\\)(?:<{escaped_name}>|\\b{escaped_name}\\b)"
            else:
                # Para símbolos, só substitui se for referência explícita <nome>
                pattern = f"(?<!\\\\)<{escaped_name}>"
            
            replacement = f"({self.raw_expressions[name]})"
            result = re.sub(pattern, lambda _: replacement, result)
        return result

    def _extract_er(self, initial_string: str) -> str:
        # Remove espaços iniciais
        er_string_raw = initial_string.strip()
        
        # Pré-processamento de caracteres especiais: \+ vira placeholder
        er_string = ""
        idx = 0
        while idx < len(er_string_raw):
            if er_string_raw[idx] == '\\' and idx + 1 < len(er_string_raw):
                char = er_string_raw[idx+1]
                if char in self.escape_map:
                    # Caracter especial: \+ vira placeholder
                    er_string += self.escape_map[char]
                else:
                    # Caracter comum, trata como literal
                    er_string += char
                idx += 2
            else:
                er_string += er_string_raw[idx]
                idx += 1
        
        # Descompacta [X-Y] de forma genérica - processa qualquer intervalo (ex: [a-zA-Z], [b-tB-T])
        lista_descompactada = list(er_string)
        nova_lista_descompactada = []
        
        i = 0
        while i < len(lista_descompactada):
            if lista_descompactada[i] == '[':
                # Encontra o conteúdo dentro dos colchetes
                descompactar = ""
                i += 1
                while i < len(lista_descompactada) and lista_descompactada[i] != ']':
                    descompactar += lista_descompactada[i]
                    i += 1
                i += 1  # Pula o ']'
                
                # Processa o conteúdo procurando por padrões X-Y (genérico)
                all_chars = []
                k = 0
                while k < len(descompactar):
                    if k < len(descompactar) - 2 and descompactar[k+1] == '-':
                        # Encontrou um intervalo X-Y
                        start = descompactar[k]
                        end = descompactar[k+2]
                        if len(start) == 1 and len(end) == 1 and ord(start) <= ord(end):
                            # Adiciona todos os caracteres do intervalo
                            for code in range(ord(start), ord(end) + 1):
                                all_chars.append(chr(code))
                            k += 3  # Pula X-Y
                        else:
                            # Hífen inválido, trata como caracteres normais
                            all_chars.append(descompactar[k])
                            k += 1
                    else:
                        # Caractere normal (não é parte de um intervalo)
                        if descompactar[k] != '-':
                            all_chars.append(descompactar[k])
                        k += 1
                
                # Constrói a expressão alternativa: (char1|char2|char3|...)
                if all_chars:
                    nova_lista_descompactada.append('(')
                    for idx, char in enumerate(all_chars):
                        nova_lista_descompactada.append(char)
                        if idx < len(all_chars) - 1:
                            nova_lista_descompactada.append('|')
                    nova_lista_descompactada.append(')')
            else:
                if not lista_descompactada[i].isspace():
                    nova_lista_descompactada.append(lista_descompactada[i])
                i += 1
        
        er_descompactada = "".join(nova_lista_descompactada)
        
        # Insere concatenação explícita
        er_concatenada = "("
        anterior = None
        for c in er_descompactada:
            if anterior is not None:
                # Se o caractere anterior é símbolo, ')' ou operador unário e c é símbolo ou '(', então precisa concatenar
                if (anterior not in ['|', '(', '.'] and anterior is not None) and (c not in ['|', ')', '*', '+', '?', '.']):
                    er_concatenada += '.'
            er_concatenada += c
            anterior = c
        er_concatenada += ").#"
                
        # Transforma em notação pós-fixada (Shunting-yard)
        precedencia = {'|': 1, '.': 2, '*': 3, '?': 4, '+': 5}
        pilha = []
        er = ""
        
        i = 0
        while i < len(er_concatenada):
            token = er_concatenada[i]
            
            if token == '(':
                pilha.append(token)
            elif token == ')':
                while pilha and pilha[-1] != '(':
                    er += pilha.pop()
                if pilha and pilha[-1] == '(':
                    pilha.pop()  # remove '('
            elif token in precedencia:
                # operador
                if token == '*' or token == '?' or token == '+':
                    # é unário e tem precedência alta
                    while pilha and pilha[-1] != '(' and precedencia.get(pilha[-1], 0) >= precedencia[token]:
                        er += pilha.pop()
                    pilha.append(token)
                else:
                    # operador binário
                    while pilha and pilha[-1] != '(' and precedencia.get(pilha[-1], 0) >= precedencia[token]:
                        er += pilha.pop()
                    pilha.append(token)
            else:
                # símbolo literal
                er += token
            
            i += 1
        
        while pilha:
            er += pilha.pop()
        
        return er

    def _build_automaton(self, er: str, token_name: str) -> Automaton:
        try:
            regular_expression = RegularExpression(er)
            leaves_dict = regular_expression.get_leaves()
            
            # Reverte os placeholders para os caracteres originais nas folhas
            new_leaves_dict = {}
            for pos, symbol in leaves_dict.items():
                if symbol in self.reverse_escape_map:
                    new_leaves_dict[pos] = self.reverse_escape_map[symbol]
                else:
                    new_leaves_dict[pos] = symbol
            leaves_dict = new_leaves_dict
            
            regular_expression.compute_parameters()
            firstpos = regular_expression.get_firstpos()
            lastpos = regular_expression.get_lastpos()
            followpos = regular_expression.get_followpos()

            initial = frozenset(firstpos)
            states = [initial]
            unvisited = [initial]
            transitions = {}
            acceptance = {}
            alphabet = set()

            # Pos da folha '#'
            final_pos = None
            for pos, symbol in leaves_dict.items():
                if symbol == '#':
                    final_pos = pos
                    break
            
            if final_pos is None:
                raise ValueError("Marcador '#' não encontrado na ER")

            self.token_final_pos[token_name] = final_pos

            while unvisited:
                S = unvisited.pop(0)

                # Agrupa posições por símbolo
                symbol_groups = {}
                for pos in S:
                    symbol = leaves_dict.get(pos)
                    if symbol and symbol != '#':
                        if symbol not in symbol_groups:
                            symbol_groups[symbol] = set()
                        symbol_groups[symbol].add(pos)

                # Para cada símbolo no estado atual
                for symbol, positions in symbol_groups.items():
                    alphabet.add(symbol)
                    U = set()
                    
                    for pos in positions:
                        if pos in followpos:
                            U.update(followpos[pos])

                    if U:
                        U_frozen = frozenset(U)
                        transitions[(S, symbol)] = U_frozen

                        if U_frozen not in states:
                            states.append(U_frozen)
                            unvisited.append(U_frozen)

                if final_pos in S:
                    acceptance[S] = token_name

            state_mapping = {}
            for i, state in enumerate(states):
                state_mapping[state] = f"q{i}"

            # Cria transições com nomes de estado string
            named_transitions = {}
            for (state, symbol), next_state in transitions.items():
                named_transitions[(state_mapping[state], symbol)] = state_mapping[next_state]

            named_states = set(state_mapping.values())
            named_accept_states = {state_mapping[state] for state in acceptance.keys()}

            automaton = Automaton(
                states=named_states,
                alphabet=alphabet,
                transitions=named_transitions,
                initial_state=state_mapping[initial],
                accept_states=named_accept_states,
                deterministic=True,
            )

            return automaton

        except Exception as e:
            print(f"ERRO ao construir autômato para '{token_name}': {e}")
            raise

    def build_final_automaton(self) -> Automaton:
        """Constrói o autômato final unindo todos os autômatos individuais"""
        if not self.automata:
            raise ValueError("Nenhum autômato foi construído")
                
        # Se só há um autômato, retorna ele mesmo
        if len(self.automata) == 1:
            token_name = list(self.automata.keys())[0]
            automaton = list(self.automata.values())[0]
            # Mapeia todos os estados de aceitação para o token
            for state in automaton.accept_states:
                self.final_state_to_token[state] = token_name
            return automaton
        
        # Para múltiplos autômatos, faz a união
        # Primeiro, cria um mapeamento de estados originais para tokens
        original_state_to_token = {}
        for token_name, automaton in self.automata.items():
            for state in automaton.accept_states:
                original_state_to_token[state] = token_name
        
        final_automaton = Automaton.union(list(self.automata.values()))
        

        # Rastreia quais estados originais estão em cada estado determinizado
        state_sets_to_tokens = {}
        for token_name, automaton in self.automata.items():
            for state in automaton.accept_states:
                state_sets_to_tokens[frozenset([state])] = token_name
        
        final_automaton.determinize()
                
        final_automaton.minimize()
        
        # Após minimização, os estados podem ter mudado novamente
        # Vamos usar uma abordagem diferente: testar o lexema contra cada autômato individual
        return final_automaton
    
    def get_lexical_table(self, automaton: Automaton) -> Dict[str, Dict[str, str]]:
        """Retorna a tabela de análise léxica"""
        table = {}
        sorted_states = sorted(list(automaton.states), key=str)
        sorted_alphabet = sorted(list(automaton.alphabet))

        for state in sorted_states:
            row = {}
            for symbol in sorted_alphabet:
                if (state, symbol) in automaton.transitions:
                    row[symbol] = automaton.transitions[(state, symbol)]
                else:
                    row[symbol] = "erro"
            table[str(state)] = row
            
        return table

    def tokenize(self, palavras: List[str], automaton: Automaton) -> List[Token]:
        """Executa análise léxica processando palavras completas"""
        tokens = []
        for palavra in palavras:
            # Para cada palavra, tenta encontrar o token correspondente
            token_type = self._identify_token_from_lexeme(palavra, automaton, None)
            if token_type:
                tokens.append(Token(token_type, palavra))
            else:
                tokens.append(Token("erro!", palavra))

        return tokens

    def _identify_token_from_lexeme(self, lexeme: str, final_automaton: Automaton, accept_state: str) -> str:
        """Identifica o token testando o lexema contra cada autômato individual"""
        # Testa na ordem de definição para respeitar precedência (primeiro ganha)
        for token_name in list(self.automata.keys()):
            individual_automaton = self.automata[token_name]
            if self._lexeme_matches_automaton(lexeme, individual_automaton):
                return token_name
        return None
    
    def _lexeme_matches_automaton(self, lexeme: str, automaton: Automaton) -> bool:
        """Verifica se um lexema é aceito por um autômato"""
        state = automaton.initial_state
        for char in lexeme:
            if (state, char) in automaton.transitions:
                state = automaton.transitions[(state, char)]
            else:
                return False
        return state in automaton.accept_states