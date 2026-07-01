library ieee;
use ieee.std_logic_1164.all;

entity controle is
    port(
        clk, rst, iniciar, proxLinha, fim_linha, fim_coluna, fim_i: in std_logic;
        pronto, write_mem_saida, read_kernel, read_mem, c_i, c_linha, c_coluna, c_soma, cDesCol, cDesLinha, c_end_mem, c_end_mem_saida, SelDesCol, SelDeslinha, sel_mux_coluna, sel_mux_linha, sel_mux_i, sel_mux_soma, sel_mux_mem_saida: out std_logic
    );
end controle;

architecture arch of controle is
    type tipo_estado is(S0, S1, S2, S2A, S3, S4 ,S5, S5A, S6, S7, S8);
    signal estadoatual: tipo_estado;

begin
    process(rst, clk)
    begin
        if rst = '1' then
            estadoatual <= S0;
        elsif(rising_edge(clk)) then
            case estadoatual is
                when S0 =>
                    if iniciar = '1' then
                        estadoatual <= S1;
                    else
                        estadoatual <= S0;
                    end if;
                when S1 =>
                    estadoatual <= S2;
                when S2 =>
                    estadoatual <= S2A;
                when S2A =>
                    estadoatual <= S3;
                when S3 =>
                    estadoatual <= S4;
                when S4 =>
                    estadoatual <= S5;
                when S5 =>
                    if fim_i = '1' then
                        estadoatual <= S5A;
                    else
                        if fim_i = '0' and proxLinha = '0' then
                            estadoatual <= S2A;
                        else
                            estadoatual <= S8;
                        end if;
                    end if;
                when S5A =>
                    estadoatual <= S6;
                when S6 =>
                    if fim_coluna = '1' then
                        estadoatual <= S7;
                    else
                        estadoatual <= S2;
                    end if;
                when S7 =>
                    if fim_linha = '1' then
                        estadoatual <= S0;
                    else
                        estadoatual <= S1;
                    end if;
                when S8 =>
                        estadoatual <= S2A;
            end case;
        end if;
    end process;
                
c_i <= '1' when (estadoatual = S2 or estadoatual = S5) else '0';
c_linha <= '1' when (estadoatual = S0 or estadoatual = S7) else '0';
c_coluna <= '1' when (estadoatual = S1 or estadoatual = S0 or estadoatual = S6) else '0';
c_soma <= '1' when (estadoatual = S0 or estadoatual = S4 or estadoatual = S6) else '0';
cDesCol <= '1' when (estadoatual = S0 or estadoatual = S2 or estadoatual = S5 or estadoatual = S8) else '0';
cDesLinha <= '1' when (estadoatual = S0 or estadoatual = S2 or estadoatual = S8) else '0';
c_end_mem <= '1' when estadoatual = S2A else '0';
c_end_mem_saida <= '1' when (estadoatual = S5A or estadoatual = S0) else '0';
SelDesCol <= '1' when estadoatual = S5 else '0';
SelDesLinha <= '1' when estadoatual = S8 else '0';
sel_mux_coluna <= '1' when (estadoatual = S0 or estadoatual = S1) else '0';
sel_mux_linha <= '1' when estadoatual = S0 else '0';
sel_mux_i <= '1' when estadoatual = S2 else '0';
sel_mux_soma <= '1' when (estadoatual = S0 or estadoatual = S6) else '0';
sel_mux_mem_saida <= '1' when estadoatual = S0 else '0';
write_mem_saida <= '1' when estadoatual = S6 else '0';
read_kernel <= '1' when estadoatual = S3 else '0';
read_mem <= '1' when estadoatual = S3 else '0';
pronto <= '1' when estadoatual = S0 else '0';

end arch;

