from CKY_algorithm import CKY
from parser import parser

FILE_PATH = "tests/input.txt"

word, grammar, ext1, ext2 = parser(FILE_PATH)

cky = CKY(extensio1=ext1, extensio2=ext2)
cky.solve(word,grammar)

