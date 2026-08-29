# Revision de componentes mecanicos

## Resultado

- **Guias HGR20 / carros HGH20CA y HGW20CC:** la nomenclatura y dimensiones aparecen de forma exacta en el catalogo oficial HIWIN. En las paginas PDF 41 y 45 se verificaron visualmente las filas `HGH20CA` y `HGW20CC`: altura de conjunto 30 mm, longitud 77,5 mm, cargas basica dinamica/estatica 27,1/36,68 kN; el ancho es 44 mm para HGH20CA y 63 mm para HGW20CC. Esto no autentica las piezas fisicas como HIWIN.
- **Husillo SFU1605:** el documento TBI vigente confirma una tuerca dimensionalmente equivalente `SFNU01605-4` de diametro 16 mm y paso 5 mm. La sigla no coincide de manera literal con `SFU1605`, por lo cual se conserva como referencia compatible y no como identificacion exacta de marca o variante.
- **Soportes BK12/BF12:** el catalogo TBI contiene `BK-12` y `BF-12`. Ambos tienen A=60, B=46, C=34, E=30, H1=32,5, h=25 y H=43 mm. El extremo BK-12 usa D1=12 mm y el BF-12 D1=10 mm.
- **Soporte DSG16H:** la primera pagina del PDF GREEN LEAF identifica `DSG16H` para tuercas SFU-1604/1605/1610 y SFS-1610/1616/1620. La tabla verificada muestra D=28, B=52, H=40, h=20, E=12, L=40, C1=8, C2=24, P=40, X=M5, W=38 y Y=M5 mm.
- **Acople D25L30-8x10:** la ficha POLTECH confirma acople de mordaza sin juego, aluminio, diametro exterior 25 mm, longitud 30 mm y cubos H7 de 8 y 10 mm. POLTECH figura como emisor/vendedor, no como fabricante demostrado de la pieza del proyecto.
- **NMRV040 100:1 compatible NEMA34:** no se encontro un unico documento primario que confirme simultaneamente las tres condiciones. Motovario confirma `NMRV040` con relacion exacta 100,00 (por ejemplo, pagina PDF 83), pero con motor IEC 56B. El manual STEPPERONLINE/SkyMotor confirma la geometria de NMRV40 usada comercialmente con NEMA34 (brida frontal 85 mm, entrada de 14 mm), pero su tabla solo incluye relaciones hasta 50:1. Hay que verificar placa, relacion grabada, diametro del eje del NEMA34 y patron de agujeros antes del montaje.

## Verificacion de los PDFs y las copias Markdown

- Se comprobaron firma `%PDF`, apertura, cifrado, numero de paginas, SHA-256, texto por pagina y errores de extraccion. El detalle reproducible esta en [_inventario_pdf.json](_inventario_pdf.json).
- Se renderizaron e inspeccionaron las paginas criticas con las referencias y tablas usadas arriba. No se observaron paginas truncadas ni tablas ilegibles en esas regiones.
- Seis documentos poseen texto nativo util. El catalogo GREEN LEAF es un escaneo de 15 paginas sin capa de texto; su Markdown incorpora autocontenida la imagen original de cada pagina y marca expresamente la ausencia de OCR.
- El catalogo Motovario tiene dos paginas sin texto nativo (2 y 327); aparecen marcadas como tales en el Markdown y no contienen valores usados en esta revision.
- Cada PDF conserva sus bytes originales y tiene una copia Markdown con el mismo nombre base.

## Limites de uso

Los catalogos son referencia de seleccion y montaje, no prueba de autenticidad. Antes de mecanizar soportes o pedir repuestos deben medirse el componente real, la precarga, la clase de precision, el patron de taladros, el diametro y tolerancia de ejes, la posicion de lubricacion y la relacion real del reductor.
