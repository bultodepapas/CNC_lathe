# Checklist de QA — QtDragon en español

## Gate 0 — Seguridad operacional

- [ ] El operador confirmó que terminó el trabajo en curso.
- [ ] LinuxCNC se cerró de forma normal.
- [ ] No hay programa automático activo.
- [ ] Se creó y verificó un respaldo recuperable de `torno_v3`.
- [ ] Se registraron hashes de INI, HAL, UI, handler y loader.
- [ ] El alcance no incluye el eje Z en reparación.

Si la primera casilla no está confirmada, sólo se permiten preparación y
pruebas fuera del controlador. No continuar con despliegue.

## Gate 1 — Catálogo fuente `.ts`

- [ ] `language` comienza por `es`.
- [ ] Se generó desde el `qtdragon.ui` con SHA-256 documentado.
- [ ] No hay traducciones terminadas vacías.
- [ ] Cobertura estática >= 98 %.
- [ ] Cobertura de textos críticos = 100 %.
- [ ] Placeholders `%1`, `%n`, `%s`, `{}`, `{0}` y `{nombre}` se conservan.
- [ ] HTML, especialmente `<sup>`, permanece equilibrado.
- [ ] Saltos de línea y espacios significativos fueron revisados.
- [ ] Aceleradores `&` no están duplicados dentro del mismo diálogo.
- [ ] Códigos G/M, HAL, INI, unidades y nombres de archivo no se tradujeron.
- [ ] Duplicados con traducciones diferentes tienen justificación contextual.
- [ ] El operador revisó el glosario crítico.

Comando mínimo:

```powershell
python scripts/qtdragon-i18n/validate_ts.py ruta/qtdragon_es.ts --min-coverage 98
```

## Gate 2 — Catálogo compilado `.qm`

- [ ] Se compiló con Qt 5 / `lrelease` compatible.
- [ ] El archivo no está vacío.
- [ ] `QTranslator.load(ruta_absoluta)` devuelve `true` offline.
- [ ] Una cadena centinela del contexto principal devuelve español.
- [ ] Una cadena centinela con placeholder conserva e interpola su valor.
- [ ] El hash del `.qm` quedó registrado.
- [ ] Una segunda compilación desde el mismo `.ts` produce el resultado esperado
      o se documenta por qué el binario no es reproducible byte a byte.

El log `Using LOCAL translation file` no satisface este gate por sí solo: el
loader 2.9.7 no comprueba el booleano de `QTranslator.load()`.

## Gate 3 — Revisión del handler local

- [ ] Parte exactamente del handler SHA-256 documentado.
- [ ] El diff sólo añade infraestructura i18n y envuelve textos visibles.
- [ ] No cambió condiciones, acciones, HAL, temporizadores ni rutas.
- [ ] Incluye las correcciones posteriores al primer commit oficial de i18n.
- [ ] Los 51 `add_status` fueron clasificados.
- [ ] Diálogos, títulos, `setText` y tooltips fueron inventariados.
- [ ] Pruebas estáticas de sintaxis pasan.
- [ ] El `.ts` se regeneró después del cambio.

## Gate 4 — Despliegue controlado

- [ ] La máquina continúa fuera de producción.
- [ ] Primera entrega: sólo `.ts` y `.qm` en
      `torno_v3/qtdragon/languages/`.
- [ ] Propietario y permisos son correctos.
- [ ] No se modificó `/usr/share` ni `qt_pstat.py`.
- [ ] No se modificó INI ni HAL.
- [ ] Qt detecta `es_CO`.
- [ ] QtVCP selecciona `qtdragon_es.qm` local.
- [ ] QtDragon abre sin traceback.

## Gate 5 — QA visual a 1600 × 849

- [ ] Pantalla principal.
- [ ] Modos Manual, MDI y Auto.
- [ ] Administrador de archivos y controles de copia.
- [ ] Editor de código G.
- [ ] Tabla de herramientas.
- [ ] Tabla de offsets.
- [ ] Calculadora y teclado virtual.
- [ ] Diálogos de confirmación, error, apertura y guardado.
- [ ] Estados E-stop, máquina deshabilitada/habilitada.
- [ ] Estados referenciado/no referenciado.
- [ ] Programa cargado, ejecutando, pausado y abortado.
- [ ] Solicitud y estado de herramienta.
- [ ] Límites y anulación de límites, sin ordenar movimiento.
- [ ] No hay truncamiento, solapamiento ni botones ambiguos.
- [ ] Las capturas antes/después están identificadas por pestaña.

## Gate 6 — Widgets y residuales en inglés

- [ ] Cada uno de los 24 módulos instanciados fue clasificado como visible o no
      visible en los flujos definidos.
- [ ] Todo residual visible tiene responsable, solución o exclusión aprobada.
- [ ] No se parcheó la biblioteca global en `/usr/lib`.
- [ ] Cero textos ingleses en los flujos operativos definidos, salvo exclusiones
      técnicas documentadas.

## Gate 7 — Regresión y reversión

- [ ] Los hashes de INI/HAL coinciden con la línea base.
- [ ] QtDragon inició y cerró tres veces sin excepción.
- [ ] Retirar el `.qm` restaura el inglés sin impedir el arranque.
- [ ] Retirar el handler local restaura el handler del sistema.
- [ ] Se ejecutó una reversión completa de ensayo.
- [ ] Catálogo, binario, handler, manifiesto, capturas y resultados están
      versionados.

