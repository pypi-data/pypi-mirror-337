from dataclasses import dataclass

@dataclass
class StackEntry:
    """Representa una entrada en la pila de estados."""    
    pos: int
    token_pos: int
    processed_string: list[str]
    processed_char: str
    token_previous: int
    token: int
    token_class: int
    lin: int
    col: int
    last_col: int
    num: float
    num_overflow: bool
    mant: int
    num_range: int