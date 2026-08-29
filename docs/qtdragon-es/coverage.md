# Cobertura de español para QtDragon 2.9.7

## Propósito

Este documento es el registro auditable de cobertura. Un porcentaje global no
es suficiente: los textos provienen de capas distintas y cada una requiere un
mecanismo diferente.

Fecha de línea base: 2026-08-29. La captura se hizo en sólo lectura mientras el
torno producía; no se modificó ni reinició LinuxCNC.

## Identidad de la línea base

| Componente | SHA-256 |
|---|---|
| `qtdragon.ui` | `d50bc9c3919302d7ec5fa7df9443ee8e852837b51f6adb555968a261b95d2039` |
| `qtdragon_handler.py` | `b00f5b5a5c3acace9c2a2fb997d5e53d561df1533c5e06c118d3fc149d6d3d03` |
| `qt_pstat.py` | `fa504445b7ceca48e07de5b7cf24532a8c7809da96eafc100983d2d31f95ef19` |
| `/usr/bin/qtvcp` | `1ca0cd23ccc5c05918aa39d47e1ded1b2242b1130488c4ff7c85129b3b6f6159` |

El detalle completo está en
`vendor/linuxcnc-2.9.7-qtdragon/manifest.json`. Si cambia cualquiera de estos
hashes, se debe regenerar el catálogo y repetir la revisión.

## Modelo de cobertura

| Bucket | Línea base | Meta | Estado actual | Evidencia requerida |
|---|---:|---:|---|---|
| A. UI estática | 696 nodos traducibles; 619 no vacíos; 346 fuentes únicas | >= 98 % y 100 % crítico | 100 % estructural; QA visual pendiente | Informe de `validate_ts.py`, carga `.qm`, capturas |
| B. Handler QtDragon | 51 `add_status`; cinco estructuras de diálogo; otros `setText`/títulos/tooltips | >= 95 % y 100 % crítico | 0 % traducible | Diff mínimo, extracción TS y matriz de estados |
| C. Widgets QtVCP visibles | 25 clases de 24 módulos; literales candidatos sin i18n | 100 % en flujos definidos | Sin clasificar | Inventario visual y prueba por widget |
| D. Diálogos estándar Qt | Catálogos `qtbase_es.qm` presentes | 100 % en flujos definidos | Por verificar | Capturas de abrir/cancelar/confirmar |
| E. LinuxCNC/core | Gettext y documentación española instalados | 100 % en mensajes críticos del flujo | Por verificar | Registro de estados y errores seguros |
| F. Términos técnicos conservados | Códigos, unidades, HAL, INI y nombres de archivo | 100 % conforme a política | Por clasificar | Lista de exclusiones aprobada |

“0 % traducible” en el bucket B significa que el handler instalado no llama a
`QCoreApplication.translate`; un `.qm` no puede interceptar esos literales.

## Inventario estático confirmado

| Métrica de `qtdragon.ui` | Cantidad |
|---|---:|
| Nodos `<string>` | 718 |
| Marcados `notr=true` | 22 |
| Potencialmente traducibles | 696 |
| Traducibles no vacíos | 619 |
| Fuentes únicas no vacías | 346 |

Reproducción:

```powershell
python scripts/qtdragon-i18n/analyze_sources.py --pretty
```

## Widgets instanciados por la UI activa

Los conteos siguientes son candidatos heurísticos, no promesas de textos
visibles. Incluyen posibles falsos positivos técnicos; deben clasificarse con
la interfaz real detenida y sin movimiento.

| Módulo | Clase(s) | Llamadas candidatas | Literales candidatos |
|---|---|---:|---:|
| `action_button` | `ActionButton` | 10 | 10 |
| `action_tool_button` | `ActionToolButton` | 0 | 0 |
| `axis_tool_button` | `AxisToolButton` | 7 | 13 |
| `camview_widget` | `CamView` | 1 | 1 |
| `dro_widget` | `DROLabel` | 1 | 1 |
| `file_manager` | `FileManager` | 25 | 27 |
| `gcode_editor` | `GcodeEditor` | 22 | 23 |
| `gcode_graphics` | `GCodeGraphics` | 5 | 5 |
| `jog_increments` | `JogIncrements` | 0 | 0 |
| `led_widget` | `LED` | 0 | 0 |
| `machine_log` | `MachineLog` | 0 | 0 |
| `mdi_line` | `MDILine` | 6 | 7 |
| `offset_tool_button` | `OffsetToolButton` | 7 | 11 |
| `origin_offsetview` | `OriginOffsetView` | 3 | 3 |
| `screen_options` | `ScreenOptions` | 11 | 15 |
| `simple_widgets` | `IndicatedPushButton`, `PushButton` | 1 | 1 |
| `state_label` | `StateLabel` | 2 | 2 |
| `state_led` | `StateLED` | 0 | 0 |
| `status_label` | `StatusLabel` | 3 | 3 |
| `status_slider` | `StatusSlider` | 0 | 0 |
| `system_tool_button` | `SystemToolButton` | 0 | 0 |
| `tool_offsetview` | `ToolOffsetView` | 3 | 3 |
| `virtualkeyboard` | `VirtualKeyboard` | 2 | 2 |
| `web_widget` | `WebWidget` | 1 | 1 |

Ejemplos prioritarios ya encontrados en `file_manager`: `Paste`, `Copy`,
`User`, `Load`, `Add Jump`, `Del Jump`, `Show Copy Controls` y sus tooltips.

## Regla de cálculo

Cada mensaje activo del `.ts` cuenta una vez por contexto. Un mensaje se
considera cubierto sólo si:

1. no está marcado `unfinished`;
2. la traducción no está vacía;
3. conserva placeholders, HTML y datos técnicos;
4. fue revisado contextualmente;
5. aparece correctamente en la geometría real si forma parte de un flujo
   operativo.

Los textos deliberadamente conservados no se cuentan como “inglés pendiente”
si están documentados en el bucket F.

## Historial de mediciones

| Fecha | Fuente | A | B | C | D | E | Resultado |
|---|---|---:|---:|---:|---:|---:|---|
| 2026-08-29 | Línea base 2.9.7 | 0 % | 0 % | Sin clasificar | Sin verificar | Sin verificar | Preparación |
| 2026-08-29 | Primera pasada offline | 100 % estructural | 0 % | Sin clasificar | Sin verificar | Sin verificar | TS/QM válidos; falta QA visual |

## Artefactos de primera pasada

| Archivo | Resultado | SHA-256 |
|---|---|---|
| `qtdragon_es.ts` | 346/346; 250 traducidos y 96 preservados | `0634f268d6640faf046b12fca2a994023b2b6e63b3f509682e978c0fa344125b` |
| `qtdragon_es.qm` | 30 954 bytes; carga Qt válida | `ad69d88c35e4a4f4b14d095373e656794d73997f8be6a3efccba8fe7dea8318b` |

Centinelas offline aprobados bajo el contexto exacto `MainWindow`: `MAIN` →
`PRINCIPAL`, `HOME` → `REFERENCIAR`, `CYCLE\nSTART` → `INICIAR\nCICLO` y
`%d %%` conservado. “100 % estructural” significa que el catálogo está completo
y consistente; no afirma todavía que todos los textos quepan o sean preferidos
por el operador.
