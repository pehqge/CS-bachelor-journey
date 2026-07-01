from view.view import View
from model.regex.converter import Converter
from model.automata.automaton import Automaton
from model.grammar.symbol_table import SymbolTable
from model.grammar.cfg import CFG
from model.parser.slr import SLR
from pathlib import Path
import hashlib
import re

class Controller:
    def __init__(self):
        self.view = View(self)
        self.converter = Converter()
        self.final_automaton = None
        
        self._automata_images_cache = {}
        
        # SLR components
        self.symbol_table = SymbolTable()
        self.current_slr = None
        self.current_grammar = None
        self.lexical_tokens = []  # Tokens from lexical analysis

    def run(self):
        self.view.run()

    # ---- Regex Tab Handlers

    def handle_process_regex(self, definitions: str):
        """Handles the request to process regular expressions."""

        self.converter = Converter()
        self.final_automaton = None
        
        lines = definitions.strip().split('\n')
        processed = False
        
        for line in lines:
            if line.strip():
                try:
                    self.converter.process_expression(line)
                    processed = True
                except Exception as e:
                    print(f"Erro ao processar '{line}': {e}")
        
        if processed:
            try:
                self.final_automaton = self.converter.build_final_automaton()
                
                automata_names = list(self.converter.automata.keys()) + ["Autômato Final"]
                self.view.update_automata_list(automata_names)
                
                # Update lexical table for final automaton
                table = self.converter.get_lexical_table(self.final_automaton)
                self.view.update_lexical_table(table)

                # Show success message
                self.view.show_success_message("Processamento Concluído", 
                    "As expressões regulares foram processadas com sucesso!\n"
                    f"Foram gerados {len(self.converter.automata)} autômatos individuais e 1 autômato final.")

            except Exception as e:
                print(f"Erro ao construir autômato final: {e}")

        else:
            print("Nenhuma expressão válida foi processada")

    # ----- Automata Tab Handlers

    def handle_automaton_selected(self, automaton_name: str):
        """Handles the selection of an automaton from the dropdown."""

        automaton = None
        
        if automaton_name == "Autômato Final":
            automaton = self.final_automaton
        else:
            automaton = self.converter.automata.get(automaton_name)
            
        if automaton:
            self.view.update_automaton_table(automaton)


    def handle_export_automaton(self, automaton_name: str, file_path: str):
        """Handles the request to export an automaton to a file."""

        path = Path(file_path)
        directory = path.parent
        filename = path.stem
        
        automaton = None

        if automaton_name == "Autômato Final":
            automaton = self.final_automaton
        else:
            automaton = self.converter.automata.get(automaton_name)
            
        if automaton:
            try:
                automaton.to_jflap_xml(filename, directory)
                self.view.show_success_message("Exportação Concluída", 
                    f"O autômato '{automaton_name}' foi exportado com sucesso! Em: {directory / f'{filename}.jff'}")
            except Exception as e:
                self.view.show_error_message("Erro ao Exportar", f"Erro ao exportar autômato: {e}")

    def handle_generate_automaton_image(self, automaton_name: str) -> bytes:
        """Gera imagem do autômato com cache."""
        automaton = self.final_automaton if automaton_name == "Autômato Final" else self.converter.automata.get(automaton_name)
        if not automaton: return None

        h = self._get_automaton_hash(automaton)
        if h not in self._automata_images_cache:
            try:
                self._automata_images_cache[h] = automaton.generate_diagram_image()
            except Exception as e:
                print(f"Erro geração imagem: {e}")
                return None
        return self._automata_images_cache[h]
    
    def _get_automaton_hash(self, automaton: Automaton) -> str:
        """Hash único para cache."""
        key = (str(sorted(automaton.states)), str(sorted(automaton.alphabet)),
               str(sorted(automaton.transitions.items())), str(automaton.initial_state),
               str(sorted(automaton.accept_states)))
        return hashlib.md5("|".join(key).encode()).hexdigest()[:12]

    # ----- Analysis Tab Handlers

    def handle_process_analysis(self, source_text: str):
        """Handles the request to analyze source text."""
        
        if not self.final_automaton:
            self.view.show_error_message("Erro", "Nenhum autômato final disponível. Processe as expressões regulares primeiro.")
            return

        # Split by newlines first, then by whitespace to handle line-by-line input
        lines = source_text.strip().split('\n')
        words = []
        for line in lines:
            if line.strip():
                words.extend(line.split())
        
        try:
            tokens = self.converter.tokenize(words, self.final_automaton)
            token_strings = [f"<{t.lexeme}, {t.type}>" for t in tokens]
            self.view.update_token_list(token_strings)
            
            # Store tokens for SLR parsing
            self.lexical_tokens = tokens
            
        except Exception as e:
            self.view.show_error_message("Erro durante a análise", e)

    def handle_save_tokens(self, file_path: str, tokens: list):
        """Handles the request to save generated tokens to a file."""

        content = "\n".join(tokens)
        self.save_content_to_file(file_path, content)
        self.view.show_success_message("Arquivo Salvo", f"Os tokens foram salvos com sucesso! Em: {file_path}")

    # ----- File Handlers

    def read_file_content(self, file_path: str) -> str:
        """Reads and returns the content of a file."""

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            self.view.show_error_message("Erro ao Ler", f"Arquivo não encontrado: {file_path}")
            return ""
        except Exception as e:
            self.view.show_error_message("Erro ao Ler", f"Erro ao ler arquivo: {e}")
            return ""

    def save_content_to_file(self, file_path: str, content: str):
        """Saves the given content to a file."""

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            self.view.show_error_message("Erro ao Salvar", f"Erro ao salvar arquivo: {e}")

    # ----- SLR Tab Handlers

    def handle_add_reserved_word(self, word: str):
        if word and word.strip():
            self.symbol_table.add_reserved(word.strip())
            self.view.update_reserved_words_list(self.symbol_table.get_reserved_words())

    def handle_remove_reserved_word(self, word: str):
        if word:
            self.symbol_table.remove_reserved(word)
            self.view.update_reserved_words_list(self.symbol_table.get_reserved_words())

    def handle_load_grammar(self, file_path: str):
        return self.read_file_content(file_path)

    def handle_save_grammar(self, file_path: str, grammar_text: str):
        self.save_content_to_file(file_path, grammar_text)

    def handle_build_slr_table(self, grammar_text: str, reserved_words: list):
        try:
            grammar = CFG.from_text(grammar_text)
            grammar.simplify_grammar()
            
            if grammar.P is None:
                return self.view.show_error_message("Erro", "Gramática inválida após simplificação.")
            
            self.current_grammar, self.current_slr = grammar, SLR(grammar)
            ACTION, GOTO = self.current_slr.build_parsing_table()
            
            self.view.update_action_table(ACTION, grammar.T)
            self.view.update_goto_table(GOTO, grammar.N)
            self.view.update_slr_information({
                'lr0_states': self.current_slr.get_lr0_states_count(),
                'productions': self.current_slr.get_productions_count(),
                'first_sets': grammar.first(),
                'follow_sets': grammar.follow()
            })
            
            self.view.show_success_message("Tabela SLR Construída", 
                f"Tabela SLR construída com sucesso!\nEstados LR(0): {self.current_slr.get_lr0_states_count()}\nProduções: {self.current_slr.get_productions_count()}")
            
            return {'action': ACTION, 'goto': GOTO}
            
        except Exception as e:
            self.view.show_error_message("Erro ao Construir Tabela SLR", f"Erro: {e}")
            return None

    def handle_import_tokens_from_lexical(self):
        if not self.lexical_tokens:
            self.view.show_error_message("Erro", "Nenhum token disponível da análise léxica.")
            return []
        
        converted = []
        for t in self.lexical_tokens:
            lexeme, token_type = self.symbol_table.get_token(t.lexeme)
        
            converted.append(f"<{lexeme}, {token_type}>")
            
        self.view.syntax_input_text.setPlainText('\n'.join(converted))
        return converted

    def handle_parse_syntax(self, tokens_input: str):
        if not self.current_slr:
            return self.view.show_error_message("Erro", "Nenhuma tabela SLR construída. Construa a tabela primeiro.")
        
        tokens = self._parse_token_input(tokens_input)
        if not tokens:
            return self.view.show_error_message("Erro", "Nenhum token válido encontrado.")
            
        token_list, token_details = [], []
        
        for t_str in tokens:
            lexeme, t_type, pos = t_str, t_str, '-'
            
            if t_str.startswith('<') and t_str.endswith('>'):
                match = re.match(r'<(.+?),\s*(.+?)>', t_str)
                if match:
                    lexeme = match.group(1).strip()
                    type_or_pos = match.group(2).strip()
                    if type_or_pos == 'PR':
                        t_type = lexeme.lower()
                    elif type_or_pos.isdigit():
                        t_type = self._find_token_type_by_lexeme(lexeme) or lexeme.lower()
                        pos = type_or_pos
                    else:
                        t_type = type_or_pos
                else:
                    # Tentar parsear sem vírgula (caso especial)
                    content = t_str[1:-1].strip()
                    t_type = content
            
            token_list.append(t_type)
            token_details.append({'token': t_type, 'lexeme': lexeme, 'position': pos})
            
        try:
            history = self.current_slr.parse(token_list, return_history=True)
            accepted = history[-1].get('accepted', False) if history else False
            
            self.view.update_syntax_tokens_table(token_details)
            self.view.update_parsing_result_table(history)
            self.view.show_parsing_result(accepted)
            
            return {'history': history, 'accepted': accepted}
        except Exception as e:
            self.view.show_error_message("Erro ao Analisar", f"Erro durante análise sintática: {e}")
            return None

    def handle_view_lr0(self) -> bytes:
        """Handles the request to view Canonical LR(0) states."""
        if not self.current_slr:
            self.view.show_error_message("Erro", "Nenhuma tabela SLR construída. Construa a tabela primeiro.")
            return None
        
        try:
            return self.current_slr.generate_canonical_collection_image()
        except Exception as e:
            print(f"Erro ao gerar diagrama LR(0): {e}")
            self.view.show_error_message("Erro", f"Erro ao gerar diagrama LR(0): {e}")
            return None

    
    def _find_token_type_by_lexeme(self, lexeme: str) -> str:
        return next((t.type for t in self.lexical_tokens if t.lexeme == lexeme), None)

    def _parse_token_input(self, text: str) -> list:
        tokens = []
        for line in text.strip().split('\n'):
            line = line.strip()
            if not line: continue
            # Se a linha começa com < e termina com >, assumimos que é um token completo
            if line.startswith('<') and line.endswith('>'):
                tokens.append(line)
            else:
                # Caso contrário, usa a estratégia antiga para pegar tokens na mesma linha
                tokens.extend(re.findall(r'<[^>]+>|\S+', line))
        return tokens
