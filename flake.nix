{
  description = "SFQED bundle - pin declarativo del MOTOR de medida. Perfil por defecto: .#gnu. Perfil historico: .#bsd.";

  # ===========================================================================
  # QUE FIJA ESTA PIEZA Y QUE NO
  #
  # (1) NO ELIGE EL MOTOR. El motor esta declarado DENTRO del instrumento:
  #       bundle/verificar.sh            l.55 -> MOTOR: shasum -a 256 | cmp | grep -F | python3 -B | git -C
  #       bundle/tests/bench_must_fail.sh l.35 -> MOTOR: /bin/sh + shasum + python3 -B + cp/rm/ln
  #     Este flake solo tiene que SATISFACER esas lineas. Elegir el motor despues
  #     de ver la salida de la puerta seria elegir el metro al final.
  #
  # (2) NO FIJA EL INTERPRETE. Los dos .sh llevan shebang #!/bin/sh, que es RUTA
  #     ABSOLUTA: la resuelve el anfitrion, no el PATH. Este pin fija el PATH de
  #     las HERRAMIENTAS, no el shell que ejecuta el script. Por eso el shellHook
  #     imprime `ls -l /bin/sh` y la version: sin esa linea, la corrida no dice
  #     con que shell midio.
  #
  # (3) NO ESTA BLOQUEADO. Medido 2026-10-11T05:55:23Z: `nix` NO esta instalado
  #     en este anfitrion => flake.lock NO se puede producir ni verificar aqui.
  #     El primer acto del receptor es el lock: `nix develop` (por defecto .#gnu)
  #     y el flake.lock que genere es su propio testigo.
  #
  # (4) NO LLEVA `checks` NI `formatter`. Un check que nadie corre informa, no
  #     protege (gate sin assert detras), y no se escriben nombres de paquete de
  #     memoria. Se declaran omitidos.
  #
  # (5) NO ENTRA AL MANIFIESTO. bundle/HASHES.sha256 cubre rutas relativas a
  #     bundle/, y este archivo vive en la raiz del repo => queda DECLARADO fuera
  #     del universo del manifiesto. Repararlo no es de esta pieza.
  #
  # INVENTARIO MEDIDO (2026-10-11T05:56:14Z; MOTOR = grep -oE sobre las piezas
  # ejecutables del bundle; UNIDAD = ocurrencia por binario; VENTANA = ese reloj):
  #   verificar.sh       : shasum 6 | git 13 | gitleaks 6 | grep 5 | python3 4 |
  #                        sed 3 | cmp 3 | wc 2 | tr 2 | date 2 | head 1 |
  #                        dirname 1 | cut 1
  #   bench_must_fail.sh : shasum 10 | git 8 | gitleaks 6 | python3 5 | wc 4 |
  #                        tr 4 | grep 4 | cut 3 | awk 3 | sed 2 | head 2 |
  #                        dirname 2 | date 2 | uniq 1 | sort 1 | mktemp 1 |
  #                        cmp 1 | basename 1
  #   instrumentos/**    : git | gitleaks | python3 | grep | cmp | shasum | sed |
  #                        cut | date | wc | tr | dirname
  #   NO APARECEN: sha256sum (el unico motor de hash es shasum, que es perl) |
  #                find | xargs | tar | gzip | diff | nix.
  #   => el juego de paquetes de abajo se fija por INVENTARIO MEDIDO, no por
  #      parecido POSIX. Lo que no aparece, no se incluye y se declara.
  #
  # CONSECUENCIA DECLARADA, y es la razon del perfil por defecto:
  #   verificar.sh l.90-91 aborta con RC=2 si `shasum` no existe, y el banco lo
  #   exige como caso C (`PATH sin shasum` -> RC=2). En GNU/Linux el paquete
  #   coreutils trae `sha256sum` y NO trae `shasum`: un perfil sin perl devuelve
  #   ROJO, no verde falso. El defecto del pin seria ruidoso, no silencioso.
  # ===========================================================================

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      sistemas = [ "aarch64-darwin" "x86_64-darwin" "aarch64-linux" "x86_64-linux" ];
      enCadaSistema = f: nixpkgs.lib.genAttrs sistemas (s: f (import nixpkgs { system = s; }));

      # Perfil por defecto: GNU. `shasum` es un script de perl, no un binario de
      # coreutils; por eso perl esta aqui y por eso sha256sum NO lo sustituye.
      motorGnu = pkgs: with pkgs; [
        bashInteractive
        coreutils
        diffutils
        gawk
        git
        gitleaks
        gnugrep
        gnused
        perl
        python3
      ];

      # Perfil historico: userland BSD del anfitrion, sin prefijo GNU.
      # En darwin resuelve al BSD del sistema (el hook pone /usr/bin y /bin
      # delante). En linux NO existe userland BSD: es una FACHADA declarada, y el
      # hook lo imprime en vez de callarlo.
      motorBsd = pkgs: with pkgs; [
        bashInteractive
        git
        gitleaks
        perl
        python3
      ];

      perfil = pkgs: nombre: paquetes: hook: pkgs.mkShell {
        name = "sfqed-" + nombre;
        packages = paquetes;
        shellHook = hook;
      };

      # El motor resuelto se IMPRIME, no se supone: si una ruta sale del store de
      # nix, el perfil es ese; si sale de /usr/bin, es el anfitrion. Sin esta
      # impresion el par gnu/bsd se elegiria en vez de medirse.
      informeMotor = ''
        echo "--- quienes resuelven, en este shell ---"
        printf '  shasum   -> %s\n' "$(command -v shasum   || echo AUSENTE)"
        printf '  gitleaks -> %s\n' "$(command -v gitleaks || echo AUSENTE)"
        printf '  python3  -> %s\n' "$(command -v python3  || echo AUSENTE)"
        printf '  git      -> %s\n' "$(command -v git      || echo AUSENTE)"
        printf '  cmp      -> %s\n' "$(command -v cmp      || echo AUSENTE)"
        printf '  awk      -> %s\n' "$(command -v awk      || echo AUSENTE)"
        printf '  grep     -> %s\n' "$(command -v grep     || echo AUSENTE)"
        printf '  sed      -> %s\n' "$(command -v sed      || echo AUSENTE)"
        echo "--- el shell que correra los .sh (shebang absoluto: NO lo fija el pin) ---"
        ls -l /bin/sh
      '';
    in {
      devShells = enCadaSistema (pkgs: {
        default = perfil pkgs "gnu" (motorGnu pkgs) ''
          export MOTOR_ETIQUETA=GNU
          echo "PERFIL NIX = gnu (por defecto)"
          echo "DECLARADO EN LA PIEZA: bundle/verificar.sh l.55"
          ${informeMotor}
        '';

        gnu = perfil pkgs "gnu" (motorGnu pkgs) ''
          export MOTOR_ETIQUETA=GNU
          echo "PERFIL NIX = gnu (explicito)"
          echo "DECLARADO EN LA PIEZA: bundle/verificar.sh l.55"
          ${informeMotor}
        '';

        bsd = perfil pkgs "bsd" (motorBsd pkgs) ''
          export PATH="/usr/bin:/bin:$PATH"
          echo "PERFIL NIX = bsd (retrocompatibilidad historica)"
          case "$(uname -s)" in
            Darwin) echo "  anfitrion darwin: el userland BSD es un OBJETO de este anfitrion" ;;
            *)      echo "  anfitrion NO darwin: este perfil es una FACHADA declarada, no un userland BSD" ;;
          esac
          # La etiqueta MOTOR se MIDE, no se asume: es lo que permite que la linea
          # declarada de cada medicion viaje con su piso (MOTORES.md 3).
          if [ "$(uname -s)" = "Darwin" ] && [ "$(command -v shasum)" = "/usr/bin/shasum" ]; then
            export MOTOR_ETIQUETA=M0
          else
            export MOTOR_ETIQUETA=BSD-NO-REPRODUCIBLE
          fi
          echo "DECLARADO EN LA PIEZA: bundle/tests/bench_must_fail.sh l.35"
          ${informeMotor}
        '';
      });

      # ---------------------------------------------------------------------
      # packages.oci · el tarball OCI sale de ESTE archivo, con el MISMO juego de
      # paquetes que .#gnu (motorGnu). NO se escribe un Dockerfile paralelo: dos
      # fuentes de verdad se desincronizan y el que clona no sabe cual manda.
      #
      # Las capas las calcula buildLayeredImage a partir del piso: no hay capa
      # escrita a mano ni paso intermedio opaco. El bundle entra por SYMLINK al
      # store, no por copia: lo que el contenedor ejecuta es el arbol medido.
      # ---------------------------------------------------------------------
      packages = enCadaSistema (pkgs:
        let
          piso = pkgs.buildEnv {
            name = "sfqed-paper-piso-gnu";
            paths = motorGnu pkgs;
            pathsToLink = [ "/bin" "/lib" "/share" ];
          };
          oci = pkgs.dockerTools.buildLayeredImage {
            name = "sfqed-paper-verificador";
            tag = "20261011";
            copyToRoot = piso;
            extraCommands = ''
              mkdir -p bin
              ln -sf ${pkgs.bashInteractive}/bin/bash bin/sh
              ln -sfn ${./bundle} bundle
            '';
            config = {
              # El gate corre como PID 1 a traves de su propio interprete: /bin/sh
              # es la RUTA ABSOLUTA del shebang, y dentro de la imagen no existe
              # el /bin/sh del anfitrion. No hay `|| true`, ni pipe, ni envoltorio
              # que colapse el codigo de retorno: 0 / 1 / 2 salen intactos.
              Entrypoint = [ "/bin/sh" "/bundle/verificar.sh" ];
              WorkingDir = "/bundle";
              # Locale NO se fija: M0 corre en UTF-8 y una imagen sin locale cae a
              # C. Es variable DECLARADA del pin, no medida en cada corrida; si la
              # primera corrida GNU diverge, el locale es sospechoso nombrado.
              # PYTHONHASHSEED tampoco se fija: fijarlo escondería una diferencia
              # real entre motores en vez de medirla.
              Env = [ "PATH=/bin" "MOTOR_ETIQUETA=GNU" "TZ=UTC" ];
              Labels = {
                "org.opencontainers.image.title" = "sfqed-paper · verificador";
                "org.opencontainers.image.version" = "20261011";
                "org.opencontainers.image.revision" =
                  builtins.toString (if self ? rev then self.rev else (if self ? dirtyRev then self.dirtyRev else "sin-rev"));
                "sfqed.motor" = "GNU";
                "sfqed.motor.referencia" = "M0 = Darwin 25.5.0 arm64 · bash 3.2.57(1) · python 3.14.7 · numpy 2.4.6 · shasum BSD";
                "sfqed.gate" = "bundle/verificar.sh (tricotomia intacta: 0 / 1 / 2)";
                "sfqed.universo" = "bundle/ = 26 archivos = 25 declarados en HASHES.sha256 + el manifiesto";
              };
            };
          };
        in { inherit oci; default = oci; });

      # ---------------------------------------------------------------------
      # INVOCACION CANONICA (declarada aqui para que viaje con el pin):
      #
      #   nix develop
      #   nix build .#oci && docker load < result
      #   docker run --rm -i --network none sfqed-paper-verificador:20261011 </dev/null
      #
      # El RC del contenedor ES el RC del verificador (0 / 1 / 2), sin traduccion.
      #
      # CORRECCION DECLARADA a la especificacion recibida: `docker run -T` NO
      # existe (unknown shorthand flag: 'T'); `-T` es bandera de `docker compose
      # run`. Lo que se busca --no pseudo-TTY-- es el DEFAULT de `docker run`: no
      # se pasa `-t` (`-t` fusiona stdout y stderr y puede alterar la tuberia).
      # `-i` + `</dev/null` deja el stdin cerrado y explicito. `--network none` es
      # anadido mio, declarado: un gate sin red no puede devolver verde por haber
      # consultado algo de afuera.
      #
      # PRE-REGISTRO FALSABLE de la primera corrida:
      #   .#gnu sobre el repo con .git   -> esperado VEREDICTO: VERDE · RC=0
      #   packages.oci (bundle sin .git) -> esperado VEREDICTO: VERDE PARCIAL · RC=0
      #     con N >= 1 bloques NO MEDIDOS (sin repo git la custodia no se audita)
      #   si .#gnu diera RC=2 -> sospechosos declarados: shasum ausente, gitleaks
      #     ausente. Eso es hallazgo del METRO, no del objeto: se declara y NO se
      #     tapa con un shim.
      # ---------------------------------------------------------------------
    };
}
