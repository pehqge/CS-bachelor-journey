library IEEE;
use IEEE.Std_Logic_1164.all;
use IEEE.Std_Logic_unsigned.all;

entity mult3_display is
    port (
        X: in std_logic_vector(3 downto 0);
        hex0, hex1, hex3, hex4: out std_logic_vector(6 downto 0)
    );
end mult3_display;

architecture struct of mult3_display is
    signal Y: std_logic_vector(4 downto 0);
    signal concatX, concatY: std_logic_vector(6 downto 0);

    component mult3 is
        port (
            X: in std_logic_vector(3 downto 0);
            Y: out std_logic_vector(4 downto 0)
        );
    end component;

    component bin7seg99 is
        port (
            binaryin: in std_logic_vector(6 downto 0);
            hex1, hex0: out std_logic_vector(6 downto 0)
        );
    end component;

begin
    mult3_inst: mult3 port map (
        X => X,
        Y => Y
    );

    concatX <= "00" & X;
    concatY <= "00" & Y;

    bin7seg99_X: bin7seg99 port map (
        binaryin => concatX,
        hex1 => hex4,
        hex0 => hex3
    );

    bin7seg99_Y: bin7seg99 port map (
        binaryin => concatY,
        hex1 => hex1,
        hex0 => hex0
    );

end struct;
