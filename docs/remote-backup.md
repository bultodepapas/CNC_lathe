# Respaldo remoto por Tailscale y SSH

## Datos de conexión recibidos

- DNS: `cnc.taila1b901.ts.net`
- Nombre corto: `cnc`
- IPv4: `100.87.222.75`
- Usuario supuesto: `cnc`
- Estado al iniciar este repositorio: máquina no conectada.

El DNS de Tailscale es preferible a fijar la IPv4. No se almacena contraseña ni
clave privada en este repositorio.

## Comprobación manual de solo lectura

Cuando la máquina vuelva a estar en línea:

```powershell
ssh -o ConnectTimeout=8 cnc@cnc.taila1b901.ts.net "hostname; uname -a; linuxcnc --version"
```

Aceptar una clave de host sólo después de comprobar que el nombre/IP corresponde
a la máquina esperada. Un cambio inesperado de huella SSH se trata como alerta,
no se corrige borrando `known_hosts` sin investigar.

## Crear una copia con `.env`

El `.env` local debe contener únicamente:

```dotenv
CNC_SSH_USER=cnc
CNC_SSH_PASSWORD=<clave>
```

Está excluido de Git. El script Python usa esas variables, valida la clave de
host ya registrada en `known_hosts` y copia `/home/cnc/linuxcnc` completo sin
escribir en la máquina:

```powershell
python ./scripts/backup-cnc.py
```

Requiere el paquete Python `paramiko`.

## Alternativa interactiva con OpenSSH

El script copia `/home/cnc/linuxcnc` completo sin escribir en la máquina remota:

```powershell
./scripts/backup-cnc.ps1 -InteractiveAuth
```

Si ya existe autenticación mediante clave SSH, omita `-InteractiveAuth` para que
el comando falle en vez de pedir contraseña:

```powershell
./scripts/backup-cnc.ps1
```

Cada ejecución crea `backups/<fecha>-cnc/`, un inventario remoto y hashes
SHA-256 de los archivos recibidos. `backups/` está excluido de Git porque puede
contener programas de producción y preferencias privadas.

## Después del respaldo

1. Detener LinuxCNC antes de considerar `linuxcnc.var` y `tool.tbl` como una
   captura consistente; la primera copia se conserva aunque se haya tomado en
   ejecución.
2. No sobrescribir todavía `linuxcnc/configs/torno_v3/`.
3. Comparar el directorio remoto que realmente usa el lanzador con la captura
   versionada.
4. Registrar qué archivo es la fuente de verdad y sólo entonces preparar un
   despliegue reversible.
