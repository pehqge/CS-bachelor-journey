<div style="text-align: center;">
  <h2>Relatório 02 | Grupo 04</h2>
</div>

**Alunos**: Pedro Henrique Gimenez (matrícula: 23102766) e Victória Rodrigues Veloso (matricula: 23100460)

---


# Circuitos e simulações

## 1. SAD V1:



No circuito SAD V1, foram montados os seguintes componentes genéricos: subtrator (com tratamento do valor absoluto embutido), somador, somador com tratamento de overflow, multiplexador e registrador. Esses componentes genéricos foram instanciados no bloco operativo com a quantidade adequada de bits e sinais necessários.

Para a simulação, foi necessário ajustar o valor padrão da duração da execução para 5000 ns, conforme ilustrado na figura 1. Com essa configuração, foram realizados dois ciclos completos de operações de soma, conforme representado na figura 2. Cada ciclo teve uma duração de aproximadamente 2000 ns.
Durante esses ciclos, os valores de entrada foram somados. No primeiro ciclo, ocorreram 64 iterações, em que os 5 primeiros valores de estímulo foram somados. No entanto, é importante observar que esses valores de estímulo foram fornecidos antes do final do primeiro ciclo de 2000 ns. Além disso, o último valor de entrada, representado como 00000000, foi forçado como entrada até o término do ciclo.
No segundo ciclo, ocorreram novamente 64 iterações, mas, desta vez, o valor de entrada foi 11111111, pois foi configurado para ser inserido após 2040 ns, ou seja, após o final do primeiro ciclo. Como resultado desses ciclos, as saídas observadas foram 00000001110101 e 11111111000000.



<div style="text-align: center;">
    <p style="text-align: center; font-style: italic; font-size: 12px;">Figura 2: Configuração Default Run para a SAD V1</p>
    <img src="https://github.com/victoriavllso/sistemas-digitais/blob/e797414d8c289b1c59cb0abcbb18fc74f5bd7caf/imagens/Captura%20de%20tela%202023-10-17%20191622.png" width="80%">
</div>
<br>
<br>
<br>
<div style="text-align: center;">
    <p style="text-align: center; font-style: italic; font-size: 12px;">Figura 1: Simulação da SAD V1</p>
    <img src="https://github.com/victoriavllso/sistemas-digitais/blob/main/imagens/Captura%20de%20tela%202023-10-17%20153211.png" width="80%">
</div>

<br>

Para a construção do circuito da SAD V3, o mesmo esquema foi utilizado. Uma análise interessante para a SAD V3 é o atraso de quase 560 ns no tempo de setup para o registrador SAD (figura 3). Os resultados obtidos foram os mesmos, pois o arquivo estimulos apenas foi adaptado para as entradas necessárias para o formato necessário. É importante observar que ambos os circuitos possuem suporte para overflow, ou seja, no segundo ciclo com as somas consecutivas da representação máxima, não ocorreu overflow.

<br>





<div style="text-align: center;">
    <p style="text-align: center; font-style: italic; font-size: 12px;">Figura 3: Atraso SAD V3</p>
    <img src="" width="80%">
</div>
<br>
<br>
<br>
<div style="text-align: center;">
    <p style="text-align: center; font-style: italic; font-size: 12px;">Figura 4: Resultado SAD V3</p>
    <img src="" width="80%">
</div>