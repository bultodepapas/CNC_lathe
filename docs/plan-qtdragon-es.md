# Plan de ingeniería: QtDragon completamente en español

## 1. Objetivo

Implementar una traducción completa, consistente y mantenible de QtDragon para
la configuración `torno_v3`, conservando LinuxCNC 2.9.7 y sin modificar la
lógica de movimiento, HAL, homing, torreta, husillo o seguridad de la máquina.

La solución final debe:

- presentar en español los textos estáticos de la interfaz;
- presentar en español los mensajes generados dinámicamente por QtDragon;
- usar terminología CNC clara para operadores de Colombia y comprensible en
  español internacional;
- mantener códigos G/M, nombres HAL, unidades y datos técnicos sin traducciones
  que alteren su significado;
- sobrevivir actualizaciones del sistema sin depender de cambios manuales en
  `/usr/share`;
- poder revertirse sin reinstalar LinuxCNC;
- quedar respaldada y versionada junto con `torno_v3`.

### 1.1 Estado de ejecución del plan

| Actividad | Estado | Evidencia |
|---|---|---|
| Investigación oficial y búsqueda de activos españoles | Completada | Secciones 4 y 4.2 |
| Auditoría viva de sólo lectura | Completada | Hashes y manifiesto local |
| Captura SFTP de fuentes exactas | Completada, cero escrituras remotas | `vendor/linuxcnc-2.9.7-qtdragon/` |
| Extracción del `.ts` estático | Completada | `i18n/qtdragon-2.9.7/qtdragon_es.ts` |
| Glosario, cobertura y checklist | Completados como línea base | `docs/qtdragon-es/` |
| Validadores TS/QM y prueba del pipeline Qt 5 | Completados | `scripts/qtdragon-i18n/` |
| Traducción estática de primera pasada | Completada: 346/346 | Catálogo y validador |
| Revisión del operador y QA visual | Pendiente | Requiere interfaz detenida |
| Despliegue y QA en QtDragon real | Bloqueado por producción activa | Requiere Gate 0 |

El `.ts` extraído contiene 346 mensajes activos bajo el contexto `MainWindow`.
La primera pasada traduce 250 y conserva explícitamente 96 cadenas técnicas,
con cobertura estructural 100 %, cero errores y cero advertencias del validador.
Esta métrica no sustituye la revisión contextual del operador ni el QA visual.

### 1.2 Frontera operativa mientras el torno está produciendo

Mientras LinuxCNC esté controlando un trabajo real sólo están autorizadas:

- consultas SSH y SFTP de lectura;
- lectura de archivos, procesos, paquetes, locale y logs ya existentes;
- investigación externa;
- creación y validación de artefactos en el repositorio de ingeniería;
- compilación y pruebas fuera del controlador.

Quedan aplazados hasta que el operador confirme que el trabajo terminó:

- copiar `.qm`, `.ts`, handlers o cualquier otro archivo al CNC;
- modificar `/home/cnc/linuxcnc` o `/usr/share`;
- instalar o actualizar paquetes;
- reiniciar QtDragon, LinuxCNC, servicios o el PC;
- abrir otra instancia de QtVCP contra la configuración real;
- tomar control de la sesión gráfica;
- ejecutar `halcmd`, MDI, código G/M o pruebas de E/S;
- cambiar permisos, propietarios, locale o variables de entorno.

Esta frontera tiene prioridad sobre el orden de fases descrito más adelante.

## 2. Alcance

### 2.1 Incluido

- QtDragon estándar iniciado mediante `DISPLAY = qtvcp qtdragon`.
- Etiquetas, pestañas, botones, tooltips, menús y diálogos definidos en
  `qtdragon.ui`.
- Mensajes visibles al operador generados desde `qtdragon_handler.py`.
- Textos visibles provenientes de widgets QtVCP utilizados realmente por la
  pantalla del torno.
- Archivo fuente de traducción Qt Linguist (`.ts`).
- Archivo compilado consumido por Qt (`.qm`).
- Glosario técnico y reglas editoriales.
- Validación visual y funcional sin movimiento.
- Procedimiento de despliegue, diagnóstico y reversión.

### 2.2 Excluido

- Traducción de nombres de variables HAL, pines, señales o parámetros INI.
- Traducción de código G, código M, nombres de archivo o rutas.
- Modificación del comportamiento de botones o widgets.
- Rediseño visual general de QtDragon.
- Migración a QtDragon HD.
- Actualización a LinuxCNC `master` o a una rama de desarrollo.
- Cambios en la configuración del eje Z actualmente en reparación.

## 3. Estado confirmado del controlador

La investigación remota del 29 de agosto de 2026 confirmó:

| Elemento | Resultado |
|---|---|
| LinuxCNC | `linuxcnc-uspace 2.9.7` |
| Interfaz activa | QtVCP `qtdragon` |
| Locale del sistema | `LANG=es_CO.UTF-8` |
| Preferencia de idiomas | `LANGUAGE=es_CO:es` |
| Locale detectado por Qt | `es_CO` |
| Paquete de documentación | `linuxcnc-doc-es 2.9.7` instalado |
| Traducciones generales Qt | `qttranslations5-l10n` instalado |
| PyQt / Qt | PyQt `5.15.9`; Qt `5.15.8` |
| Traducción QtDragon española | No existe `qtdragon_es.ts` ni `qtdragon_es.qm` |
| Versión interna de QtDragon | `1.4` |
| Textos en `qtdragon.ui` | 718 elementos `<string>` |
| Textos marcados como no traducibles | 22 |
| Textos estáticos traducibles | 696 nodos; 619 no vacíos; 346 fuentes únicas |
| `_translate(...)` en el handler 2.9.7 | 0 llamadas |
| Mensajes dinámicos `add_status(...)` | 51 llamadas, además de diálogos y `setText(...)` |
| Herramientas disponibles | `pylupdate5`, `pyuic5` |
| Herramientas ausentes | `lrelease`, `linguist` |

Conclusión: el locale está correctamente configurado. El problema no se
resuelve cambiando Debian, `LANG`, `LANGUAGE` ni `qtdragon.pref`. QtDragon no
encuentra una traducción española y su handler 2.9.7 tampoco marca los mensajes
dinámicos para traducción.

### 3.1 Fuentes exactas en ejecución

La pantalla activa usa el `.ui` y el handler del paquete del sistema; la
configuración local sólo sustituye `resources.py`. La línea base es:

| Archivo | Bytes | SHA-256 |
|---|---:|---|
| `qtdragon.ui` | 841936 | `d50bc9c3919302d7ec5fa7df9443ee8e852837b51f6adb555968a261b95d2039` |
| `qtdragon_handler.py` | 74457 | `b00f5b5a5c3acace9c2a2fb997d5e53d561df1533c5e06c118d3fc149d6d3d03` |
| `version.txt` | 505 | `3cd326f29a124d9b6fc5235033cc2226584c5fe99148ff9616c139a332bb4e6d` |
| `qt_pstat.py` | 19471 | `fa504445b7ceca48e07de5b7cf24532a8c7809da96eafc100983d2d31f95ef19` |
| `/usr/bin/qtvcp` | 22740 | `1ca0cd23ccc5c05918aa39d47e1ded1b2242b1130488c4ff7c85129b3b6f6159` |

Una copia SFTP de sólo lectura y su manifiesto se conservan en
`vendor/linuxcnc-2.9.7-qtdragon/`. Éstas son las fuentes que deben alimentar el
catálogo, aunque aparezca una versión más reciente en internet.

## 4. Funcionamiento de la internacionalización de QtDragon

QtVCP calcula el identificador del idioma así:

```python
lang = QtCore.QLocale.system().name().split('_')[0]
qm_fn = "languages/{}_{}.qm".format(self.BASEPATH, lang)
```

Con el locale `es_CO`, QtDragon busca `qtdragon_es.qm`. El país no forma parte
del nombre del archivo; una sola traducción `es` sirve para `es_CO`, `es_ES`,
`es_MX` y otros locales españoles.

La documentación oficial describe el flujo `.ts` -> Qt Linguist -> `.qm` y
confirma que QtDragon selecciona el idioma a partir del locale actual:

- [QtDragon: Internationalisation](https://linuxcnc.org/docs/master/html/en/gui/qtdragon.html#_internationalisation)
- [Primer soporte oficial de traducción en QtDragon](https://github.com/LinuxCNC/linuxcnc/commit/2939708a75)
- [Corrección posterior del soporte de traducción](https://github.com/LinuxCNC/linuxcnc/commit/4590758fbc)
- [Loader QtVCP 2.9.7](https://github.com/LinuxCNC/linuxcnc/blob/v2.9.7/src/emc/usr_intf/qtvcp/qtvcp.py)

La versión estable más reciente comprobada durante esta investigación es
LinuxCNC 2.9.10. Su rama `2.9` tampoco incluye un catálogo español de QtDragon,
el handler conserva cero llamadas `_translate(...)` y el defecto de la ruta
local continúa presente. Actualizar LinuxCNC puede tener otros beneficios, pero
**no es la solución de internacionalización** y no se mezcla con este trabajo.

### 4.1 Particularidad de LinuxCNC 2.9.7

La versión instalada contiene un defecto en la primera ruta local evaluada por
`qt_pstat.py`: concatena `qrc_fn` donde debería usar `qm_fn`. La segunda ruta
local, denominada legado, sí es válida.

El proyecto corrigió el typo únicamente en su rama de desarrollo mediante el
commit [`3bd7c3e8b8db`](https://github.com/LinuxCNC/linuxcnc/commit/3bd7c3e8b8db).
No se parcheará `qt_pstat.py` en el torno: usar su fallback válido es más simple
y reversible.

Por esta razón, la ubicación compatible con el torno es:

```text
/home/cnc/linuxcnc/configs/torno_v3/qtdragon/languages/qtdragon_es.qm
```

No se debe depender de esta ubicación defectuosa:

```text
/home/cnc/linuxcnc/configs/torno_v3/qtvcp/screens/qtdragon/languages/
```

Tampoco se instalará la traducción en:

```text
/usr/share/qtvcp/screens/qtdragon/languages/
```

Modificar `/usr/share` requeriría privilegios administrativos, mezclaría el
trabajo local con archivos administrados por Debian y permitiría que una
actualización lo sobrescribiera.

### 4.2 Reutilización de traducciones existentes

La búsqueda en el repositorio oficial, paquetes Debian, Weblate, foros y forks
no encontró ningún `qtdragon_es.ts` o `qtdragon_es.qm` público, verificable y
apto para reutilización directa. El directorio actual de idiomas upstream sólo
contiene el script de extracción:

- [QtDragon `languages/` en upstream](https://github.com/LinuxCNC/linuxcnc/tree/master/share/qtvcp/screens/qtdragon/languages)
- [Archivos del paquete Debian `linuxcnc-uspace`](https://packages.debian.org/bookworm/amd64/linuxcnc-uspace/filelist)
- [Proyecto LinuxCNC en Weblate](https://hosted.weblate.org/projects/linuxcnc/)

El `es.po` del núcleo LinuxCNC y su glosario pueden usarse como memoria de
consulta, no como importación automática. Una comparación sobre la UI upstream
2.9.7 encontró coincidencias exactas en sólo 61 de 338 cadenas únicas (18 %),
incluyendo opciones poco apropiadas para el torno, por ejemplo `HOME` como
“Inicio”. Cada coincidencia debe pasar por el glosario local y revisión humana.

Política de licencias:

- recursos de código/PO de LinuxCNC bajo GPL pueden reutilizarse conservando
  atribución y licencia;
- la documentación GFDL sirve como referencia terminológica, pero no se copia
  masivamente al catálogo;
- forks sin licencia explícita no se toman como fuente de traducciones.

## 5. Arquitectura propuesta

```text
torno_v3/
├── qtdragon/
│   ├── languages/
│   │   ├── qtdragon_es.ts      # fuente revisable y mantenible
│   │   └── qtdragon_es.qm      # binario cargado por QtVCP
│   └── qtdragon_handler.py     # sólo en la fase de mensajes dinámicos
├── qtvcp/
│   └── screens/
│       └── qtdragon/
│           └── resources.py    # recurso actual; no modificar por i18n
├── qtdragon.pref
├── torno_v3.ini
└── ...
```

Documentación de soporte en el repositorio:

```text
docs/qtdragon-es/
├── glossary.md
├── coverage.md
├── qa-checklist.md
└── screenshots/
```

Herramientas reproducibles:

```text
scripts/qtdragon-i18n/
├── extract.ps1 o extract.sh
├── compile.ps1 o compile.sh
├── validate.py
└── README.md
```

Los nombres definitivos de scripts pueden adaptarse al entorno de compilación,
pero el proceso no debe depender de comandos recordados manualmente.

Los artefactos ya definidos son:

```text
scripts/qtdragon-i18n/
├── fetch-installed-sources.py # captura SFTP de sólo lectura
├── analyze_sources.py         # métricas y hashes reproducibles
├── apply_static_es.py          # traducciones y exclusiones explícitas
├── validate_ts.py             # cobertura, placeholders, HTML y consistencia
├── validate_qm.py             # carga Qt y centinelas por contexto
├── build.ps1                   # gate TS -> QM -> hash
└── README.md                  # uso y frontera operacional
```

No se copiará `qtdragon.ui` al directorio operativo sólo para traducirlo. Un
`.qm` válido puede traducir la UI del sistema y evita crear un fork innecesario
de 842 kB. La copia exacta del `.ui` se conserva únicamente como entrada de
compilación y evidencia de versión.

## 6. Estrategia de implementación

La implementación se divide en dos entregas. La primera traduce los textos
estáticos con un riesgo muy bajo. La segunda adapta de forma mínima el handler
2.9.7 para traducir mensajes dinámicos.

### Fase 0. Línea base y respaldo

La parte de sólo lectura de esta fase ya se completó sin interferir con el
trabajo activo: se identificaron versiones y locale, se calcularon hashes y se
copiaron por SFTP los siete fuentes necesarios al directorio `vendor/`. No se
escribió nada en el CNC.

Cuando termine la producción:

1. Detener LinuxCNC de forma normal.
2. Crear un respaldo nuevo de `/home/cnc/linuxcnc`.
3. Revalidar los hashes de:
   - `/usr/share/qtvcp/screens/qtdragon/qtdragon.ui`;
   - `/usr/share/qtvcp/screens/qtdragon/qtdragon_handler.py`;
   - `/usr/share/qtvcp/screens/qtdragon/version.txt`;
   - `/usr/lib/python3/dist-packages/qtvcp/qt_pstat.py`;
   - `/usr/bin/qtvcp`.
4. Confirmar que coinciden con la copia de trabajo ya capturada.
5. Capturar imágenes de todas las pestañas y diálogos principales en inglés o
   español parcial.
6. Crear una rama Git dedicada, por ejemplo:

   ```text
   feat/qtdragon-es
   ```

#### Criterio de salida

- Respaldo recuperable.
- Hashes registrados.
- Capturas de referencia.
- Fuentes de QtDragon 2.9.7 identificadas sin ambigüedad.

### Fase 1. Traducción estática

#### 6.1 Extracción

Generar `qtdragon_es.ts` usando las fuentes exactas del controlador. En la
primera entrega se extrae únicamente la UI estática; el handler se agrega sólo
después de hacer traducibles sus literales. Como referencia, Qt emplea un
comando de esta forma:

```bash
pylupdate5 qtdragon.py -ts qtdragon_es.ts
```

El comando definitivo debe registrar explícitamente la lista de entradas. No se
usarán globs demasiado amplios que incorporen pantallas o widgets no usados por
el torno.

Si `pylupdate5` no procesa correctamente el `.ui` en el entorno elegido, se
generará primero una representación Python sólo para extracción:

```bash
pyuic5 qtdragon.ui > qtdragon.py
pylupdate5 qtdragon.py -ts qtdragon_es.ts
```

`qtdragon.py` es un artefacto de generación y no reemplaza el `.ui` instalado.

En la línea base instalada, `pylupdate5` sí procesó directamente el `.ui` y
generó 346 mensajes en el contexto `MainWindow`; no fue necesario conservar el
Python temporal. El archivo resultante está en:

```text
i18n/qtdragon-2.9.7/qtdragon_es.ts
```

La primera pasada estática quedó en 346/346 mensajes terminados: 250 tienen
traducción española y 96 se conservan de forma explícita por ser códigos,
formatos, identificadores, unidades o comandos técnicos. No se usó una regla
genérica que pudiera ocultar inglés accidental.

#### 6.2 Traducción

Editar `qtdragon_es.ts` con Qt Linguist. Aplicar estas reglas:

- no traducir códigos G/M;
- no traducir nombres de pines HAL;
- no traducir nombres de parámetros INI;
- conservar placeholders como `%1`, `%2`, `%n`, `{}`, `{0}` y secuencias `\n`;
- conservar etiquetas HTML y aceleradores de teclado;
- no introducir espacios dentro de valores numéricos;
- mantener las traducciones de botones tan cortas como el original;
- usar mayúsculas sólo cuando la jerarquía visual lo requiera;
- marcar como `unfinished` cualquier texto cuya intención técnica no sea clara;
- no usar traducción automática sin revisión humana contextual.

#### 6.3 Compilación

Compilar la traducción mediante Qt Linguist o `lrelease`:

```bash
lrelease qtdragon_es.ts -qm qtdragon_es.qm
```

Las herramientas de compilación no están instaladas actualmente en el CNC. Se
prefiere compilar fuera del controlador o dentro de un entorno Debian 12
reproducible. Si fuera necesario instalarlas en el CNC, el paquete esperado es:

```bash
sudo apt install qttools5-dev-tools pyqt5-dev-tools
```

La instalación de paquetes no debe formar parte del primer despliegue si el
`.qm` puede compilarse en otro entorno.

El pipeline de ingeniería ya fue probado offline con PyQt 5.15.9, Qt 5.15.2 y
un catálogo fixture: `lrelease` generó el `.qm`, `QTranslator.load()` devolvió
`true` y dos centinelas por contexto resolvieron exactamente al español. Antes
del artefacto final se repetirá en Debian 12/Qt 5 o se documentará la
compatibilidad del compilador utilizado.

El catálogo compilado de primera pasada mide 30 954 bytes y tiene SHA-256:

```text
ad69d88c35e4a4f4b14d095373e656794d73997f8be6a3efccba8fe7dea8318b
```

`QTranslator.load()` devolvió `true`. Los centinelas `MAIN`, `HOME`,
`CYCLE\nSTART` y `%d %%` resolvieron exactamente al valor esperado.

#### 6.4 Validación estática

El validador debe rechazar:

- traducciones vacías marcadas como terminadas;
- placeholders eliminados o añadidos;
- etiquetas HTML desequilibradas;
- saltos de línea incompatibles;
- traducciones duplicadas inconsistentes;
- caracteres de control;
- archivos `.qm` vacíos o no reconocidos por Qt;
- textos críticos sin revisar.

Además debe advertir aceleradores `&` duplicados dentro del mismo diálogo,
espacios significativos alterados y traducciones excesivamente largas. Estas
advertencias requieren revisión visual; no se corrigen automáticamente.

#### Criterio de salida

- `qtdragon_es.ts` válido y revisado.
- `qtdragon_es.qm` reproducible.
- Cero errores de placeholders.
- Cobertura estática objetivo >= 98 %.
- Todos los controles de seguridad visibles traducidos al 100 %.

### Fase 2. Despliegue inicial del `.qm`

1. Mantener LinuxCNC cerrado.
2. Crear el directorio local reconocido por 2.9.7:

   ```text
   /home/cnc/linuxcnc/configs/torno_v3/qtdragon/languages/
   ```

3. Copiar `qtdragon_es.qm` y conservar `qtdragon_es.ts` como fuente.
4. Confirmar propietario `cnc:cnc` y permisos de lectura normales.
5. No modificar `torno_v3.ini` ni `qtdragon.pref`.
6. Arrancar LinuxCNC desde una terminal con mayor nivel de registro.
7. Confirmar un mensaje equivalente a:

   ```text
   Using LOCAL translation file .../qtdragon_es.qm
   ```

   Este mensaje sólo confirma selección de ruta/existencia. El loader 2.9.7
   instala el traductor sin comprobar el resultado de `QTranslator.load()`.
   Antes de este arranque, una prueba offline debe haber confirmado:

   ```text
   QTranslator.load(ruta_qm) == true
   traducción_centinela(contexto_exacto, fuente) == texto_español
   ```

8. Si el log indica `Using no translations`, detener la prueba y verificar:
   - que Qt detecta `es_CO`;
   - que el nombre es exactamente `qtdragon_es.qm`;
   - que el archivo está en la ruta legado;
   - que el usuario `cnc` puede leerlo.

#### Criterio de salida

- QtVCP confirma que seleccionó la ruta local.
- La carga offline del `.qm` devuelve `true` y resuelve centinelas por contexto.
- QtDragon inicia sin excepciones.
- HAL e INI conservan sus hashes.
- Los textos estáticos principales aparecen en español.

### Fase 3. Mensajes dinámicos del handler

El handler de LinuxCNC 2.9.7 no contiene llamadas `_translate(...)`. Por eso la
fase estática no traducirá todos los mensajes de estado, confirmación y error.

El inventario mínimo del handler incluye 51 llamadas `add_status(...)`, cinco
diccionarios principales de diálogo y textos adicionales asignados mediante
`setText(...)`, `setToolTip(...)` y títulos de ventana. La cobertura dinámica se
medirá sobre ese inventario, no sólo contando `_translate(...)`.

#### 6.5 Política de modificación

No se copiará el `qtdragon_handler.py` actual de `master`. Su tamaño, APIs y
comportamiento han cambiado y no se debe introducir código de una versión nueva
en un controlador 2.9.7 de producción.

Se realizará un backport mínimo sobre una copia exacta del handler instalado:

```python
from PyQt5.QtCore import QCoreApplication

_translate = QCoreApplication.translate
```

Después se envolverán exclusivamente textos visibles:

```python
self.add_status(_translate("HandlerClass", "All homed"))
```

No se modificarán:

- condiciones;
- conexiones de señales;
- comandos LinuxCNC;
- llamadas HAL;
- temporizadores;
- gestión de herramientas;
- rutas de archivos;
- acciones QtVCP.

El diff debe limitarse a importaciones de traducción, literales visibles y
variables temporales necesarias para construir mensajes traducibles.

#### 6.6 Fuente de referencia

Usar como guía los commits oficiales de QtDragon:

- `2939708a75`: primera adaptación de mensajes dinámicos;
- `4590758fbc`: correcciones posteriores de interpolación;
- revisiones posteriores sólo cuando resuelvan una cadena presente en 2.9.7.

Cada cambio debe compararse con el handler 2.9.7 y portarse manualmente. No se
aplicará el commit completo sin revisar.

#### 6.7 Ubicación del handler local

La copia adaptada se instalará en una ruta local reconocida por QtVCP:

```text
/home/cnc/linuxcnc/configs/torno_v3/qtdragon/qtdragon_handler.py
```

Al arrancar, el log debe confirmar que QtVCP usa el handler local. Si no existe
el handler local, QtVCP vuelve al handler del sistema.

#### 6.8 Regeneración de traducciones

Regenerar `qtdragon_es.ts` incluyendo el handler adaptado. Qt Linguist debe
conservar las traducciones existentes y añadir los nuevos mensajes bajo el
contexto `HandlerClass`.

#### Criterio de salida

- El diff del handler no altera lógica funcional.
- Todos los mensajes críticos están marcados para traducción.
- La traducción dinámica tiene cobertura >= 95 %.
- No aparecen excepciones durante la navegación y operación simulada.

### Fase 4. Widgets QtVCP compartidos

La UI activa instancia 25 clases de 24 módulos `qtvcp.widgets.*`. En la versión
instalada ninguno de esos módulos usa `_translate`,
`QCoreApplication.translate` o `self.tr`. Esto no implica que todos sus
literales sean visibles, pero demuestra que el catálogo del `.ui` y el handler
no pueden garantizar por sí solos una interfaz completa.

La medición detallada se mantiene en `docs/qtdragon-es/coverage.md`. Los casos
prioritarios confirmados incluyen:

- `file_manager`: `Paste`, `Copy`, `User`, `Load`, `Add Jump`, `Del Jump`,
  `Show Copy Controls`, tooltips y errores;
- `gcode_editor`: menús, status tips y errores;
- `camview_widget`: `Cam View`;
- `state_label` y `status_label`: errores y advertencias;
- `screen_options` y `web_widget`: textos creados en tiempo de ejecución.

Durante la prueba visual se incorporarán sólo los widgets que realmente
muestren inglés al operador. Se prefiere cambiar presentación desde una capa
local post-inicialización. Si un widget exige lógica propia, se congelará una
copia local exacta y se documentará su divergencia; nunca se editará
`/usr/lib/python3/dist-packages`.

Orden recomendado:

1. tabla de herramientas;
2. tabla de offsets;
3. administrador de archivos;
4. editor de G-code;
5. diálogos de entrada y confirmación;
6. mensajes de límites y errores;
7. calculadora;
8. utilidades realmente habilitadas.

No se traducirá toda la biblioteca QtVCP de forma indiscriminada. Eso aumenta
el catálogo, mezcla contextos ajenos al torno y dificulta el mantenimiento.

La cobertura se publica por buckets independientes:

1. UI estática;
2. handler QtDragon;
3. widgets QtVCP visibles;
4. diálogos estándar Qt;
5. LinuxCNC/core;
6. términos técnicos deliberadamente conservados.

No se declarará “100 % español” con un promedio global si algún flujo operativo
conserva inglés no aprobado.

### Fase 5. Revisión lingüística y visual

#### 6.9 Glosario inicial

| Inglés | Traducción preferida | Evitar |
|---|---|---|
| Home | Referenciar / referencia máquina | Casa, inicio |
| Home All | Referenciar todo | Inicio de todo |
| Homed | Referenciado | En casa |
| Jog | Movimiento manual | Trote |
| Feed | Avance | Alimentación |
| Feed Override | Corrección de avance | Sobrealimentación |
| Rapid | Rápido | Rapidez |
| Spindle | Husillo | Eje |
| Tool | Herramienta | Útil, tool |
| Tool Offset | Compensación de herramienta | Desfase de tool |
| Touch Off | Fijar referencia | Tocar fuera |
| Work Offset | Cero de pieza / sistema de trabajo | Offset de trabajo |
| Machine Coordinates | Coordenadas máquina | Coordenadas mecánicas |
| Run | Ejecutar | Correr |
| Run From Line | Ejecutar desde línea | Correr desde línea |
| Hard Limit | Final de carrera | Límite duro |
| Limit Override | Anular límites | Sobrescribir límites |
| E-Stop | Parada de emergencia | Stop de emergencia |
| Coolant | Refrigerante | Enfriador |
| Mist | Neblina | Niebla |
| Flood | Refrigeración abundante | Inundación |
| Probe | Palpador / palpado | Sonda, cuando sea ambiguo |
| Pocket | Posición de torreta | Bolsillo, cavidad |
| Tool Change | Cambio de herramienta | Cambio de útil |
| Apply | Aplicar | Aplicar cambios, si el contexto ya lo expresa |
| Reload | Recargar | Refrescar |
| Abort | Abortar | Cancelar, cuando implica detener ejecución |
| Pause | Pausar | Parar |
| Resume | Reanudar | Continuar, cuando pueda confundirse |

El glosario definitivo debe validarse con el operador. Se prefiere lenguaje
directo, frases cortas y verbos de acción.

#### 6.10 Reglas para textos críticos

- `ABORT` debe diferenciarse visual y verbalmente de `PAUSE`.
- `MACHINE ON` no debe traducirse como husillo encendido.
- `SPINDLE ON` debe referirse exclusivamente al husillo.
- `HOME` no debe confundirse con cero de pieza.
- `TOOL CHANGE` no debe sugerir que el cambio ya terminó mientras sólo exista
  una solicitud.
- `LIMIT OVERRIDE` debe expresar claramente que se están anulando límites.
- Los diálogos destructivos deben usar verbos explícitos: eliminar, sobrescribir,
  apagar o abortar.

#### 6.11 Prueba de disposición

Validar en la geometría real guardada por QtDragon: `1600 x 849`.

Revisar:

- texto truncado;
- superposición con iconos;
- saltos de línea;
- botones con altura insuficiente;
- pestañas demasiado anchas;
- valores numéricos desplazados;
- pérdida de aceleradores de teclado;
- tooltips sin traducir;
- contraste de mensajes críticos.

No se cambiará el tamaño global de fuentes para ocultar problemas de longitud.
Primero se acortará la traducción conservando el significado.

## 7. Estrategia de pruebas

### 7.1 Entorno seguro

Las primeras pruebas se ejecutarán con:

- máquina en E-stop;
- husillo apagado físicamente;
- potencia de movimiento inhibida cuando sea posible;
- ningún programa automático iniciado;
- ningún cambio de herramienta solicitado.

La traducción no requiere movimiento para ser validada.

### 7.2 Matriz mínima de pruebas

| Área | Prueba | Resultado esperado |
|---|---|---|
| Arranque | Iniciar `torno_v3` | QtDragon inicia sin traceback |
| Carga i18n | Revisar log QtVCP | Se carga el `.qm` local español |
| Principal | Recorrer controles | Etiquetas completas y coherentes |
| Modos | Manual, MDI, Auto | Nombres correctos, comportamiento intacto |
| Homing | Inspección sin movimiento | Referenciar no se confunde con cero de pieza |
| Programa | Abrir diálogo de archivo | Acciones y filtros en español |
| G-code | Cargar archivo de prueba | Visualización intacta |
| Herramientas | Abrir tabla | Columnas y acciones comprensibles |
| Offsets | Abrir tabla | Sistemas y acciones sin ambigüedad |
| Límites | Simular/observar mensajes seguros | Advertencia inequívoca |
| E-stop | Activar/desactivar entrada | Estado correctamente traducido |
| Errores | Generar error no motriz | Mensaje completo y variables visibles |
| Apagado | Abrir y cancelar diálogo | Botones y consecuencias claras |
| Reversión | Retirar overrides locales | Regresa QtDragon estándar |

### 7.3 Pruebas de regresión

Antes y después del despliegue:

- comparar SHA-256 de `torno_v3.ini`, `torno_v3.hal`, `custom.hal` y
  `qtvcp_postgui.hal`;
- ejecutar `scripts/verify-config.ps1`;
- confirmar que la pantalla sigue siendo `qtdragon`, no `qtdragon_hd`;
- confirmar que el handler local sólo cambia presentación de textos;
- comparar señales HAL visibles, sin ordenar movimiento;
- cerrar y reiniciar QtDragon al menos tres veces;
- comprobar que un `.qm` ausente o inválido no impide arrancar la interfaz.

## 8. Despliegue

### 8.1 Primera entrega

Desplegar únicamente:

```text
qtdragon/languages/qtdragon_es.ts
qtdragon/languages/qtdragon_es.qm
```

Esta entrega es puramente declarativa. Si falla la carga, QtDragon utiliza los
textos originales.

### 8.2 Segunda entrega

Después de aprobar la primera:

```text
qtdragon/qtdragon_handler.py
qtdragon/languages/qtdragon_es.ts
qtdragon/languages/qtdragon_es.qm
```

El handler local debe desplegarse en un commit separado para que pueda
revertirse sin retirar la traducción estática.

### 8.3 Orden de commits recomendado

1. `docs: define qtdragon spanish glossary and qa plan`
2. `build: add reproducible qtdragon translation tooling`
3. `i18n: add spanish translation for qtdragon 2.9.7 ui`
4. `i18n: backport translatable dynamic messages to qtdragon handler`
5. `test: record qtdragon spanish visual and runtime validation`

## 9. Reversión

### Nivel 1: traducción compilada

Retirar o renombrar:

```text
qtdragon/languages/qtdragon_es.qm
```

QtDragon volverá a mostrar los textos originales.

### Nivel 2: handler local

Retirar o renombrar:

```text
qtdragon/qtdragon_handler.py
```

QtVCP volverá al handler instalado en `/usr/share`.

### Nivel 3: restauración completa

Restaurar el directorio `torno_v3` desde el respaldo previo al despliegue y
verificar sus hashes. No se requiere reinstalar LinuxCNC.

## 10. Riesgos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---:|---:|---|
| QtVCP no encuentra el `.qm` | Media | Bajo | Usar la ruta legado confirmada y revisar el log |
| Texto crítico mal traducido | Media | Alto | Glosario, revisión humana y prueba con operador |
| Placeholders dañados | Baja | Alto | Validador automático antes de compilar |
| Texto recortado | Alta | Medio | QA visual a `1600 x 849` |
| Handler moderno incompatible | Alta | Alto | No copiar `master`; backport mínimo sobre 2.9.7 |
| Cambio funcional accidental en handler | Baja | Alto | Diff restringido y revisión línea por línea |
| Actualización invalida el catálogo | Media | Medio | Hash de origen y regeneración por versión |
| Archivos del sistema sobrescritos | Baja | Medio | No modificar `/usr/share` |
| Traducción parcial de widgets comunes | Alta | Bajo | Inventario visual y fases incrementales |
| `.qm` existente pero inválido | Baja | Medio | `QTranslator.load()==true`, centinelas y QA visual |
| Operador confunde Home y cero pieza | Media | Alto | Terminología explícita y prueba de comprensión |

## 11. Observabilidad y soporte

Durante el arranque se conservará el log QtVCP necesario para responder:

- qué locale detectó Qt;
- qué `.qm` intentó cargar;
- si usó la traducción local o la predeterminada;
- qué handler cargó;
- si se produjo una excepción durante la inicialización.

El procedimiento de diagnóstico debe incluir:

```bash
locale
python3 -c "from PyQt5.QtCore import QLocale; print(QLocale.system().name())"
find /home/cnc/linuxcnc/configs/torno_v3 -name 'qtdragon_*.qm' -print
```

No se deben registrar contraseñas, claves SSH ni variables sensibles.

## 12. Mantenimiento futuro

La traducción está ligada a la versión del `.ui` y del handler, no únicamente a
la versión general de LinuxCNC.

Ante una actualización:

1. guardar los hashes de las nuevas fuentes;
2. regenerar el `.ts` con `pylupdate5`;
3. revisar mensajes nuevos, obsoletos y modificados;
4. recompilar el `.qm`;
5. ejecutar nuevamente la matriz de QA;
6. actualizar `coverage.md`;
7. conservar la traducción anterior en el historial Git, no como archivos
   paralelos dentro de la configuración activa.

Una contribución futura al proyecto LinuxCNC puede enviar `qtdragon_es.ts` y
`qtdragon_es.qm` upstream. La versión local seguirá siendo necesaria mientras
el torno permanezca en una rama que no incluya oficialmente esos archivos.

## 13. Definición de terminado

El trabajo se considera completo únicamente cuando:

- [ ] Qt detecta `es_CO`.
- [ ] QtVCP selecciona el `qtdragon_es.qm` local.
- [ ] `QTranslator.load()` devuelve `true` en una prueba offline.
- [ ] Las traducciones centinela resuelven los contextos exactos esperados.
- [ ] Cobertura de textos estáticos >= 98 %.
- [ ] Cobertura de mensajes dinámicos >= 95 %.
- [ ] Controles y mensajes críticos tienen cobertura del 100 %.
- [ ] Cero textos ingleses no aprobados en los flujos operativos definidos.
- [ ] Los 24 módulos de widgets instanciados están clasificados por visibilidad.
- [ ] No existen errores de placeholders, HTML o caracteres de control.
- [ ] No aparecen textos truncados en la resolución real.
- [ ] Un operador valida la terminología CNC.
- [ ] QtDragon inicia y cierra repetidamente sin traceback.
- [ ] No cambió ningún hash de INI/HAL relacionado con movimiento o seguridad.
- [ ] La reversión fue ejecutada y comprobada una vez.
- [ ] La traducción, herramientas y evidencias están versionadas.
- [ ] El respaldo posterior contiene `.ts`, `.qm` y handler local, si aplica.

## 14. Resultado esperado

La entrega final será una versión de QtDragon coherente en español, adaptada al
torno y mantenida como una capa local sobre LinuxCNC 2.9.7. El controlador
seguirá usando los componentes oficiales de LinuxCNC; únicamente la
presentación de textos será personalizada.

La estrategia evita tres riesgos innecesarios: modificar paquetes de Debian,
mezclar una pantalla moderna con LinuxCNC 2.9.7 y alterar la lógica de la
máquina para resolver un problema exclusivamente lingüístico.
