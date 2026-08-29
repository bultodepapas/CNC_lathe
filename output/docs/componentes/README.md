# Biblioteca tecnica de componentes

Fecha de recopilacion: **2026-08-29**.

Esta biblioteca conserva por separado los PDF descargados y sus copias
Markdown. Los PDF son los originales sin modificar. Cada grupo incluye una
tabla de fuentes con URL, emisor, SHA-256, numero de paginas y resultado de la
comparacion con el inventario de `docs/hardware.md`.

## Como interpretar el estado

- **Exacto en catalogo**: la referencia aparece literalmente en el documento,
  pero esto no autentica la marca de la pieza fisica.
- **Compatible**: coinciden familia o dimensiones utiles; no debe asumirse que
  es la misma variante instalada.
- **Ambiguo**: faltan marca, modelo, etiqueta o datos suficientes para asignar
  el documento a la pieza real.

## Indice

| Componente del inventario | Documentacion importada | Estado |
|---|---|---|
| Mesa 7I76E / 7I76EU | [Fuentes y correspondencia](control/_fuentes.md) | Ambiguo entre 7I76E/ED y 7I76EU; verificar la serigrafia fisica antes de cablear o mover jumpers. |
| LinuxCNC 2.9 / QtDragon | [Manual oficial 2.9 en Markdown](control/linuxcnc-2.9-documentacion-es.md) | Compatible con la rama 2.9; el equipo reporta 2.9.7. |
| HLTNC HBS86H | [Revision de accionamientos](accionamientos/_revision.md) | Kit y variante confirmados; no se localizo un manual PDF primario HLTNC. Leadshine queda solo como comparativa. |
| HLTNC 86HB250-156/156B, 12 N.m, eje de 14 mm | [Manual compatible HBS86H/86HB250](accionamientos/hbs86h_manual_86hb250_reference.md) | Modelo comercial confirmado; falta resolver el sufijo exacto en la placa. El PDF no es oficial HLTNC. |
| Fuente HLTNC S-400-60, 60 VDC | [Fuentes de accionamientos](accionamientos/_fuentes.md) | Familia incluida confirmada; fabricante OEM y manual PDF no identificados. |
| Cable de encoder HLTNC de 3 m | [Fuentes de accionamientos](accionamientos/_fuentes.md) | Inclusion y longitud confirmadas; pinout fisico pendiente de continuidad/etiqueta. |
| HGR20, HGH20CA, HGW20CC | [Catalogo HIWIN HG/QH](mecanica/HIWIN_catalogo_guias_lineales_HG_QH.md) | Referencias exactas en catalogo; marca de las piezas fisicas sin confirmar. |
| SFU1605 | [Catalogo TBI Motion](mecanica/TBI_MOTION_catalogo_husillos_bolas_SFU.md) | Compatible: documenta una variante 16 x 5, no autentica el SFU1605 instalado. |
| BK12 / BF12 | [Unidades de soporte TBI Motion](mecanica/TBI_MOTION_unidades_soporte_BK_BF.md) | Referencias exactas en catalogo; fabricante fisico sin confirmar. |
| DSG16H | [Catalogo Green Leaf](mecanica/GREENLEAF_catalogo_rodamientos_soporte_DSG.md) | Referencia exacta en catalogo escaneado; fabricante fisico sin confirmar. |
| D25L30-8x10 | [Ficha Poltech](mecanica/POLTECH_ficha_acople_mordaza_D25L30_8x10.md) | Coincide tipo y dimensiones; Poltech es el emisor, no prueba el fabricante. |
| NMRV040, 100:1, NEMA 34 | [Revision mecanica](mecanica/_revision.md) | Ambiguo: ningun documento confirma simultaneamente las tres condiciones. |
| PC Hewlett-Packard, 16 GB, supuesto "Core i9-9500T" | Sin manual asignado | Identificacion inconsistente: Intel documenta `i5-9500T`, no `i9-9500T`; falta modelo HP o numero de producto/serie. |

## Inventarios auditables

- [Control: fuentes](control/_fuentes.md) e [inventario PDF](control/_inventario_pdf.json).
- [Accionamientos: fuentes](accionamientos/_fuentes.md), [revision](accionamientos/_revision.md) e [inventario](accionamientos/_inventario.md).
- [Mecanica: fuentes](mecanica/_fuentes.md), [revision](mecanica/_revision.md) e [inventario PDF](mecanica/_inventario_pdf.json).

## Datos que faltan para cerrar las identificaciones

1. Fotografia legible de la serigrafia y jumpers de la tarjeta Mesa.
2. Fotografia de la placa frontal y lateral de cada HBS86H.
3. Etiqueta completa de un motor, una fuente de 60 V y ambos extremos del cable
   de encoder.
4. Etiquetas, grabados o facturas de guias, husillos, soportes y acople.
5. Placa del reductor NMRV040 y medicion de su brida, eje de entrada y relacion
   real.
6. Modelo exacto, product number o service tag del PC HP y salida de
   `lscpu | grep 'Model name'`.

No deben usarse los documentos marcados como compatibles o ambiguos para fijar
corriente, tension, jumpers, mecanizados o repuestos sin contrastarlos con el
componente fisico.
