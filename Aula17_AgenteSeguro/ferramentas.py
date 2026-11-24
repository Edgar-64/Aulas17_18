def calcular(a, b):
    if type(a) not in (int, float):
        return {'erro': 'O primeiro valor deve ser numérico.'}
    if type(b) not in (int, float):
        return {'erro': 'O segundo valor deve ser numérico.'}
    return {'resultado': a + b}


def executar_ferramenta(nome, argumentos):
    if nome != 'calcular':
        return {'erro': 'Ferramenta não autorizada.'}
    if not isinstance(argumentos, dict) or set(argumentos) != {'a', 'b'}:
        return {'erro': 'Argumentos inválidos.'}
    return calcular(argumentos['a'], argumentos['b'])
