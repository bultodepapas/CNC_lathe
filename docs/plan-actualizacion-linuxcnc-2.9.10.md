# Plan de actualización del torno: LinuxCNC 2.9.7 → 2.9.10

**Documento:** runbook de cambio y validación  
**Máquina:** `torno_v3`  
**Fecha de preparación:** 2026-08-29  
**Estado:** preparación de sólo lectura en curso; instalación no ejecutada  
**Clasificación del cambio:** software de control de máquina, riesgo alto si se
ejecuta sin inhibición física y validación presencial

## 1. Resumen ejecutivo

Se propone actualizar como conjunto atómico los seis paquetes LinuxCNC
instalados (`linuxcnc-uspace`, `linuxcnc-uspace-dev` y documentación
de/en/es/fr) desde `1:2.9.7` hasta `1:2.9.10`, manteniendo:

- Debian 12 Bookworm;
- kernel `6.1.0-41-rt-amd64` PREEMPT_RT;
- firmware actual de la Mesa 7I76E/7I76EU;
- configuración activa `torno_v3`;
- QtVCP/QtDragon;
- parámetros mecánicos, escalas, límites, aceleraciones y homing actuales.

LinuxCNC 2.9.10 es la versión estable vigente. LinuxCNC 2.9.9 fue retirada y
no debe instalarse. LinuxCNC 2.10 continúa como prerelease y queda fuera de este
cambio.

El beneficio esperado es seguridad y robustez: parche RTAPI, corrección del
ciclo de torno `G71`, mejoras de QtDragon y de la previsualización, y semántica
correcta de los parámetros de offset de herramienta. No se espera una mejora
automática de precisión, latencia, acabado superficial, sincronismo de Z ni
roscado.

La actualización se tratará como un cambio aislado. La auditoría del 29 de
agosto de 2026 se hizo por SSH con comandos de sólo lectura mientras el torno
estaba en producción; no se ejecutó `apt-get update`, no se escribió en el CNC
y no se modificó HAL. La instalación sigue bloqueada hasta una parada
programada.

No se combinará con:

- conexión o activación de las alarmas `ALM` de Z1/Z2;
- limpieza de `tool.tbl`;
- cambio del homing tándem;
- instalación de VFD o encoder de husillo;
- actualización de Debian, kernel, firmware Mesa o Mesaflash;
- regeneración de la configuración mediante PNCconf.

## 2. Objetivos y no objetivos

### 2.1 Objetivos

1. Llevar LinuxCNC a `2.9.10` sin modificar intencionalmente la configuración
   funcional de la máquina.
2. Conservar un rollback probado hacia `2.9.7`.
3. Demostrar que QtDragon, HostMot2 Ethernet, E-stop, límites, homing, Z tándem,
   torreta y offsets mantienen el comportamiento anterior.
4. Registrar versiones, paquetes, hashes, logs y resultados de todas las
   pruebas.
5. Evitar movimiento inesperado mediante inhibición física y validación por
   etapas.

### 2.2 No objetivos

- Corregir la desincronización física de Z1/Z2.
- Convertir el husillo fijo en un husillo controlado por LinuxCNC.
- Habilitar `G95`, `G96`, `G33` o `G76` con garantías metrológicas.
- Recalibrar `STEP_SCALE`, velocidad, aceleración, `FERROR` o límites.
- Corregir deuda técnica existente en HAL/INI.
- Adoptar LinuxCNC 2.10, Debian 13 o un kernel PREEMPT_RT más reciente.
- Ejecutar pruebas de corte durante la ventana inicial de actualización.

## 3. Línea base confirmada

| Subsistema | Estado actual |
|---|---|
| LinuxCNC | `linuxcnc-uspace 2.9.7` |
| Sistema operativo | Debian 12.12 Bookworm |
| Tiempo real | `6.1.0-41-rt-amd64`, PREEMPT_RT |
| Interfaz | QtVCP `qtdragon`, modo torno, geometría XZ |
| Cinemática | `trivkins coordinates=XZZ kinstype=BOTH` |
| Juntas | 0 = X, 1 = Z1, 2 = Z2 |
| Movimiento | Mesa 7I76E/7I76EU, `hm2_eth`, `192.168.1.121` |
| Servo thread | 1 ms |
| Torreta | `carousel.0`, cuatro posiciones, `stepgen.00` |
| Husillo | Trifásico fijo, externo a LinuxCNC; `at-speed` forzado |
| Configuración activa | `/home/cnc/linuxcnc/configs/torno_v3/torno_v3.ini` |
| Administración | SSH/Tailscale; las pruebas físicas requieren operador local |

### 3.1 Evidencia de la auditoría remota de sólo lectura

Captura local más reciente:
`backups/20260829-112809-readonly-audit/remote-audit.json`, SHA-256
`82599a4fdb3145f060a9c4079317d18df776e8a792eeba5adbedc31ae44d3023`.
El directorio `backups/` está excluido de Git porque puede contener datos
operacionales. El auditor reproducible es `scripts/audit-cnc-readonly.py`.

| Hallazgo confirmado | Impacto en el cambio |
|---|---|
| Debian 12.12, kernel `6.1.0-41-rt-amd64`, Python 3.11.2 | Compatibles con el paquete Bookworm amd64 2.9.10; se congelan durante este cambio |
| Los seis paquetes LinuxCNC están en `1:2.9.7` y fueron instalados manualmente | Los seis se actualizan y revierten juntos; `linuxcnc-uspace-dev` exige versión exacta del paquete principal |
| APT conserva candidato 2.9.7 porque la caché está desactualizada | `apt-get update` y la simulación 2.9.10 quedan aplazados hasta la ventana de mantenimiento |
| Fuentes externas activas: QtPyVCP `develop`, EtherLab, Tailscale | Revisar rigurosamente la resolución APT; ningún paquete de esas fuentes entra al cambio |
| Configuración remota activa: 11 archivos operacionales comparables coinciden con los hashes locales | Buena línea base; repetir con LinuxCNC detenido porque `linuxcnc.var` es mutable en ejecución |
| QtDragon sólo tiene overrides locales `resources.py`/`.pyc`; no hay `.ui` ni handler locales | Las correcciones del handler upstream deberían aplicar; validar iconos y recursos locales |
| No se encontraron componentes `.comp`/`.so` personalizados | Riesgo bajo del cambio de contrato RTAPI, pero debe repetirse el inventario antes de instalar |
| Mesa: cero packet errors, cero fallos seriales, `io_error=FALSE`, watchdog inactivo | Línea base de aceptación HostMot2; no cambiar NIC, kernel ni firmware |
| Servo thread: periodo 1,000,000 ns; captura actual 698,552 ns; máximo histórico 1,030,982 ns | El máximo supera el periodo en 3.1 %. Es un riesgo previo, no atribuido a 2.9.10; exige gate de tiempo real en parada |
| Logs de kernel restringidos para el usuario SSH | El operador con `sudo` debe capturar `journalctl`/`dmesg` durante mantenimiento |
| Partición EFI al 84 %, raíz al 3 % | No instalar kernel en este cambio; confirmar que APT no lo proponga |
| No hay `.deb` LinuxCNC en la caché APT del CNC | El rollback offline debe existir antes de G3 |

Durante la captura LinuxCNC estaba habilitado, los tres joints estaban homed y
el torno llegó a estar en movimiento. Por ello no se hicieron pruebas de
latencia, ping a la Mesa, reinicios de métricas, escritura HAL ni consultas que
pudieran competir con el control en tiempo real.

Archivos de especial sensibilidad:

- `linuxcnc/configs/torno_v3/torno_v3.ini`;
- `linuxcnc/configs/torno_v3/torno_v3.hal`;
- `linuxcnc/configs/torno_v3/custom.hal`;
- `linuxcnc/configs/torno_v3/qtvcp_postgui.hal`;
- `linuxcnc/configs/torno_v3/tool.tbl`;
- `linuxcnc/configs/torno_v3/linuxcnc.var`;
- `linuxcnc/configs/torno_v3/qtdragon.pref`;
- `linuxcnc/configs/torno_v3/qtvcp/screens/qtdragon/resources.py`.

## 4. Cambios relevantes de 2.9.7 a 2.9.10

| Cambio upstream | Aplicabilidad | Validación requerida |
|---|---|---|
| Parche de escalamiento de privilegios en RTAPI | Alta para seguridad del host; no es una función de seguridad de máquina | Confirmar arranque de los componentes uspace y `hm2_eth` |
| Corrección de bucle infinito en `G71` | Alta si existen programas de desbaste `G71/G70` | Ejecutar un programa de regresión primero en simulación y después en dry-run |
| Actualizaciones de QtDragon y jogging incremental | Media/alta para operación manual | Probar todos los incrementos configurados y ambos sentidos de X/Z |
| Gremlin inicia con los códigos modales activos | Media; el INI fuerza `G21 G40 G90 G94 G97 G64` | Comparar vista previa con posición, unidades, WCS y offsets activos |
| `#5021`–`#5029` exponen posición absoluta de máquina | Potencial para futuras macros | No adoptar macros nuevas durante este cambio |
| `#5401`–`#5409` = offset almacenado; `#5081`–`#5089` = offset aplicado | Alta si existen macros/remaps de herramienta o palpado | Buscar su uso y probar offsets/Tn M6/G43/G49 |
| Mejoras HALShow/HALScope | Útil para diagnóstico | Abrir watchlist y capturar señales sin alterar parámetros |
| Detección PREEMPT_RT 6.12+ | No aplica al kernel 6.1 actual | Ninguna |
| Correcciones `hm2_modbus` | No aplican a `hm2_eth` sin Modbus | Ninguna |

### 4.1 Hallazgos de investigación que endurecen el plan

- La regresión real de `G38.2` en 2.9.9 motivó su retirada; el salto autorizado
  es directo 2.9.7 → 2.9.10. Se mantiene una prueba negativa: no usar palpado
  mientras `probe-in` no tenga fuente física confirmada.
- La corrección `G71` elimina un bucle infinito conocido, pero existe un issue
  distinto y anterior sobre geometrías `G71`; cada programa real debe validarse
  en preview, simulación y dry-run.
- No se encontró una regresión específica 2.9.10 de `hm2_eth`. Sí existen
  reportes históricos de latencia/red; por eso se conserva kernel, firmware,
  NIC y topología, y se compara contra los contadores Mesa de la línea base.
- Un `.ui` o handler QtDragon local puede ocultar el archivo del sistema tras
  una actualización. No ocurre en la captura actual, pero el `resources.py`
  local todavía requiere una prueba visual completa.
- El parche de seguridad RTAPI sanea nombres de módulos y exige que componentes
  uspace exporten el punto de salida esperado. No hay componentes compilados
  personalizados en la configuración capturada; cualquier aparición posterior
  es NO-GO hasta recompilarla/probarla con 2.9.10.

## 5. Principios de ejecución

1. **Nunca actualizar con una pieza, herramienta o persona en la zona de
   peligro.**
2. **La inhibición debe ser física.** E-stop lógico, `machine-off` o un pin HAL
   no sustituyen la desconexión de energía de drivers y husillo.
3. Debe haber un operador presencial autorizado durante toda prueba de E/S o
   movimiento. SSH no se utilizará para ordenar movimiento sin comunicación
   directa y confirmación del operador.
4. El husillo se mantendrá desconectado durante las pruebas iniciales. Debido a
   que `spindle-at-speed` está forzado, la GUI no puede demostrar que el husillo
   esté realmente detenido.
5. No se ejecutarán `M100`–`M104`: son scripts históricos incompatibles con el
   control `carousel` activo.
6. No se abrirá ni guardará la configuración con PNCconf. Los HAL contienen
   cambios manuales posteriores y PNCconf puede sobrescribirlos.
7. Cada gate debe quedar aprobado antes de continuar. Ante duda, comportamiento
   distinto o evidencia incompleta, se detiene el cambio y se hace rollback.
8. Mientras LinuxCNC esté activo no se ejecutarán `apt-get update`, pruebas de
   latencia, ping/flood a la Mesa, Mesaflash, reinicios de red ni escrituras HAL.
9. No se ejecutará `apt autoremove` durante preparación, upgrade o rollback,
   aunque APT muestre kernels/headers antiguos como candidatos.

## 6. Roles mínimos

| Rol | Responsabilidad |
|---|---|
| Responsable del cambio | Ejecuta comandos, registra evidencia y decide avance/rollback |
| Operador presencial | Inhibe energía, inspecciona la máquina y opera E-stop |
| Observador de seguridad | Vigila zona peligrosa y puede detener la prueba |

Una persona puede asumir los dos primeros roles sólo durante actividades sin
energía de potencia. Toda prueba con movimiento requiere al menos operador
presencial y comunicación continua.

## 7. Estrategia de gates

```text
G0  Congelar alcance y ventana
 |
G1  Inventario + respaldo + rollback disponible
 |
G2  Resolver candidato exacto 2.9.10 y simular APT
 |
G3  Instalar paquetes con potencia físicamente inhibida
 |
G4  Arranque y pruebas lógicas sin potencia
 |
G5  Pruebas físicas de E/S y movimiento reducido
 |
G6  Observación, cierre y conservación de evidencia
```

### 7.1 Estado real al cierre de esta preparación

| Gate | Estado 2026-08-29 | Evidencia / pendiente |
|---|---|---|
| G0 | **NO-GO temporal** | El torno está en producción; falta ventana con inhibición física y operador local |
| G1 | **Parcial** | Inventario SSH, hashes de configuración y 12 `.deb` verificados; faltan backup consistente con LinuxCNC detenido, segunda copia e imagen opcional |
| G2 | **Pendiente** | La caché APT aún ofrece 2.9.7; falta `apt-get update` y simulación exacta durante la parada |
| G3 | **Bloqueado** | No se instalará nada mientras LinuxCNC esté activo |
| G4 | **Pendiente** | Requiere 2.9.10 instalado y potencia de actuadores inhibida |
| G5 | **Pendiente presencial** | Requiere operador, zona despejada y pruebas P01–P14 |
| G6 | **Pendiente** | Sólo tras un ciclo representativo y observación |

El avance seguro ya implementado no equivale a aprobación: permite llegar a la
ventana con menos incertidumbre, pero ninguna descarga local ni lectura SSH
autoriza movimiento o instalación.

## 8. Gate G0: preparación y congelación

### 8.1 Condiciones de entrada

- Ventana sin producción y con tiempo suficiente para rollback.
- Consola local, teclado, monitor y acceso `sudo` disponibles.
- Operador conoce la ubicación del seccionador, contactores y E-stop.
- No hay pieza montada, programa en ejecución ni herramienta cerca del material.
- Se conoce cómo iniciar `torno_v3` desde el lanzador local.

### 8.2 Congelación del alcance

- Etiquetar o registrar el commit actual del repositorio.
- No editar INI, HAL, preferencias ni tabla de herramientas durante la ventana.
- No limpiar duplicados de `tool.tbl`.
- No activar `drafts/alarmas-z/`.
- No aceptar una actualización de distribución (`bookworm` → `trixie`).
- No actualizar firmware Mesa.

### 8.3 Go/no-go G0

**GO:** ventana, personal, consola local e inhibición física disponibles.  
**NO-GO:** sólo hay acceso remoto, hay producción pendiente o no se puede cortar
la energía del husillo y drivers independientemente del software.

## 9. Gate G1: inventario y respaldo

### 9.1 Captura de línea base

Ejecutar en el PC CNC y guardar la salida completa:

```bash
mkdir -p "$HOME/upgrade-linuxcnc-2.9.10/evidence"

date --iso-8601=seconds | tee "$HOME/upgrade-linuxcnc-2.9.10/evidence/date-before.txt"
uname -a | tee "$HOME/upgrade-linuxcnc-2.9.10/evidence/uname-before.txt"
cat /etc/os-release | tee "$HOME/upgrade-linuxcnc-2.9.10/evidence/os-release.txt"
linuxcnc_var LINUXCNCVERSION | tee "$HOME/upgrade-linuxcnc-2.9.10/evidence/linuxcnc-version-before.txt"
dpkg-query -W -f='${Package}|${Version}|${Architecture}|${Status}\n' \
  linuxcnc-uspace linuxcnc-uspace-dev \
  linuxcnc-doc-de linuxcnc-doc-en linuxcnc-doc-es linuxcnc-doc-fr \
  mesaflash linux-image-rt-amd64 \
  | tee "$HOME/upgrade-linuxcnc-2.9.10/evidence/controlled-packages-before.txt"
dpkg-query -W | tee "$HOME/upgrade-linuxcnc-2.9.10/evidence/packages-before.txt"
apt-mark showmanual | tee "$HOME/upgrade-linuxcnc-2.9.10/evidence/packages-manual-before.txt"
systemctl --failed | tee "$HOME/upgrade-linuxcnc-2.9.10/evidence/systemd-failed-before.txt"
df -h | tee "$HOME/upgrade-linuxcnc-2.9.10/evidence/disk-before.txt"
```

`linuxcnc --version` y `mesaflash --version` no son interfaces CLI válidas en
las versiones instaladas; se usa `linuxcnc_var` y el inventario de paquetes.

Confirmar específicamente:

```bash
dpkg-query -W 'linuxcnc*' 'mesaflash*'
dpkg --audit
```

`dpkg --audit` debe terminar sin incidencias.

### 9.2 Manifiesto de la configuración

Crear el manifiesto fuera del directorio configurado para no modificar su hash:

```bash
find "$HOME/linuxcnc" -type f -print0 \
  | sort -z \
  | xargs -0 sha256sum \
  > "$HOME/upgrade-linuxcnc-2.9.10/evidence/linuxcnc-before.sha256"
```

### 9.3 Respaldo de datos

Debe existir una copia nueva y verificable de:

- `/home/cnc/linuxcnc/` completo;
- lanzadores de escritorio usados para `torno_v3`;
- `/etc/apt/sources.list` y `/etc/apt/sources.list.d/`;
- `/etc/apt/preferences` y `/etc/apt/preferences.d/`;
- conffiles del paquete: `/etc/linuxcnc/rtapi.conf`,
  `/etc/X11/app-defaults/TkLinuxCNC` y
  `/etc/xdg/menus/applications-merged/CNC.menu`;
- inventario de paquetes;
- `tool.tbl`, `linuxcnc.var` y `qtdragon.pref` con LinuxCNC detenido;
- cualquier componente personalizado fuera de `/home/cnc/linuxcnc`.

Guardar permisos, propietarios y hashes de los conffiles antes de instalar. La
instalación debe detenerse si `dpkg --verify linuxcnc-uspace` muestra cambios
no explicados.

Ejemplo, después de cerrar LinuxCNC:

```bash
backup_stamp="$(date +%Y%m%d-%H%M%S)"
mkdir -p "$HOME/upgrade-linuxcnc-2.9.10/backups"

tar --acls --xattrs -C "$HOME" -czf \
  "$HOME/upgrade-linuxcnc-2.9.10/backups/linuxcnc-${backup_stamp}.tar.gz" \
  linuxcnc

sha256sum "$HOME/upgrade-linuxcnc-2.9.10/backups/linuxcnc-${backup_stamp}.tar.gz" \
  > "$HOME/upgrade-linuxcnc-2.9.10/backups/linuxcnc-${backup_stamp}.tar.gz.sha256"
```

Verificar la integridad y listar el contenido:

```bash
sha256sum -c "$HOME/upgrade-linuxcnc-2.9.10/backups/linuxcnc-${backup_stamp}.tar.gz.sha256"
tar -tzf "$HOME/upgrade-linuxcnc-2.9.10/backups/linuxcnc-${backup_stamp}.tar.gz" \
  | less
```

Copiar el respaldo y la evidencia a un segundo dispositivo o al repositorio de
ingeniería. Un respaldo que sólo existe en el disco que se va a modificar no es
suficiente.

### 9.4 Imagen del sistema

Para máxima recuperabilidad, crear una imagen de disco con la máquina apagada
mediante Clonezilla u otra herramienta de imagen sectorial. Si el sistema usa
LVM/Btrfs y ya existe un procedimiento probado de snapshots, puede utilizarse;
no se debe improvisar un esquema de snapshots durante esta ventana.

### 9.5 Artefactos obligatorios de rollback

Antes de instalar 2.9.10 deben estar descargados y accesibles sin internet:

- `linuxcnc-uspace`, `linuxcnc-uspace-dev` y `linuxcnc-doc-de/en/es/fr`
  2.9.7 del repositorio APT oficial Bookworm;
- dependencias exactas que APT indique que cambiarán;
- hashes o firma de los paquetes;
- respaldo verificado de `/home/cnc/linuxcnc`.

Conservar también los mismos seis paquetes 2.9.10. Los `.deb` 2.9.7 de GitHub
y del repositorio APT tienen el mismo número de versión pero hashes diferentes;
el rollback primario utiliza la variante APT que coincide con el canal
instalado. No mezclar variantes dentro de una misma transacción.

Los 12 artefactos requeridos ya están preparados localmente bajo
`backups/upgrade-packages/`. Verificarlos antes de transferir y nuevamente en
el CNC:

```powershell
pwsh -NoProfile -File scripts/verify-upgrade-packages.ps1
```

El verificador compara tamaño y SHA-256 con el índice oficial. La existencia
local no aprueba G1 hasta que haya una segunda copia y se haya probado que el
CNC puede acceder a ella durante la ventana.

### 9.6 Go/no-go G1

**GO:** dos copias verificadas, manifiesto de hashes y paquetes 2.9.7 de
rollback disponibles.  
**NO-GO:** no se puede restaurar 2.9.7 sin depender de que el repositorio remoto
siga disponible.

### 9.7 Gate específico de tiempo real previo al cambio

La captura activa mostró `servo-thread` con máximo histórico 1,030,982 ns para
un periodo de 1,000,000 ns. No diagnosticarlo mientras se mecaniza.

En una parada, antes de instalar:

1. Capturar `halcmd show thread` y logs con el CNC recién arrancado.
2. Con LinuxCNC cerrado, ejecutar la prueba oficial de latencia bajo una carga
   representativa; nunca ejecutar `latency-test` simultáneamente con LinuxCNC.
3. Reiniciar LinuxCNC sin potencia de actuadores y observar al menos 30 minutos
   de GUI, preview y E/S, capturando de nuevo los máximos del servo thread.
4. Si el máximo vuelve a superar 1 ms, aparecen `real-time delay`/watchdog o el
   margen se degrada, abrir un diagnóstico separado y mantener 2.9.7. No
   “resolver” este gate actualizando kernel, NIC o firmware dentro del upgrade.

Este dato es una línea base preexistente. Tras 2.9.10 se repite exactamente la
misma prueba y se compara, en vez de exigir que el upgrade corrija la latencia.

## 10. Gate G2: resolución y simulación de paquetes

### 10.1 Revisar fuentes APT

```bash
grep -R --line-number --no-messages \
  -E 'linuxcnc|bookworm|trixie|bullseye' \
  /etc/apt/sources.list /etc/apt/sources.list.d
```

Requisitos:

- distribución `bookworm`;
- repositorio LinuxCNC `2.9-uspace`;
- ninguna fuente destinada a `trixie` o a la rama de desarrollo;
- arquitectura `amd64`.

La auditoría encontró además repositorios QtPyVCP `develop`, EtherLab y
Tailscale. No se deshabilitan mientras hay producción. En la ventana, registrar
su estado y comprobar que la simulación no selecciona desde ellos ningún
paquete de la transacción. Si lo hace, NO-GO y revisar prioridades/fuentes antes
de continuar.

### 10.2 Actualizar metadatos, no paquetes

```bash
sudo apt-get update
apt-cache policy \
  linuxcnc-uspace linuxcnc-uspace-dev \
  linuxcnc-doc-de linuxcnc-doc-en linuxcnc-doc-es linuxcnc-doc-fr
```

La versión candidata debe ser `1:2.9.10` o el empaquetado equivalente que
identifique inequívocamente `2.9.10`.

**Bloqueo absoluto:** si aparece `2.9.9`, no instalar. Si sólo aparece `2.9.8`,
conservar 2.9.7 hasta resolver la fuente; no mezclar repositorios ni descargar
paquetes de sitios no oficiales.

### 10.3 Simular la actualización

```bash
sudo apt-get -s install \
  linuxcnc-uspace=1:2.9.10 \
  linuxcnc-uspace-dev=1:2.9.10 \
  linuxcnc-doc-de=1:2.9.10 \
  linuxcnc-doc-en=1:2.9.10 \
  linuxcnc-doc-es=1:2.9.10 \
  linuxcnc-doc-fr=1:2.9.10 \
  | tee "$HOME/upgrade-linuxcnc-2.9.10/evidence/apt-simulation.txt"
```

Adaptar el epoch sólo si `apt-cache policy` muestra otro valor oficial. Revisar
línea por línea la simulación.

La simulación no debe:

- eliminar `linuxcnc-uspace`;
- cambiar Debian 12 por Debian 13;
- sustituir PREEMPT_RT por un kernel genérico;
- instalar RTAI;
- eliminar QtVCP/PyQt;
- actualizar cientos de paquetes mediante `dist-upgrade`;
- cambiar la arquitectura;
- proponer 2.9.9.

También debe mantener los seis paquetes en la misma versión exacta y no debe
tomar dependencias de QtPyVCP `develop` ni EtherLab. Registrar `Inst`, `Conf`,
paquete origen y toda adición/eliminación. El movimiento de
`python3-poppler-qt5` de dependencia a sugerencia no autoriza su eliminación.

### 10.4 Descargar sin instalar

```bash
sudo apt-get --download-only install \
  linuxcnc-uspace=1:2.9.10 \
  linuxcnc-uspace-dev=1:2.9.10 \
  linuxcnc-doc-de=1:2.9.10 \
  linuxcnc-doc-en=1:2.9.10 \
  linuxcnc-doc-es=1:2.9.10 \
  linuxcnc-doc-fr=1:2.9.10
```

Registrar los `.deb` descargados y sus hashes. No usar paquetes de foros,
mirrors no oficiales ni builds de terceros.

### 10.5 Go/no-go G2

**GO:** candidato exacto 2.9.10, simulación limpia y paquetes descargados.  
**NO-GO:** cambios de kernel/OS inesperados, dependencias rotas o versión
candidata distinta.

## 11. Gate G3: instalación controlada

### 11.1 Estado físico requerido

Antes de ejecutar APT:

- LinuxCNC cerrado normalmente;
- husillo físicamente aislado;
- potencia de drivers X/Z1/Z2 y torreta inhibida;
- E-stop accionado;
- pieza y herramientas retiradas;
- operador frente a la máquina;
- consola local disponible aunque se use SSH como apoyo.

Confirmar que no quedan procesos activos:

```bash
pgrep -a -f 'linuxcnc|linuxcncsvr|milltask|rtapi|halrun|qtvcp'
```

No continuar mientras aparezca una sesión de control activa. Cerrar la
aplicación de forma normal; no automatizar un `kill -9`.

### 11.2 Instalar sólo los paquetes aprobados

```bash
sudo apt-get install \
  linuxcnc-uspace=1:2.9.10 \
  linuxcnc-uspace-dev=1:2.9.10 \
  linuxcnc-doc-de=1:2.9.10 \
  linuxcnc-doc-en=1:2.9.10 \
  linuxcnc-doc-es=1:2.9.10 \
  linuxcnc-doc-fr=1:2.9.10 \
  | tee "$HOME/upgrade-linuxcnc-2.9.10/evidence/apt-install.txt"
```

No ejecutar `apt full-upgrade`, `apt dist-upgrade` ni una actualización de
distribución dentro de esta intervención. Tampoco ejecutar `apt autoremove`:
la simulación 2.9.7 ya mostró kernels/headers antiguos como candidatos y su
retiro no pertenece a este cambio.

### 11.3 Verificación inmediata

```bash
linuxcnc_var LINUXCNCVERSION | tee "$HOME/upgrade-linuxcnc-2.9.10/evidence/linuxcnc-version-after.txt"
dpkg-query -W 'linuxcnc*' | tee "$HOME/upgrade-linuxcnc-2.9.10/evidence/linuxcnc-packages-after.txt"
dpkg --audit | tee "$HOME/upgrade-linuxcnc-2.9.10/evidence/dpkg-audit-after.txt"
dpkg --verify linuxcnc-uspace | tee "$HOME/upgrade-linuxcnc-2.9.10/evidence/dpkg-verify-after.txt"
```

Esperado: versión `2.9.10`, auditoría vacía y ninguna modificación dentro de
`/home/cnc/linuxcnc`.

Recalcular hashes:

```bash
find "$HOME/linuxcnc" -type f -print0 \
  | sort -z \
  | xargs -0 sha256sum \
  > "$HOME/upgrade-linuxcnc-2.9.10/evidence/linuxcnc-after-install.sha256"

diff -u \
  "$HOME/upgrade-linuxcnc-2.9.10/evidence/linuxcnc-before.sha256" \
  "$HOME/upgrade-linuxcnc-2.9.10/evidence/linuxcnc-after-install.sha256"
```

Cualquier diferencia requiere explicación. La actualización del paquete no
debe reescribir la configuración ubicada en el home del usuario.

## 12. Gate G4: validación sin potencia

### 12.1 Arranque supervisado

Iniciar desde la consola gráfica local usando el lanzador habitual
`torno_v3`. No iniciar por primera vez una GUI de máquina únicamente a través de
SSH.

Validar:

- no hay error de parsing INI;
- todos los HALFILE y POSTGUI_HALFILE cargan;
- `hm2_eth` encuentra `192.168.1.121`;
- QtDragon abre sin trazas Python ni recursos faltantes;
- la geometría sigue siendo XZ y aparecen tres joints;
- la torreta expone `carousel.0`;
- no hay error de pin renombrado o componente faltante;
- la máquina permanece deshabilitada.

Guardar logs de terminal y de LinuxCNC. Consultar además:

```bash
journalctl -b --priority=warning..alert --no-pager
dmesg --level=err,warn
```

Filtrar en una copia de la evidencia términos como:

```bash
journalctl -b --no-pager \
  | grep -Ei 'linuxcnc|rtapi|hostmot2|hm2|watchdog|realtime|latency|packet|error'
```

### 12.2 Inspección HAL de sólo lectura

Con LinuxCNC iniciado y la potencia inhibida:

```bash
halcmd show thread
halcmd show comp
halcmd show pin iocontrol.0
halcmd show pin motion
halcmd show pin carousel.0
halcmd show pin hm2_7i76e.0
```

Capturar al menos estos valores:

```bash
halcmd getp carousel.0.homed
halcmd getp carousel.0.ready
halcmd getp iocontrol.0.emc-enable-in
halcmd getp joint.0.amp-enable-out
halcmd getp joint.1.amp-enable-out
halcmd getp joint.2.amp-enable-out
halcmd getp spindle.0.at-speed
halcmd getp spindle.0.speed-in
```

No usar `setp` o `sets` durante la inspección. El objetivo es observar, no
forzar estados.

### 12.3 QtDragon y persistencia

Comprobar sin movimiento:

- preferencias cargadas desde `qtdragon.pref`;
- tabla de herramientas visible;
- herramienta/pocket actual coherente;
- unidades en milímetros;
- límites y DRO X/Z coherentes;
- botones de E-stop y machine-on reflejan el estado real;
- vista previa sin ejes Y o movimientos inesperados;
- no desaparecen iconos por el `resources.py` local;
- no se resetean silenciosamente preferencias.

No borrar `qtdragon.pref` como solución rápida. Si una preferencia es
incompatible, conservarla como evidencia y tratar su migración en un cambio
separado.

### 12.4 Prueba del intérprete y offsets

Buscar antes de ejecutar programas:

```bash
grep -R --line-number --include='*.ngc' --include='*.py' --include='M*' \
  -E '#50(8[1-9]|2[1-9])|#540[1-9]|G3[348]|G4[39]|G7[01]|G9[4567]' \
  "$HOME/linuxcnc"
```

Revisar manualmente cualquier uso de:

- `#5081`–`#5089`;
- `#5401`–`#5409`;
- `G38.x`;
- `G43`, `G43.1`, `G43.2`, `G49`;
- `G70`, `G71`;
- `G95`, `G96`, `G97`;
- `G33`, `G76`.

La configuración capturada contiene una señal `probe-in` sin fuente física
visible. No probar ciclos `G38.x` hasta confirmar y verificar el palpador.

### 12.5 Programa mínimo de dry-run

Crear fuera de la configuración productiva un programa de validación que no
encienda husillo, refrigerante ni torreta. Debe probar únicamente parsing,
modos, preview y movimientos dentro de una envolvente reducida y conocida. El
programa debe ser revisado por dos personas antes de ejecutarse.

No usar las macros históricas `M100`–`M104`.

### 12.6 Go/no-go G4

**GO:** arranque limpio, HAL completo, interfaz coherente, configuración sin
cambios y dry-run aprobado.  
**NO-GO:** excepción Python, pin HAL faltante, Mesa inestable, offsets distintos,
tool table alterada, preview incoherente o cualquier intento de habilitación
inesperada.

## 13. Gate G5: commissioning físico

Las siguientes pruebas se realizan una por una, con velocidades reducidas,
zona despejada y capacidad inmediata de retirar energía.

### 13.1 Matriz de pruebas

| ID | Prueba | Método | Criterio de aceptación |
|---|---|---|---|
| P01 | E-stop físico | Accionar/liberar observando entrada Mesa 08 y `emc-enable-in` | La habilitación cae inmediatamente y no se recupera sola |
| P02 | Machine enable | Habilitar sin ordenar movimiento | Ningún eje o torreta se mueve al habilitar |
| P03 | Límites X | Accionar cada switch manualmente | Pin y GUI cambian con polaridad correcta |
| P04 | Home X | Buscar home a velocidad reducida | Secuencia, dirección y posición final iguales a la línea base |
| P05 | Límites Z | Accionar switches compartidos | Ambos joints reflejan el estado esperado |
| P06 | Home Z tándem | Observar Z1/Z2 y tener E-stop preparado | Ambos motores arrancan/paran juntos, sin torsión ni descuadre visible |
| P07 | Jog X/Z continuo | Recorrido mínimo en ambos sentidos | Dirección, parada y DRO correctos |
| P08 | Jog incremental | `.005` a `5 mm`, empezando por el menor | Un comando produce exactamente un incremento y se detiene |
| P09 | Límites suaves | Aproximación sin alcanzar límite físico | QtDragon/LinuxCNC impiden exceder el rango |
| P10 | Torreta T1–T4 | Sin herramienta y husillo aislado | Cada pocket se indexa, bloquea y declara `ready` una sola vez |
| P11 | Offsets | Cargar cada herramienta conocida sin cortar | X/Z y orientación coinciden con registro previo |
| P12 | Abort/pausa | Durante un movimiento corto y lento | Movimiento se detiene de forma controlada |
| P13 | Reinicio | Cerrar y abrir LinuxCNC | Estado persistente y herramienta actual coherentes |
| P14 | HostMot2 | Observar logs durante todas las pruebas | Sin watchdog, packet error ni real-time delay nuevo |

### 13.2 Restricciones específicas

- Empezar con el incremento mínimo y velocidad no superior al 10 % de la
  habitual.
- No validar `MAX_LINEAR_VELOCITY = 100 mm/s` en esta ventana.
- No hacer homing Z si la geometría física o los switches no han sido
  inspeccionados presencialmente.
- Debido a que Z1/Z2 no reportan actualmente `ALM`, detener ante cualquier
  diferencia de sonido, vibración o movimiento.
- La torreta se prueba sin herramienta y con el husillo físicamente detenido,
  aunque `TOOL_CHANGE_WITH_SPINDLE_ON = 1` permita el cambio lógicamente.
- No probar `G95/G96/G33/G76`: falta realimentación física de husillo.

### 13.3 Prueba de regresión G71

Si se usa `G71` en producción:

1. Copiar un programa real y anonimizarlo para prueba.
2. Revisar límites X/Z y retirar M-codes de husillo/refrigerante.
3. Ejecutarlo primero en una configuración simulada de LinuxCNC 2.9.10.
4. Verificar que la vista previa termina y que el ciclo no entra en bucle.
5. Ejecutar dry-run en la máquina, sin pieza y con husillo aislado.
6. Comparar trayectoria y tiempo con el registro 2.9.7.
7. Autorizar corte sólo en una ventana posterior.

### 13.4 Go/no-go G5

**GO:** todas las pruebas aplicables aprobadas y firmadas.  
**NO-GO:** movimiento inesperado, homing distinto, pérdida de una junta Z,
torreta sin bloqueo, tool offset distinto o error HostMot2.

## 14. Gate G6: observación y cierre

### 14.1 Periodo de observación

Durante las primeras horas de producción:

- comenzar con una pieza no crítica y programa conocido;
- usar velocidades y overrides conservadores;
- observar logs HostMot2/RTAPI;
- revisar cada cambio de herramienta;
- evitar editar offsets mientras se evalúa la estabilidad;
- mantener disponible el paquete 2.9.7 y el respaldo.

No declarar estable la actualización sólo porque LinuxCNC abre. Debe completarse
como mínimo un ciclo representativo sin alarmas, errores de tiempo real,
descuadre Z ni diferencias de offsets.

### 14.2 Evidencia de cierre

Conservar:

- versiones antes/después;
- simulación y log de APT;
- hashes antes/después;
- salida de `dpkg --audit`;
- logs de arranque y kernel;
- capturas HAL relevantes;
- matriz P01–P14 firmada;
- desviaciones encontradas;
- decisión final de aceptación o rollback.

Copiar la evidencia a `docs/evidence/upgrade-linuxcnc-2.9.10/` sólo después de
revisarla y eliminar secretos, direcciones innecesarias o datos personales.

## 15. Plan de rollback

### 15.1 Disparadores

Rollback inmediato ante cualquiera de estas condiciones:

- LinuxCNC o QtDragon no arrancan limpiamente;
- faltan componentes o pines HAL;
- aparecen watchdog, packet errors o real-time delays nuevos;
- la herramienta cargada, offsets o `tool.tbl` cambian inesperadamente;
- homing, límites o sentidos difieren de 2.9.7;
- la torreta no alcanza `homed/ready` de forma determinista;
- se ordena movimiento no solicitado;
- no puede demostrarse que la configuración permaneció intacta;
- una prueba crítica P01–P14 falla.

### 15.2 Procedimiento

1. Accionar E-stop y retirar físicamente energía de husillo y drivers.
2. Cerrar LinuxCNC de forma normal.
3. Guardar logs y evidencia del fallo antes de modificar el sistema.
4. Reinstalar los paquetes 2.9.7 previamente descargados.
5. Restaurar `/home/cnc/linuxcnc` sólo si los hashes demuestran cambios o si la
   investigación lo requiere.
6. Reiniciar el PC si se sustituyeron librerías cargadas o RTAPI quedó en estado
   dudoso.
7. Repetir las pruebas G4 y G5 con 2.9.7 antes de devolver la máquina a servicio.

Si la versión 2.9.7 sigue disponible en las fuentes aprobadas:

```bash
sudo apt-get install --allow-downgrades \
  linuxcnc-uspace=1:2.9.7 \
  linuxcnc-uspace-dev=1:2.9.7 \
  linuxcnc-doc-de=1:2.9.7 \
  linuxcnc-doc-en=1:2.9.7 \
  linuxcnc-doc-es=1:2.9.7 \
  linuxcnc-doc-fr=1:2.9.7
```

Si no está en APT, instalar los `.deb` oficiales previamente conservados usando
APT con rutas locales para que resuelva dependencias:

```bash
sudo apt-get install --allow-downgrades \
  ./linuxcnc-uspace_2.9.7_amd64.deb \
  ./linuxcnc-uspace-dev_2.9.7_amd64.deb \
  ./linuxcnc-doc-de_2.9.7_all.deb \
  ./linuxcnc-doc-en_2.9.7_all.deb \
  ./linuxcnc-doc-es_2.9.7_all.deb \
  ./linuxcnc-doc-fr_2.9.7_all.deb
```

Los nombres reales pueden incluir epoch o revisión de empaquetado; deben tomarse
de los archivos descargados, no asumirse. No usar `dpkg --force-*`.

### 15.3 Restauración de configuración

Antes de restaurar, conservar la copia fallida para análisis. Extraer el backup
en un directorio temporal, comparar y restaurar únicamente el árbol validado.
No reemplazar recursivamente `/home/cnc` ni borrar el directorio actual sin una
copia recuperable.

## 16. Registro de riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---:|---:|---|
| Instalar 2.9.9 retirada | Baja si se verifica candidato | Alto | Pin exacto a 2.9.10 y bloqueo en G2 |
| Cambio inesperado de offsets | Media | Alto | Backup `tool.tbl`, búsqueda de variables, pruebas P10/P11 |
| Preferencias/recursos QtDragon incompatibles | Media | Medio | Conservar prefs/resources y probar sin borrar archivos |
| Dependencias APT cambian kernel/OS | Baja | Alto | Simulación previa; prohibir `dist-upgrade` |
| Falla de arranque HAL | Baja/media | Alto | Potencia inhibida, logs y paquete 2.9.7 disponible |
| Movimiento inesperado al habilitar | Baja | Crítico | Corte físico, zona despejada, prueba P02 |
| Descuadre de Z tándem durante prueba | Media por diseño actual | Crítico | Velocidad reducida, observación directa, E-stop, no mezclar cambio ALM |
| Torreta cambia con husillo externo activo | Media | Crítico | Aislar físicamente husillo, retirar herramientas |
| Problema de red Mesa confundido con upgrade | Baja/media | Alto | Línea base de red/logs; no cambiar firmware ni NIC |
| Rollback depende de internet | Media si no se prepara | Alto | Pre-descargar paquetes y segunda copia verificada |
| Deadline servo preexistente (>1 ms histórico) | Media hasta medir en parada | Alto | Gate 9.7 antes/después, misma carga y kernel; NO-GO si se reproduce |
| Mezcla de versiones main/dev/docs | Media sin pin exacto | Alto | Transacción atómica de seis paquetes y verificación `dpkg-query` |
| Dependencias seleccionadas desde repos externos | Baja/media | Alto | Revisar origen en simulación; QtPyVCP develop/EtherLab fuera de alcance |
| Rollback 2.9.7 con rebuild diferente | Media | Medio/alto | Usar los seis `.deb` exactos del índice APT y verificar SHA-256 |

## 17. Criterios finales de aceptación

La actualización sólo se considera aceptada cuando:

- `linuxcnc_var LINUXCNCVERSION` devuelve 2.9.10 y los seis paquetes reportan
  exactamente `1:2.9.10`;
- Debian y el kernel PREEMPT_RT permanecen en la línea aprobada;
- la configuración activa conserva los hashes esperados;
- QtDragon inicia sin errores y mantiene geometría/unidades/preferencias;
- HostMot2 se conecta sin errores nuevos;
- E-stop físico inhibe la máquina correctamente;
- X, Z1 y Z2 conservan sentidos, límites y homing;
- el jogging continuo e incremental funciona de forma determinista;
- la torreta completa T1–T4 y confirma `ready`;
- tabla y offsets de herramientas no cambian silenciosamente;
- programas representativos terminan preview/dry-run;
- no aparecen regresiones durante el periodo de observación;
- la prueba de tiempo real posterior no empeora la línea base aprobada;
- el rollback sigue disponible y verificado.

## 18. Mejoras posteriores, como cambios independientes

Prioridad recomendada después de estabilizar 2.9.10:

1. Conectar `ALM` individual de HBS86H Z1 y Z2 a entradas Mesa y validar la
   parada conjunta.
2. Diseñar una cadena eléctrica de seguridad independiente de LinuxCNC.
3. Instalar supervisión real del husillo; idealmente VFD más encoder.
4. Revisar homing tándem y posibilidad de sensores independientes para Z1/Z2.
5. Calibrar `STEP_SCALE` con comparador y documentar la derivación mecánica.
6. Reducir `FERROR/MIN_FERROR` sólo después de disponer de realimentación y
   pruebas que justifiquen nuevos límites.
7. Limpiar `tool.tbl` con LinuxCNC detenido, backup y prueba específica.
8. Retirar o archivar definitivamente `M100`–`M104` tras reconciliar la lógica
   histórica de torreta.

Estas mejoras tienen mayor efecto sobre seguridad, capacidad y calidad que el
cambio de versión por sí solo, pero no deben mezclarse con el upgrade porque
harían ambiguo el origen de cualquier regresión.

## 19. Checklist operativo

### Antes

- [ ] Ventana aprobada y producción detenida.
- [ ] Operador presencial y observador disponibles.
- [ ] Pieza y herramientas retiradas.
- [ ] Husillo y drivers físicamente inhibidos.
- [ ] Inventario de versiones y paquetes guardado.
- [ ] Backup verificado en dos ubicaciones.
- [ ] Paquetes 2.9.7 de rollback disponibles offline.
- [ ] Los seis paquetes 2.9.7 APT y seis 2.9.10 pasan
      `scripts/verify-upgrade-packages.ps1`.
- [ ] Candidato APT exacto 2.9.10.
- [ ] Simulación APT revisada y aprobada.
- [ ] Gate de tiempo real previo ejecutado en parada; resultado aceptado.
- [ ] Ningún cambio de Debian/kernel/firmware/configuración incluido.

### Durante

- [ ] LinuxCNC cerrado antes de instalar.
- [ ] Log APT capturado.
- [ ] Versión 2.9.10 confirmada.
- [ ] Main/dev/docs de/en/es/fr están todos en `1:2.9.10`.
- [ ] `dpkg --audit` limpio.
- [ ] Hashes de configuración comparados.
- [ ] Arranque inicial con potencia inhibida.
- [ ] Logs RTAPI/HostMot2 revisados.
- [ ] QtDragon, tabla y offsets verificados.
- [ ] Gates G3 y G4 firmados.

### Después

- [ ] Pruebas P01–P14 ejecutadas y registradas.
- [ ] Programa `G71` probado si aplica.
- [ ] Primer ciclo productivo supervisado.
- [ ] Comparación de tiempo real antes/después aprobada.
- [ ] Evidencia copiada y revisada.
- [ ] Desviaciones documentadas.
- [ ] Decisión aceptar/rollback firmada.
- [ ] Backups y paquetes de rollback conservados.

## 20. Fuentes oficiales

- [LinuxCNC 2.9.10 released](https://linuxcnc.org/2026/07/09/LinuxCNC-2.9.10/)
- [LinuxCNC 2.9.9 withdrawn](https://linuxcnc.org/2026/07/03/2.9.9-Withdrawn/)
- [Updating LinuxCNC](https://www.linuxcnc.org/docs/stable/html/getting-started/updating-linuxcnc.html)
- [LinuxCNC downloads](https://linuxcnc.org/downloads/)
- [LinuxCNC 2.9.10 release assets](https://github.com/LinuxCNC/linuxcnc/releases/tag/v2.9.10)
- [Índice oficial APT Bookworm 2.9-uspace](https://linuxcnc.org/dists/bookworm/2.9-uspace/binary-amd64/Packages)
- [Changelog completo de la rama 2.9](https://github.com/LinuxCNC/linuxcnc/blob/2.9/debian/changelog)
- [Corrección del bucle infinito G71](https://github.com/LinuxCNC/linuxcnc/pull/3790)
- [Issue G71 distinto que sigue abierto](https://github.com/LinuxCNC/linuxcnc/issues/2844)
- [Regresión G38 de 2.9.9](https://github.com/LinuxCNC/linuxcnc/issues/4216)
- [Discusión de usuario sobre G38.2 en 2.9.9](https://forum.linuxcnc.org/38-general-linuxcnc-questions/58927-g38-2-weird-behaviour)
- [Cambio QtDragon de jogging incremental](https://github.com/LinuxCNC/linuxcnc/commit/f0e353d90385e37a3103fdb6f4768798b4bf4be2)
- [Issue histórico de latencia hm2_eth](https://github.com/LinuxCNC/linuxcnc/issues/2281)
- [Documentación HostMot2 Ethernet](https://linuxcnc.org/docs/stable/html/man/man9/hm2_eth.9.html)
- [Prueba de latencia LinuxCNC](https://linuxcnc.org/docs/stable/html/install/latency-test.html)
- [Parámetros del intérprete y offsets](https://www.linuxcnc.org/docs/2.9/html/gcode/overview.html)
- [Documentación estable y prerelease](https://linuxcnc.org/documents/)
- [Ciclo de vida de Debian](https://www.debian.org/releases/)

La investigación se ejecutó con más de cinco búsquedas independientes:
releases/changelog, retiro 2.9.9, empaquetado Bookworm, G38, G71, QtDragon,
offsets, RTAPI, compatibilidad Mesa/hm2_eth y experiencias de actualización en
el foro. Las decisiones de versión y hashes se apoyan en fuentes oficiales; los
foros se usan para descubrir escenarios de regresión, no como fuente de
paquetes.

## 21. Manifiesto mínimo de paquetes preparado

Los hashes 2.9.10 coinciden entre los assets oficiales de GitHub y el índice
APT Bookworm. Para 2.9.7 se conservan específicamente los archivos del índice
APT, que difieren de los rebuilds publicados en GitHub. El archivo genérico
`SHA256SUMS.txt` de la página de descargas estaba desactualizado durante la
investigación; no debe usarse como única prueba. La autoridad operativa será la
metadata APT firmada y/o el digest individual del release oficial.

| Versión/canal | Paquete | Bytes | SHA-256 |
|---|---|---:|---|
| 2.9.10 oficial | `linuxcnc-uspace` | 25,665,664 | `09c8d93ed6ddb197a57695e473a7fb6d930fd17cffb77d8f0fa24f2a79b561b2` |
| 2.9.10 oficial | `linuxcnc-uspace-dev` | 276,380 | `cd6e609d04f973ab402dd30b09186136beb68807d46f5628bdbf03cbfa56d8ae` |
| 2.9.10 oficial | `linuxcnc-doc-de` | 26,639,908 | `281a43e355df78c063f4045e4192aa42fe2dcb4c4106dcd627a77945ace2ccaa` |
| 2.9.10 oficial | `linuxcnc-doc-en` | 27,224,432 | `8e729dec3dfdc0df4f64f10087ab7b2edf7d6e0aeff8b44ffa9cc0573e55b27d` |
| 2.9.10 oficial | `linuxcnc-doc-es` | 26,369,832 | `01a08eae108578903eea8f8990afa3089117b5620e8e05f7be4a708342aba33c` |
| 2.9.10 oficial | `linuxcnc-doc-fr` | 26,287,408 | `633969ddee40aabd371c3547c03f5eb36d3ee99008796d2a8926c675453a1982` |
| 2.9.7 APT rollback | `linuxcnc-uspace` | 25,672,688 | `db2528514b986ca12c194f6c171a081124930d7df0ea87017ac10cc4ce12d1c2` |
| 2.9.7 APT rollback | `linuxcnc-uspace-dev` | 273,812 | `3083df1ef53a8d91acf89762d67831a121f7ff183e385c637b8e5f4d04fd4dc1` |
| 2.9.7 APT rollback | `linuxcnc-doc-de` | 26,418,960 | `f371cfd3cd1a65155fd1a0292755cc565aa004b8bc3f124464988a11a12960a0` |
| 2.9.7 APT rollback | `linuxcnc-doc-en` | 26,995,856 | `0600cb3cfb83105810a8e02d3fe3472291ff4cb2f0362481d0030453eb22ebf2` |
| 2.9.7 APT rollback | `linuxcnc-doc-es` | 26,143,948 | `ed00d12c0a2ea49b15bc483df95eee681bd3119c4ee1ea25fbe0df44230d10d0` |
| 2.9.7 APT rollback | `linuxcnc-doc-fr` | 26,064,672 | `37cd3df7829271412f74e31997f53c7104bdb5dda43322f630e9a19fec43b563` |

## 22. Aprobación

| Gate | Responsable | Fecha/hora | Resultado | Evidencia/observaciones |
|---|---|---|---|---|
| G0 Preparación |  |  | GO / NO-GO |  |
| G1 Respaldo |  |  | GO / NO-GO |  |
| G2 Paquetes |  |  | GO / NO-GO |  |
| G3 Instalación |  |  | GO / NO-GO |  |
| G4 Sin potencia |  |  | GO / NO-GO |  |
| G5 Commissioning |  |  | GO / NO-GO |  |
| G6 Cierre |  |  | ACEPTADO / ROLLBACK |  |
