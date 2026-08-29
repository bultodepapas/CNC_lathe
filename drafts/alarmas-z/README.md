# Borrador LinuxCNC — alarmas Z1/Z2

## Estado

Preparado, **no activo**. No se modifico la configuracion remota ni se agrego
`z_drive_faults.hal` al INI operativo.

## Archivos de la futura actualizacion

1. Copiar `linuxcnc/configs/torno_v3/z_drive_faults.hal` junto al INI.
2. Aplicar `torno_v3.ini.patch`, que agrega una sola linea:

   ```ini
   HALFILE = z_drive_faults.hal
   ```

No se requieren cambios en los bloques `[JOINT_1]` o `[JOINT_2]` del INI ni en
el HAL principal generado por PNCconf.

El OR de alarmas se inserta en la posicion 2 del `servo-thread`: despues de la
lectura de la Mesa y antes del controlador de movimiento.

## Valores que deben comprobarse antes de habilitar movimiento

| Estado sano | Valor esperado |
|---|---:|
| `hm2_7i76e.0.7i76.0.0.input-09` | TRUE |
| `hm2_7i76e.0.7i76.0.0.input-10` | TRUE |
| `z1-drive-fault` | FALSE |
| `z2-drive-fault` | FALSE |
| `z-drive-fault` | FALSE |

Al abrir cualquiera de los dos circuitos `ALM`, con la máquina imposibilitada
para moverse, deben ponerse en `TRUE` `z-drive-fault` y los dos pines
`joint.1.amp-fault-in` / `joint.2.amp-fault-in`. LinuxCNC debe quitar la
habilitacion de ambas juntas y exigir rearme del operador.

No provocar un atasco para probarlo. Si la logica aparece invertida en estado
sano, revisar primero cableado y configuracion de `ALM` del driver.

## Pendiente separado

Este borrador implementa la parada común por LinuxCNC. El interbloqueo común
por hardware mediante `ENA` no se incluye hasta rastrear y medir el cableado
actual de `ENA+`/`ENA-`.
