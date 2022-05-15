import sys

sys.path.append('src')
sys.path.append('../src')

import nukleus as nl

filename = 'files/summe_v6/main.kicad_sch'
sexp = nl.SexpWriter()
with nl.schema(filename, sexp) as _:
    pass
print(sexp)
