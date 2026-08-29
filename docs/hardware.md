# CNC Lathe Bill of Materials (BOM)

> Datasheets, manuales, copias Markdown y estado de identificacion:
> [`output/docs/componentes/README.md`](../output/docs/componentes/README.md).
> Las referencias compatibles o ambiguas no sustituyen la lectura de la placa
> o la medicion del componente fisico.

## Control System

| Item | Model / Specification | Quantity |
|-----|-----------------------|---------|
| Control Computer | Hewlett‑Packard Microcomputer, Intel Core i9‑9500T CPU, 16 GB RAM | 1 |
| Motion Control Board | Mesa Electronics 7I76EU Step/Dir I/O daughtercard | 1 |
| Communication | Ethernet connection between PC and Mesa board | 1 |

La identificacion `Core i9-9500T` esta pendiente de corregir: Intel documenta
un `Core i5-9500T`, y el modelo o numero de producto del equipo HP no figura en
el inventario. No se asigno un manual del PC hasta confirmar ambos datos.


## Closed‑Loop Motor Control System

Fuente de compra confirmada por el propietario:
[kit HLTNC de cuatro ejes](https://es.aliexpress.com/item/4000642135176.html),
variante indicada en el pedido como `4kit 12Nm, with HBS86H power, 14mm shaft`.
La publicación identifica el modelo comercial, pero el cableado definitivo debe
seguir las etiquetas impresas en las unidades instaladas.

La imagen técnica suministrada del HLTNC HBS86H muestra estas borneras, en orden:

- Control: `PUL+`, `PUL-`, `DIR+`, `DIR-`, `ENA+`, `ENA-`.
- Estado: `PEND+`, `PEND-`, `ALM+`, `ALM-`.
- Encoder: `EB+`, `EB-`, `EA+`, `EA-`, `VCC`, `EGND`.

También se recibió una imagen de un HBS57H. Ese modelo tiene una distribución
diferente y no muestra `PEND`; no debe usarse como referencia de cableado para
los Z si las unidades instaladas son HBS86H.

Fotografías posteriores del tablero confirmaron dos HLTNC HBS86H instalados y
rotulados `Z1` y `Z2`, ambos encendidos con LED verde. En los dos drivers:

- El bloque de cuatro salidas `PEND+/PEND-/ALM+/ALM-` está sin conductores.
- El cable fino multicolor entra en el bloque inferior de seis entradas del
  encoder, no en el bloque de alarmas.
- El conector superior de control parece tener ocupadas las seis posiciones,
  incluidas `ENA+` y `ENA-`; se necesita una prueba de continuidad para saber a
  dónde llegan esos dos conductores.

La tarjeta de movimiento visible es una Mesa 7I76EU.

| Item | Model / Specification | Quantity |
|-----|-----------------------|---------|
| Hybrid Closed‑Loop Stepper Driver | HLTNC HBS86H Hybrid Servo Drive | 4 |
| Closed‑Loop Stepper Motor | HLTNC 86HB250‑156/156B, NEMA 34, 12 Nm, 14 mm shaft | 4 |
| Encoder Cable | 3 meter encoder cable (included with motor kit) | 4 |
| Switching Power Supply | S‑400‑60, 60 VDC, 6.7 A, 402 W (commercially 400 W) | 4 |


### HLTNC HBS86H Driver Technical Specifications

- Input voltage: **18–70 VAC or 24–100 VDC**
- Maximum peak current: **8 A**
- Logic input current: **7–20 mA**
- Maximum pulse frequency: **200 kHz**
- Control interface: **Step / Direction**
- Encoder feedback: **1000 lines**

Driver dimensions:

- Height: **approximately 152 mm**
- Width: **107 mm**
- Depth: **approximately 52 mm**


### HLTNC 86HB250‑156/156B Motor Technical Specifications

- Motor type: **Hybrid closed‑loop stepper**
- Frame size: **NEMA 34**
- Holding torque: **12 Nm**
- Step angle: **1.8°**
- Phase number: **2**
- Rated current: **6 A**
- Shaft diameter: **14 mm**
- Phase resistance: **0.55 Ω ±10%**
- Phase inductance: **5.2 mH**
- Insulation class: **Class B**
- Insulation resistance: **100 MΩ @ 500 VDC**
- Rotor inertia: **not published in the located HLTNC source**
- Motor weight without brake: **5.8 kg**

El sufijo aparece como `156B` en la tabla/variante y como `156` en el titulo
comercial. Debe copiarse literalmente de la placa del motor antes de pedir un
repuesto.


### Motor Allocation

| Machine Function | Motor Quantity |
|------------------|---------------|
| Z Axis (dual ball screw drive) | 2 |
| X Axis | 1 |
| Tool Turret Drive | 1 |


## Linear Motion System

| Item | Model / Specification | Quantity |
|-----|-----------------------|---------|
| Linear Guide Rail | HGR20 | 2 |
| Linear Guide Block | HGH20CA / HGW20CC | 4 |


## Ball Screw System

| Item | Model / Specification | Quantity |
|-----|-----------------------|---------|
| Ball Screw (Z Axis) | SFU1605 – long screws | 2 |
| Ball Screw (X Axis) | SFU1605 – short screw | 1 |
| Ball Screw Support Set | BK/BF12 | 1 set |
| Ball Screw Nut Seat | DSG16H | 1 |
| Shaft Coupling | D25L30‑8×10 | 1 |


## Tool Turret Drive

| Item | Model / Specification | Quantity |
|-----|-----------------------|---------|
| Worm Gear Reducer | NMRV040 | 1 |

Specifications:

- Gear ratio: **100:1**
- Compatible motor: **NEMA 34**
- Application: **4‑tool indexing turret**


## Hardware Summary

| Component Category | Quantity |
|-------------------|---------|
| Control Computer | 1 |
| Motion Control Board | 1 |
| Closed‑Loop Drivers | 4 |
| NEMA34 Motors | 4 |
| Encoder Cables | 4 |
| Power Supplies | 4 |
| Linear Rails | 2 |
| Linear Blocks | 4 |
| Ball Screws | 3 |
| Worm Gear Reducer | 1 |
