# Auditoría inicial de `torno_v3`

Fecha de revisión: 2026-08-29. La primera revisión se hizo sobre archivos locales
desactualizados; después se contrastó por SSH con la configuración activa y el
HAL en ejecución. No se ordenó movimiento ni se modificó la máquina remota.

## Configuración observada

| Elemento | Valor observado |
|---|---|
| LinuxCNC | 2.9.7 uspace sobre Debian 12.12 PREEMPT_RT |
| Interfaz | QtVCP `qtdragon`, modo torno, geometría XZ |
| Cinemática | `trivkins coordinates=XZZ kinstype=BOTH` |
| Juntas | 0 = X, 1 = Z, 2 = segundo motor Z |
| Control de movimiento | Mesa `hm2_7i76e.0`, Ethernet `192.168.1.121` |
| Periodo servo | 1 ms |
| Generadores de pasos | 4 disponibles; 3 usados (`03` X, `01` Z, `02` Z2) |
| Husillo | PID declarado; sin enlace físico visible en esta captura |
| Torreta | Hardware de cuatro posiciones; control HAL no implementado en la captura |

## Estado de subsistemas críticos

### Cadena de parada de emergencia

La captura inicial sólo tenía un puente lógico. La configuración activa carga
`and2.0`: combina `iocontrol.0.user-enable-out` con la entrada física Mesa 08 y
entrega `estop-chain-ok` a `iocontrol.0.emc-enable-in`. En la consulta remota las
tres señales estaban verdaderas. Esto confirma el cableado HAL, no que exista un
relé de seguridad independiente ni que el botón elimine energía peligrosa; esa
prueba física sigue siendo obligatoria.

### Husillo

Confirmado por el propietario: actualmente es un motor trifásico de velocidad
fija y se opera fuera de LinuxCNC. Por eso `spindle-at-speed` se fuerza a
verdadero y no hay salida de velocidad ni realimentación RPM. Es una decisión
deliberada para esta etapa, no un fallo pendiente. La limitación conocida es que
LinuxCNC no puede confirmar si el motor está realmente encendido o detenido; si
más adelante se instala contactor supervisado o variador, deberá añadirse el
interlock correspondiente.

### Cambio de herramienta y torreta

La configuración activa carga `carousel.0`, usa `stepgen.00` y el sensor Hall de
la entrada Mesa 01. En ejecución se observó `carousel.0.homed = TRUE`,
`carousel.0.ready = TRUE` y posición actual 2; `ready` confirma el cambio a
`iocontrol.0.tool-changed`. Esto confirma el funcionamiento lógico observado,
pero faltan pruebas mecánicas del bloqueo y de las cuatro posiciones.

### Captura incompleta

Resuelto por la copia remota: existen `qtvcp_postgui.hal` y `qtdragon.pref`. El
postgui desactiva el cambio manual porque la confirmación procede de
`carousel.0.ready`.

## Puntos de ingeniería que requieren confirmación

1. Los HBS86H cierran su lazo internamente con el encoder del motor, pero
   LinuxCNC recibe como posición la realimentación del propio `stepgen`. Por
   tanto, desde LinuxCNC esta captura se comporta como step/dir sin medición de
   posición mecánica real ni detección directa del error del driver.
2. Z y Z2 comparten home y límites. Ambos usan `HOME_SEQUENCE = 2`; en una
   estructura tándem debe verificarse si el movimiento final necesita secuencia
   negativa sincronizada para evitar descuadre del puente.
3. Z usa `HOME_OFFSET = -20`, mientras el límite suave mínimo es `-10` y el
   destino `HOME` es `0`. Verificar posiciones físicas y recorrido antes de
   intentar homing.
4. `HOME_IGNORE_LIMITS = NO` debe contrastarse con el cableado real si un mismo
   interruptor actúa como home y límite.
5. La configuración activa unificó pantalla, trayectoria, eje Z y juntas Z/Z2
   en 100 mm/s; X permanece limitado a 50 mm/s. Aun así, 100 mm/s debe validarse
   mecánicamente antes de tomarlo como velocidad segura.
6. `FERROR = 10 mm` y `MIN_FERROR = 1 mm` son tolerancias muy amplias para una
   máquina con husillos de bolas. Como la realimentación proviene del stepgen,
   tampoco equivalen al error real del motor.
7. Confirmar experimentalmente `STEP_SCALE`: X = `-300` pasos/mm; Z y Z2 =
   `317.5` pasos/mm. Deben derivarse de pasos por vuelta, micropasos, relación y
   paso de husillo, y luego validarse con comparador.
8. Los comandos MDI incluyen Y (`X0 Y0`) aunque la cinemática sólo declara XZZ.
   Deben probarse o eliminarse tras recuperar la configuración real.
9. La conexión de límite negativo Z aparece duplicada. Repetir un enlace al
   mismo pin y señal puede ser aceptado por HAL, pero conviene eliminar el ruido
   sólo después de confirmar que no oculta una edición incompleta.
10. `tool.tbl` activo contiene numerosas repeticiones de `T9901` y `T19901`,
    aparentemente acumuladas por el manejo de desgaste de QtDragon. La máquina
    arranca con ellas, pero se requiere una limpieza controlada con LinuxCNC
    detenido y respaldo previo.
11. M100–M104 son ejecutables históricos de torreta que escriben señales
    `turret-search-speed`, `turret-home-mode` y `turret-index-pos`; esas señales
    no existen en el HAL `carousel` actual. Se conservaron como evidencia, pero
    no deben ejecutarse hasta reconciliar o retirar ese mecanismo anterior.

## Datos faltantes a recoger por SSH

- Versión exacta de LinuxCNC y paquetes instalados.
- Árbol completo de `/home/cnc/linuxcnc`, incluidos `nc_files` y preferencias.
- Configuración seleccionada por el lanzador/escritorio.
- Todos los HAL/INI y componentes personalizados (`.comp`, Python, ClassicLadder).
- Salidas de `halcmd show`, `mesaflash`, interfaces de red y latencia en tiempo real.
- Modelo/firmware exacto de Mesa y asignación de conectores/pines.
- Esquemas eléctricos: E-stop, límites, home, VFD/husillo, torreta y enables.
- Copia de tabla de herramientas y parámetros persistentes con LinuxCNC detenido.

## Criterio para una primera prueba

No debe habilitarse movimiento hasta contar con copia recuperable, esquema de
E/S, cadena física de E-stop probada y correspondencia entre cada pin HAL y el
borne real. La primera carga debe hacerse con el husillo y potencia de drivers
inhibidos, observando HAL; después se habilita un subsistema a la vez y con
límites de velocidad reducidos.
