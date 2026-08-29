# Torno CNC de madera — LinuxCNC

Repositorio de ingeniería y respaldo de la máquina `torno_v3`, basada en
LinuxCNC 2.9, una Mesa 7I76EU/7I76E por Ethernet y tres juntas de movimiento:
X, Z y Z tándem.

> Estado actual: copia de la configuración que estaba ejecutándose en la
> máquina el 2026-08-29. El arranque y las señales HAL principales se verificaron
> remotamente, pero no se realizaron pruebas físicas de movimiento ni seguridad.

## Estructura

- `linuxcnc/configs/torno_v3/`: configuración operativa que debe permanecer
  autocontenida para que las rutas relativas de LinuxCNC funcionen.
- `docs/hardware.md`: inventario mecánico, eléctrico y de control recibido.
- `output/pdf/componentes/`: datasheets y manuales originales descargados.
- `output/docs/componentes/`: copias Markdown, fuentes, hashes, auditoría e
  índice de correspondencia de los componentes.
- `docs/configuration-audit.md`: auditoría inicial y puntos pendientes.
- `docs/plan-actualizacion-linuxcnc-2.9.10.md`: runbook completo para actualizar
  LinuxCNC 2.9.7 a 2.9.10, validar la máquina por gates y ejecutar rollback.
- `docs/incidente-desincronizacion-z.md`: diagnóstico y plan para evitar que un
  motor Z continúe cuando el otro se atasca o entra en alarma.
- `docs/manual-cableado-alarmas-z.md`: hoja corta de conexión de `ALM` para Z1
  y Z2 hacia las entradas de campo de la Mesa.
- `drafts/alarmas-z/`: cambio HAL preparado pero inactivo hasta terminar el
  cableado físico y las pruebas sin movimiento.
- `docs/remote-backup.md`: acceso y procedimiento de respaldo por Tailscale/SSH.
- `scripts/backup-cnc.ps1`: copia remota de solo lectura hacia `backups/`.
- `scripts/backup-cnc.py`: respaldo no interactivo usando las credenciales
  locales excluidas de Git.
- `scripts/verify-config.ps1`: comprobaciones estáticas que no requieren LinuxCNC.
- `scripts/audit-cnc-readonly.py`: inventario SSH con allowlist estática; no
  usa `sudo`, no escribe en el CNC y no modifica HAL/APT.
- `scripts/verify-upgrade-packages.ps1`: valida tamaño y SHA-256 del conjunto
  offline 2.9.10 y del rollback APT exacto 2.9.7.
- `archive/imported/`: archivos recibidos cuya función o vigencia no está
  confirmada; nunca se despliegan automáticamente.
- `backups/`: copias fechadas de la máquina, excluidas de Git.

## Máquina conocida

- Host Tailscale: `cnc.taila1b901.ts.net`
- Nombre corto: `cnc`
- IPv4 Tailscale: `100.87.222.75`
- Usuario SSH supuesto: `cnc` (pendiente de confirmar)
- Sistema reportado: Linux con kernel `6.1.0-41-rt-amd64`

La placa Mesa se configura en `192.168.1.121`; esa dirección pertenece a la
red local entre el controlador y la tarjeta, no a Tailscale.

## Flujo seguro de trabajo

1. Obtener una copia remota completa antes de cambiar la máquina.
2. Comparar esa copia con `linuxcnc/configs/torno_v3/`.
3. Resolver los puntos críticos de la auditoría con diagramas y pruebas de E/S.
4. Validar HAL e INI en el PC CNC con potencia de motores/husillo inhibida.
5. Probar E-stop, límites, sentido y homing a velocidad reducida.
6. Desplegar únicamente cambios revisados y con una copia recuperable.

Ejecute la comprobación local desde PowerShell:

```powershell
./scripts/verify-config.ps1
```

La configuración principal, confirmada desde los procesos activos y el lanzador,
es `linuxcnc/configs/torno_v3/torno_v3.ini`. La configuración histórica
`my_LinuxCNC_machine` sólo se conserva dentro del respaldo remoto, no en el árbol
operativo del repositorio.
