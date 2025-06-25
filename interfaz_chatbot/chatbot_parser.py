import ply.lex as lex
import ply.yacc as yacc
import random

# ---------------------------
# 1. Lexer
# ---------------------------

tokens = (
    'CLAVE',
    'PREP',
    'CIUDAD',
    'FECHA'
)

# Palabras clave
def t_CLAVE(t):
    r'clima|temperatura|pronostico|tiempo'
    return t

# Preposiciones
def t_PREP(t):
    r'en|de|para'
    return t

# Fechas (hoy, mañana, pasado mañana o dd/mm como 25_06)
def t_FECHA(t):
    r'hoy|manana|pasado_manana|[0-9]{2}_[0-9]{2}'
    return t

# Ciudades válidas
def t_CIUDAD(t):
    r'corrientes|san_cosme|empedrado|itati|posadas|resistencia'
    return t

# Ignorar espacios y tabs
t_ignore = ' \t\n'

# Manejo de errores léxicos
def t_error(t):
    raise ValueError(f"Token inválido: {t.value}")

# Crear el lexer
lexer = lex.lex()

# ---------------------------
# 2. Parser
# ---------------------------

# Regla: consulta simple -> clave + prep + ciudad + fecha
def p_consulta_simple(p):
    'consulta : CLAVE PREP CIUDAD FECHA'
    temperatura = random.randint(0, 45)
    p[0] = f"La temperatura de {p[3].capitalize()} es {temperatura}°C el {p[4]}."
    

# Regla: consulta con doble preposición -> clave + prep + ciudad + prep + fecha
def p_consulta_con_doble_prep(p):
    'consulta : CLAVE PREP CIUDAD PREP FECHA'
    temperatura = random.randint(0, 45)
    p[0] = f"La temperatura de {p[3].capitalize()} es {temperatura}°C  {p[5]}."

# Manejo de errores sintácticos
def p_error(p):
    raise SyntaxError("Consulta mal formada o no reconocida.")

# Crear el parser
parser = yacc.yacc()

# ---------------------------
# 3. Función de interfaz para Django u otros
# ---------------------------

def procesar_mensaje(user_message):
    try:
        # Normalizar entrada del usuario
        msg = user_message.lower().strip()
        msg = (
            msg.replace("á", "a").replace("é", "e").replace("í", "i")
               .replace("ó", "o").replace("ú", "u").replace("ñ", "n")
               .replace("pasado mañana", "pasado_manana")
               .replace("/", "_")
        )
        resultado = parser.parse(msg)
        return resultado
    except (SyntaxError, ValueError) as e:
        return f"❌ Error: {e}"
