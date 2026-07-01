#Makefile

#Para executar tudo, rode: make setup

# Detecta sistema operacional
UNAME_S := $(shell uname -s)

ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
else ifeq ($(UNAME_S),Linux)
    DETECTED_OS := Linux
else ifeq ($(UNAME_S),Darwin)
    DETECTED_OS := macOS
else
    DETECTED_OS := Unknown
endif

# Nome do ambiente virtual
VENV := venv

# Target padrão
all: info

info:
	@echo "Sistema detectado: $(DETECTED_OS)"
	@echo "Targets disponíveis:"
	@echo "  make graphviz      -> instala Graphviz"
	@echo "  make venv          -> cria ambiente virtual"
	@echo "  make deps          -> instala dependências"
	@echo "  make setup         -> tudo acima (graphviz + venv + deps)"

# Instalação do GRAPHVIZ
graphviz:
ifeq ($(DETECTED_OS),Linux)
	sudo apt install -y graphviz
else ifeq ($(DETECTED_OS),macOS)
	brew install graphviz
else ifeq ($(DETECTED_OS),Windows)
	@echo "Tentando instalar via winget..."
	winget install Graphviz.Graphviz || choco install graphviz -y
endif

# Criação do ambiente virtual
venv:
	python3 -m venv $(VENV)
	@echo "Ambiente virtual criado!"
	@echo "Ative com:"
	@echo " Linux/macOS: source $(VENV)/bin/activate"
	@echo " Windows:     $(VENV)\\Scripts\\activate"

# Instala requirements.txt
deps:
ifeq ($(DETECTED_OS),Windows)
	$(VENV)/Scripts/pip install -r requirements.txt
else
	$(VENV)/bin/pip install -r requirements.txt
endif

# Instala tudo
setup: graphviz venv deps
	@echo "Ambiente completo instalado!"