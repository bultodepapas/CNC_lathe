# Herramientas de internacionalización de QtDragon

Estas herramientas trabajan contra una copia local de los fuentes activos. No
se conectan al control CNC salvo `fetch-installed-sources.py`, cuya única
función remota es leer por SSH/SFTP y registrar hashes.

## Flujo seguro durante producción

1. Capturar una vez los fuentes instalados:

   ```powershell
   python scripts/qtdragon-i18n/fetch-installed-sources.py
   ```

2. Comprobar la línea base local:

   ```powershell
   python scripts/qtdragon-i18n/analyze_sources.py --pretty
   ```

3. Extraer el catálogo con PyQt 5.15, revisar `qtdragon_es.ts` en Qt Linguist y
   validarlo:

   ```powershell
   python scripts/qtdragon-i18n/validate_ts.py ruta/qtdragon_es.ts --min-coverage 98
   ```

   Para reproducir la primera pasada controlada sobre un TS recién extraído:

   ```powershell
   python scripts/qtdragon-i18n/apply_static_es.py `
     i18n/qtdragon-2.9.7/qtdragon_es.ts --check
   python scripts/qtdragon-i18n/apply_static_es.py `
     i18n/qtdragon-2.9.7/qtdragon_es.ts
   ```

   `--check` exige que las 346 fuentes estén clasificadas. El script sólo
   termina traducciones o preservaciones enumeradas explícitamente.

4. Compilar con `lrelease` y validar el `.qm` en un entorno PyQt 5.15 fuera del
   CNC. La carga debe devolver `true` y las traducciones centinela deben
   resolverse usando los mismos contextos que aparecen en el `.ts`.

   En Windows se puede ejecutar el gate completo indicando herramientas
   explícitas:

   ```powershell
   scripts/qtdragon-i18n/build.ps1 `
     -Catalog i18n/qtdragon-2.9.7/qtdragon_es.ts `
     -Output build/qtdragon_es.qm `
     -Python .work/qtdragon-i18n-venv/Scripts/python.exe `
     -LRelease .work/qtdragon-i18n-venv/Lib/site-packages/qt5_applications/Qt/bin/lrelease.exe
   ```

   Tras compilar, añadir centinelas exactos:

   ```powershell
   python scripts/qtdragon-i18n/validate_qm.py build/qtdragon_es.qm `
     --sentinel 'MainWindow|MAIN|PRINCIPAL'
   ```

## Reglas de reproducibilidad

- El manifiesto y los hashes deciden qué fuentes se traducen; la versión que
  aparezca en internet no sustituye la instalada.
- No se genera el catálogo con globs amplios.
- `qtdragon.ui` puede usarse directamente con `pylupdate5`; si el entorno no lo
  admite, `pyuic5` genera un Python temporal que nunca se despliega.
- `validate_ts.py` falla por catálogo no español, cobertura insuficiente,
  traducciones terminadas vacías, placeholders distintos, HTML incompatible o
  caracteres de control. Los saltos de línea y duplicados inconsistentes se
  reportan como advertencias para revisión humana.
- El mensaje de QtVCP `Using LOCAL translation file` no demuestra que el `.qm`
  sea válido: siempre se exige una carga offline y pruebas centinela.
- `build.ps1` no despliega: sólo valida, compila y calcula el hash dentro del
  equipo de ingeniería.

## Frontera de despliegue

No ejecutar instalación, copia al controlador, reinicio, `halcmd` ni pruebas de
la interfaz real mientras el torno esté produciendo. El procedimiento de
despliegue está en `docs/plan-qtdragon-es.md` y requiere confirmación explícita
del operador.
