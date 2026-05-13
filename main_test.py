from CKY_algorithm import CKY

# ─── TESTS CKY / PCKY ───────────────────────────────────────────────────────
# Gramàtica mínima en FNC per a les paraules: "a", "ab", "aab"
# S → A B | 'a'
# A → 'a'
# B → 'b'

grammar_cky = {
    'S': [('A', 'B'), 'a'],
    'A': ['a'],
    'B': ['b'],
}

grammar_pcky = {
    'S': [(('A', 'B'), 0.5), ('a', 0.5)],
    'A': [('a', 1.0)],
    'B': [('b', 1.0)],
}

# Gramàtica que necessita transform (té regles unitàries i híbrides)
# S → A B C  (no binària)
# S → A      (unitària)
# A → 'a'
# B → 'b'
# C → 'c'
grammar_transform_cky = {
    'S': [('A', 'B', 'C'), 'A'],
    'A': ['a'],
    'B': ['b'],
    'C': ['c'],
}

grammar_transform_pcky = {
    'S': [(('A', 'B', 'C'), 0.6), ('A', 0.4)],
    'A': [('a', 1.0)],
    'B': [('b', 1.0)],
    'C': [('c', 1.0)],
}

cky   = CKY(extensio1=False, extensio2=False)
pcky  = CKY(extensio1=False, extensio2=True)
tcky  = CKY(extensio1=True,  extensio2=False)
tpcky = CKY(extensio1=True,  extensio2=True)

print("=" * 55)
print("TEST 1 — CKY bàsic (gramàtica ja en FNC)")
print("=" * 55)
assert cky.solve('a',  grammar_cky) == True,  "FAIL: 'a' hauria de ser True"
assert cky.solve('ab', grammar_cky) == True,  "FAIL: 'ab' hauria de ser True"
assert cky.solve('b',  grammar_cky) == False, "FAIL: 'b' hauria de ser False"
assert cky.solve('ba', grammar_cky) == False, "FAIL: 'ba' hauria de ser False"
assert cky.solve('',   grammar_cky) == False, "FAIL: '' hauria de ser False"
print("Tots correctes ✓")

print()
print("=" * 55)
print("TEST 2 — PCKY bàsic (gramàtica ja en FNC amb probs)")
print("=" * 55)
assert pcky.solve('a',  grammar_pcky) == True,  "FAIL: 'a' hauria de ser True"
assert pcky.solve('ab', grammar_pcky) == True,  "FAIL: 'ab' hauria de ser True"
assert pcky.solve('b',  grammar_pcky) == False, "FAIL: 'b' hauria de ser False"
assert pcky.solve('',   grammar_pcky) == False, "FAIL: '' hauria de ser False"
print("Tots correctes ✓")

print()
print("=" * 55)
print("TEST 3 — CKY + transform (regles unitàries i no binàries)")
print("=" * 55)
assert tcky.solve('a',   grammar_transform_cky) == True,  "FAIL: 'a' hauria de ser True"   # S→A→a
assert tcky.solve('abc', grammar_transform_cky) == True,  "FAIL: 'abc' hauria de ser True"  # S→ABC
assert tcky.solve('ab',  grammar_transform_cky) == False, "FAIL: 'ab' hauria de ser False"
assert tcky.solve('b',   grammar_transform_cky) == False, "FAIL: 'b' hauria de ser False"
print("Tots correctes ✓")

print()
print("=" * 55)
print("TEST 4 — PCKY + transform (regles unitàries i no binàries)")
print("=" * 55)
assert tpcky.solve('a',   grammar_transform_pcky) == True,  "FAIL: 'a' hauria de ser True"
assert tpcky.solve('abc', grammar_transform_pcky) == True,  "FAIL: 'abc' hauria de ser True"
assert tpcky.solve('ab',  grammar_transform_pcky) == False, "FAIL: 'ab' hauria de ser False"
print("Tots correctes ✓")

print()
print("=" * 55)
print("TEST 5 — Casos límit")
print("=" * 55)
assert cky.solve('aab', grammar_cky)  == False, "FAIL: 'aab' no és al llenguatge"
assert pcky.solve('aab', grammar_pcky) == False, "FAIL: 'aab' no és al llenguatge"
# Paraula llarga vàlida: 'ab' repetit no és vàlid (S no és recursiva)
assert cky.solve('abab', grammar_cky) == False, "FAIL: 'abab' no és al llenguatge"
print("Tots correctes ✓")

print()
print("=" * 55)
print("TOTS ELS TESTS HAN PASSAT ✓")
print("=" * 55)

print("=" * 55)
print("TEST — CKY vs PCKY: mateix resultat de pertenença")
print("=" * 55)

# Gramàtica ambigua: 'aa' té DOS arbres de parse possibles
#   S → S S (p=0.4)  →  [S→a][S→a]
#   S → 'a' (p=0.6)
# PCKY ha de triar el parse MÉS PROBABLE, però tots dos han de dir True/False igual

grammar_ambigu_cky = {
    'S': [('S', 'S'), 'a'],
}

grammar_ambigu_pcky = {
    'S': [(('S', 'S'), 0.4), ('a', 0.6)],
}

words = ['a', 'aa', 'aaa', 'aaaa', 'b', 'ab', '']

cky_res  = CKY(extensio1=False, extensio2=False)
pcky_res = CKY(extensio1=False, extensio2=True)

all_match = True
for w in words:
    r_cky  = cky_res.solve(w,  grammar_ambigu_cky)
    r_pcky = pcky_res.solve(w, grammar_ambigu_pcky)
    match = r_cky == r_pcky
    if not match:
        all_match = False
    print(f"  '{w}': CKY={r_cky}, PCKY={r_pcky}  {'✓' if match else '✗ DIFERENCIA!'}")

print()
if all_match:
    print("CKY i PCKY coincideixen en totes les paraules ✓")
else:
    print("DIFERENCIES DETECTADES — revisar implementació ✗")