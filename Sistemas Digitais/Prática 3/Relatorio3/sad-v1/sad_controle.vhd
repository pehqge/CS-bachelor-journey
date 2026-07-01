library ieee;
use ieee.std_logic_1164.all;

entity sad_controle is
    port (
        iniciar, rst, clk, menor : in std_logic;
        pronto, read, zi, ci, cpa, cpb, zsoma, csoma, csad_reg : out std_logic
    );
end sad_controle;

architecture bloco of sad_controle is
    type Tipo_estado is (S0, S1, S2, S3, S4, S5);
    signal EstadoAtual : Tipo_estado;
    
begin
    process (rst, clk)
    begin
        if rst = '1' then
            EstadoAtual <= S0;
        elsif (rising_edge(clk)) then
            case EstadoAtual is
                when S0 =>
                    if iniciar = '0' then
                        EstadoAtual <= S0;
                    else
                        EstadoAtual <= S1;
                    end if;
                when S1 =>
                    EstadoAtual <= S2;
                when S2 =>
                    if menor = '1' then
                        EstadoAtual <= S3;
                    else
                        EstadoAtual <= S5;
                    end if;
                when S3 =>
                    EstadoAtual <= S4;
                when S4 =>
                    EstadoAtual <= S2;
                when S5 =>
                    EstadoAtual <= S0;
            end case;
        end if;
    end process;

    pronto <= '1' when EstadoAtual = S0 else '0';
    read <= '1' when EstadoAtual = S3 else '0';
    zi <= '1' when EstadoAtual = S1 else '0';
    ci <= '1' when EstadoAtual = S1 or EstadoAtual = S4 else '0';
    cpa <= '1' when EstadoAtual = S3 else '0';
    cpb <= '1' when EstadoAtual = S3 else '0';
    zsoma <= '1' when EstadoAtual = S1 else '0';
    csoma <= '1' when EstadoAtual = S1 or EstadoAtual = S4 else '0';
    csad_reg <= '1' when EstadoAtual = S5 else '0';

end bloco;