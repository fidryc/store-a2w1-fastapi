"""Пока вместо этого класса используется встроенная фукнция jinja из-за ошибки передачи экземпляра"""

from typing import Protocol

class ISeparationTextHelper(Protocol):   
    def separate_text(self, *args, **kwargs) -> list[str]:
        """Метод для получения разделенного текста"""
    
class SeparationTextBySymbol(ISeparationTextHelper):
    def __init__(self, symbol: str):
        self.symbol = symbol
        
    def separate_text(self, text: str):
        return text.split(self.symbol)
    

class SeparationByEqualLenghtsSententces(ISeparationTextHelper):
    pass