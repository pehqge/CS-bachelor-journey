# Alterações feitas aqui
1. Organização das pastas para deixar mais claro onde estão as coisas.
2. Criação de uma classe sistema que organiza o pygame e faz o gerenciamento dos estados
   - Como ela funciona:
        - Eu criei um dicionario com todos os estados possiveis (já abordarei como funciona um estado). Depois instancio o estado atual, que é o estado que deverá ser renderizado na tela.
        - Por ultimo, criei uma função que gerencia o estado atual para o proximo estado
3. Criação de Estados
    - Como os estados funcionam:
       - Existem 4 funções principais de cada estado (nem todas elas vão ser usadas no momento por motivos de: MVP)
         - **Render:** O objetivo dessa função é unicamente cuidar das partes gráficas, então tudo que é blit vai nela
         - **Update:** A função update é quem cuida de todos os tratamentos de teclas e funções. Tanto é que ela recebe os eventos direto do loop principal para poder usar funções do tipo if event.type == pygame.KEYDOWN...
         - **Entering:** Esta função é a que cuida de gerenciamentos que se devem fazer quando o estado começa. Coisas do tipo setar a música atual, reiniciar uma variável que precisa...
         - **Exiting:** Função para fazer a mesma coisa da de cima só que na saída. Então se é necessário salvar os dados do jogador, é aqui que se faz isso. Ou até mesmo se precisar apagar tudo que já se fez.
       - A ideia dos estados é que se crie o nível inteiro nele e que dentro dele ocorra o gerenciamento da troca de fases. Tanto é que criei dentro de Jogo() uma lista de fases para se fazer a troca entre elas dentro desse estado.
       - A atual classe Fase() vai ser útil apenas para gerenciar o mapa do tile e suas colisões, mas o suco inteiro será feito no Jogo().
       - Olhe para a classe MenuState() para ter uma noção de como implementei ela. No init começo definindo todas as imagens que vou usar e depois faço o desenho em render(), e o tratamento de eventos em update()
4. Criação de uma classe Botão()
    - Nela, fiz 2 funções principais, uma que desenha o botão e outra que faz a checagem se o botão está clicado no momento e retorna uma Bool para fazer gerenciamento de eventos posteriormente.
5. Criação da classe Mapas()
    - A ideia aqui foi tirar aquele arquivo presets, já que isso não pode existir em POO. Então, criamos uma lista com todos os mapas e a definição do tamanho que a tela deverá ter

## O que precisa mudar?
- Organização da classe Fase e Jogador
  - Para isso, seria interessante deixá-las mais coesas e POO. A dica que pensei é tentar especializar o máximo que conseguir na classe Fase, para ela ser tipo o Modelo (pensando em MVC) e o estado Jogo() ser o controle que faz todo o gerenciamento.
- Fazer a transição de fases utilizando a classe Jogo()
  - Nela, eu fiz um atributo chamado self.__fase_atual que é um número, este número é o indice da lista de fases totais. Então tente fazer uma implementação que some 1 a esse atributo toda vez que progredir o nivel, mas também fazendo uma verificação que não ultrapasse o total de níveis.