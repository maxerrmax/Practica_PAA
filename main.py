from CKY_algorithm import CKY

cky = CKY(extensio2=True)

word = 'aabbc'

grammar = {
    'S': [(('X','A'), 0.25), (('A','X'), 0.25), ('a', 0.25), ('b', 0.25)],
    'A': [(('R','B'), 1.0)],
    'B': [(('A','X'), 0.5), ('b', 0.25), ('a', 0.25)],
    'X': [('a', 1.0)],
    'R': [(('X','B'), 1.0)],
}

cky.solve(word,grammar)

