## SGI - Sistema Gráfico Interativo

Seguem abaixo as instruções para rodar o SGI.

#### Opção 1: via Makefile
- Utilize o comando `make`. Ele automaticamente criará um ambiente virtual, onde serão instaladas todas as dependências, e o programa irá executar a partir desse ambiente.


#### Opção 2: instalação manual
- Instale as dependências: `pip install -r requirements.txt`
- Execute o arquivo `main.py`: `python main.py`


### Como testar?
No canto inferior direito da tela, existe um botão chamado "Add Test Objects". Ao pressioná-lo, uma série de objetos pré-definidos - como um cubo, alguns segmentos de reta, etc - serão adicionados ao mundo do sistema gráfico (ver display_file_manager.py). Você pode então testar as funcionalidades do SGI (rotação, zoom,  ransformações, etc) e observar os efeitos provocados nesses objetos, verificando se comportam-se da maneira esperada.