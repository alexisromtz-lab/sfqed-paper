# Fe de erratas: referencias de rutas históricas

<!-- HUELLA-ERRATA-RUTAS-HISTORICAS-20261022 -->

## Alcance

Se registran cuatro referencias absolutas al entorno de ejecución original, conservadas en tres artefactos del repositorio:

- `bundle/instrumentos/medidores/fuego_pestana2_20261011.py:36`: `/Users/marlene/sfqed-paper/sim`.
- `sim/evaluador_adjuntos_tres_mallas.py:31,48`: referencia a `sim/data/invariantes/adjuntos_tres_mallas_20261013.json`.
- `sim/n3_fasores_20261011.py:58`: `/Users/marlene/sfqed-paper`.

Estos contenidos se preservan sin reescritura retroactiva. Para reproducirlos en otro checkout, la raíz histórica `/Users/marlene/sfqed-paper` se interpreta como la raíz local del repositorio (`$SFQED_ROOT`); se conserva el sufijo relativo de cada referencia. Esta equivalencia documenta la portabilidad del contexto, no garantiza por sí sola la existencia de cada archivo referenciado.

## Adjudicación de rutas relativas

Las seis coincidencias `RUTA_CRUZADA` revisadas son rutas internas del árbol de este repositorio —incluidos `../main.tex` y el destino relativo de `git-hooks`—, no imports ni dependencias hacia otro repositorio. Se conservan sin cambios y se adjudican como falsos positivos del detector.
