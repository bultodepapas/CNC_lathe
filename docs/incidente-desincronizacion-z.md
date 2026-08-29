# Incidente: pérdida de sincronismo del eje Z tándem

## Síntoma reportado

El eje Z utiliza dos motores, dos drivers y dos husillos. Si el carro encuentra
resistencia o se atasca por viruta, madera u otro obstáculo, un husillo puede
detenerse mientras el otro continúa. La estructura se descuadra y se rompen los
tornillos plásticos instalados como elementos mecánicos sacrificiales.

El operador corrigió el reporte inicial: cuando se activa un fin de carrera, los
dos lados sí se detienen. Por tanto, los límites no están provocando el problema
descrito. El fallo aparece específicamente ante una obstrucción o frenado
mecánico del carro.

Los tornillos plásticos han limitado el daño y deben conservarse mientras se
valida una protección mejor. No obstante, son la última barrera: el control debe
detener ambos lados antes de cargar esos elementos hasta rotura.

## Análisis de causa raíz

Hay que distinguir el evento que inicia el problema del defecto que permite que
se convierta en daño:

| Nivel | Causa |
|---|---|
| Disparador | El carro encuentra una resistencia anormal; uno de los dos conjuntos motor/driver/husillo llega primero a su límite de torque, error de posición o capacidad mecánica. |
| Causa del descuadre | El fallo de ese driver no se comunica a LinuxCNC ni deshabilita el driver del otro lado. |
| Consecuencia | El lado sano continúa recibiendo pulsos, el eje Z se retuerce y rompe el elemento plástico sacrificial. |

La causa raíz del daño repetitivo es, por tanto, la ausencia de una detección e
interbloqueo común entre los dos accionamientos Z. La obstrucción explica por qué
se detiene el primer lado, pero una obstrucción aislada no debería permitir que
el segundo lado continúe.

### Evidencia en la configuración

Los drivers HBS86H cierran internamente el lazo con el encoder de cada motor,
pero LinuxCNC no recibe esa posición real. En HAL:

- `joint.1.motor-pos-fb` recibe `stepgen.01.position-fb`.
- `joint.2.motor-pos-fb` recibe `stepgen.02.position-fb`.
- No hay señales conectadas a `joint.1.amp-fault-in` ni
  `joint.2.amp-fault-in`.

La posición del stepgen representa los pulsos generados, no la rotación física
del motor. Si el primer driver se protege o el motor no puede vencer un atasco,
LinuxCNC puede seguir creyendo que ambos lados avanzan correctamente y mantener
el comando al segundo motor.

La corrección del operador confirma además que la ruta de parada común de
LinuxCNC funciona: los límites están conectados a las dos juntas y detienen ambos
lados. Lo que falta es que la condición interna de cada driver entre por una
ruta equivalente.

`FERROR` y `MIN_FERROR` no resuelven esta falla mientras la realimentación siga
procediendo del stepgen. Reducir esos números únicamente produciría una
tolerancia menor sobre una posición calculada, no sobre la posición mecánica.

LinuxCNC dispone específicamente de `joint.N.amp-fault-in` para recibir fallas
externas del accionamiento. El HBS86H documenta salidas `ALM+`/`ALM-` y una alarma
por error de posición, además de otras protecciones. La polaridad y variante
exacta deben confirmarse en los drivers instalados.

## Homing y límites: mejora separada, no causa del incidente

La configuración actual conecta una sola entrada de home Z a ambas juntas y
una sola entrada por cada extremo a los dos límites:

```text
input-02-not -> joint.1.home-sw-in y joint.2.home-sw-in
input-06-not -> límites negativos de joint.1 y joint.2
input-07-not -> límites positivos de joint.1 y joint.2
```

Además, ambas juntas usan `HOME_SEQUENCE = 2`. LinuxCNC permite homing individual
con secuencias positivas. Para un eje tándem, una secuencia negativa común
sincroniza el movimiento final y bloquea el jogging individual de las juntas
antes del homing, reduciendo el riesgo de descuadre. El cambio a `-2` no debe
hacerse remotamente sin revisar sensores, geometría y procedimiento de escuadra.

Con un único sensor compartido, LinuxCNC tampoco puede saber cuál lado llegó
primero ni escuadrar los dos husillos por separado. Lo preferible es un sensor de
home por cada lado, en entradas diferentes.

Esta mejora sigue siendo recomendable, pero no explica el atasco durante el
movimiento normal ni debe distraer de la conexión urgente de las alarmas de los
drivers.

## Por qué se detiene primero un solo lado

El interbloqueo faltante está demostrado por HAL. Todavía debe identificarse el
motivo exacto por el que un lado pierde movimiento antes que el otro. Las causas
posibles, en orden práctico de comprobación, son:

1. El HBS86H entra en alarma de error de posición al no poder vencer la carga.
2. Un lado tiene mayor fricción, desalineación, precarga o contaminación.
3. Los dos drivers tienen ajustes distintos de corriente o umbral de error.
4. Una fuente de 60 V, cable, conector de motor o encoder cae bajo carga.
5. El motor sigue girando, pero patina o falla el acople o elemento plástico.
6. La velocidad/aceleración deja poco margen de torque y la pequeña obstrucción
   hace que el lado más débil cruce primero el umbral.

No se debe adivinar cuál es. En el próximo evento hay que observar, antes de
reiniciar o apagar:

- Qué lado se detuvo: Z1 o Z2, siempre identificados de la misma forma.
- Si el eje del motor se detuvo o continuó mientras el husillo dejó de girar.
- LED rojo y número/patrón de alarma del HBS86H detenido.
- Estado del segundo driver.
- Lugar físico y causa visible de la resistencia.

Si siempre falla el mismo lado, la búsqueda se concentra en ese driver, fuente,
motor, encoder, acople y mecánica. Si alterna según el lugar del atasco, el
problema dominante es la carga mecánica y la falta de interbloqueo común.

## Corrección recomendada

### Etapa 1 — alarma común de ambos accionamientos

1. Confirmar en cada driver la marca, versión, bornes `ALM+`/`ALM-`, polaridad y
   estado normal/falla.
2. Llevar la alarma de Z1 y Z2 a dos entradas libres distintas de la Mesa,
   mediante el circuito de adaptación correcto para 24 V.
3. Conectar cada señal a su `joint.N.amp-fault-in` en HAL.
4. Combinar ambas alarmas para deshabilitar los dos drivers Z, no únicamente el
   lado que detectó la falla.
5. Preferiblemente, usar también un circuito cableado o relé de interfaz que
   retire `ENA` a ambos drivers aunque LinuxCNC o la red Ethernet fallen.

La salida de alarma del driver no debe asumirse como dispositivo de seguridad
certificado. Sirve para protección de la máquina; la protección de personas
continúa dependiendo de E-stop, contactores y diseño eléctrico adecuado.

### Etapa 2 — sensores independientes

1. Instalar o separar home Z1 y home Z2 en dos entradas Mesa.
2. Si hay límites por lado, conectarlos también por separado para identificar
   cuál costado se activó.
3. Configurar ambas juntas con secuencia sincronizada y realizar el escuadrado
   mediante `HOME_OFFSET` individuales.

### Etapa 3 — validación y protección mecánica

1. Mantener los tornillos plásticos sacrificiales durante las pruebas.
2. Añadir guardas, fuelles o limpiadores para impedir la entrada de viruta y
   fragmentos al carro y husillos.
3. Considerar acoples limitadores de torque si la mecánica lo permite.
4. Ajustar el umbral de error del HBS86H para que la alarma ocurra antes de la
   rotura, evitando falsos disparos durante aceleración normal.

## Medidas temporales

Hasta instalar la realimentación de alarma:

- No operar el eje Z sin supervisión directa.
- Reducir significativamente velocidad y aceleración Z mediante una prueba
  controlada; actualmente llegan a 100 mm/s y 1000 mm/s².
- Limpiar y revisar el recorrido completo antes de cada ciclo.
- No puentear límites ni continuar después de un descuadre: detener, liberar la
  carga, escuadrar y volver a hacer homing.
- Verificar si el LED rojo o código de alarma del driver que se detiene coincide
  con cada rotura; registrar el código antes de apagarlo.

## Prueba de aceptación propuesta

La prueba debe hacerse con el husillo apagado, velocidad muy reducida y medios
para retirar energía:

1. Activar manualmente la alarma Z1 sin mover el carro: ambos enables Z deben
   caer y LinuxCNC debe indicar falla de junta.
2. Repetir con Z2.
3. Desconectar un conductor de alarma: el diseño fail-safe debe generar falla.
4. Activar cada límite y confirmar que no queda un lado recibiendo pulsos.
5. Realizar homing y medir la escuadra en ambos extremos.
6. Sólo después efectuar una prueba de atasco controlada con el elemento
   sacrificial instalado y carga mínima.

## Referencias técnicas

- [LinuxCNC MOTION: `joint.N.amp-fault-in`](https://linuxcnc.org/docs/html/man/man9/motion.9.html)
- [LinuxCNC 2.9: secuencia de homing sincronizada](https://www.linuxcnc.org/docs/2.9/html/es/config/ini-homing.html)
- [Mesa 7I76E: características de entradas de campo](https://www.mesanet.com/pdf/parallel/7i76eman.pdf)
- [Leadshine HBS86: salida de alarma y error de seguimiento](https://leadshineusa.com/UploadFile/Down/HBS86Hd.pdf)
