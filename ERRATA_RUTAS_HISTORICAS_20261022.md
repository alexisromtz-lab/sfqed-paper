# Fe de erratas: referencias de rutas históricas

<!-- HUELLA-ERRATA-RUTAS-HISTORICAS-20261022 -->

## Alcance

Se registran dos clases de referencias absolutas al entorno de ejecución original:

- **Sanitizadas el 2026-10-22** (commit `1d7b45b`): `sim/n3_fasores_20261011.py:58` y
  `sim/evaluador_adjuntos_tres_mallas.py:31,48` anclan ahora la raíz al propio módulo
  (`Path(__file__).resolve().parents[1]`). La ruta del entorno ya no aparece en el código.
- **Conservada** en `bundle/instrumentos/medidores/fuego_pestana2_20261011.py:36`, que pertenece al
  bundle sellado por `bundle/HASHES.sha256`: reescribirla rompería `tools/verificar_bundle.sh`.

Para reproducir los artefactos históricos en otro checkout, toda referencia a
`/Users/<usuario>/sfqed-paper` se interpreta como la raíz local del repositorio (`$SFQED_ROOT`), conservando
el sufijo relativo de cada referencia. Esta equivalencia documenta la portabilidad del contexto, no garantiza
por sí sola la existencia de cada archivo referenciado.

## Adjudicación de rutas relativas

Las seis coincidencias `RUTA_CRUZADA` revisadas son rutas internas del árbol de este repositorio —incluidos `../main.tex` y el destino relativo de `git-hooks`—, no imports ni dependencias hacia otro repositorio. Se conservan sin cambios y se adjudican como falsos positivos del detector.
