# Symbol table for managing reserved words and identifiers
from typing import Dict, Tuple, Optional

class SymbolTable:
    """Manages reserved words and identifiers for lexical analysis."""
    
    def __init__(self):
        self.reserved_words: set[str] = set()
        self.identifiers: Dict[str, int] = {}  # lexeme -> line number
        self._next_id_line = 1
    
    def add_reserved(self, word: str) -> None:
        """Add a reserved word to the table."""
        if word:
            self.reserved_words.add(word)
    
    def remove_reserved(self, word: str) -> None:
        """Remove a reserved word from the table."""
        self.reserved_words.discard(word)
    
    def is_reserved(self, lexeme: str) -> bool:
        """Check if a lexeme is a reserved word."""
        return lexeme in self.reserved_words
    
    def get_token(self, lexeme: str) -> Tuple[str, str]:
        """
        Get token representation for a lexeme.
        
        Returns:
            Tuple of (lexeme, type/position):
            - If reserved: (lexeme, 'PR')
            - If identifier: (lexeme, line_number as string)
        """
        if self.is_reserved(lexeme):
            return (lexeme, 'PR')
        
        # Add to identifiers if not present
        if lexeme not in self.identifiers:
            self.identifiers[lexeme] = self._next_id_line
            self._next_id_line += 1
        
        return (lexeme, str(self.identifiers[lexeme]))
    
    def get_reserved_words(self) -> list[str]:
        """Get list of reserved words."""
        return sorted(list(self.reserved_words))
    
    def clear(self) -> None:
        """Clear all entries."""
        self.reserved_words.clear()
        self.identifiers.clear()
        self._next_id_line = 1

