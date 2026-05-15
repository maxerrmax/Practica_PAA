from CKY_algorithm import CKY
from parser import parser

# Especificar quin fitxer de prova es vol executar
RUTA_FITXER = "tests/input.txt"

# Amb la funció parser aconseguim tot el necessari del
# fitxer donat
paraula, gramatica, ext1, ext2 = parser(RUTA_FITXER)

# Apliquem l'algoritme
cky = CKY(extensio1=ext1, extensio2=ext2)
cky.solve(paraula, gramatica)

