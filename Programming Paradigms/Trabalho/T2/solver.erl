-module(solver).
-export([main/0]).

% ----- * definicoes de modelagem do puzzle * -----

-define(WIDTH, 8).
-define(HEIGHT, 8).

% cria o grid inicial combinando as posicoes com os valores iniciais
initial_grid() ->
    PosList = positions(),
    Values = initial_grid_values(),
    Pairs = lists:zip(PosList, Values),
    maps:from_list(Pairs).

% lista dos valores iniciais do grid (0 significa celula vazia)
initial_grid_values() ->
  [0, 0, 0, 6, 5, 3, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 2, 4, 0, 0, 3, 0, 0, 3, 1, 0, 6, 0, 0, 0, 4, 0, 0, 3, 0, 6, 0, 0, 0, 4, 0, 2, 0, 0, 0, 0, 1, 3, 0, 0, 5, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 2, 4].

% rotulos das regioes
region_map() ->
    PosList = positions(), % lista de tuplas com todas as posicoes
    Values = region_map_values(), % numero da regiao de cada celula
    Pairs = lists:zip(PosList, Values), % junta as posicoes com os numeros das regioes
    maps:from_list(Pairs). % cria um map de posicoes para numeros de regioes

% valores dos numeros das regioes para cada posicao
region_map_values() ->
  [1, 5, 2, 9, 9, 9, 9, 9, 1, 2, 2, 10, 9, 15, 9, 19, 2, 2, 2, 10, 11, 15, 16, 16, 2, 3, 3, 11, 11, 16, 16, 16, 3, 3, 7, 8, 12, 12, 18, 18, 4, 3, 3, 8, 8, 17, 17, 18, 4, 3, 8, 8, 13, 13, 18, 18, 4, 6, 6, 8, 14, 14, 14, 14].

% cria um mapa onde a chave e o numero da regiao e o valor e uma lista com as posicoes que pertencem a essa regiao
regions() ->
    RegionMap = region_map(),
    lists:foldl(
        fun(Pos, Acc) ->
            RegionNum = maps:get(Pos, RegionMap), % pega o numero da regiao da posicao
            OldList = maps:get(RegionNum, Acc, []), % pega a lista de posicoes ja acumuladas para essa regiao
            maps:put(RegionNum, [Pos | OldList], Acc) % adiciona a posicao atual na lista da regiao
        end, % funcao que vai ser aplicada a cada posicao
        #{}, % inicia o acumulador como um map vazio
        positions() % lista de todas as posicoes
    ).

% gera uma lista de todas as posicoes do grid
positions() ->
    [{Y, X} || Y <- lists:seq(1, ?HEIGHT), X <- lists:seq(1, ?WIDTH)].

% ----- * algoritmo de solving * -----

main() ->
    Grid = initial_grid(),
    case solve(Grid) of
        {ok, Solution} -> display_grid(Solution);  % mostra a solucao caso encontre
        error -> io:format("Nenhuma solucao encontrada~n")  % se nao encontrar, avisa
    end.

% comeca resolvendo pela posicao (1,1)
solve(Grid) ->
    solver(Grid, {1, 1}).

% funcao recursiva principal do backtracking
solver(Grid, {Y, _X}) when Y > ?HEIGHT ->
    {ok, Grid};  % quando o Y e maior que a altura, chegou ao fim (solucao encontrada)
solver(Grid, {Y, X}) when X > ?WIDTH ->
    solver(Grid, {Y + 1, 1});  % X maior que a largura, avanca para a proxima linha
solver(Grid, Pos = {Y, X}) ->
    case maps:get(Pos, Grid, 0) of % obtem o valor da posicao, se nao existir retorna 0
        Value when Value =/= 0 ->
            solver(Grid, {Y, X + 1});  % se a celula ja esta preenchida, avanca para a proxima
        0 -> % se a celula esta vazia
            Options = available_numbers(Grid, Pos),  % obtem os numeros disponiveis para a celula
            try_options(Grid, Pos, Options)  % tenta cada opcao disponivel
    end.

% tenta recursivamente cada opcao disponivel para a celula
try_options(_, _, []) ->
    error;  % se nao ha mais opcoes, retorna erro
try_options(Grid, Pos, [N | Ns]) ->
    NewGrid = maps:put(Pos, N, Grid),  % atualiza o grid com o novo numero
    case solver(NewGrid, {element(1, Pos), element(2, Pos) + 1}) of  % avanca para a proxima coluna
        {ok, Result} -> {ok, Result};  % se encontrou solucao, retorna o grid completo
        error -> try_options(Grid, Pos, Ns)  % se nao, tenta a proxima opcao
    end.

% obtem as opcoes de numeros disponiveis para a celula
available_numbers(Grid, Pos) ->
    AdjNums = adjacent_numbers(Grid, Pos),  % numeros dos vizinhos (nao podem ser iguais)
    RegNums = region_numbers(Grid, Pos),    % numeros ja usados na regiao
    ValidNums = valid_numbers(Grid, Pos),   % numeros validos pela regra do jogo
    ForbiddenNums = lists:usort(AdjNums ++ RegNums),  % numeros que nao podem ser usados
    lists:subtract(ValidNums, ForbiddenNums).  % numeros que podem ser usados

% retorna os numeros dos vizinhos da celula
adjacent_numbers(Grid, {Y, X}) ->
    Positions = [{Y - 1, X}, {Y + 1, X}, {Y, X - 1}, {Y, X + 1}],  % posicoes vizinhas
    [Value || Pos <- Positions,
               in_bounds(Pos),
               Value <- [maps:get(Pos, Grid, 0)],
               Value =/= 0].  % pega valores diferentes de 0 dentro do grid

% retorna os numeros ja usados na mesma regiao
region_numbers(Grid, Pos) ->
    RegionNum = maps:get(Pos, region_map()),
    Positions = maps:get(RegionNum, regions()),
    [Value || P <- Positions,
               Value <- [maps:get(P, Grid, 0)],
               Value =/= 0].  % pega valores diferentes de 0 na regiao

% retorna os numeros validos para a celula de acordo com a regra do jogo
valid_numbers(Grid, Pos = {Y, X}) ->
    Lower = get_neighbor_value(Grid, Pos, {Y + 1, X}, 0),  % valor do vizinho de baixo (ou 0)
    Upper = get_neighbor_value(Grid, Pos, {Y - 1, X}, region_size(Pos) + 1),  % valor do vizinho de cima (ou tamanho da regiao + 1)
    From = Lower + 1,  % minimo valor possivel
    To = Upper - 1,    % maximo valor possivel
    if From =< To ->
        lists:seq(From, To);  % lista de numeros validos
       true ->
        []  % se nao houver, retorna lista vazia
    end.

% retorna o valor do vizinho desejado na mesma regiao, se nao tiver retorna valor padrao
get_neighbor_value(Grid, Pos, Neighbor, DefaultValue) ->
    RegionMap = region_map(),
    case in_bounds(Neighbor) andalso maps:get(Pos, RegionMap) =:= maps:get(Neighbor, RegionMap) of
        true ->
            Val = maps:get(Neighbor, Grid, 0),
            if Val =/= 0 -> Val; true -> DefaultValue end;  % se vizinho preenchido, retorna valor, senao, valor padrao
        false ->
            DefaultValue  % se nao estiver na mesma regiao, retorna valor padrao
    end.

% calcula o tamanho da regiao da celula
region_size(Pos) ->
    RegionNum = maps:get(Pos, region_map()),
    length(maps:get(RegionNum, regions())).

% verifica se a posicao esta dentro do grid
in_bounds({Y, X}) ->
    Y >= 1 andalso Y =< ?HEIGHT andalso X >= 1 andalso X =< ?WIDTH.

% exibe o grid
display_grid(Grid) ->
    display_rows(Grid, 1).

display_rows(Grid, Y) when Y =< ?HEIGHT ->
    Row = [show_cell(maps:get({Y, X}, Grid, 0)) || X <- lists:seq(1, ?WIDTH)],
    io:format("~s~n", [string:join(Row, " ")]),
    display_rows(Grid, Y + 1);
display_rows(_, _) ->
    ok.

% converte o valor da celula para string para exibicao
show_cell(0) -> "-";
show_cell(N) -> integer_to_list(N).