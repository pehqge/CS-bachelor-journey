library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity contador is
    generic (N: integer:=10);
port(
	 CONSTANTE, constante_comparador : in std_logic_vector(N-1 downto 0);
    sel_mux, carga : in std_logic;
	 clk: std_logic;
    fim: out std_logic;
	 Saida: out std_logic_vector(N-1 downto 0)
	);

end contador;

architecture cnt of contador is

   ----- componentes
    component MUX2X1 is
        generic (N : integer);
        port (
            sel : in std_logic;
            ent0, ent1 : in std_logic_vector(N - 1 downto 0);
            output : out std_logic_vector(N - 1 downto 0)
        );
    end component;

    component registrador is
	generic (N : integer);
	port (
		clk, carga : in std_logic;
		d : in std_logic_vector(N - 1 downto 0);
		q : out std_logic_vector(N - 1 downto 0));
    end component;

    component somador is
    generic (N : integer);
    port (
        A, B : in std_logic_vector(N - 1 downto 0);
        S : out std_logic_vector(N downto 0));
    end component;

    ----signals
   
    signal S_mux, S_reg, intermediario, ENT_mux, constante_1: std_logic_vector(N-1 downto 0);
	 signal S_somador: std_logic_vector(N downto 0);
    
    
begin


    ---mux
    mux: MUX2X1
	 generic MAP(N => N)
	 port map(sel_mux, ENT_mux, CONSTANTE, S_mux);
   
    ---comparador
	 fim <= '1' when S_mux = constante_comparador else '0';
 

    ---reg
    reg: registrador 
	 generic MAP(N => N)
	 port map(clk, carga, S_mux, S_reg);
        

    constante_1 <= std_logic_vector(to_unsigned(1, N));
    ---somador
    sum: somador 
	 generic MAP(N => N)
	 port map(S_reg, constante_1, S_somador);

   ENT_mux <= S_somador(n-1 downto 0);
   Saida <= S_reg;

end cnt;