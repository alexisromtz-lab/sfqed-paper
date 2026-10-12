# AGENTS.md — protocolo de telemetría atómica (`sfqed-paper`)

UNIVERSO DECLARADO: la raíz de este repositorio. MOTOR: lo lee cualquier pestaña o subagente que abra el workspace. UNIDAD: axioma. VENTANA: reloj UTC del acto; toda cifra de este archivo caduca al escribirse y se re-mide antes de citarla.

NATURALEZA: instrumento, NO medida. Este archivo no entra a su propio censo.

## A1 — El puntero viaja, el cuerpo no

Prohibido volcar archivos, diffs largos o logs en el chat. Se reporta por ruta, línea y `sha16`. `sha16` = `sha256` truncado a 16 caracteres hexadecimales.

## A2 — La línea atómica

Toda corrida se reporta en una sola línea:

`VEREDICTO · RC · MOTOR · SHA16 · CRUDO: /ruta/en/disco`

`RC` es el del comando, no el del rótulo. Si el crudo tiene algo que medir, se imprimen los dos operandos, nunca solo el conteo. Una salida que no puede diferir no es evidencia.

## A3 — `bundle/` es inmutable

`bundle/` (35 archivos, sello `0ce97cf9d8c44987`) no se edita y no se audita desde dentro. La auditoría entra solo desde afuera, por `tools/verificar_bundle.sh` (`09ab3b5b24d9bb47`).

## A4 — Las simulaciones van por el camino declarado

Toda simulación corre por `sim/fuego_sensible.py` (`3ec003de4cb848d6`), respetando el filtro analítico previo antes de FDTD.

## Guardas de la cabecera

- **Ningún `HEAD` se escribe en este archivo.** Se mide vivo con `git rev-parse --short HEAD`. Una cabecera con `HEAD` escrito envejece y miente: defecto ya pagado.
- **Cero signos monetarios en texto de reemplazo.** El signo dispara la familia de variables de sustitución e inyecta texto del archivo dentro de sí mismo.
- **Un cero de un comando inválido no es un cero del objeto.** Nunca se canaliza un comando sin validar hacia un contador. Para la lista de modificados se usa `git diff --name-only --diff-filter=M`, nunca `git status --diff-filter=M`.
- **`git status --porcelain` sin `-uall` no cuenta el objeto.** Se declara cuál de los dos anchos se usó, y se imprimen los dos.
- **Toda ausencia se mide** (`test -f`, `grep -c`), jamás se asume. Y al verificar una edición se cuentan los encabezados vecinos, no se lee el fragmento de éxito.
