# Fuentes oficiales — control CNC

Fecha de acceso de todas las fuentes: **2026-08-29**.

| Componente | Título del documento | URL directa oficial | Fabricante / proyecto | Estado | SHA-256 | Páginas PDF | PDF original | Copia Markdown |
|---|---|---|---|---|---|---:|---|---|
| Mesa 7I76E / 7I76ED | 7I76E/7I76ED Ethernet Step/Dir Plus I/O Daughtercard, V1.17 | https://www.mesanet.com/pdf/parallel/7i76eman.pdf | Mesa Electronics | ambiguo | `7a18d60d1d737ec0dd973f8762ccf84542844ba30d71024c2039232a61db57b6` | 86 | `output/pdf/componentes/control/mesa-7i76e-manual.pdf` | `output/docs/componentes/control/mesa-7i76e-manual.md` |
| Mesa 7I76EU | 7I76EU Ethernet Step/Dir Plus I/O Daughtercard, V1.11 | https://www.mesanet.com/pdf/parallel/7i76euman.pdf | Mesa Electronics | ambiguo | `c5d9130ebf2c5c4fffc7466e6d4102ae18cc778ca7e6bfb420a538722e1226d3` | 88 | `output/pdf/componentes/control/mesa-7i76eu-manual-v1.11.pdf` | `output/docs/componentes/control/mesa-7i76eu-manual-v1.11.md` |
| LinuxCNC 2.9 / QtDragon | LinuxCNC V2.9.7-9-gd435482ad1, 22 Oct 2025 — documentación completa (ES) | https://linuxcnc.org/docs/2.9/pdf/LinuxCNC_Documentation_es.pdf | LinuxCNC Project | compatible | `a23364f58377ddbbd5774b5b47f251b62a9c50acae00b2a6b0df816c0b6b49e4` | 1343 | `output/pdf/componentes/control/linuxcnc-2.9-documentacion-es.pdf` | `output/docs/componentes/control/linuxcnc-2.9-documentacion-es.md` |

## Correspondencia con el repositorio

- La configuración activa declara `CARD0=hm2_7i76e.0`. Ese nombre identifica la familia/driver HostMot2, pero no demuestra por sí solo si la placa física es una 7I76E/7I76ED o una 7I76EU.
- El propio repositorio describe el hardware como “Mesa 7I76EU/7I76E”. No hay en el material revisado una fotografía, etiqueta, número de parte o lectura de inventario que resuelva la revisión física. Por ello los dos manuales Mesa se clasifican como **ambiguos**, no intercambiables sin verificar la placa.
- Los manuales muestran diferencias materiales. Entre otras, la 7I76E V1.17 indica alimentación host de 5 V y límites de campo de hasta 32 VDC; la 7I76EU V1.11 incorpora opciones de alimentación lógica no regulada y especifica límites de campo de hasta 28 VDC. Debe verificarse el modelo impreso antes de cablear o seleccionar jumpers.
- La configuración declara LinuxCNC 2.9 y `DISPLAY = qtvcp qtdragon`. El PDF oficial corresponde a la rama 2.9, incluye la sección QtDragon en las páginas PDF 715–746 y se clasifica como **compatible** porque no está confirmado el parche/build exacto instalado.

## Verificación PDF y extracción

- Los tres archivos empiezan con una cabecera PDF válida, no están cifrados y tienen capa de texto nativa; se clasificaron como documentos digitales y no se aplicó OCR.
- La extracción se realizó página por página con PyMuPDF, preservando los límites de página en Markdown. No se registraron errores de extracción.
- La página PDF 2 de cada manual Mesa no contiene texto nativo; es una página intencionalmente vacía en el original. El PDF de LinuxCNC no tiene páginas sin texto nativo.
- Se inspeccionaron visualmente las portadas, planos de conectores, especificaciones y dibujos de ambos manuales Mesa, además de la portada y páginas críticas de QtDragon del manual LinuxCNC. No se observaron páginas rotas, recortadas ni ilegibles en la muestra.
- Las copias Markdown son transcripciones textuales completas, no reproducciones visuales. Los diagramas, capturas y dibujos permanecen íntegros únicamente en los PDF originales; el Markdown conserva los rótulos y pies que forman parte de la capa de texto.
- El inventario auditable, con caracteres por página, páginas vacías, metadatos, parser y páginas renderizadas, está en `output/docs/componentes/control/_inventario_pdf.json`.
