#!/usr/bin/env python3
"""
lint_tex.py -- verificacion ESTRUCTURAL de main.tex, sin motor TeX.

Cubre, por conteo y no por lectura, los defectos que pdflatex reporta primero:
  (1) entornos \\begin/\\end balanceados y bien anidados
  (2) llaves y signos de dolar balanceados
  (3) toda \\label referenciada existe, y toda \\label se usa
  (4) toda clave \\cite existe en refs.bib, y ninguna entrada queda sin citar
  (5) cero meta-lenguaje del corpus interno
  (6) inventario de entornos flotantes y de ecuaciones

Uso: python3 -B lint_tex.py [main.tex] [refs.bib]
"""
import re
import sys
from collections import Counter

tex_path = sys.argv[1] if len(sys.argv) > 1 else "main.tex"
bib_path = sys.argv[2] if len(sys.argv) > 2 else "refs.bib"

src = open(tex_path, encoding="utf-8").read()
bib = open(bib_path, encoding="utf-8").read()

# quitar comentarios (un % no escapado corta la linea)
body = re.sub(r"(?<!\\)%.*", "", src)

rojos = []

# ---------------- (1) entornos ----------------
begins = re.findall(r"\\begin\{([^}]*)\}", body)
ends = re.findall(r"\\end\{([^}]*)\}", body)
stack, malos = [], []
for m in re.finditer(r"\\(begin|end)\{([^}]*)\}", body):
    kind, env = m.group(1), m.group(2)
    if kind == "begin":
        stack.append(env)
    else:
        if not stack:
            malos.append(f"\\end{{{env}}} sin \\begin")
        elif stack[-1] != env:
            malos.append(f"\\end{{{env}}} cierra a \\begin{{{stack[-1]}}}")
            stack.pop()
        else:
            stack.pop()
if stack:
    malos.append("sin cerrar: " + ", ".join(stack))
if malos:
    rojos.append("ENTORNOS: " + " | ".join(malos))

# ---------------- (2) llaves y dolares ----------------
def balance(ch_open, ch_close):
    o = len(re.findall(r"(?<!\\)" + re.escape(ch_open), body))
    c = len(re.findall(r"(?<!\\)" + re.escape(ch_close), body))
    return o, c

bo, bc = balance("{", "}")
if bo != bc:
    rojos.append(f"LLAVES desbalanceadas: {{ {bo} vs }} {bc}")

dol = len(re.findall(r"(?<!\\)\$", body))
if dol % 2 != 0:
    rojos.append(f"\\$ impar: {dol}")

# ---------------- (3) labels y refs ----------------
labels = set(re.findall(r"\\label\{([^}]*)\}", body))
refs = set(re.findall(r"\\(?:eqref|ref|autoref)\{([^}]*)\}", body))
faltan = sorted(refs - labels)
huerfanos = sorted(labels - refs)
if faltan:
    rojos.append("REFS sin destino: " + ", ".join(faltan))

# ---------------- (4) citas vs bib ----------------
bibkey = set(re.findall(r"@\w+\{([^,]+),", bib))
citas = set()
for m in re.finditer(r"\\cite\{([^}]*)\}", body):
    citas |= {k.strip() for k in m.group(1).split(",")}
sin_entrada = sorted(citas - bibkey)
sin_citar = sorted(bibkey - citas)
if sin_entrada:
    rojos.append("CITAS sin entrada en .bib: " + ", ".join(sin_entrada))
if sin_citar:
    rojos.append("ENTRADAS sin citar: " + ", ".join(sin_citar))

# ---------------- (5) meta-lenguaje ----------------
meta = ["sello", "UNIVERSO DECLARADO", "acta", "corpus", "mesa/", "sha16",
        "boolean", "gate", "expediente", "particion", "PARTICIONADOR"]
golpes = []
low = body.lower()
for w in meta:
    n = low.count(w.lower())
    if n:
        golpes.append(f"{w}={n}")
if golpes:
    rojos.append("META-LENGUAJE: " + " ".join(golpes))

# ---------------- (6) inventario ----------------
eqs = len(re.findall(r"\\begin\{equation\}", body))
eqstar = len(re.findall(r"\\begin\{equation\*\}", body))
figs = len(re.findall(r"\\begin\{figure\}", body))
tabs = len(re.findall(r"\\begin\{table\}", body))
comillas = Counter(re.findall(r"\\cite\{([^}]*)\}", body))

# ---------------- salida ----------------
print("UNIVERSO DECLARADO: main.tex + refs.bib del paper SFQED; el lint cuenta "
      "estructura (entornos, llaves, dolares, labels, citas, meta-lenguaje) "
      "sobre el texto sin comentarios.")
print(f"bytes tex={len(src)}  bytes sin comentarios={len(body)}")
print(f"entornos begin/end = {len(begins)}/{len(ends)}  "
      f"cuentas: equation={eqs} equation*={eqstar} figure={figs} table={tabs}")
print(f"llaves {{={bo} }}={bc}   dolares={dol}   labels={len(labels)} "
      f"refs={len(refs)}")
print(f"citas distintas={len(citas)}  entradas bib={len(bibkey)}  "
      f"\\cite totales={len(comillas)}")
if huerfanos:
    print("labels sin usar (no es error): " + ", ".join(huerfanos))
print("ROJOS: " + ("NINGUNO" if not rojos else str(len(rojos))))
for r in rojos:
    print("  ROJO " + r)
print("VEREDICTO: " + ("estructura limpia" if not rojos else "hay rojos, ver arriba"))
