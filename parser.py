def parser(filepath):
    with open(filepath, 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    # ── Paraula (primera línia) ──────────────────────────────────────────
    word = lines[0].strip()

    # ── Regles (línies no buides després de la primera) ──────────────────
    rule_lines = [l for l in lines[1:] if l.strip()]

    # ── Detectar si hi ha probabilitats ──────────────────────────────────
    # Una regla té prob si l'últim token és un float
    def has_prob(tokens):
        try:
            float(tokens[-1])
            return True
        except ValueError:
            return False

    extensio2 = any(has_prob(l.split()) for l in rule_lines)

    # ── Construir gramàtica ───────────────────────────────────────────────
    grammar = {}
    for line in rule_lines:
        tokens = line.split()
        # Format: SimbolEsquerra  Sim1 [Prob1]  Sim2 [Prob2] ...
        head = tokens[0]
        rest = tokens[1:]

        if extensio2:
            # Els tokens van en parells: Simbol Prob  (l'últim és la prob de tota la regla)
            # Format real: A a E 1.0  → A → ('a','E') amb prob 1.0
            prob = float(rest[-1])
            syms = rest[:-1]
        else:
            prob = None
            syms = rest

        # Construir el símbol dret
        if len(syms) == 1:
            sym = syms[0]           # terminal o no-terminal unitari
        else:
            sym = tuple(syms)       # regla binària o més

        rule = (sym, prob) if extensio2 else sym

        if head not in grammar:
            grammar[head] = []
        grammar[head].append(rule)

    # ── Detectar si cal transform (extensio1) ────────────────────────────
    # Cal si hi ha: regles unitàries a NT, regles >2 símbols, o híbrides
    non_terminals = set(grammar.keys())

    def needs_transform(sym):
        s = sym
        if isinstance(s, tuple):
            if len(s) > 2:
                return True                         # no binària
            if any(x not in non_terminals for x in s):
                return True                         # híbrida
        elif isinstance(s, str) and s in non_terminals:
            return True                             # unitària a NT
        return False

    extensio1 = any(
        needs_transform(sym if not extensio2 else rule[0])
        for rules in grammar.values()
        for rule in rules
        for sym in [rule[0] if extensio2 else rule]
    )

    return word, grammar, extensio1, extensio2


# ── Test ràpid ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    word, grammar, ext1, ext2 = parser('input.txt')
    print(f"Paraula:   '{word}'")
    print(f"extensio1: {ext1}")
    print(f"extensio2: {ext2}")
    print("Gramàtica:")
    for head, rules in grammar.items():
        print(f"  {head}: {rules}")