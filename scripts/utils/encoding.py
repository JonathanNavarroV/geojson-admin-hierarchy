def fix_encoding(text):
    """
    Corrige errores comunes de codificación cuando los caracteres especiales (como tildes o eñes)
    se ven mal (ej: 'RegiÃ³n' en lugar de 'Región'). Esto suele ocurrir cuando texto originalmente
    en UTF-8 fue mal interpretado como Latin-1.

    Args:
        text (str): Texto posiblemente mal codificado.

    Returns:
        str: Texto corregido si es posible, o el original si no se puede corregir.
    """
    if not isinstance(text, str) or not text:
        return text
    try:
        return text.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text
