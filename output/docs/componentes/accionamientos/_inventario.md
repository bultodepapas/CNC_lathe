# Inventario final — accionamientos eléctricos

Actualizado y verificado el 2026-08-29.

## Originales PDF conservados

| Archivo | Tamaño (bytes) | Páginas | Copia Markdown | Clasificación actual |
|---|---:|---:|---|---|
| `hbs86h_manual_86hb250_reference.pdf` | 165762 | 6 | `hbs86h_manual_86hb250_reference.md` | referencia específica compatible; no oficial HLTNC |
| `86hse12n_bc38_drawing_jss.pdf` | 449146 | 1 | `86hse12n_bc38_drawing_jss.md` | alternativa, descartada como exacta |
| `hbs86h_datasheet_leadshine.pdf` | 256471 | 7 | `hbs86h_datasheet_leadshine.md` | comparativa Leadshine, no exacta |
| `hbs_series_hardware_manual_leadshine.pdf` | 2262004 | 22 | `hbs_series_hardware_manual_leadshine.md` | comparativa Leadshine, no exacta |
| `s400_60_product_sheet_rd.pdf` | 119062 | 2 | `s400_60_product_sheet_rd.md` | fuente compatible, no exacta |

Ruta PDF: `output/pdf/componentes/accionamientos/`. Total: **5 PDF, 38 páginas**.

## Documentación Markdown

| Archivo | Función |
|---|---|
| `_fuentes.md` | evidencia primaria HLTNC/AliExpress, procedencia PDF, URL, estado y SHA-256 |
| `_revision.md` | identificación confirmada, especificaciones HLTNC, correcciones al BOM y límites |
| `hbs86h_manual_86hb250_reference.md` | transcripción completa de 6 páginas |
| `86hse12n_bc38_drawing_jss.md` | transcripción del plano alternativo JSS |
| `hbs86h_datasheet_leadshine.md` | transcripción completa de 7 páginas |
| `hbs_series_hardware_manual_leadshine.md` | transcripción completa de 22 páginas |
| `s400_60_product_sheet_rd.md` | transcripción completa de 2 páginas |

## Controles finales

- Todos los PDF comienzan con firma `%PDF-`, no están cifrados y tienen SHA-256 reproducible en `_fuentes.md`.
- Las copias Markdown cubren sus páginas completas; el plano vectorial JSS fue transcrito visualmente.
- Las seis páginas del manual HBS86H/86HB250 se renderizaron e inspeccionaron.
- No se encontró ni se inventó un PDF oficial HLTNC.
- Los renders y las imágenes temporales de inspección fueron eliminados; no queda carpeta `_qa`.

