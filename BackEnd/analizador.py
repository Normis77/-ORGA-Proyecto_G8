import re
from Poss import Posicion

reserved = {
    'conf_ini':'conf_ini',
    'add':'add'
}
# matrix[x-1][y-1]
matrix = [[0,1,2,3],
          [4,5,6,7],
          [ 8,9,'A','B'],
          ['C','D','E','F']]

posiciones = []

lexemas = list(reserved.values())

global list_lex

n_line = 0
n_column = 0

def Analizer(entrada):
    global n_line
    global n_column
    lex = ''
    puntero = 0
     
    while puntero < len(entrada):

        char = entrada[puntero]
        lex+=char
        n_column+=1

        if lex == 'conf_ini':
            print(f'-->{lex}')
            chars_consumed = interpretar_lex(entrada[puntero+1:])
            lex = ''
            puntero += chars_consumed
            continue
        elif lex == '//':
            puntero+= comments(entrada[puntero:])
            lex = ''
            continue

        elif char.isspace():
            lex=''
        puntero+=1

def interpretar_lex(cadena):
    puntero = 0
    token = ''
    while puntero < len(cadena):
        char = cadena[puntero]
        token+=char
        if token.lower() == 'add':
            print(f'-->{token}')
            token =''
            puntero +=1

            while puntero<len(cadena) and cadena[puntero].isspace():
                puntero+=1

            sig_token=''
            while puntero<len(cadena) and cadena[puntero] not in  ['\n', '\r']:
                sig_token+=cadena[puntero]                    
                puntero+=1
            
            sig_token=sig_token.strip().replace(' ','')
            
            match = re.match(r'x:(\d+),y:(\d+)', sig_token, re.IGNORECASE)
            if match:
                px = int(match.group(1))
                py = int(match.group(2))
                print(f'--> Coordenadas: {px},{py}')
                posiciones.append(Posicion(px,py))
            else:
                print('⚠️ Formato inválido. Se esperaba "x:<num>, y:<num>"')       
            
            continue

        elif token.isspace():
            token=''
        elif token.lower() == 'conf:fin':
            print(f'-->{token}')
            token = ''
            puntero += 1
            return puntero 
        elif token == '//':
            puntero += comments(cadena[puntero:])
            token=''
            continue
        puntero+=1
    return puntero

def comments(cadena):
    for i, char in enumerate(cadena):
        if char == '\n':
            return i+1
    return len(cadena)

