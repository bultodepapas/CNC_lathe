# Revisión de accionamientos eléctricos

Fecha de revisión: 2026-08-29.

## Identificación confirmada por la compra

El propietario confirmó la publicación HLTNC de AliExpress y la variante `4kit 12Nm, with HBS86H power, 14mm shaft`. La misma configuración aparece en el sitio oficial HLTNC como modelo comercial `12N-HBS86H-400W`.

| Componente | Identificación actual | Estado | Evidencia y límites |
|---|---|---|---|
| Driver | HLTNC HBS86H | **Exacto a nivel de publicación/variante** | La imagen oficial muestra marca, modelo, carcasa y terminales. No hay manual PDF oficial HLTNC accesible; la etiqueta física sigue siendo la autoridad para la revisión concreta. |
| Motor | HLTNC 86HB250-156 / 86HB250-156B, sin freno, eje Ø14 | **Exacto a nivel de publicación/variante** | El sitio HLTNC identifica el modelo y publica dibujo y parámetros. El sufijo aparece como `156B` en la tabla/variante y como `156` en el título; debe copiarse literalmente de la placa real al cerrar el inventario. |
| Fuente | S-400-60, 60 VDC, comercialmente 400 W | **Exacto como familia incluida en el kit** | La imagen HLTNC especifica 60 V, 6.7 A y 402 W. El fabricante OEM de la fuente no está identificado y no se encontró manual PDF primario. |
| Cable encoder | Cable incluido de 3 m | **Exacto en inclusión y longitud** | AliExpress/HLTNC confirman 3 m. El pinout de seis señales y las terminaciones deben comprobarse contra etiquetas/continuidad porque no hay hoja oficial específica del cable. |

## Especificaciones visibles en la publicación oficial HLTNC

### Driver HLTNC HBS86H

- Entrada: AC 18–70 V o DC 24–100 V.
- Corriente pico: 8.0 A.
- Corriente lógica: 7–20 mA.
- Frecuencia de pulsos: 0–200 kHz.
- Encoder: 1000 líneas.
- Motores adecuados: 86HB250-82B, 86HB250-118B y 86HB250-156B.
- Resistencia de aislamiento: ≥500 MΩ.
- Dimensiones exteriores visibles: aproximadamente 152 × 107 × 52 mm.
- Borneras mostradas, en orden: `PUL±`, `DIR±`, `ENA±`; `PEND±`, `ALM±`; `EB±`, `EA±`, `VCC`, `EGND`; `A±`, `B±`; `AC`, `AC`.

### Motor HLTNC 86HB250-156B

| Parámetro | Valor publicado por HLTNC |
|---|---:|
| Fases | 2 |
| Par de retención | 12 N·m |
| Paso | 1.8° ±5 % |
| Tensión | 3.3 VDC |
| Corriente | 6.0 A |
| Resistencia | 0.55 Ω ±10 % |
| Inductancia | 5.2 mH ±20 % |
| Rigidez dieléctrica | 500 VAC / 5 mA / 1 min |
| Resistencia de aislamiento | ≥100 MΩ a 500 VDC |
| Clase | B |
| Cable | RVV 4 × 0.5 mm² |
| Peso sin freno | 5800 g |
| Cuerpo | 156 mm máx. |
| Eje | Ø14 mm, salida 32 ±1 mm, chaveta de 25 mm |

La publicación HLTNC no aporta la inercia del rotor.

### Fuente S-400-60 del kit

- Salida: 60 VDC.
- Corriente nominal y rango: 6.7 A; 0–6.7 A.
- Potencia indicada: 402 W, comercializada como 400 W.
- Tolerancia: ±1 %.
- Rizado/ruido: 150 mV pico a pico.
- Eficiencia: 84 %.
- Ajuste de tensión: ±10 %.
- Dimensiones visibles: 215 × 115 × 50 mm.

## Correcciones frente al BOM anterior

| Elemento | BOM anterior | Evidencia HLTNC confirmada |
|---|---|---|
| Driver | 24–60 VDC, 5 A, 151 × 107 × 29 mm | DC 24–100 V o AC 18–70 V, 8 A pico, aprox. 152 × 107 × 52 mm |
| Motor | 0.45 Ω, 5 kg, inercia 4.9 kg·cm² | 0.55 Ω ±10 %, 5.8 kg; inercia no publicada |
| Fuente | 400 W, 60 VDC | S-400-60, 60 V, 6.7 A, 402 W en la imagen técnica |
| Cable encoder | 3 m | 3 m confirmado |

El plano JSS 86HSE12N-BC38 ya no es la mejor coincidencia y se conserva solo como referencia alternativa. La ficha Gotronik S-400-60 tampoco es exacta porque declara 6.6 A/396 W.

## Estado de los manuales

No se encontró un manual o datasheet PDF primario emitido por HLTNC. Se importó `hbs86h_manual_86hb250_reference.pdf` porque:

- identifica HBS86H y la familia de motor 86HB250-156;
- reproduce las mismas borneras `PUL/DIR/ENA`, `PEND/ALM`, encoder, motor y alimentación;
- especifica AC 18–70 V / DC 24–100 V, 8 A, encoder de 1000 líneas y cable estándar de 3 m.

Su emisor no está identificado; por tanto, es una **referencia específica compatible**, no un manual oficial HLTNC. Los PDF Leadshine siguen siendo comparativos y no exactos.

## Verificación PDF

Los cinco PDF originales se conservaron sin modificación. Todos abren, comienzan con `%PDF-`, no están cifrados y no presentan páginas vacías ni errores de extracción. Se inspeccionaron visualmente todas las seis páginas del manual nuevo y las páginas críticas de los cuatro documentos previos. Los renders temporales fueron eliminados.

