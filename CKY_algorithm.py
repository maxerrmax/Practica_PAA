class CKY:

    def __init__(self,extensio1=False,extensio2=False):
        self.extensio1 = extensio1
        self.extensio2 = extensio2

    def _transform(self, grammar, with_probs=False):
        # Helpers per desempaquetar/empaquetar regles segons el format
        def unpack(rule):
            if with_probs:
                return rule[0], rule[1]   # (sym, prob)
            else:
                return rule, None         # (sym, None)

        def pack(sym, prob):
            if with_probs:
                return (sym, prob)
            else:
                return sym

        G = {A: list(rules) for A, rules in grammar.items()}

        # ── PAS 1: Regles híbrides ──────────────────────────────────────────
        # Si una regla binària conté un terminal, crear un nou no-terminal per ell
        for A in list(G):
            new_rules = []
            for rule in G[A]:
                sym, prob = unpack(rule)
                if isinstance(sym, tuple):
                    new_sym = []
                    for s in sym:
                        if s not in G:          # és un terminal
                            T = f"T_{s}"
                            if T not in G:
                                G[T] = [pack(s, 1.0)]
                            new_sym.append(T)
                        else:
                            new_sym.append(s)
                    new_rules.append(pack(tuple(new_sym), prob))
                else:
                    new_rules.append(pack(sym, prob))
            G[A] = new_rules

        # ── PAS 2: Regles unitàries ─────────────────────────────────────────
        # Si A → B i B és un no-terminal, substituir per totes les regles de B
        changed = True
        while changed:
            changed = False
            for A in list(G):
                new_rules = []
                for rule in G[A]:
                    sym, prob = unpack(rule)
                    if isinstance(sym, str) and sym in G:   # regla unitària a NT
                        for rule2 in G[sym]:
                            sym2, prob2 = unpack(rule2)
                            new_prob = prob * prob2 if with_probs else None
                            new_rules.append(pack(sym2, new_prob))
                        changed = True
                    else:
                        new_rules.append(pack(sym, prob))
                G[A] = new_rules

        # ── PAS 3: Regles no binàries ───────────────────────────────────────
        # Si A → B C D..., binaritzar amb símbols auxiliars __X1, __X2, ...
        count = [0]
        for A in list(G):
            new_rules = []
            for rule in G[A]:
                sym, prob = unpack(rule)
                while isinstance(sym, tuple) and len(sym) > 2:
                    count[0] += 1
                    X = f"__X{count[0]}"
                    G[X] = [pack(sym[1:], 1.0)]  # X → C D ... (prob 1.0)
                    sym = (sym[0], X)             # A → B X
                new_rules.append(pack(sym, prob))
            G[A] = new_rules

        return G

    def _cky(self,word,grammar):
        if not word:
            print(f"'' no forma part del llenguatge")
            return None
        n = len(word)
        claus = list(grammar.keys())
        r = len(claus)
        P = [[[False for _ in range(r)] for _ in range(n + 1)] for _ in range(n + 1)]
        back = [[[[] for _ in range(r)] for _ in range(n + 1)] for _ in range(n + 1)]
        index = {A:i for i, A in enumerate(claus)}

        for s in range(1, n+1):
            for v, R_v in enumerate(grammar):
                if word[s - 1] in grammar[R_v]:
                    P[1][s][v] = True

        for l in range(2,n+1):
            for s in range(1,n-l+2):
                for p in range(1,l):
                    for a, R_a in enumerate(grammar):
                        for rule in grammar[R_a]:
                            if isinstance(rule, tuple):
                                b, c = index[rule[0]], index[rule[1]]
                                if P[p][s][b] and P[l-p][s+p][c]:
                                    P[l][s][a] = True
                                    back[l][s][a].append([p,b,c])
        
        if P[n][1][0]:
            print(f"{word} forma part del llenguatge")
            return back
        else:
            print(f"{word} no forma part del llenguatge")
            return None

    def _pcky(self,word,grammar):
        if not word:
            print(f"'' no forma part del llenguatge")
            return None
        n = len(word)
        claus = list(grammar.keys())
        r = len(claus)
        P = [[[0 for _ in range(r)] for _ in range(n + 1)] for _ in range(n + 1)]
        back = [[[[] for _ in range(r)] for _ in range(n + 1)] for _ in range(n + 1)]
        index = {A:i for i, A in enumerate(claus)}

        for s in range(1, n+1):
            for v, R_v in enumerate(grammar):
                for rule, prob in grammar[R_v]:
                    if isinstance(rule, str) and rule == word[s-1]:
                        P[1][s][v] = prob
        
        for l in range(2,n+1):
            for s in range(1,n-l+2):
                for p in range(1,l):
                    for a, R_a in enumerate(grammar):
                        for rule, prob in grammar[R_a]:
                            if isinstance(rule, tuple):
                                b, c, = index[rule[0]], index[rule[1]]
                                prob_splitting = prob * P[p][s][b] * P[l-p][s+p][c]
                                if prob_splitting > P[l][s][a]:
                                    P[l][s][a] = prob_splitting
                                    back[l][s][a] = [p,b,c]
        
        if P[n][1][0]>0:
            print(f"{word} forma part del llenguatge")
            return back
        else:
            print(f"{word} no forma part del llenguatge")
            return None
    
    def solve(self,word,grammar):
        if self.extensio1:
            grammar = self._transform(grammar,with_probs=self.extensio2)
        if self.extensio2:
            result = self._pcky(word,grammar)
            return True if result else False
        else:
            result = self._cky(word,grammar)
            return True if result else False