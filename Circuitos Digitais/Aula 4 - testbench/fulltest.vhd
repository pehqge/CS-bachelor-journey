library ieee;
use ieee.std_logic_1164.all;
entity fulltest is
end fulltest;
architecture tb of fulltest is
    signal A, B, Cin, S, Cout : std_logic;
    component fulladder is
        port (A: in std_logic;
              B: in std_logic;
              Cin: in std_logic;
              S: out std_logic;
              Cout: out std_logic
              );
    end component;
    
begin
    DUT : fulladder port map (A => A, 
                              B => B, 
                              Cin => Cin,
                              S => S,
                              Cout => Cout);
 process
  constant period: time := 10 ns;
  begin
    A <= '0'; B <= '0'; Cin <= '0'; 
    wait for period;
    assert ((S = '0') and (Cout = '0'))
    report "Failed for 000." severity error;
    
    A <= '0'; B <= '0'; Cin <= '1'; 
    wait for period;
    assert ((S = '1') and (Cout = '0'))
    report "Failed for 001." severity error;
    
    A <= '0'; B <= '1'; Cin <= '0'; 
    wait for period;
    assert ((S = '1') and (Cout = '0'))
    report "Failed for 010." severity error;
    
    A <= '0'; B <= '1'; Cin <= '1'; 
    wait for period;
    assert ((S = '0') and (Cout = '1'))
    report "Failed for 011." severity error;
    
    A <= '1'; B <= '0'; Cin <= '0'; 
    wait for period;
    assert ((S = '1') and (Cout = '0'))
    report "Failed for 100." severity error;
    
    A <= '1'; B <= '0'; Cin <= '1'; 
    wait for period;
    assert ((S = '0') and (Cout = '1'))
    report "Failed for 101." severity error;
    
    A <= '1'; B <= '1'; Cin <= '0'; 
    wait for period;
    assert ((S = '0') and (Cout = '1'))
    report "Failed for 110." severity error;
    
    A <= '1'; B <= '1'; Cin <= '1'; 
    wait for period;
    assert ((S = '1') and (Cout = '1'))
    report "Failed for 111." severity error;
    
    wait;
 end process;
end tb;