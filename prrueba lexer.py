from abc import ABC, abstractmethod

class Expression (ABC):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    @abstractmethod
    def getFila(self):
        return self.fila
    
    @abstractmethod
    def getColumna(self):
        return self.columna
    
class Lexema(Expression):
    def __init__(self, lexema, fila, columna):
        self.lexema = lexema
        super().__init__(fila, columna)

    def getFila(self):
        return super().getFila()
    
    def getColumna(self):
        return super().getColumna()
    
class Token(Lexema):
    def __init__(self, token, lexema, fila, columna):
        self.token = token
        super().__init__(lexema, fila, columna)

# analizador lexico

def armar_lexema(cadena, analisis="ext") -> tuple:
    lexema = ''
    puntero = ''
    if analisis == "ext":
        for caracter in cadena:
            puntero += caracter
            if caracter == ' ' or caracter == '(':
                return lexema, cadena[len(puntero) - 1:]
            elif not caracter.isalpha():
                return lexema, cadena[len(puntero) - 1:]
            else:
                lexema += caracter
    else:
        for caracter in cadena:
            puntero += caracter
            if caracter == '”':
                aux = cadena[len(puntero):]
                if aux[0] == '{':
                    for i in aux:
                        puntero += i
                        lexema += i
                        if i == ')':
                            return lexema, aux[len(puntero) - 1:]
                else:
                    return lexema, cadena[len(puntero) - 1:]
            else:
                lexema += caracter
    return None, None

class Lexer:

    def _init_(self):
        self.nlinea = 0
        self.ncolumna = 0
        self.lexemas = []
        self.tokens = []
        self.errores = []

    def analizador_lexico(self, cadena):
        lexema = ""
        puntero = 0

        while cadena:
            caracter = cadena[puntero]
            puntero += 1

            if caracter == '“':
                lexema, cadena = armar_lexema(cadena[puntero:], "inter")
                if lexema and cadena:
                    l = Lexema(f'"{lexema}"', self.nlinea, self.ncolumna)
                    t = Token( "Valor interno",l.lexema, l.getfila(), l.getcolumna())
                    self.lexemas.append(l)
                    self.tokens.append(t)
                    self.ncolumna += len(lexema) + 1
                    puntero = 0
            elif caracter == '”':
                self.ncolumna += 1
                cadena = cadena[1:]
                puntero = 0
            elif caracter.isupper() or caracter.islower():
                lexema, cadena = armar_lexema(cadena[puntero - 1:])
                if lexema and cadena:
                    l = Lexema(lexema, self.nlinea, self.ncolumna)
                    if caracter.isupper():
                        t = Token("Palabra reservada", l.lexema, l.getfila(), l.getcolumna())
                    else:
                        t = Token("Identificador", l.lexema, l.getfila(), l.getcolumna())
                    self.lexemas.append(l)
                    self.tokens.append(t)
                    self.ncolumna += len(lexema) + 1
                    puntero = 0
            elif caracter == '=' or caracter == ';' or caracter == ')' or caracter == ',':
                l = Lexema(caracter, self.nlinea, self.ncolumna)
                t = Token("Simbolo", l.lexema, l.getfila(), l.getcolumna())
                self.lexemas.append(l)
                self.tokens.append(t)
                self.ncolumna += 1
                cadena = cadena[1:]
                puntero = 0
            elif caracter == '(':
                l = Lexema(caracter, self.nlinea, self.ncolumna)
                t = Token("Simbolo", l.lexema, l.getfila(), l.getcolumna())
                self.lexemas.append(l)
                self.tokens.append(t)
                self.ncolumna += 1
                cadena = cadena[1:]
                puntero = 0
            elif caracter == "\t":
                self.ncolumna += 4
                cadena = cadena[4:]
                puntero = 0
            elif caracter == "\n":
                self.nlinea += 1
                self.ncolumna = 1
                cadena = cadena[1:]
                puntero = 0
            elif caracter == ' ' or caracter == '\r':
                self.ncolumna += 1
                cadena = cadena[1:]
                puntero = 0
            else:
                error = Token("lexico",caracter, self.nlinea, self.ncolumna)
                self.errores.append(error)
                self.ncolumna += 1
                cadena = cadena[1:]
                puntero = 0

lexer = Lexer()
var = '''CrearBD ejemplo = nueva CrearBD();
EliminarBD elimina = nueva EliminarBD();
CrearColeccion colec = nueva CrearColeccion(“NombreColeccion”);

EliminarColeccion eliminacolec = nueva
EliminarColeccion(“NombreColeccion”);

InsertarUnico insertadoc = nueva InsertarUnico(“NombreColeccion”,“
{
    "nombre":"Obra Literaria",
    "autor":"Jorge Luis"
}
”);

ActualizarUnico actualizadoc = nueva ActualizarUnico(“NombreColeccion”, “
{

    "nombre": "Obra Literaria"
},
{
    $set: {"autor": "Mario Vargas"}
}
”);

EliminarUnico eliminadoc = nueva EliminarUnico(“NombreColeccion”, “
{
    "nombre": "Obra Literaria"
}
”);
BuscarTodo todo = nueva BuscarTodo (“NombreColeccion”);
BuscarUnico todo = nueva BuscarUnico (“NombreColeccion”);
'''
lexer.analizador_lexico(var)

for i in lexer.tokens:
    print(i.token, i.lexema, i.fila, i.columna)
