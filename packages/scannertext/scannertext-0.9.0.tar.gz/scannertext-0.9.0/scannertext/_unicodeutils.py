class UnicodeUtils:
    """Define constantes enteras útiles para trabajo con Unicode."""

    MIN_SUPPLEMENTARY_CODE_POINT = 0x010000
    MIN_HIGH_SURROGATE = 0xD800
    MAX_HIGH_SURROGATE = 0xDBFF
    MIN_LOW_SURROGATE = 0xDC00
    MAX_LOW_SURROGATE = 0xDFFF


def is_high_surrogate(ch: str) -> bool:
    """Devuelve True si el carácter se considera una unidad
    de código Unicode sustituta superior."""
    return UnicodeUtils.MIN_HIGH_SURROGATE <= ord(ch[0]) <= UnicodeUtils.MAX_HIGH_SURROGATE


def is_low_surrogate(ch: str) -> bool:
    """Devuelve True si el carácter se considera una unidad
    de código Unicode sustituta inferior."""
    return UnicodeUtils.MIN_LOW_SURROGATE <= ord(ch[0]) <= UnicodeUtils.MAX_LOW_SURROGATE


def to_code_point(high: str, low: str) -> int:
    """Convierte el par sustituto especificado en su valor de
    punto de código Unicode suplementario.

    Parameters:
        high (str): Unidad de código sustituto superior.
        low (str): Unidad de código sustituto inferior.

    Returns:
        int: El punto de código suplementario compuesto por el par
        sustituto especificado.
    """
    return ((ord(high) << 10) + ord(low)) + (
        UnicodeUtils.MIN_SUPPLEMENTARY_CODE_POINT
        - (UnicodeUtils.MIN_HIGH_SURROGATE << 10)
        - UnicodeUtils.MIN_LOW_SURROGATE
    )


if __name__ == "__main__":
    print(is_high_surrogate('\ud83c'), is_low_surrogate('\udf15'))
    cp = to_code_point('\ud83c', '\udf15')
    ch = chr(cp)
    print(cp, f"'\\U{cp:08x}'", ch, len(ch))
    print("\U0001f315")
    print(format(ord(ch) & 0xFFFF, "04x"))
    print(format((ord(ch) & 0xFFFF0000) >> 16, "04x"))
