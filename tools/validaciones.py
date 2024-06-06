import re

def solo_numeros(cadena):
    return bool(re.match("^[0-9]+$", cadena))

def is_nombre(nombre):
    patron_espacios = r'\s{4,}'
    res = re.search(patron_espacios,nombre)
    if  res:
        print('xd1')
        return False
    if len(nombre) <= 4:
        print('xd2')
        return False
    if solo_numeros(nombre):
        print('xd')
        return False
    return True

def is_telefono(cadena):
    if not solo_numeros(cadena):
        return False
    if len(cadena) != 10:
        return False
    
    return True


