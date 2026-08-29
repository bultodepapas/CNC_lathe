# Fuentes de componentes mecanicos

Fecha de acceso para todas las fuentes: **2026-08-29**.

Estados usados:

- **Exacto**: la referencia aparece literalmente y el documento corresponde al fabricante o proveedor indicado.
- **Compatible**: coinciden familia y dimensiones funcionales, pero el fabricante de la pieza instalada no esta demostrado.
- **Ambiguo**: ningun documento confirma por si solo toda la combinacion solicitada.

| Componente | Titulo / documento | URL directa | Fabricante o emisor | Estado | SHA-256 | Paginas | PDF local | Markdown local |
|---|---|---|---|---|---|---:|---|---|
| HGR20, HGH20CA, HGW20CC | Linear Guideway, HG Series | https://www.hiwin.us/wp-content/uploads/Linear_Guideway-E-1.pdf | HIWIN Corporation USA | **Exacto en catalogo**; no demuestra que la pieza fisica del repo sea HIWIN | `9ded66067f740e90837e3a355b886782ec0ca2a12cf5e37907de49b800733103` | 245 | [PDF](../../../pdf/componentes/mecanica/HIWIN_catalogo_guias_lineales_HG_QH.pdf) | [MD](HIWIN_catalogo_guias_lineales_HG_QH.md) |
| SFU1605 | TBI MOTION Ball Screw | https://i0528.tbimotion.com.tw/storage/pdf/TBIMOTION_BallScrew_25.02-1F%28EN%29.pdf | TBI MOTION | **Compatible / ambiguo**: el catalogo actual contiene `SFNU01605-4` (16 x 5), no demuestra fabricante ni sufijo de la pieza generica `SFU1605` | `26016dac2c8238f16e47eaaaced604f087184be591f9b41e246af3f29ff49665` | 88 | [PDF](../../../pdf/componentes/mecanica/TBI_MOTION_catalogo_husillos_bolas_SFU.pdf) | [MD](TBI_MOTION_catalogo_husillos_bolas_SFU.md) |
| BK12 / BF12 | Linear Ball Bearing Series / Support Unit of Ball Screw / Coupling | https://i0528.tbimotion.com.tw/storage/pdf/TBIMOTION_Other_25.02%28EN%29.pdf | TBI MOTION | **Compatible**: aparecen `BK-12` y `BF-12`; fabricante de las unidades fisicas no verificado | `f2d4a9472213fd4b62e119b8215c2ca5512d1811db0f8ddcd962f4daa1e85495` | 35 | [PDF](../../../pdf/componentes/mecanica/TBI_MOTION_unidades_soporte_BK_BF.pdf) | [MD](TBI_MOTION_unidades_soporte_BK_BF.md) |
| DSG16H | Linear Bearings / DSG Ball Screw Nut Support | https://www.zjgreenleaf.com/download/5-linear-bearing.pdf | GREEN LEAF / Zhejiang Green Leaf Machinery | **Compatible**: aparece literalmente `DSG16H` y declara compatibilidad con SFU-1604/1605/1610; fabricante fisico no verificado | `14cbc3773a2b7a128d227a45dd30bdff462e553eb06809710ece16ac0f65fa8b` | 15 | [PDF](../../../pdf/componentes/mecanica/GREENLEAF_catalogo_rodamientos_soporte_DSG.pdf) | [MD](GREENLEAF_catalogo_rodamientos_soporte_DSG.md) |
| Acople D25L30-8x10 | Sprzeglo bezluzowe klowe CNC D25 L30 - 8x10 mm | https://poltech24.pl/sprzeglo-bezluzowe-klowe-cnc-d25l30-8x10-mm-kartapdf-263.html | Poltech s.c. (ficha de proveedor; fabricante no declarado) | **Exacto en dimensiones y tipo**, fabricante de la pieza fisica ambiguo | `836a09b5f1d4c78f943882ba2f487406180499eb9a28779111b5dd64ca358aa4` | 4 | [PDF](../../../pdf/componentes/mecanica/POLTECH_ficha_acople_mordaza_D25L30_8x10.pdf) | [MD](POLTECH_ficha_acople_mordaza_D25L30_8x10.md) |
| NMRV040, relacion 100:1 | Technical Catalogue VSF Series / Standard / IEC | https://my.motovario.com/uploads/pdf_static/TECHNICAL%20CATALOGUE_VSF_IEC_STD_EN_rev0_2017.pdf | Motovario | **Compatible / ambiguo**: confirma `NMRV040` e `i=100,00`, pero con interfaz IEC (por ejemplo 56B), no NEMA 34 | `1871eba830bee1b4c0b114e00a7a1a1e2a570a092bdf2b411cd133955b14c154` | 328 | [PDF](../../../pdf/componentes/mecanica/MOTOVARIO_catalogo_tecnico_VSF_NMRV_IEC.pdf) | [MD](MOTOVARIO_catalogo_tecnico_VSF_NMRV_IEC.md) |
| NMRV40, interfaz geometrica asociada a NEMA 34 | Worm Gear Speed Reducer NMRV30/40/50 | https://www.skysmotor.co.uk/images/upload/File/NMRV030-40-50%288%29.pdf | STEPPERONLINE, copia alojada por SkyMotor | **Compatible / ambiguo**: confirma geometria NMRV40 (entrada de 14 mm y brida de 85 mm), pero su tabla NMRV40 solo cubre 5:1 a 50:1 y el PDF no rotula literalmente `NEMA 34` | `8317f0de3707173cfda64c5299a5338d45c7a4bd64c21adc0206cb503d3f0add` | 7 | [PDF](../../../pdf/componentes/mecanica/SKYSMOTOR_manual_NMRV30_40_50_NEMA.pdf) | [MD](SKYSMOTOR_manual_NMRV30_40_50_NEMA.md) |

## Nota de atribucion

Las referencias `SFU1605`, `BK/BF12`, `DSG16H`, `D25L30-8x10` y `NMRV040` circulan en productos de multiples fabricantes. La presencia de la misma nomenclatura en un catalogo no autentica la marca de una pieza generica. Para atribuir fabricante se requiere placa, grabado, embalaje, factura o trazabilidad del componente fisico.
