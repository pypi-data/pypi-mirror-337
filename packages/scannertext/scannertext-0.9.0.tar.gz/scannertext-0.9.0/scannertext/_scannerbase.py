class ScannerBase:
    """Representa la clase base de un scanner de texto."""
    MAX_USER_INDEX = 4096
    """Mayor índice que puede dar el usuario a sus palabras reservadas y
	operadores."""
    STRING = MAX_USER_INDEX + 1
    """Indica que el tipo de token es una cadena."""
    COMMENT = MAX_USER_INDEX + 2
    """Indica que el tipo de token es un comentario."""
    UNKNOWN = MAX_USER_INDEX + 3
    """Indica que el tipo de token es un carácter no reconocido."""
    SPACE = MAX_USER_INDEX + 4
    """Indica que el tipo de token es un espacio."""
    EOF = MAX_USER_INDEX + 5
    """Indica que el tipo de token es el final de fichero."""
    EOL = MAX_USER_INDEX + 6
    """Indica que el tipo de token es un final de línea."""
    IDENT = MAX_USER_INDEX + 7
    """Indica que el tipo de token es un identificador."""
    NUMBER = MAX_USER_INDEX + 8
    """Indica que el tipo de token es un número."""
    OPERATOR = MAX_USER_INDEX + 9
    """Indica que el tipo de token es un operador."""
    KEYWORD = MAX_USER_INDEX + 10
    """Indica que el tipo de token es una palabra clave."""
    CHAR = MAX_USER_INDEX + 11
    """Indica que el tipo de token es un carácter."""

    _COMMENT_EOL = 0
    """Indica comentario final de línea."""
    _COMMENT_MULTILINE = 1
    """Indica comentario multilínea."""

    _MAX_INTEGER = 2_147_483_647
    """Entero positivo más grande de 32 bits con signo"""
    _MAX_LONG = 9_223_372_036_854_775_807
    """Entero positivo largo más grande de 64 bits con signo"""
    MAX_EXPO = _MAX_INTEGER
    """Valor absoluto del exponente más grande en un número real."""
    MAX_EXPO_NORM = 309
    """Máximo exponente de un número normalizado positivo o negativo antes
    de desbordamiento."""
    MIN_EXPO_NORM = -323
    """Mínimo exponente de un número normalizado positivo o negativo
    antes de cero."""
    MAX_MANTISA = _MAX_LONG
    """Mantisa más grande que puede tener un número"""

    # Enumeración de los tipos de rango más pequeño donde cabe el último número
    NUM_RANGE_INT = 0
    """El número cabe en un entero con signo de 32 bits."""
    NUM_RANGE_LONG = 1
    """número cabe en un entero largo con signo de 64 bits."""
    NUM_RANGE_DOUBLE = 2
    """El número es de doble precisión de 64 bits."""
    NUM_RANGE_OVERFLOW = 3
    """El número es demasiado grande y provoca desbordamiento."""
