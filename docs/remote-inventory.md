# Inventario remoto confirmado

Captura realizada por SSH el 2026-08-29, sin escribir en la máquina. El respaldo
completo quedó en `backups/20260829-094345-cnc/` y contiene 48 archivos, 11.84 MB
y un manifiesto SHA-256. La carpeta `backups/` no se versiona.

## Sistema

| Dato | Valor |
|---|---|
| Host | `cnc` / `cnc.taila1b901.ts.net` |
| Usuario | `cnc` |
| Distribución | Debian 12.12 |
| Kernel | `6.1.0-41-rt-amd64`, PREEMPT_RT |
| LinuxCNC | `linuxcnc-uspace 2.9.7` |
| Mesaflash | 3.4.9 |

## Configuración realmente activa

Los procesos `linuxcnc`, `linuxcncsvr`, `io`, `halui`, `milltask` y QtVCP
apuntaban todos a:

```text
/home/cnc/linuxcnc/configs/torno_v3/torno_v3.ini
```

El lanzador `/home/cnc/Escritorio/torno_v3.desktop` apunta a la misma ruta. Hay
otro lanzador y directorio llamado `my_LinuxCNC_machine`, pero no estaba en uso y
no se copió al árbol operativo del repositorio.

## Red

| Interfaz | Función | Dirección |
|---|---|---|
| `eno1` | Enlace dedicado Mesa | PC `192.168.1.1/24`; ruta a Mesa `192.168.1.121` |
| `enxc8a362ca2b22` | Red general | `192.168.110.173/24` |
| `tailscale0` | Administración remota | `100.87.222.75/32` |

Esta separación evita que el tráfico general dependa de la interfaz de tiempo
real usada para HostMot2.

## HAL observado en ejecución

- `carousel.0` cargado, homed y ready; se observó la posición de bolsillo 2.
- `tool-change-confirmed` provenía de `carousel.0.ready`.
- `ext-estop-ok` provenía de la entrada Mesa 08 y se combinaba mediante `and2.0`.
- El husillo tenía orden lógica de 500 RPM, realimentación de 0 RPM y
  `spindle-at-speed = TRUE`. El propietario confirmó que actualmente es un motor
  trifásico de velocidad fija, operado fuera de LinuxCNC; se registra como una
  limitación conocida, no como un fallo de la configuración actual.

## Selección copiada al árbol operativo

- Archivos activos INI/HAL, tabla de herramientas, variables y preferencias.
- `qtvcp/screens/qtdragon/resources.py`, correspondiente a la pantalla activa.
- M100–M104, conservando el requisito remoto de modo ejecutable `0755`.
- Fuente PNCconf `torno_v3.pncconf`.

Quedaron únicamente en el respaldo completo: `my_LinuxCNC_machine`, la carpeta
`respaldo original`, `qtdragon_hd`, archivos `.bak`, `__pycache__` y `.pyc`.
