#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
telemetria_minima.py — contrato de telemetria de minima entropia (una pieza, stdlib).

TESIS
  Un script no narra: emite estado. El delta se transmite; el procedimiento y la
  condicion normal NO se transmiten (silencio). La prosa se activa de forma
  asimetrica --solo-- cuando se rompe un gate, y entonces lleva la coordenada de
  la fractura, no una justificacion.

UNIDAD DE TRANSMISION
  Una linea JSONL por check, claves en ORDEN CANONICO FIJO:

      t   id   o   u   m   d   rc   r

  t   (str)  hora UTC ISO-8601 terminada en Z.  Sin hora la cifra no es cifra:
             toda cifra de conteo caduca al escribirse.
  id  (str)  namespace unico del emisor, "script/huella".  Evita que dos scripts
             homonimos crucen estados y lo llamen divergencia.
  o   (str)  sha16 del OBJETO medido (no del emisor).  Impide validar un script
             contra el hash que el propio script imprimio de su version previa.
  u   (obj)  universo declarado = {"n": int, "git": bool, "venv": bool}.
             "git"/"venv" declaran si el arbol INCLUYE .git y .venv; forzarlos
             evita que dos conteos con arbol distinto se lean como discrepancia
             del objeto.  Sin denominador declarado no hay medida.
  m   (str)  motor: el comando exacto que produjo la cifra.  grep BRE y re no
             son el mismo metro para el mismo patron.
  d   ([..]) delta = [unidad, antes, despues], o AUSENTE si no hay cambio.
             La unidad es adjetiva y de lista cerrada: archivo != linea !=
             ocurrencia != byte != encabezado.  Un delta nulo NO se emite.
  rc  (int)  codigo de salida REAL.  Un rotulo impreso no es un exit.
  r   (obj)  fractura = null, o {"archivo","linea","esperado","hallado"}.
             Unico campo con texto, y solo la coordenada.  Obligatorio si rc != 0.

REGLAS
  1. Delta nulo -> se omite d.  Gate verde -> r = null.
  2. El receptor compara campo a campo: nada de parsear prosa.
  3. Fail-closed: clave fuera de orden, campo faltante, tipo equivocado, d
     presente con delta nulo, rc != 0 sin r, o r sin rc != 0 -> aborta (2).

MEJORAS SOBRE EL ESQUEMA BASE (encontradas al implementar)
  a. u pasa de entero a objeto {n, git, venv}: la exclusion del arbol deja de ser
     implicita (era la causa de dos cifras para el mismo conteo).
  b. d prohibe antes == despues: un delta nulo es ruido, no dato.
  c. check separa TRES codigos de salida: 0 = todo verde, 1 = fractura reportada
     por un emisor (objeto rojo), 2 = contrato roto (metro roto).  Un objeto rojo
     y un metro roto no son el mismo fallo.
  d. selftest lleva control POSITIVO: si el validador aceptara todo, el test no
     discriminaria.  Se cuentan casos validos y casos que DEBEN fallar.
  e. check distingue el SILENCIO del VERDE: un archivo con 0 lineas no vacias
     salia 0 (falso verde medido el 2026-10-11 con el archivo vacio).  Cero
     medidas no pueden diferir; ausencia de linea no es gate verde -> 2.

USO
  python3 -B telemetria_minima.py sha RUTA
  python3 -B telemetria_minima.py emit --id s/x --o SHA16 --u-n N --m "comando" \
        [--d unidad antes despues] [--rc 1 --r archivo linea esperado hallado]
  python3 -B telemetria_minima.py check [RUTA|-]
  python3 -B telemetria_minima.py selftest
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ORDEN = ("t", "id", "o", "u", "m", "d", "rc", "r")
ORDEN_SIN_D = tuple(k for k in ORDEN if k != "d")
UNIDADES = frozenset(
    {"archivo", "linea", "ocurrencia", "byte", "encabezado", "segundo", "ratio"}
)
RE_SHA16 = re.compile(r"^[0-9a-f]{16}$")
RE_T = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
RE_ID = re.compile(r"^[^\s/]+/[^\s/]+$")
COMPACT = {"separators": (",", ":"), "ensure_ascii": False}


class ErrorContrato(Exception):
    """El emisor rompio el contrato. Fail-closed: no se adivina nada."""


def _entero(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def hora_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha16_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]


def sha16_archivo(ruta) -> str:
    return sha16_bytes(Path(ruta).read_bytes())


# --------------------------------------------------------------------------
# VALIDADOR
# --------------------------------------------------------------------------
def valida(linea: str) -> dict:
    """Devuelve el objeto validado o lanza ErrorContrato. Nunca repara."""
    if not isinstance(linea, str):
        raise ErrorContrato("la linea debe ser texto")
    texto = linea.strip()
    if not texto:
        raise ErrorContrato("linea vacia: el silencio no es una linea, no se emite")

    try:
        obj = json.loads(texto)
    except json.JSONDecodeError as e:
        raise ErrorContrato("json invalido: %s" % e) from None
    if not isinstance(obj, dict):
        raise ErrorContrato("la linea debe ser un objeto json, no %s" % type(obj).__name__)

    claves = tuple(obj.keys())
    if claves not in (ORDEN, ORDEN_SIN_D):
        raise ErrorContrato(
            "claves fuera de orden canonico: %s (esperado %s, o el mismo sin 'd')"
            % (claves, ORDEN)
        )

    t = obj["t"]
    if not isinstance(t, str) or not RE_T.match(t):
        raise ErrorContrato("t debe ser UTC ISO-8601 terminado en Z, no %r" % (t,))

    ident = obj["id"]
    if not isinstance(ident, str) or not RE_ID.match(ident):
        raise ErrorContrato(
            "id debe ser 'script/namespace' sin espacios, no %r" % (ident,)
        )

    o = obj["o"]
    if not isinstance(o, str) or not RE_SHA16.match(o):
        raise ErrorContrato("o debe ser sha16 en minusculas, no %r" % (o,))

    u = obj["u"]
    if not isinstance(u, dict) or tuple(u.keys()) != ("n", "git", "venv"):
        raise ErrorContrato("u debe ser {n, git, venv}, no %r" % (u,))
    if not _entero(u["n"]) or u["n"] < 0:
        raise ErrorContrato("u.n debe ser entero >= 0, no %r" % (u["n"],))
    if not isinstance(u["git"], bool) or not isinstance(u["venv"], bool):
        raise ErrorContrato(
            "u.git y u.venv deben ser booleanos (declarar si el arbol los INCLUYE)"
        )

    m = obj["m"]
    if not isinstance(m, str) or not m:
        raise ErrorContrato("m debe ser el comando motor, texto no vacio")

    if "d" in obj:
        d = obj["d"]
        if not isinstance(d, list) or len(d) != 3:
            raise ErrorContrato("d debe ser [unidad, antes, despues], no %r" % (d,))
        unidad, antes, despues = d
        if unidad not in UNIDADES:
            raise ErrorContrato(
                "d[0] debe ser unidad de la lista cerrada, no %r" % (unidad,)
            )
        if not _entero(antes) or not _entero(despues):
            raise ErrorContrato("d[1] y d[2] deben ser enteros, no %r" % (d[1:],))
        if antes == despues:
            raise ErrorContrato("delta nulo (antes == despues): no se emite 'd'")

    rc = obj["rc"]
    if not _entero(rc):
        raise ErrorContrato("rc debe ser el entero de salida real, no %r" % (rc,))

    r = obj["r"]
    if rc == 0:
        if r is not None:
            raise ErrorContrato("rc == 0 con fractura declarada: gate verde emite r = null")
    else:
        if not isinstance(r, dict) or tuple(r.keys()) != (
            "archivo",
            "linea",
            "esperado",
            "hallado",
        ):
            raise ErrorContrato(
                "rc != 0 exige r = {archivo, linea, esperado, hallado}, no %r" % (r,)
            )
        if not isinstance(r["archivo"], str) or not r["archivo"]:
            raise ErrorContrato("r.archivo debe ser texto no vacio")
        if not _entero(r["linea"]) or r["linea"] < 1:
            raise ErrorContrato("r.linea debe ser entero >= 1")
    return obj


# --------------------------------------------------------------------------
# EMISOR DE REFERENCIA
# --------------------------------------------------------------------------
def emite(id, o, u, m, rc=0, d=None, r=None, t=None) -> str:
    """Construye, valida contra el contrato y devuelve UNA linea JSONL."""
    if not isinstance(u, dict):
        raise ErrorContrato("u debe ser {n, git, venv}")
    obj = {
        "t": hora_utc() if t is None else t,
        "id": id,
        "o": o,
        "u": {"n": u.get("n"), "git": u.get("git"), "venv": u.get("venv")},
        "m": m,
    }
    if d is not None:
        obj["d"] = [d[0], d[1], d[2]]
    obj["rc"] = rc
    obj["r"] = r
    linea = json.dumps(obj, **COMPACT)
    valida(linea)  # gate interno: el emisor no puede emitir lo que el validador rechaza
    return linea


# --------------------------------------------------------------------------
# AUTO-TEST: control positivo (casos que DEBEN fallar) + control negativo
# --------------------------------------------------------------------------
_VALIDOS = (
    '{"t":"2026-10-11T00:00:00Z","id":"demo/a","o":"0123456789abcdef",'
    '"u":{"n":86,"git":false,"venv":false},"m":"grep -cE","rc":0,"r":null}',
    '{"t":"2026-10-11T00:00:00Z","id":"demo/a","o":"0123456789abcdef",'
    '"u":{"n":86,"git":false,"venv":false},"m":"grep -cE","d":["linea",44,48],'
    '"rc":0,"r":null}',
    '{"t":"2026-10-11T00:00:00Z","id":"demo/a","o":"0123456789abcdef",'
    '"u":{"n":86,"git":false,"venv":false},"m":"grep -cE","rc":1,'
    '"r":{"archivo":"x.md","linea":17,"esperado":1,"hallado":2}}',
)

_MALOS = (
    ("claves desordenadas",
     '{"t":"2026-10-11T00:00:00Z","id":"demo/a","o":"0123456789abcdef",'
     '"u":{"n":86,"git":false,"venv":false},"rc":0,"m":"grep","r":null}'),
    ("falta u",
     '{"t":"2026-10-11T00:00:00Z","id":"demo/a","o":"0123456789abcdef",'
     '"m":"grep","rc":0,"r":null}'),
    ("delta nulo",
     '{"t":"2026-10-11T00:00:00Z","id":"demo/a","o":"0123456789abcdef",'
     '"u":{"n":86,"git":false,"venv":false},"m":"grep","d":["linea",5,5],'
     '"rc":0,"r":null}'),
    ("rc != 0 sin fractura",
     '{"t":"2026-10-11T00:00:00Z","id":"demo/a","o":"0123456789abcdef",'
     '"u":{"n":86,"git":false,"venv":false},"m":"grep","rc":1,"r":null}'),
    ("rc == 0 con fractura",
     '{"t":"2026-10-11T00:00:00Z","id":"demo/a","o":"0123456789abcdef",'
     '"u":{"n":86,"git":false,"venv":false},"m":"grep","rc":0,'
     '"r":{"archivo":"x.md","linea":1,"esperado":1,"hallado":2}}'),
    ("u sin declarar git",
     '{"t":"2026-10-11T00:00:00Z","id":"demo/a","o":"0123456789abcdef",'
     '"u":{"n":86},"m":"grep","rc":0,"r":null}'),
    ("o no es sha16",
     '{"t":"2026-10-11T00:00:00Z","id":"demo/a","o":"XYZ",'
     '"u":{"n":86,"git":false,"venv":false},"m":"grep","rc":0,"r":null}'),
    ("unidad fuera de la lista cerrada",
     '{"t":"2026-10-11T00:00:00Z","id":"demo/a","o":"0123456789abcdef",'
     '"u":{"n":86,"git":false,"venv":false},"m":"grep","d":["archivos",1,2],'
     '"rc":0,"r":null}'),
    ("id sin namespace",
     '{"t":"2026-10-11T00:00:00Z","id":"demo","o":"0123456789abcdef",'
     '"u":{"n":86,"git":false,"venv":false},"m":"grep","rc":0,"r":null}'),
    ("linea vacia (silencio leido como dato)", "   "),
)


def selftest() -> int:
    ok_validos = 0
    for i, linea in enumerate(_VALIDOS, 1):
        try:
            valida(linea)
            ok_validos += 1
        except ErrorContrato as e:
            print("  FALLO: valido %d rechazado: %s" % (i, e))
    ok_malos = 0
    for nombre, linea in _MALOS:
        try:
            valida(linea)
            print("  FALLO: malo aceptado (%s): el validador no discrimina" % nombre)
        except ErrorContrato:
            ok_malos += 1

    # control de NIVEL DE ARCHIVO: el silencio no es verde
    rc_vacio = -1
    ruta_vacia = Path(tempfile.mkstemp(suffix=".jsonl")[1])
    try:
        ruta_vacia.write_text("", encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            rc_vacio = cmd_check(str(ruta_vacia))
    except OSError:
        rc_vacio = -1
    finally:
        try:
            ruta_vacia.unlink()
        except OSError:
            pass
    ok_vacio = rc_vacio == 2

    print(
        "UNIVERSO DECLARADO: %d lineas de prueba (3 validas + 10 malformadas) + 1 "
        "archivo vacio, motor = valida() sobre casos literales y cmd_check() sobre "
        "archivo de 0 bytes, unidad = caso, ventana = reloj local."
        % (len(_VALIDOS) + len(_MALOS))
    )
    print(
        "  validos aceptados = %d/%d · malformados rechazados = %d/%d"
        % (ok_validos, len(_VALIDOS), ok_malos, len(_MALOS))
    )
    print(
        "  control de archivo vacio: rc = %d (esperado 2) -> %s"
        % (rc_vacio, "OK" if ok_vacio else "FALLO")
    )
    verdes = (
        ok_validos == len(_VALIDOS) and ok_malos == len(_MALOS) and ok_vacio
    )
    print("  veredicto = %s" % ("VERDE" if verdes else "ROJO"))
    return 0 if verdes else 1


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def cmd_check(ruta: str) -> int:
    try:
        if ruta in ("-", None):
            texto = sys.stdin.read()
        else:
            texto = Path(ruta).read_text(encoding="utf-8")
    except OSError as e:
        print("CONTRATO ROTO: no se pudo leer %s: %s" % (ruta, e), file=sys.stderr)
        return 2

    lineas = [l for l in texto.splitlines() if l.strip()]
    if not lineas:
        print(
            "CONTRATO ROTO: 0 lineas no vacias: el silencio no es una linea, y un "
            "archivo vacio NO es verde (cero medidas no pueden diferir)",
            file=sys.stderr,
        )
        print(
            "UNIVERSO DECLARADO: 0 lineas no vacias leidas, motor = valida() por linea, "
            "unidad = linea, ventana = sin reloj (entrada de archivo)."
        )
        return 2
    validas = malformadas = fracturas = 0
    for i, linea in enumerate(lineas, 1):
        try:
            obj = valida(linea)
        except ErrorContrato as e:
            malformadas += 1
            print("  l.%d CONTRATO ROTO: %s" % (i, e), file=sys.stderr)
            continue
        validas += 1
        if obj["rc"] != 0:
            fracturas += 1
            fr = obj["r"]
            print(
                "  l.%d FRACTURA %s:%s esperado=%r hallado=%r"
                % (i, fr["archivo"], fr["linea"], fr["esperado"], fr["hallado"])
            )

    print(
        "UNIVERSO DECLARADO: %d lineas no vacias leidas, motor = valida() por linea, "
        "unidad = linea, ventana = sin reloj (entrada de archivo)."
        % len(lineas)
    )
    print(
        "  validas=%d · malformadas=%d · con fractura=%d" % (validas, malformadas, fracturas)
    )
    if malformadas:
        return 2
    if fracturas:
        return 1
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="telemetria_minima",
        description="Contrato de telemetria de minima entropia (JSONL, orden canonico).",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    ps = sub.add_parser("sha", help="sha16 del archivo (para el campo o)")
    ps.add_argument("ruta")

    pe = sub.add_parser("emit", help="emite una linea de estado")
    pe.add_argument("--id", required=True)
    pe.add_argument("--o", required=True)
    pe.add_argument("--u-n", required=True, type=int)
    pe.add_argument("--u-git", action="store_true")
    pe.add_argument("--u-venv", action="store_true")
    pe.add_argument("--m", required=True)
    pe.add_argument("--d", nargs=3, metavar=("UNIDAD", "ANTES", "DESPUES"))
    pe.add_argument("--rc", type=int, default=0)
    pe.add_argument("--r", nargs=4, metavar=("ARCHIVO", "LINEA", "ESPERADO", "HALLADO"))
    pe.add_argument("--t", default=None)

    pc = sub.add_parser("check", help="valida un archivo JSONL o '-' (stdin)")
    pc.add_argument("ruta", nargs="?", default="-")

    sub.add_parser("selftest", help="control positivo + negativo del validador")

    args = p.parse_args(argv)
    try:
        if args.cmd == "sha":
            print(sha16_archivo(args.ruta))
            return 0
        if args.cmd == "emit":
            d = None
            if args.d:
                d = (args.d[0], int(args.d[1]), int(args.d[2]))
            r = None
            if args.r:
                esp, hal = args.r[2], args.r[3]
                r = {
                    "archivo": args.r[0],
                    "linea": int(args.r[1]),
                    "esperado": int(esp) if esp.lstrip("-").isdigit() else esp,
                    "hallado": int(hal) if hal.lstrip("-").isdigit() else hal,
                }
            print(
                emite(
                    id=args.id,
                    o=args.o,
                    u={"n": args.u_n, "git": args.u_git, "venv": args.u_venv},
                    m=args.m,
                    rc=args.rc,
                    d=d,
                    r=r,
                    t=args.t,
                )
            )
            return args.rc
        if args.cmd == "check":
            return cmd_check(args.ruta)
        if args.cmd == "selftest":
            return selftest()
    except ErrorContrato as e:
        print("CONTRATO ROTO: %s" % e, file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
