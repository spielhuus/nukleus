import sys

sys.path.append('src')
sys.path.append('../src')

import nukleus

filename = 'files/summe_v6/main.kicad_sch'
schema = nukleus.load_schema(filename)
print(schema.sexp())
