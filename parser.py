from typing import Tuple, Dict, List, Any, Union, Set

def parser(ruta_fitxer: str) -> Tuple[str, Dict[str, List[Any]], bool, bool]:
    """
    Funció que llegeix un fitxer i determina si hi ha probabilitats (`extensio2`) i 
    si la gramàtica es necessita transformar de CFG a CNF (`extensio1`). A més, extreu la paraula
    a analitzar (`paraula`) i construeix la gramàtica (`gramatica`).

    Es retornen les quatre variables: `paraula`, `gramatica`, `extensio1` i `extensio2`
    """
    def te_probabilitats(elements: List[str]) -> bool:
        """
        Funció auxiliar que detecta si una regla presenta probabilitats. Una regla
        té probabilitats si l'últim element és un `float`.
        """
        try:
            float(elements[-1])
            return True
        except ValueError:
            return False

    def necessita_trasformacio(simbol: Union[str, Tuple[str, ...]], no_terminals: Set[str]) -> bool:
        """
        Funció auxiliar que detecta si una gramàtica necessita transformar-se de
        CFG a CNF. Cal fer una transformació si tenim regles híbrides, regles amb
        més de 2 símbols o regles unitàries que apunten a no terminals.
        """
        if isinstance(simbol, tuple):
            if len(simbol) > 2:
                return True # Regla no binària
            if any(x not in no_terminals for x in simbol):
                return True # Regla híbrida
        elif isinstance(simbol, str) and simbol in no_terminals:
            return True # Regla unitària que apunta a no terminal
        return False
    
    with open(ruta_fitxer, 'r') as f:
        linies = [linia.rstrip('\n') for linia in f.readlines()]

    # Paraula (primera línia)
    paraula = linies[0].strip()

    # Regles (línies no buides després de la primera)
    linies_regles = [l for l in linies[1:] if l.strip()]

    # Comprovem si utilitzem l'extensió 2
    extensio2 = any(te_probabilitats(l.split()) for l in linies_regles)

    # Construïm la gramàtica segons el format que hem escollit
    gramatica = {}
    for linia in linies_regles:
        elements = linia.split()
        primer_element = elements[0]
        resta_elements = elements[1:]

        if extensio2:
            prob = float(resta_elements[-1])
            simbols = resta_elements[:-1]
        else:
            prob = None
            simbols = resta_elements

        # Construïm la regla
        if len(simbols) == 1:
            simbol = simbols[0] # Terminal o no-terminal unitari
        else:
            simbol = tuple(simbols) # Regla binària o més de dos símbols

        regla = (simbol, prob) if extensio2 else simbol

        if primer_element not in gramatica:
            gramatica[primer_element] = []
        gramatica[primer_element].append(regla)

    no_terminals = set(gramatica.keys())

    # Comprovem si utilitzem l'extensió 1
    extensio1 = any(
        necessita_trasformacio(simbol if not extensio2 else regla[0], no_terminals)
        for regles in gramatica.values()
        for regla in regles
        for simbol in [regla[0] if extensio2 else regla]
    )

    return paraula, gramatica, extensio1, extensio2