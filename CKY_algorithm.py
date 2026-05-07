class CKY:

    def __init__(self,extensio1=False,extensio2=False):
        self.extensio1 = extensio1
        self.extensio2 = extensio2
    
    def _transform(self,grammar,with_probs):
        new_grammar = {A: list(rules) for A, rules in grammar.items()}
        for A, rules in grammar.items():
            for b in rules:
                if b.islower():
                    rules.delete(b)
                    rules.append()

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
            grammar = self._transform(grammar)
        if self.extensio2:
            result = self._pcky(word,grammar)
            return True if result else False
        else:
            result = self._cky(word,grammar)
            return True if result else False




# cky = CKY()
# print(cky.test(grammar, word))

'''
grammar = {
    'S': [(('X','A'),0.1), (('A','X'),0.1), ('a',0.3), ('b',0.5)],
    'A': [('R','B')],
    'B': [('A','X'), 'b', 'a'],
    'X': ['a'],
    'R': [('X','B')],
}


def _transform(self, grammar, with_probs=False):
    G = {A: list(rules) for A, rules in grammar.items()}
    count = [0]

    def new_sym():
        count[0] += 1
        return f"__X{count[0]}"

    def get(rule):
        return rule if with_probs else (rule, None)

    def put(sym, prob):
        return (sym, prob) if with_probs else sym

    # 1. Híbrides
    for A in list(G):
        G[A] = []
        for rule in grammar[A]:
            sym, prob = get(rule)
            if isinstance(sym, tuple):
                sym = tuple(s if s in G else (T := f"T_{s}", G.setdefault(T, [put(s, 1.0)]), T)[2] for s in sym)
            G[A].append(put(sym, prob))

    # 2. Unitàries
    changed = True
    while changed:
        changed = False
        for A in list(G):
            for rule in list(G[A]):
                sym, prob = get(rule)
                if isinstance(sym, str) and sym in G:
                    G[A].remove(rule)
                    for r2 in G[sym]:
                        s2, p2 = get(r2)
                        G[A].append(put(s2, prob * p2))
                    changed = True

    # 3. No binàries
    for A in list(G):
        new_rules = []
        for rule in G[A]:
            sym, prob = get(rule)
            while isinstance(sym, tuple) and len(sym) > 2:
                X = new_sym()
                G[X] = [put(sym[1:], 1.0)]
                sym = (sym[0], X)
            new_rules.append(put(sym, prob))
        G[A] = new_rules

    return G

'''