library IEEE;
use IEEE.Std_Logic_1164.all;
use IEEE.Std_Logic_unsigned.all;

entity somador_display is
    port (
        A: in std_logic_vector(3 downto 0);
        B: in std_logic_vector(3 downto 0);
        hex0, hex1, hex2, hex3, hex4, hex5: out std_logic_vector(6 downto 0)
    );
end somador_display;

architecture struct of somador_display is
    signal S: std_logic_vector(4 downto 0);
    signal concatA, concatB, concatS: std_logic_vector(6 downto 0);

    component somador is
        port (
            A, B: in std_logic_vector(3 downto 0);
            S: out std_logic_vector(4 downto 0)
        );
    end component;

    component bin7seg99 is
        port (
            binaryin: in std_logic_vector(6 downto 0);
            hex1, hex0: out std_logic_vector(6 downto 0)
        );
    end component;

begin
    somador_inst: somador port map (
        A => A,
        B => B,
        S => S
    );

    concatA <= "000" & A;
    concatB <= "000" & B;
    concatS <= "00" & S;

    bin7seg99_A: bin7seg99 port map (
        binaryin => concatA,
        hex1 => hex5,
        hex0 => hex4
    );

    bin7seg99_B: bin7seg99 port map (
        binaryin => concatB,
        hex1 => hex3,
        hex0 => hex2
    );

    bin7seg99_S: bin7seg99 port map (
        binaryin => concatS,
        hex1 => hex1,
        hex0 => hex0
    );

end struct;
