PYTHON = python3

VENV_DIR = venv

VENV_PYTHON = $(VENV_DIR)/bin/python
VENV_PIP = $(VENV_DIR)/bin/pip

run: $(VENV_DIR)/bin/activate install run_main

$(VENV_DIR)/bin/activate:
	@test -d $(VENV_DIR) || (echo "Criando ambiente virtual em $(VENV_DIR)..."; $(PYTHON) -m venv $(VENV_DIR))
	@touch $(VENV_DIR)/bin/activate

install: $(VENV_DIR)/bin/activate
	@echo "Instalando dependências de requirements.txt..."
	@$(VENV_PIP) install -q -r requirements.txt

run_main: $(VENV_DIR)/bin/activate
	@echo "Executando main.py..."
	@$(VENV_PYTHON) main.py

clean:
	@echo "Limpando arquivos gerados e ambiente virtual..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@rm -rf $(VENV_DIR)

.PHONY: run install run_main clean