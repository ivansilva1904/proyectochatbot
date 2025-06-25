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
climas = ["despejado", "nublado", "lluvioso", "tormenta", "llovizna"]

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
# 2. Función auxiliar para generar respuesta
# ---------------------------

def generar_respuesta(clave, ciudad, fecha):
    
    if ciudad == "san_cosme":
        ciudad_legible = "San Cosme"
    else:
        ciudad_legible = ciudad.capitalize()

    if fecha == "pasado_manana":
        fecha_legible = "pasado mañana"
    else:
        fecha_legible = fecha.replace("_", "/")
        
    if clave == 'temperatura':
        temperatura = random.randint(0, 45)
        return f"La temperatura de {ciudad_legible} es {temperatura}°C para {fecha_legible}."
    else:
        estado_clima = random.choice(climas)
        return f"El {clave} en {ciudad_legible} para {fecha_legible} será {estado_clima}."

# ---------------------------
# 3. Parser
# ---------------------------

def p_consulta_simple(p):
    'consulta : CLAVE PREP CIUDAD FECHA'
    p[0] = generar_respuesta(p[1], p[3], p[4])

def p_consulta_con_doble_prep(p):
    'consulta : CLAVE PREP CIUDAD PREP FECHA'
    p[0] = generar_respuesta(p[1], p[3], p[5])

def p_error(p):
    raise SyntaxError("Consulta mal formada o no reconocida.")

parser = yacc.yacc()

# Manejo de errores sintácticos
def p_error(p):
    raise SyntaxError("Consulta mal formada o no reconocida.")

# Crear el parser
parser = yacc.yacc()

# ---------------------------
# 4. Función de interfaz 
# ---------------------------

def procesar_mensaje(user_message):
    try:
        # Normalizar entrada del usuario
        msg = user_message.lower().strip()
        msg = (
            msg.replace("san cosme", "san_cosme")
               .replace("pasado mañana", "pasado_manana")
        )

        # Reemplazo de tildes y otros
        msg = (
            msg.replace("á", "a").replace("é", "e").replace("í", "i")
               .replace("ó", "o").replace("ú", "u").replace("ñ", "n")
               .replace("/", "_")
        )
        
        resultado = parser.parse(msg)
        return resultado
    except (SyntaxError, ValueError) as e:
        return f"❌ Error: {e}"
