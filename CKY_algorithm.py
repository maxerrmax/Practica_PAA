from typing import Dict, List, Tuple, Any, Optional

class CKY:
    """
    Classe que defineix l'estructura general de l'algoritme de Cocke-Kasami-Younger (CKY).
    L'algoritme, a partir d'una gramàtica i una paraula, determina si la paraula pertany al
    llenguatge generat per la gramàtica.
    """

    def __init__(self, extensio1: bool = False, extensio2: bool = False) -> None:
        """
        Inicialitza de la classe CKY. Guarda en dues variables separades quina o quines extensions
        estem utilitzant.
        - Si no volem cap extensió: els dos arguments a `False` (per defecte)
        - Per utilitzar l'extensió 1: `extensio1=True`, `extensio2=False`
        - Per utilitzar l'extensió 2: `extensio1=False`, `extensio2=True`
        - Per utilitzar les dues extensions: els dos arguments a `True`
        """
        self.extensio1 = extensio1
        self.extensio2 = extensio2

    def _transforma(self, gramatica: Dict[str, List[Any]], probabilitats: bool = False) -> Dict[str, List[Any]]:
        """
        Mètode auxiliar que transforma una gramàtica de context lliure (CFG) a
        CNF (Forma Normal de Chomsky) per tal de ser acceptada pels algoritmes de
        CKY clàssic i CKY probabilístic. Si estem treballant amb probabilitats, 
        aquesta transformació les manté (`probabilitats=True`).

        El métode realitza les següents transformacions:

        - Regles híbrides (per exemple, `A → a B`): substitueix els símbols terminals 
        de les regles binàries per nous símbols no terminals artificials (per exemple, `T_a`).

        - Regles unitàries: si `A → B` i B és no terminal, substitueix B per totes les seves 
        regles ajustant les probabilitats.

        - Regles no binàries: modifica les regles de més de dos no terminals creant símbols
        auxiliars `__X1`, `__X2`, etc. de manera que les regles no continguin més de dos elements
        (per exemple, `A → B C D` es transforma en `A → B __X1` i `__X1 → C D`).

        Retorna la gramàtica en format CNF.
        """
        def desempaquetar(regla: Any) -> Tuple[Any, Optional[float]]:
            """
            Funció auxiliar que desempaqueta un regla en (simbols, probabilitat) o (simbols, None) 
            en funció de si estem utilitzant probabilitats o no, respectivament.
            """
            if probabilitats:
                return regla[0], regla[1]
            else:
                return regla, None

        def empaquetar(simbols: Any, prob: Optional[float]) -> Any:
            """
            Funció auxiliar que empaqueta els simbols en una regla de format (simbols, probabilitat) 
            o simplement simbols, en funció de si estem utilitzant probabilitats o no, respectivament.
            """
            if probabilitats:
                return (simbols, prob)
            else:
                return simbols

        # Fem una copia profunda de la gramàtica
        G = {A: list(regles) for A, regles in gramatica.items()}

        # Regles híbrides:
        for A in list(G):
            regles_noves = []
            for regla in G[A]:
                simbols, prob = desempaquetar(regla)
                if isinstance(simbols, tuple): # Comprovem si la regla és binària
                    nous_simbols = []
                    for simbol in simbols:
                        if simbol not in G: # Comprovem si el símbol és un terminal
                            T = f"T_{simbol}"
                            if T not in G:
                                G[T] = [empaquetar(simbol, 1.0)]
                            nous_simbols.append(T)
                        else: # El símbol és no terminal
                            nous_simbols.append(simbol)
                    regles_noves.append(empaquetar(tuple(nous_simbols), prob))
                else: # La regla no és binària
                    regles_noves.append(empaquetar(simbols, prob))
            G[A] = regles_noves

        # Regles unitàries
        modificat = True
        while modificat:
            modificat = False
            for A in list(G): # Repasem totes les claus per si ha hagut modificacions
                regles_noves = []
                for regla in G[A]:
                    simbols, prob = desempaquetar(regla)
                    if isinstance(simbols, str) and simbols in G and simbols != A: # Comprovem si la regla és unitària i apunta a un no terminal
                                                                                   # També comprovem que la regla no pot apuntar a si mateixa (per exemple: A → A)
                        for regla2 in G[simbols]:
                            simbols2, prob2 = desempaquetar(regla2)
                            nova_prob = prob * prob2 if probabilitats else None
                            nova_regla = empaquetar(simbols2, nova_prob)
                            if nova_regla not in regles_noves:
                                regles_noves.append(nova_regla)
                        
                        # Indiquem que hem de tornar a revisar perquè hi ha hagut modificacions
                        modificat = True
                    else:
                        regles_noves.append(empaquetar(simbols, prob))
                G[A] = regles_noves

        # Regles no binàries:
        num = [0] # Comptador per generar identificadors únics
        claus = list(G)
        for A in claus:
            regles_noves = []
            for regla in G[A]:
                simbols, prob = desempaquetar(regla)
                while isinstance(simbols, tuple) and len(simbols) > 2: # Comprovem si la regla segueix tenint més de 2 símbols
                    num[0] += 1
                    X = f"__X{num[0]}"
                    claus.append(X)
                    G[X] = [empaquetar(simbols[1:], 1.0)] # X agafa tots els símbols menys el primer
                    simbols = (simbols[0], X) # Ara la regla original apunta al primer símbol i a X
                regles_noves.append(empaquetar(simbols, prob))
            G[A] = regles_noves

        return G

    def _cky(self, paraula: str, gramatica: Dict[str, List[Any]]) -> bool:
        """
        Mètode auxiliar que aplica l'algoritme de CKY clàssic. Indica si una paraula pertany al llenguatge
        generat per la gramàtica indicada. El procediment segueix el pseudocodi presentat a l'article 
        "CYK algorithm" de Wikipedia: https://en.wikipedia.org/wiki/CYK_algorithm
        """
        # Assumim que la paraula buida no forma part del llenguatge
        if not paraula:
            print(f"'' no forma part del llenguatge")
            return False
        n = len(paraula)
        claus = list(gramatica.keys())
        r = len(claus)
        P = [[[False for _ in range(r)] for _ in range(n + 1)] for _ in range(n + 1)]
        index = {A:i for i, A in enumerate(claus)}

        for s in range(1, n+1):
            for v, R_v in enumerate(gramatica):
                if paraula[s - 1] in gramatica[R_v]:
                    P[1][s][v] = True

        for l in range(2,n+1):
            for s in range(1,n-l+2):
                for p in range(1,l):
                    for a, R_a in enumerate(gramatica):
                        for regla in gramatica[R_a]:
                            if isinstance(regla, tuple):
                                b, c = index[regla[0]], index[regla[1]]
                                if P[p][s][b] and P[l-p][s+p][c]:
                                    P[l][s][a] = True
        
        if P[n][1][0]:
            print(f"{paraula} forma part del llenguatge")
            return True
        else:
            print(f"{paraula} no forma part del llenguatge")
            return False

    def _pcky(self, paraula: str, gramatica: Dict[str, List[Any]]) -> bool:
        """
        Mètode auxiliar que aplica l'algoritme de CKY probabilístic. Indica si una paraula pertany al llenguatge
        generat per la gramàtica indicada. El procediment segueix el pseudocodi presentat a l'article "CYK algorithm" 
        de Wikipedia: https://en.wikipedia.org/wiki/CYK_algorithm
        """
        # Assumim que la paraula buida no forma part del llenguatge
        if not paraula:
            print(f"'' no forma part del llenguatge")
            return False
        n = len(paraula)
        claus = list(gramatica.keys())
        r = len(claus)
        P = [[[0 for _ in range(r)] for _ in range(n + 1)] for _ in range(n + 1)]
        index = {A:i for i, A in enumerate(claus)}

        for s in range(1, n+1):
            for v, R_v in enumerate(gramatica):
                for regla, prob in gramatica[R_v]:
                    if isinstance(regla, str) and regla == paraula[s-1]:
                        P[1][s][v] = prob
        
        for l in range(2,n+1):
            for s in range(1,n-l+2):
                for p in range(1,l):
                    for a, R_a in enumerate(gramatica):
                        for regla, prob in gramatica[R_a]:
                            if isinstance(regla, tuple):
                                b, c, = index[regla[0]], index[regla[1]]
                                prob_splitting = prob * P[p][s][b] * P[l-p][s+p][c]
                                if prob_splitting > P[l][s][a]:
                                    P[l][s][a] = prob_splitting
        
        if P[n][1][0] > 0:
            print(f"{paraula} forma part del llenguatge")
            return True
        else:
            print(f"{paraula} no forma part del llenguatge")
            return False
    
    def solve(self, paraula: str, gramatica: Dict[str, List[Any]]) -> bool:
        """
        Mètode principal de la classe CKY. Donades una paraula i una gramàtica:

        - En cas d'haver presentat una gramàtica CFG, la transforma a CNF.
        - En cas d'haver presentat una gramàtica amb probabilitats, aplica l'algoritme de
        CKY probabilístic. En cas contrari, aplica l'algoritme de CKY clàssic.

        Retorna `True` o `False` en funció de si la paraula pertany o no al llenguatge
        que genera la gramàtica.
        """
        if self.extensio1:
            gramatica = self._transforma(gramatica, probabilitats=self.extensio2)
        if self.extensio2:
            return self._pcky(paraula, gramatica)
        else:
            return self._cky(paraula, gramatica)