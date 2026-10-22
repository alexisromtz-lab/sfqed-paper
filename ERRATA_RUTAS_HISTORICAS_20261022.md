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

## Menciones al arbol de custodia

<!-- HUELLA-ERRATA-MENCIONES-CUSTODIA-20261022 -->

**7 lineas** de los registros y del expediente de deposito nombran el arbol privado
donde viven el instrumento de pre-vuelo, el catalogo interno y el corpus de trabajo.
Designan el **origen de la custodia**, no una dependencia: ningun archivo publico de este
repositorio lo importa, lo ejecuta ni lo necesita para medir.

Se conservan por la misma razon que las rutas: son la transcripcion de lo que se ejecuto y
lo que se deposito. Reescribirlas cambiaria el contenido sobre el que se sostienen las
conclusiones y el deposito. Quedan adjudicadas por huella con las demas lineas de este
libro: si alguien las edita, la huella caduca y el hallazgo vuelve a abrirse.

Nota sobre el expediente de deposito: cuando un metadato ya publicado acredita el arbol
privado como identificador relacionado, la correccion no se hace aqui — el registro
externo es inmutable en su version. Se declara en esta errata y se corrige en la version
siguiente del deposito.

## Adjudicación de rutas relativas

Las seis coincidencias `RUTA_CRUZADA` revisadas son rutas internas del árbol de este repositorio —incluidos `../main.tex` y el destino relativo de `git-hooks`—, no imports ni dependencias hacia otro repositorio. Se conservan sin cambios y se adjudican como falsos positivos del detector.
