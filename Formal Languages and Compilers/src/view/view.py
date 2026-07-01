import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QStringListModel, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QImageReader
from view.automata_image_dialog import AutomataImageDialog

class View(QtWidgets.QMainWindow):
    def __init__(self, controller):
        self.app = QtWidgets.QApplication(sys.argv)
        
        # Aumentar limite de alocação de imagem para evitar erro com imagens grandes
        QImageReader.setAllocationLimit(0)

        super().__init__()
        uic.loadUi("view/main.ui", self)
        self.controller = controller

        self.connect_signals()
        self.analysis_input.setPlaceholderText("a + b * c\n24566\nvariavel1")
        
        self.show()

    def run(self):
        sys.exit(self.app.exec())
    
    # ----- Message Helpers

    def show_success_message(self, title: str, message: str):
        """Displays a success message to the user."""

        QtWidgets.QMessageBox.information(
            self,
            title,
            message,
            QtWidgets.QMessageBox.StandardButton.Ok
        )

    def show_error_message(self, title: str, message: str):
        """Displays an error message to the user."""

        QtWidgets.QMessageBox.warning(
            self,
            title,
            message,
            QtWidgets.QMessageBox.StandardButton.Ok
        )

    # ----- UI Signal Connections

    def connect_signals(self):

        # Regex tab
        self.regex_load_button.clicked.connect(self.on_load_regex_file)
        self.regex_save_button.clicked.connect(self.on_save_regex_file)
        self.regex_process_button.clicked.connect(self.on_process_regex)

        # Automata tab
        self.automata_combo.currentIndexChanged.connect(self.on_select_automaton)
        self.automata_export_button.clicked.connect(self.on_export_automaton)
        self.automata_expand.clicked.connect(self.on_expand_automata_image)

        # Analysis tab
        self.analysis_load_button.clicked.connect(self.on_load_source_file)
        self.analysis_save_button.clicked.connect(self.on_save_source_file)
        self.analysis_process_button.clicked.connect(self.on_process_source)
        self.analysis_save_tokens_button.clicked.connect(self.on_save_tokens)
        
        # SLR tab signals
        self.connect_slr_signals()

    # ----- File Dialog Helpers

    def _get_open_filepath(self, caption="Open File", filter="Text Files (*.txt)"):
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, caption, "", filter)
        return filepath

    def _get_save_filepath(self, caption="Save File", filter="Text Files (*.txt)"):
        filepath, _ = QtWidgets.QFileDialog.getSaveFileName(self, caption, "", filter)
        return filepath

    def _validate_content_before_save(self, content, error_message: str) -> bool:

        is_empty = False
        if isinstance(content, str):
            is_empty = not content.strip()
        elif isinstance(content, list):
            is_empty = len(content) == 0
        else:
            is_empty = not bool(content)
        
        if is_empty:
            self.show_error_message("Erro ao Salvar", error_message)
            return False
        return True

    # ---- Regex Tab Handlers

    def on_load_regex_file(self):

        filepath = self._get_open_filepath("Carregar Definições Regulares")
        if filepath:
            content = self.controller.read_file_content(filepath)
            self.regex_input.setPlainText(content)

    def on_save_regex_file(self):

        content = self.regex_input.toPlainText()
        if not self._validate_content_before_save(
            content,
            "Não há definições regulares para salvar."
        ):
            return
        
        filepath = self._get_save_filepath("Salvar Definições Regulares")
        if filepath:
            self.controller.save_content_to_file(filepath, content)

    def on_process_regex(self):

        definitions = self.regex_input.toPlainText()
        if not definitions or not definitions.strip():
            self.show_error_message("Erro ao Processar", "Por favor, preencha o campo com definições regulares antes de processar.")
            return
        
        self.controller.handle_process_regex(definitions)

    # ----- Automata Tab Handlers

    def on_select_automaton(self):

        selected_automaton = self.automata_combo.currentText()
        if selected_automaton:
            self.controller.handle_automaton_selected(selected_automaton)

    def on_export_automaton(self):

        selected_automaton = self.automata_combo.currentText()
        if not selected_automaton:
            self.show_error_message("Erro ao Exportar", "Não há um autômato selecionado para exportar.")
            return

        filepath = self._get_save_filepath("Exportar Autômato para JFLAP", "JFLAP Files (*.jff)")
        if filepath:
            self.controller.handle_export_automaton(selected_automaton, filepath)

    # ----- Analysis Tab Handlers

    def on_load_source_file(self):

        filepath = self._get_open_filepath("Carregar Arquivo Fonte")
        if filepath:
            content = self.controller.read_file_content(filepath)
            self.analysis_input.setPlainText(content)

    def on_save_source_file(self):

        content = self.analysis_input.toPlainText()
        if not self._validate_content_before_save(
            content,
            "Não há código fonte para salvar."
        ):
            return
        
        filepath = self._get_save_filepath("Salvar Arquivo Fonte")
        if filepath:
            self.controller.save_content_to_file(filepath, content)

    def on_process_source(self):

        source_text = self.analysis_input.toPlainText()
        if source_text:
            self.controller.handle_process_analysis(source_text)
        else:
            self.show_error_message("Erro ao Processar", "Não há lexemas para processar.")
            self.update_token_list([])
            return

    def on_save_tokens(self):

        model = self.analysis_token_list.model()
        if not model:
            self.show_error_message("Erro ao Salvar", "Não há tokens gerados para salvar.")
            return

        tokens = model.stringList()
        if not self._validate_content_before_save(
            tokens,
            "Não há tokens gerados para salvar."
        ):
            return

        filepath = self._get_save_filepath("Salvar Tokens Gerados")
        if filepath:
            self.controller.handle_save_tokens(filepath, tokens)

    # ----- Public Methods Called by Controller

    def update_automata_list(self, automata_names: list[str]):

        self.automata_combo.clear()
        self.automata_combo.addItems(automata_names)

    def update_automaton_table(self, automaton):
        """Updates the transition table of the selected automaton."""
        if not automaton:
            self._update_table(self.automata_table, [], [])
            return
        
        # Get sorted alphabet without epsilon
        sorted_alphabet = sorted([s for s in automaton.alphabet if s != "&"])
        
        # Sort states naturally
        try:
            sorted_states = sorted(list(automaton.states), key=lambda x: int(x[1:]) if x.startswith('q') and x[1:].isdigit() else x)
        except:
            sorted_states = sorted(list(automaton.states))
        
        headers = ["Estado"] + sorted_alphabet
        rows = []
        
        for state in sorted_states:
            # Mark initial and acceptance states
            state_label = str(state)
            if state == automaton.initial_state:
                state_label = f"→ {state_label}"
            if state in automaton.accept_states:
                state_label = f"{state_label} *"
            
            row = [state_label]
            for symbol in sorted_alphabet:
                transition_key = (state, symbol)
                if transition_key in automaton.transitions:
                    target = automaton.transitions[transition_key]
                    if isinstance(target, set) or isinstance(target, list):
                        target_str = ",".join(sorted([str(t) for t in target]))
                        row.append(f"{{{target_str}}}")
                    else:
                        row.append(str(target))
                else:
                    row.append("-")
            rows.append(row)
        
        self._update_table(self.automata_table, headers, rows)

    def update_token_list(self, tokens: list[str]):

        model = QStringListModel()
        model.setStringList(tokens)
        self.analysis_token_list.setModel(model)

    def update_lexical_table(self, table_data: dict):
        if not table_data:
            self._update_table(self.table_table, [], [])
            return

        all_symbols = set()
        for row in table_data.values():
            all_symbols.update(row.keys())
        sorted_symbols = sorted(list(all_symbols))
        
        try:
            sorted_states = sorted(list(table_data.keys()), key=lambda x: int(x[1:]) if x.startswith('q') and x[1:].isdigit() else x)
        except:
            sorted_states = sorted(list(table_data.keys()))

        headers = ["State"] + sorted_symbols
        rows = []
        
        for state in sorted_states:
            row = [str(state)]
            transitions = table_data[state]
            for symbol in sorted_symbols:
                target = transitions.get(symbol, "")
                if isinstance(target, set) or isinstance(target, list):
                    target_str = ",".join(sorted([str(t) for t in target]))
                    row.append(f"{{{target_str}}}")
                else:
                    row.append(str(target))
            rows.append(row)
        
        self._update_table(self.table_table, headers, rows)


    def on_expand_automata_image(self):
        """Dialog com imagem expandida do autômato."""
        name = self.automata_combo.currentText()
        if not name: 
            return self.show_error_message("Erro", "Selecione um autômato.")
        
        try:
            if img := self.controller.handle_generate_automaton_image(name):
                AutomataImageDialog(img, name, self).exec()
            else:
                self.show_error_message("Erro", "Falha ao gerar imagem.")
        except Exception as e:
            self.show_error_message("Erro", f"Erro ao abrir imagem: {e}")

    # ----- SLR Tab Signal Connections

    def connect_slr_signals(self):
        """Connect all SLR tab signals."""
        # Reserved words
        self.reserved_add.clicked.connect(self.on_add_reserved_word)
        self.reserved_remove.clicked.connect(self.on_remove_reserved_word)
        self.reserved_input.returnPressed.connect(self.on_add_reserved_word)
        
        # Grammar
        self.gramatic_load.clicked.connect(self.on_load_grammar)
        self.gramatic_save.clicked.connect(self.on_save_grammar)
        self.gramatic_build.clicked.connect(self.on_build_slr_table)
        
        # Syntax analysis
        self.syntax_import_button.clicked.connect(self.on_import_tokens)
        self.syntax_load_button.clicked.connect(self.on_load_syntax_tokens)
        self.syntax_input_save.clicked.connect(self.on_save_syntax_tokens)
        self.syntax_input_button.clicked.connect(self.on_parse_syntax)
        self.lr0_button.clicked.connect(self.on_view_lr0)

    # ----- SLR Tab Handlers

    def on_add_reserved_word(self):
        """Handle adding reserved word."""
        word = self.reserved_input.text().strip()
        if word:
            self.controller.handle_add_reserved_word(word)
            self.reserved_input.clear()

    def on_remove_reserved_word(self):
        """Handle removing reserved word."""
        selected = self.reserved_list.currentItem()
        if selected:
            word = selected.text()
            self.controller.handle_remove_reserved_word(word)

    def on_load_grammar(self):
        """Handle loading grammar from file."""
        filepath = self._get_open_filepath("Carregar Gramática")
        if filepath:
            content = self.controller.handle_load_grammar(filepath)
            if content:
                self.gramatic_input.setPlainText(content)

    def on_save_grammar(self):
        """Handle saving grammar to file."""
        content = self.gramatic_input.toPlainText()
        if not self._validate_content_before_save(content, "Não há gramática para salvar."):
            return
        
        filepath = self._get_save_filepath("Salvar Gramática")
        if filepath:
            self.controller.handle_save_grammar(filepath, content)

    def on_build_slr_table(self):
        """Handle building SLR table."""
        grammar_text = self.gramatic_input.toPlainText()
        if not grammar_text or not grammar_text.strip():
            self.show_error_message("Erro", "Por favor, preencha a gramática antes de construir a tabela.")
            return
        
        reserved_words = self.controller.symbol_table.get_reserved_words()
        self.controller.handle_build_slr_table(grammar_text, reserved_words)

    def on_import_tokens(self):
        """Handle importing tokens from lexical analysis."""
        self.controller.handle_import_tokens_from_lexical()

    def on_load_syntax_tokens(self):
        """Handle loading syntax tokens from file."""
        filepath = self._get_open_filepath("Carregar Tokens")
        if filepath:
            content = self.controller.read_file_content(filepath)
            if content:
                self.syntax_input_text.setPlainText(content)

    def on_save_syntax_tokens(self):
        """Handle saving syntax tokens to file."""
        content = self.syntax_input_text.toPlainText()
        if not self._validate_content_before_save(content, "Não há tokens para salvar."):
            return
        
        filepath = self._get_save_filepath("Salvar Tokens")
        if filepath:
            self.controller.save_content_to_file(filepath, content)

    def on_parse_syntax(self):
        """Handle syntax parsing."""
        tokens_input = self.syntax_input_text.toPlainText()
        if not tokens_input or not tokens_input.strip():
            self.show_error_message("Erro", "Por favor, preencha os tokens antes de analisar.")
            return
        
        self.controller.handle_parse_syntax(tokens_input)

    def on_view_lr0(self):
        """Handle view LR(0) states button click."""
        try:
            img_data = self.controller.handle_view_lr0()
            if img_data:
                AutomataImageDialog(img_data, "Diagrama Canônico LR(0)", self).exec()
        except Exception as e:
            self.show_error_message("Erro", f"Erro ao visualizar diagrama: {e}")

    # ----- SLR View Update Methods

    def _update_table(self, view, headers, rows, force_stretch=False):
        """Generic helper to update QTableView models."""
        if not rows:
            view.setModel(None)
            return
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)
        for row in rows:
            model.appendRow([QStandardItem(str(item)) for item in row])
        view.setModel(model)
        
        # Make table non-editable
        view.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # Enable word wrap and auto-resize rows
        view.setWordWrap(True)
        view.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        
        # Determine resize mode: Stretch if content fits, ResizeToContents if too wide
        header = view.horizontalHeader()
        
        if force_stretch:
            header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        else:
            header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            view.resizeColumnsToContents()

            total_width = sum(header.sectionSize(i) for i in range(header.count()))

            available_width = view.width()
            if hasattr(self, 'tabWidget'):
                available_width = self.tabWidget.width() - 45
            
            if total_width <= available_width * 0.8 and available_width > 0:
                header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
            else:
                header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

    def update_reserved_words_list(self, words: list):
        """Update reserved words list."""
        self.reserved_list.clear()
        self.reserved_list.addItems(words)

    def update_action_table(self, action_table: dict, terminals: set):
        """Update ACTION table view."""
        if not action_table: 
            return self.action_table.setModel(None)
        
        terminals = sorted(list(terminals | {'$'}))
        rows = []
        slr = self.controller.current_slr
        
        for state in sorted(action_table.keys()):
            row = [state]
            for term in terminals:
                action = action_table[state].get(term)
                row.append(slr.format_action(action) if slr and action else "-")
            rows.append(row)
            
        self._update_table(self.action_table, ["Estado"] + terminals, rows)

    def update_goto_table(self, goto_table: dict, non_terminals: set):
        """Update GOTO table view."""
        if not goto_table: 
            return self.goto_table.setModel(None)
        
        nts = sorted(list(non_terminals))
        rows = [[state] + [goto_table[state].get(nt, "-") for nt in nts] 
                for state in sorted(goto_table.keys())]
        
        self._update_table(self.goto_table, ["Estado"] + nts, rows)

    def update_slr_information(self, info: dict):
        """Update SLR information display."""
        lines = []
        
        for key in ['first_sets', 'follow_sets']:
            if key in info:
                name = key.replace('_sets', '').upper()
                lines.append(f"--- {name} ---")
                for k, v in sorted(info[key].items()):
                    lines.append(f"{k} = {{ {', '.join(sorted(v))} }}")
                lines.append("") 
        
        model = QStringListModel()
        model.setStringList(lines)
        self.informations_text.setModel(model)

    def update_syntax_tokens_table(self, tokens: list):
        """Update syntax tokens input table."""
        rows = [[t.get('token', ''), t.get('lexeme', ''), t.get('position', '')] for t in tokens] if tokens else []
        self._update_table(self.syntax_tokens_table, ["Token", "Lexema", "Posição"], rows)

    def update_parsing_result_table(self, history: list):
        """Update parsing result table."""
        rows = []
        if history:
            rows = [[
                str(step.get('stack', [])),
                ' '.join(str(t) for t in step.get('input', [])),
                step.get('action', '-')
            ] for step in history]
        self._update_table(self.syntax_parsing_table, ["Stack", "Input", "Action"], rows, force_stretch=True)

    def show_parsing_result(self, accepted: bool):
        """Show final parsing result."""
        title, msg = "Análise Sintática", "Sentença Aceita!" if accepted else "Sentença Rejeitada!"
        func = self.show_success_message if accepted else self.show_error_message
        func(title, msg)
