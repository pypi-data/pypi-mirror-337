import os
from pathlib import Path
import codecs
import math
from scannertext import ScannerBase
from scannertext import _unicodeutils
from scannertext import StackEntry

class Scanner(ScannerBase):
    """
    Implementación de una clase cuya función principal es la de
    servir de analizador léxico o escáner.
    Las clases de componentes léxicos que puede reconocer son:

        Blancos (espacio, tabulador horizontal y vertical, avance de forma).
        Comentarios.
        Palabras Clave.
        Identificadores.
        Constantes numéricas.
        Constantes de carácter.
        Constantes de cadena.
        Operadores.
        Final de línea (retorno de carro y/o nueva de línea).
        Continuador de línea.
        Fin de archivo.
        Carácter desconocido.

    En caso de ambigüedad la prioridad se establece
    por el orden dado anteriormente de arriba hacia abajo.
    """    

    @property
    def size(self):
        """Devuelve el tamaño actual de la pila del analizador."""
        return len(self._stack)


    def __init__(
        self,
        text: str = None,
        filename: str = None,
        ignore_case: bool = False,
        encoding: str = None,
    ):
        """Inicia un Scanner a partir de una cadena dada o bien
         una cadena leída desde un fichero.
        Parameters:
            text (str): Texto que será analizado.

            filename (str): Ruta del fichero desde donde se leerá el texto. Nota: Si se pasa 'text', filename será ignorado.

            ignore_case (bool): Si es verdadero las palabras clave no distinguirán
            mayúsculas de minúsculas.

            encoding (str): Codificación del fichero, preferiblemente UTF-8.
        """
        if text is None and filename is None:
            raise TypeError(f"'text' o 'filename' son requeridos")

        # Atributos de implementación interna
        self._digits: int = 0
        """Número actual de dígitos de la mantisa decimal"""
        self._stack: list[StackEntry] = []
        """Pila del analizador"""
        self._ignore_case: bool = ignore_case
        self._keywords: dict[str, int] = {}
        """Palabras reservadas asociadas a tu token."""
        self._operators: dict[str, int] = {}
        """Operadores asociados a su token."""
        self._buffer_ubound: int = 0
        """Límite superior del buffer."""
        self._token_pos = 0
        """Índice de comienzo del último token leído."""
        self._text_in: str = None
        """Referencia al texto de entrada."""
        self._pos: int = 0
        """Índice a la posición en el buffer de lectura."""
        self._processed_string: list[str] = []
        """Cuando se lee una cadena contiene los caracteres normales y los
        caracteres a los que equivalen las secuencias de escape."""
        self._double_operator_string: str = ""
        """En el modo CSV se reemplaz por un carácter de cadena."""
        self._last_operator: str = ""
        """Último operador leído."""
        self._is_integer: bool = False
        """Indica si el último número leido es entero."""
        self._exp1: int = 0
        """El exponente final de la mantisa para decimal y binario."""
        self._exp2: int = 0
        """El exponente explícito para números reales."""
        self._max_len_operator = 0
        """Longitud del operador más grande cargado en el Scanner."""

        # Atributos externos
        self.ignore_eol: bool = True
        """Devuelve o establece si se ignoran los token final de línea."""
        self.ignore_comments: bool = True
        """Devuelve o establece si se ignoran los comentarios."""
        self.ignore_spaces: bool = True
        """Devuelve o establece si se ignoran los espacios en blanco distintos de
        final de línea."""
        self.csv_mode: bool = False
        """Devuelve o establece si se trabaja en el modo CSV.
        Con el modo CSV activado, si en una cadena aparece:
	    "hola ""mundo"" nuevo", "" se trasforma a un solo "
	    y la cadena resultante a [hola "mundo" nuevo]."""
        self._processed_char = "\0"
        """Devuelve un único carácter si se ha leido un carácter."""
        self._operator_comment_eol: str = ""
        """Devuelve o establece el operador de comentario final de línea."""
        self._operator_comment_mls: str = ""
        """Devuelve o establece el operador de comentario nultilínea inicial."""
        self._operator_comment_mle: str = ""
        """Devuelve o establece el operador de comentario nultilínea final."""
        self._operator_string: str = ""
        """Devuelve o establece el operador de cadena literal."""
        self._operator_char: str = ""
        """Devuelve o establece el operador de caracteres."""
        self._token_class: int = 0
        """Devuelve la clase del último componente léxico leido."""
        self._token: int = 0
        """Devuelve el código del último token calculado."""
        self._token_previous: int = 0
        """Dvuelve el código del penúltimo token calculado."""
        self._lin: int = 1
        """Devuelve la línea actual en examen."""
        self._col: int = 1
        """Devuelve la columna actual en examen."""
        self._last_col: int = self._col
        """Devuelve la última columna de la línea anteriormente leida."""
        self.use_point: bool = True
        """Devuelve o establece si se usa el punto decimal (.) o la
         coma (,) como separador decimal."""
        self._num_range: int = Scanner.NUM_RANGE_OVERFLOW
        """Devuelve el tipo de rango asociado al último número leido."""
        self._num: float = 0.0
        """Devuelve el último número leido en formato "float"."""
        self._mant: int = 0
        """Devuelve la última mantisa leida. También se puede
        considerar como el último entero positivo leido si se
        ha leido un número entero."""
        self._num_overflow: bool = False
        """Devuelve un valor que indica si al leer un número se ha
         producido desbordamiento."""

        # Inicializa el Scanner
        self._new_buffer(text, filename, encoding)
        self.reset_var_analysis()

    @staticmethod
    def _bom_utf8(filename: str, encoding: str) -> bool:
        """Comprueba si el fichero tiene un BOM UTF-8, si
        lo tiene devuelve "utf-8-sig", si no devuelve el
        mismo valor de "encoding"."""
        bytes = min(3, os.path.getsize(filename))
        raw = open(filename, "rb").read(bytes)
        if raw.startswith(codecs.BOM_UTF8):
            return "utf-8-sig"
        else:
            return encoding

    @staticmethod
    def is_ident(s: str) -> bool:
        """Devuelve True si la cadena "s" es un identificador."""
        if s is None or s == "":
            return False
        if not (s[0].isalpha() or s[0] == "_"):
            return False
        # Todos los caracteres deben ser letras, dígitos o _
        for c in s:
            if not (c.isalnum() or c == "_"):
                return False
        return True

    @staticmethod
    def _is_operator(opr: str) -> bool:
        if not opr:
            return False
        for i in range(len(opr)):
            if opr[i].isalnum() or opr[i].isspace() or (0x00 <= ord(opr[i]) <= 0x1F):
                return False
        return True

    @classmethod
    def _read_file(cls, filename: str, encoding: str):
        encoding = cls._bom_utf8(filename, encoding)
        return Path(filename).read_text(encoding=encoding)

    def _new_buffer(self, text: str, filename: str, encoding: str):
        if filename:
            self._text_in = self._read_file(filename, encoding)
        else:
            self._text_in = text

    def add_operator(self, opr: str, token: int):
        """Agrega un nuevo operador al scanner.

        opr (str): Cadena que contiene los caracteres del operador.

        token (int): Token que representará al operador.
        """
        if token > Scanner.MAX_USER_INDEX:
            raise IndexError(
                "El valor de índice del token "
                f"no debe ser mayor a {Scanner.MAX_USER_INDEX}"
            )
        if not self._is_operator(opr):
            raise ValueError("El operador no es válido.")
        elif opr in self._operators:
            raise KeyError("El operador ya existe.")
        else:
            self._add_operator(opr, token)

    def add_keyword(self, kw: str, token: int):
        """Agrega una nueva palabra clave al scanner.

        kw (str): Cadena que contiene los caracteres de la plabra clave.

        token (int): Token que representará a la palabra clave.
        """
        if token > Scanner.MAX_USER_INDEX:
            raise IndexError(
                "El valor de índice del token "
                f"no debe ser mayor a {Scanner.MAX_USER_INDEX}"
            )
        if not self.is_ident(kw):
            raise ValueError("El identificador no es válido.")
        elif kw in self._keywords:
            raise KeyError("El identificador ya existe.")
        else:
            self._keywords[kw] = token

    @property
    def stack(self):
        """Devuelve la pila del analizador."""
        return self._stack

    @property
    def operator_char(self) -> str:
        """Devuelve el operador de caracteres."""
        return self._operator_char

    @operator_char.setter
    def operator_char(self, value: str):
        """Establece el operador de caracteres."""
        if not value:
            self._operator_char = ""
        elif not self._is_operator(value):
            raise ValueError("El operador no es válido.")
        elif value in self._operators:
            raise KeyError("El operador ya existe.")
        else:
            self._operator_char = value
            self._add_operator(self._operator_char, Scanner.CHAR)

    @property
    def operator_comment_eol(self) -> str:
        """Devuelve el operador de comentario final de línea."""
        return self._operator_comment_eol

    @operator_comment_eol.setter
    def operator_comment_eol(self, value: str):
        """Establece el operador de comentario final de línea."""
        if not value:
            self._operator_comment_eol = ""
        elif not self._is_operator(value):
            raise ValueError("El operador no es válido.")
        elif value in self._operators:
            raise KeyError("El operador ya existe.")
        else:
            self._operator_comment_eol = value
            self._add_operator(self._operator_comment_eol, Scanner.COMMENT)

    @property
    def operator_comment_mls(self) -> str:
        """Devuelve el operador de comentario multilínea inicial."""
        return self._operator_comment_mls

    @operator_comment_mls.setter
    def operator_comment_mls(self, value: str):
        """Establece el operador de comentario multilínea inicial."""
        if not value:
            self._operator_comment_mls = ""
            self._operator_comment_mle = ""
        elif not self._is_operator(value):
            raise ValueError("El operador no es válido.")
        elif value in self._operators:
            raise KeyError("El operador ya existe.")
        else:
            self._operator_comment_mls = value
            self._add_operator(self._operator_comment_mls, Scanner.COMMENT)

    @property
    def operator_comment_mle(self) -> str:
        """Devuelve el operador de comentario multilínea final."""
        return self._operator_comment_mle

    @operator_comment_mle.setter
    def operator_comment_mle(self, value: str):
        """Establece el operador de comentario multilínea final."""
        if not value:
            self._operator_comment_mls = ""
            self._operator_comment_mle = ""
        elif not self._is_operator(value):
            raise ValueError("El operador no es válido.")
        elif value in self._operators:
            raise KeyError("El operador ya existe.")
        else:
            self._operator_comment_mle = value
            self._add_operator(self._operator_comment_mle, Scanner.COMMENT)

    @property
    def operator_string(self) -> str:
        """Devuelve el operador de cadenas."""
        return self._operator_string

    @operator_string.setter
    def operator_string(self, value: str):
        """Establece el operador de comentario multilínea final."""
        if not value:
            self._operator_string = ""
            self._double_operator_string = ""
        elif not self._is_operator(value):
            raise ValueError("El operador no es válido.")
        elif value in self._operators:
            raise KeyError("El operador ya existe.")
        else:
            self._operator_string = value
            self._double_operator_string = self._operator_string * 2
            self._add_operator(self._operator_string, Scanner.STRING)

    @property
    def _current(self) -> str:
        """Devuelve el carácter actual."""
        return self._text_in[self._pos]

    @property
    def _current_and_next(self) -> str:
        """Devuelve el carácter actual y avanza el puntero del búffer."""
        c = self._current
        self._pos += 1
        return c

    def _read_operator(self, advance_reader):
        """Devuelve True si se puede leer un operador de la entrada.
        Si hay éxito _last_operator es el operador en el diccionario
        de operadores. Se puede elegir entre avanzar la lectura
        o continuar en la posición de entrada."""
        if self._pos > self._buffer_ubound:
            self._last_operator = ""
            return False
        # Leemos la cadena con longitud menor o igual que el operador más largo
        max_len = (
            (len(self._text_in) - self._pos)
            if (self._pos + self._max_len_operator) > len(self._text_in)
            else self._max_len_operator
        )
        self._last_operator = self._text_in[self._pos : self._pos + max_len]

        while self._operators.get(self._last_operator) is None and self._last_operator:
            self._last_operator = self._last_operator[0:-1]

        if advance_reader and self._last_operator:
            self._token_pos = self._pos
            self._pos += len(self._last_operator)
            self._col += len(self._last_operator)

        return len(self._last_operator) > 0

    def _match_string(self, s):
        """Devuelve true si se puede hacer coincidir carácter
        a carácter la cadena pasada con el contenido
        siguiente del buffer de lectura, pero no
        avanza el puntero del buffer."""
        if not s:
            return False
        i = self._pos
        j = 0
        while i <= self._buffer_ubound and j < len(s):
            if self._text_in[i] != s[j]:
                break
            i += 1
            j += 1

        return j == len(s)

    def _add_operator(self, opr, token):
        if len(opr) > self._max_len_operator:
            self._max_len_operator = len(opr)
        self._operators[opr] = token

    @property
    def token(self):
        """Devuelve el código del último token calculado."""
        return self._token

    @property
    def token_class(self):
        """Devuelve la clase del último componente léxico leido."""
        return self._token_class

    @property
    def token_previous(self):
        """Dvuelve el código del penúltimo token calculado."""
        return self._token_previous

    @property
    def pos(self):
        """Devuelve la posición actual del índice del buffer."""
        return self._pos

    @property
    def token_pos(self):
        """Devuelve la posición de comienzo del último token leído."""
        return self._token_pos

    @property
    def lin(self):
        """Devuelve la línea actual en examen."""
        return self._lin

    @property
    def col(self):
        """Devuelve la columna actual en examen."""
        return self._col

    @property
    def last_col(self):
        """Devuelve la última columna de la línea anteriormente leida."""
        return self._last_col

    @property
    def length(self):
        """Devuelve la longitud de la entrada."""
        return len(self._text_in)

    @property
    def lexeme(self):
        """Devuelve el último lexema leido en estado bruto."""
        return self._text_in[self._token_pos : self._pos]

    @property
    def text_in(self):
        """Devuelve el texto de entrada."""
        return self._text_in

    @text_in.setter
    def text_in(self, text: str):
        """Establecee el texto de entrada."""
        self._new_buffer(text, False, None)
        self.reset_var_analysis()

    @property
    def token_length(self) -> int:
        """Devuelve la longitud del último token leído."""
        return self._pos - self._token_pos

    @property
    def processed_string(self):
        """Devuelve el último string leido y procesado, es decir, se
        sustituyen las secuencias de escape, por los caracteres a los
        que equivalen."""
        return "".join(self._processed_string)

    @property
    def processed_char(self):
        """Devuelve el último carácter leído y procesado, es decir, se
        sustituye cualquier secuencia de escape, por el el caracter al
        que representa."""
        return self._processed_char

    @property
    def num_range(self):
        """Devuelve el tipo de  rango asociado al último número leido."""
        return self._num_range

    @property
    def num(self):
        """Devuelve el último número leido en formato "float"."""
        return self._num

    @property
    def mant(self):
        """Devuelve la última mantisa leida. También se puede
        considerar como el último entero positivo leido si se
        ha leido un número entero."""
        return self._mant

    @property
    def num_overflow(self):
        """Devuelve un valor que indica si al leer un número se ha
        producido desbordamiento."""
        return self._num_overflow

    def reset_var_analysis(self):
        """Reinicia las variables de análisis."""        
        self._stack.clear()
        self._token_pos = 0
        self._pos = 0
        self._lin = 1
        self._col = 1
        self._last_col = self._col
        self._token = ScannerBase.EOF
        self._token_previous = ScannerBase.EOF
        self._token_class = ScannerBase.EOF
        self._processed_char = "\0"
        self._buffer_ubound = len(self._text_in) - 1

    def load_file(self, filename: str, encoding: str = None):
        """Carga el buffer de análisis con un fichero de disco.
        Este método crea un nuevo buffer e inicializa las variables de
        análisis. La configuración de esta instancia no se ve afectada.

        Parameters:
            filename (str): Ruta del fichero que será escaneado.
            encoding (str): Codificación de caracteres usada.
        """
        self._new_buffer(text_or_path=filename, is_file=True, encoding=encoding)
        self.reset_var_analysis()

    @staticmethod
    def _is_line_separator(c):
        return c in ("\n", "\r")

    @staticmethod
    def _is_white_space(c):
        """Devuelve un valor True que indica si un carácter se considera
        un espacio en blanco."""
        return c in ("\t", "\n", "\u000b", "\f", "\r", " ")

    def _is_eol(self):
        if self._pos > self._buffer_ubound:
            return False
        elif Scanner._is_line_separator(self._current):
            return True
        else:
            return False

    def _advance_line(self):
        """Avanza a la siguiente línea. Supone que el carácter actual
        es un separador de líneas."""
        self._last_col = self._col  # Última columna de esta línea
        if self._current == "\r":
            self._pos += 1
            if self._pos <= self._buffer_ubound:
                if self._current == "\n":
                    self._pos += 1
        else:  # \n
            self._pos += 1
        self._lin += 1
        self._col = 1

    def _is_blank(self, pos):
        """Devuelve True si el carácter apuntado por pos es un blanco:
        espacio, tabulador horizontal, tabulador vertical, o avance de forma."""
        if pos < 0 or pos > self._buffer_ubound:
            return False
        return Scanner._is_white_space(
            self._text_in[pos]
        ) and not Scanner._is_line_separator(self._text_in[pos])

    def _in_operator(self, opr):
        if self._pos > self._buffer_ubound:
            return False
        if not opr:
            return False
        if not self._read_operator(False):
            return False
        if opr != self._last_operator:
            return False
        return True

    def _advance_entry(self):
        """Avanza el puntero de lectura hasta el siguiente token no ignorable."""
        in_comment = False
        comment_class = -1

        while self._pos <= self._buffer_ubound:
            if in_comment:
                if comment_class == Scanner._COMMENT_EOL:
                    if self._is_eol():
                        in_comment = False
                        if self.ignore_eol:
                            self._advance_line()
                        else:
                            break
                    else:
                        self._pos += 1
                        self._col += 1
                else:  # COMMENT_MULTILINE
                    if self._is_eol():
                        self._advance_line()
                    elif self._match_string(self._operator_comment_mle):
                        self._pos += len(self._operator_comment_mle)
                        self._col += len(self._operator_comment_mle)
                        in_comment = False
                    else:
                        self._pos += 1
                        self._col += 1
            else:  # Fuera de comentarios
                if self.ignore_spaces and self._is_blank(self._pos):
                    self._pos += 1
                    self._col += 1
                elif self.ignore_eol and self._is_eol():
                    self._advance_line()
                elif self.ignore_comments and self._in_operator(
                    self._operator_comment_eol
                ):
                    # COMMENT_EOL
                    self._pos += len(self._operator_comment_eol)
                    self._col += len(self._operator_comment_eol)
                    in_comment = True
                    comment_class = Scanner._COMMENT_EOL
                elif self.ignore_comments and self._in_operator(
                    self._operator_comment_mls
                ):
                    # COMMENT_MULTILINE
                    self._pos += len(self._operator_comment_mls)
                    self._col += len(self._operator_comment_mls)
                    in_comment = True
                    comment_class = Scanner._COMMENT_MULTILINE
                else:  # El token debe tratarse
                    break

    def _read_blanks(self):
        """Devuelve True si puede leer una cadena de blancos."""
        self._token_pos = self._pos
        while self._is_blank(self._pos):
            self._pos += 1
        if self._pos > self._token_pos:  # Se leyeron blancos
            self._col += self.token_length
            return True
        return False

    def _read_identifier(self):
        if self._pos > self._buffer_ubound:
            return False
        if not (self._current.isalpha() or self._current == "_"):
            return False
        # El token comienza
        self._token_pos = self._pos
        self._pos += 1
        while self._pos <= self._buffer_ubound:
            if self._current.isalnum() or self._current == "_":
                self._pos += 1
            else:
                break
        self._col += self.token_length
        return True

    def _in_eol(self):
        """Devuelve True si a continuación viene un END de línea
        o bien se llegó al final de la entrada."""
        if self._pos > self._buffer_ubound or self._is_eol():
            return True
        return False

    def _read_comment_eol(self):
        """Devuelve True si lee un comentario hasta el final de línea."""
        if not self._in_operator(self._operator_comment_eol):
            return False
        self._token_pos = self._pos
        self._pos += len(self._operator_comment_eol)
        self._col += len(self._operator_comment_eol)
        while not self._in_eol():
            self._pos += 1
            self._col += 1
        return True

    def _read_comment_ml(self):
        """Devuelve True si lee un comentario multilínea."""
        if not self._in_operator(self._operator_comment_mls):
            return False
        self._token_pos = self._pos
        self._pos += len(self._operator_comment_mls)
        self._col += len(self._operator_comment_mls)
        while self._pos <= self._buffer_ubound:
            if self._is_eol():
                self._advance_line()
            elif self._match_string(self._operator_comment_mle):
                self._pos += len(self._operator_comment_mle)
                self._col += len(self._operator_comment_mle)
                break
            else:
                self._pos += 1
                self._col += 1
        return True

    def _calc_integer(self, digit, b):
        if self._mant <= (Scanner.MAX_MANTISA - digit) // b:
            self._mant = self._mant * b + digit
            self._num = self._mant
        else:
            self._num_overflow = True

    def _range_mant(self):
        """Devuelve una constante inddicadora del rango de la mantisa."""
        if self._mant <= Scanner._MAX_INTEGER:
            return Scanner.NUM_RANGE_INT
        else:
            return Scanner.NUM_RANGE_LONG

    def _read_num_hex(self):
        """Intenta leer un número hexadecimal usando un AFD:
        Estado 0 -> 1: 0
        Estado 1 -> 2: 'x'|'X'
        Estado 2 -> 3: ('0'..'9')|('A'..'F')|('a'..'f'). [Si]
        Estado 3 -> 3:
        """
        END = 4
        c = "\0"
        state = 0
        lng_partial = 0
        lng_accepted = 0
        pos = self._pos  # Utilizará pos para apuntar al buffer
        self._num = 0.0
        self._mant = 0
        self._exp1 = 0
        self._num_overflow = False

        while state != END:
            if pos <= self._buffer_ubound:
                c = self._text_in[pos]
                pos += 1
                lng_partial += 1
            else:
                state = END  # Fin de la cadena de entrada
            if state == 0:
                if c == "0":
                    state = 1
                else:
                    state = END
            elif state == 1:
                if c == "X" or c == "x":
                    state = 2
                else:
                    state = END
            elif state == 2 or state == 3:
                if "0" <= c <= "9":
                    state = 3
                    lng_accepted = lng_partial
                    if not self._num_overflow:
                        self._calc_integer(ord(c) - 48, 16)
                elif "A" <= c <= "F":
                    state = 3
                    lng_accepted = lng_partial
                    if not self._num_overflow:
                        self._calc_integer(ord(c) - 55, 16)
                elif "a" <= c <= "f":
                    state = 3
                    lng_accepted = lng_partial
                    if not self._num_overflow:
                        self._calc_integer(ord(c) - 87, 16)
                else:
                    state = END
        if lng_accepted > 0:  # Se devuelve lo aceptado
            self._token_pos = self._pos
            self._pos += lng_accepted
            self._col += lng_accepted
            return True
        return False

    def _read_num(self):
        """Lee un número entero o real."""
        if self._read_num_hex():
            if self._num_overflow:
                self._num_range = Scanner.NUM_RANGE_OVERFLOW
            else:
                self._num_range = self._range_mant()
            return True
        elif self._read_decimal_number():
            if self._num_overflow:
                self._num_range = Scanner.NUM_RANGE_OVERFLOW
            elif self._is_integer:
                self._num_range = self._range_mant()
            else:
                self._num_range = Scanner.NUM_RANGE_DOUBLE
            return True

        return False

    def _calc_decimal_int_part(self, digit):
        if self._mant <= (Scanner.MAX_MANTISA - digit) // 10:
            self._mant = self._mant * 10 + digit
            # Si ya hay dígitos significativos reconocidos
            if self._digits != 0:
                self._digits += 1
            else:  # Ningún dígito significativo se reconoció
                # Sólo si es distinto de cero
                if digit != 0:
                    self._digits += 1
        else:
            # Ignora el carácter, ya que provocaría desbordamiento
            self._exp1 += 1
            # Ahora deja de ser un número entero
            self._is_integer = False

    def _calc_decimal_exp_part(self, digit):
        # Se ignoran los resultados que provoquen desbordamiento
        if self._exp2 <= (Scanner.MAX_EXPO - digit) // 10:
            self._exp2 = self._exp2 * 10 + digit

    def _calc_decimal(self, is_integer, sig_neg):
        self._num_overflow = False
        if is_integer or self._mant == 0:
            self._num = self._mant
            return
        if sig_neg:
            self._exp1 -= self._exp2
        else:
            self._exp1 += self._exp2
        # mant * 10 ^ exp1 = 0.dd..dd * 10 ^ (exp1 + nDigits)
        if (self._exp1 + self._digits) > Scanner.MAX_EXPO_NORM:
            self._num_overflow = True
            self._num = math.inf
        elif (self._exp1 + self._digits) < Scanner.MIN_EXPO_NORM:
            self._num = 0.0
        else:
            self._num = self._mant * pow(10.0, self._exp1)

    def _calc_decimal_fract_part(self, digit):
        if self._mant <= (Scanner.MAX_MANTISA - digit) // 10:
            self._mant = self._mant * 10 + digit
            self._exp1 -= 1
            # Si ya hay dígitos significativos reconocidos
            if self._digits != 0:
                self._digits += 1
            else:  # Ningún dígito significativo se reconoció
                # Sólo si es distinto de cero
                if digit != 0:
                    self._digits += 1
        # Se ignoran los resultados que provoquen desbordamiento

    def _read_decimal_number(self):
        r"""Esta función devuelve una constante numérica real, la sintaxis en
            formato CIN es la siguiente:
        num_real = (digitos ["." digitos]) [exponente]
        digitos = {\d}+
        exponente = ("E" | "e") ["+" | "-"] digitos

        Dada la compejidad de un número general,
        se implementa en un autómata finito determinista.
        Esta es la tabla de transiciones
        Estado 0 -> 1: (0-9)[Sí]
        Estado 1 -> 1: (0-9)[Sí], 2: (.), 4: (E|e)
        Estado 2 -> 3: (0-9)[Sí]
        Estado 3 -> 3: (0-9)[Sí], 4: (E|e)
        Estado 4 -> 5: (+|-), 6: (0-9)[Sí]
        Estado 5 -> 6: (0-9[Sí]
        Estado 6 -> 6: (0-9)[Sí]
        Estado 7: Fin
        """
        END = 7
        state = 0
        lng_partial = 0
        lng_accepted = 0
        pos = self._pos  # Utilizará pos para apuntar al buffer
        sig_neg = False  # Indica si el exponente tiene signo menos

        self._is_integer = True  # Lo cambian el state 2 y el 4
        self._num = 0.0
        self._mant = 0
        self._exp1 = 0
        self._exp2 = 0
        self._digits = 0

        if pos <= self._buffer_ubound:
            c = self._text_in[pos]
            if c < "0" or c > "9":
                return False
        else:
            return False

        while state != END:
            if pos <= self._buffer_ubound:
                c = self._text_in[pos]
                pos += 1
                lng_partial += 1
            else:
                state = END  # Fin de la cadena de entrada
            if state == 0:
                if "0" <= c <= "9":
                    state = 1
                    lng_accepted = lng_partial
                    self._calc_decimal_int_part(ord(c) - 48)
                else:
                    state = END
            elif state == 1:
                if "0" <= c <= "9":
                    lng_accepted = lng_partial
                    self._calc_decimal_int_part(ord(c) - 48)
                elif c == ("." if self.use_point else ","):
                    state = 2
                elif c == "E" or c == "e":
                    state = 4
                    self._is_integer = False
                else:
                    state = END
            elif state == 2:
                if "0" <= c <= "9":
                    state = 3
                    self._is_integer = False
                    lng_accepted = lng_partial
                    self._calc_decimal_fract_part(ord(c) - 48)
                else:
                    state = END
            elif state == 3:
                if "0" <= c <= "9":
                    lng_accepted = lng_partial
                    self._calc_decimal_fract_part(ord(c) - 48)
                elif c == "E" or c == "e":
                    state = 4
                else:
                    state = END
            elif state == 4:
                if "0" <= c <= "9":
                    state = 6
                    self._is_integer = False
                    lng_accepted = lng_partial
                    self._calc_decimal_exp_part(ord(c) - 48)
                elif c == "+":
                    state = 5
                elif c == "-":
                    state = 5
                    sig_neg = True
                else:
                    state = END
            elif state == 5:
                if "0" <= c <= "9":
                    state = 6
                    lng_accepted = lng_partial
                    self._calc_decimal_exp_part(ord(c) - 48)
                else:
                    state = END
            elif state == 6:
                if "0" <= c <= "9":
                    lng_accepted = lng_partial
                    self._calc_decimal_exp_part(ord(c) - 48)
                else:
                    state = END
        if lng_accepted > 0:
            # Se devuelve lo aceptado
            self._calc_decimal(self._is_integer, sig_neg)
            self._token_pos = self._pos
            self._pos += lng_accepted
            self._col += lng_accepted
            return True
        return False

    def _read_char(self):
        if not self._in_operator(self._operator_char):
            return False
        self._token_pos = self._pos
        self._pos += len(self._operator_char)
        if self._pos > self._buffer_ubound:
            self._pos = self._token_pos
            return False
        elif self._current == "\\":
            value = self._escape_char()
            if value != -1:
                self._processed_char = value
            else:
                self._pos = self._token_pos
                return False
        elif not self._match_string(self._operator_char):
            self._processed_char = self._current_and_next
        else:
            self._pos = self._token_pos
            return False
        # Se comprueba el delimitador final
        if not self._match_string(self._operator_char):
            self._pos = self._token_pos
            return False
        self._pos += 1
        self._col += self.token_length
        return True

    def _escape_char(self):
        """El puntero de lectura apunta a '\' y se intenta leer una
        secuencia de escape. Devuelve el carácter equivalente, o -1, si no
         es una secuencia válida."""
        self._pos += 1
        if self._in_eol():
            return -1

        # Escapes directos
        dict_espapes = {
            "a": "\u0007",
            "b": "\b",
            "f": "\f",
            "n": "\n",
            "r": "\r",
            "t": "\t",
            "v": "\u000b",
            "0": "\0",
            "'": "'",
            '"': '"',
            "\\": "\\",
        }
        c = self._current
        value = dict_espapes.get(c)
        if value is not None:
            self._pos += 1
            return value

        if c == "x":  # Carácter Unicode codificado en hexadecimal
            self._pos += 1
            if self._pos > self._buffer_ubound:
                return -1

            c = self._current_and_next
            if "0" <= c <= "9":
                code = ord(c) - 48
            elif "A" <= c <= "F":
                code = ord(c) - 55
            elif "a" <= c <= "f":
                code = ord(c) - 87
            else:
                return -1

            if self._pos > self._buffer_ubound:
                return -1

            c = self._current_and_next
            if "0" <= c <= "9":
                code = 16 * code + ord(c) - 48
            elif "A" <= c <= "F":
                code = 16 * code + ord(c) - 55
            elif "a" <= c <= "f":
                code = 16 * code + ord(c) - 87
            else:
                self._pos -= 1
                return chr(code)

            if self._pos > self._buffer_ubound:
                return -1

            c = self._current_and_next
            if "0" <= c <= "9":
                code = 16 * code + ord(c) - 48
            elif "A" <= c <= "F":
                code = 16 * code + ord(c) - 55
            elif "a" <= c <= "f":
                code = 16 * code + ord(c) - 87
            else:
                self._pos -= 1
                return chr(code)

            if self._pos > self._buffer_ubound:
                return -1

            c = self._current_and_next
            if "0" <= c <= "9":
                code = 16 * code + ord(c) - 48
            elif "A" <= c <= "F":
                code = 16 * code + ord(c) - 55
            elif "a" <= c <= "f":
                code = 16 * code + ord(c) - 87
            else:
                self._pos -= 1
                return chr(code)

            return chr(code)
        elif c == "u":  # Carácter Unicode codificado en hexadecimal
            self._pos += 1

            if self._pos > self._buffer_ubound:
                return -1

            c = self._current_and_next
            if "0" <= c <= "9":
                code = ord(c) - 48
            elif "A" <= c <= "F":
                code = ord(c) - 55
            elif "a" <= c <= "f":
                code = ord(c) - 87
            else:
                return -1

            if self._pos > self._buffer_ubound:
                return -1

            c = self._current_and_next
            if "0" <= c <= "9":
                code = 16 * code + ord(c) - 48
            elif "A" <= c <= "F":
                code = 16 * code + ord(c) - 55
            elif "a" <= c <= "f":
                code = 16 * code + ord(c) - 87
            else:
                return -1

            if self._pos > self._buffer_ubound:
                return -1

            c = self._current_and_next
            if "0" <= c <= "9":
                code = 16 * code + ord(c) - 48
            elif "A" <= c <= "F":
                code = 16 * code + ord(c) - 55
            elif "a" <= c <= "f":
                code = 16 * code + ord(c) - 87
            else:
                return -1

            if self._pos > self._buffer_ubound:
                return -1

            c = self._current_and_next
            if "0" <= c <= "9":
                code = 16 * code + ord(c) - 48
            elif "A" <= c <= "F":
                code = 16 * code + ord(c) - 55
            elif "a" <= c <= "f":
                code = 16 * code + ord(c) - 87
            else:
                return -1

            return chr(code)
        else:
            return self._current_and_next

    def _read_string(self):
        """Lee una cadena entre 2 operadores de cadena."""
        if not self._in_operator(self._operator_string):
            return False
        self._processed_string = []
        self._token_pos = self._pos
        cont = True
        res = False
        self._pos += len(self._operator_string)

        while cont:
            if (not self.csv_mode or self.is_eof()) and self._in_eol():
                cont = False
            elif self.csv_mode and self._match_string(self._double_operator_string):
                self._pos += len(self._double_operator_string)
                self._processed_string.append(self._operator_string)
            elif self._match_string(self._operator_string):
                self._pos += len(self._operator_string)
                cont = False
                res = True
            elif not self.csv_mode and self._current == "\\":
                value = self._escape_char()
                if value != -1:
                    self._processed_string.append(value)
                else:
                    cont = False
            else:
                self._processed_string.append(self._current_and_next)
        if res:
            self._col += self.token_length
        else:
            self._pos = self._token_pos
        return res

    def is_eof(self):
        """Devuelve un valor que indica si el scanner ha leído toda la entrada."""
        return self._pos > self._buffer_ubound

    def _read_eol(self):
        r"""Comprueba si puede leer un final de línea: \r, o \r\n o \n."""
        if self._is_eol():
            self._token_pos = self._pos
            self._advance_line()
            return True
        else:
            return False

    def next_token(self) -> int:
        """Devuelve el siguiente token."""
        self._token_previous = self._token
        self._advance_entry()

        # Espacios en la misma línea
        if not self.ignore_spaces:
            if self._read_blanks():
                self._token_class = Scanner.SPACE
                self._token = Scanner.SPACE
                return self._token

        # Comentarios
        if not self.ignore_comments:
            if self._read_comment_eol() or self._read_comment_ml():
                self._token_class = Scanner.COMMENT
                self._token = Scanner.COMMENT
                return self._token

        # Identificadores y palabras clave
        if self._read_identifier():
            index = self._keywords.get(self.lexeme)
            if index is None:  # Identificador
                self._token_class = Scanner.IDENT
                self._token = Scanner.IDENT
            else:  # Palabra clave
                self._token_class = Scanner.KEYWORD
                self._token = index
            return self._token

        # Constantes numéricas
        if self._read_num():
            self._token_class = Scanner.NUMBER
            self._token = Scanner.NUMBER
            return self._token

        # Constantes de carácter
        if self._read_char():
            self._token_class = Scanner.CHAR
            self._token = Scanner.CHAR
            return self._token

        # Constantes de cadena
        if self._read_string():
            self._token_class = Scanner.STRING
            self._token = Scanner.STRING
            return self._token

        # Antes que los operadores deben procesarse: Números, caracteres
        # y cadenas, el motivo es que comienzan por un operador

        # Operadores
        if self._read_operator(True):
            self._token_class = Scanner.OPERATOR
            self._token = self._operators.get(self._last_operator)
            return self._token

        # Finales de línea
        if not self.ignore_eol:
            if self._read_eol():
                self._token_class = Scanner.EOL
                self._token = Scanner.EOL
                return self._token

        # Final de fichero
        if self._pos > self._buffer_ubound:
            self._token_pos = self._pos
            self._token_class = Scanner.EOF
            self._token = Scanner.EOF
            return self._token

        # Carácter no reconocido
        self._token_pos = self._pos
        c = self._current_and_next
        self._processed_char = c

        # Intenta leer un carácter Unicode de 32 bits que estaría codificado
        # por un par de sustitutos, alto (U+D800 a U+DBFF) y bajo (U+DC00 a U+DFFF).
        # Es un error que un carácter se inicie con un sustituto bajo pero por
        # efeciencia no se hace ningún cambio en el carácter leido. También es un error
        # que que comience por uno alto y no le siga uno bajo, pero por el mismo motivo
        # no se hace cambio alguno. El usuario de la clase puede detectar este error
        # usando la función "boolean Character.isSurrogate(char)".
        if _unicodeutils.is_high_surrogate(c):  # Sustituto alto
            if _unicodeutils.is_low_surrogate(self._current):  # Sustituto bajo
                # Lo convertimos a un punto de código válido. Nótese que aunque
                # leemos un carácter más, la columna no aumenta ya que se
                # considera como un carácter único
                self._processed_char = chr(
                    _unicodeutils.to_code_point(c, self._current_and_next)
                )
        self._col += 1
        self._token_class = Scanner.UNKNOWN
        self._token = Scanner.UNKNOWN
        return self._token
    
    def push(self):
            """Salva en la pila del analizador el estado actual
            que está compuesto de las propiedades que se
            devuelven después de una llamada al método next_token().
            """                        
            self._stack.append(StackEntry(self._pos, self._token_pos,
                self._processed_string, self._processed_char, self._token_previous,
                self._token, self._token_class, self._lin, self._col, self._last_col,
                self._num, self._num_overflow, self._mant, self._num_range))

    def pop(self):
        """Recupera el estado del analizado desde la cima de
        la pila de estados y retorna el token almacenado en
        dicho estado.
        """
        state = self._stack.pop()
        self._pos = state.pos
        self._token_pos = state.token_pos
        self._processed_string = state.processed_string
        self._processed_char = state.processed_char
        self._token_previous = state.token_previous
        self._token = state.token
        self._token_class = state.token_class
        self._lin = state.lin
        self._col = state.col
        self._last_col = state.last_col
        self._num = state.num
        self._num_overflow = state.num_overflow
        self._mant = state.mant
        self._num_range = state.num_range

        return state.token

    def remove_top_stack(self):
        """Elimina la cima de la pila de análisis pero no
        recupera el state del analizador."""
        self._stack.pop()

    def clear_stack(self):
        """Borra la pila de análisis sin afectar al estado del analizador."""
        self._stack.clear()

    @property
    def size_stack(self):
        """Devuelve el tamaño de la pila de análisis."""
        return len(self._stack)
