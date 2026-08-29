# Glosario operativo QtDragon — español

## Convención lingüística

Se usa español técnico claro para un operador de torno CNC en Colombia, sin
regionalismos que dificulten el soporte internacional. Los botones usan verbos
breves; los mensajes de riesgo explican la consecuencia.

Este glosario es normativo para el catálogo. Las alternativas sólo se aceptan
cuando el contexto visual cambia el significado.

| Inglés | Traducción preferida | Nota de uso |
|---|---|---|
| Abort | Abortar | Detiene la ejecución; no confundir con pausar |
| Apply | Aplicar | Confirmar un cambio no destructivo |
| Back | Atrás | Navegación |
| Clear | Limpiar | Mensajes/listas; usar “Borrar” para datos |
| Close | Cerrar | Ventana o diálogo |
| Coolant | Refrigerante | Término general |
| Copy | Copiar | Archivos o valores |
| Delete | Eliminar | Debe pedir confirmación si es destructivo |
| E-Stop | Parada de emergencia | Puede abreviarse “Parada E.” si no cabe |
| Feed | Avance | Nunca “alimentación” |
| Feed Override | Corrección de avance | Porcentaje aplicado al avance programado |
| Flood | Refrigerante abundante | Evitar “inundación” |
| G-code | Código G | Conservar letras y números |
| Hard Limit | Final de carrera | Estado físico, no límite de software |
| Home | Referenciar | Acción de buscar referencia máquina |
| Home All | Referenciar todo | Todos los ejes configurados |
| Homed | Referenciado | Estado ya alcanzado |
| Jog | Movimiento manual | En botones estrechos puede usarse “Manual” |
| Lathe | Torno | No “torneadora” en controles breves |
| Limit Override | Anular límites | Acción excepcional y explícita |
| Load | Cargar | Archivo, programa o tabla |
| Machine Coordinates | Coordenadas máquina | Nunca “cero de pieza” |
| Machine On | Máquina habilitada | No significa husillo encendido |
| MDI | MDI | Sigla técnica conservada |
| Mist | Neblina | Tipo de refrigeración |
| Offset | Compensación | “Cero” sólo cuando el contexto sea de pieza |
| Pause | Pausar | Conserva el estado para reanudar |
| Pocket | Posición de torreta | No “bolsillo” |
| Probe | Palpador | “Palpado” para la acción |
| Rapid | Rápido | “Corrección de rápido” para override |
| Reload | Recargar | Vuelve a leer el mismo recurso |
| Resume | Reanudar | Continúa una ejecución pausada |
| Run | Ejecutar | No “correr” |
| Run From Line | Ejecutar desde línea | Debe conservar el número de línea |
| Save | Guardar | Archivo o configuración |
| Spindle | Husillo | Nunca “eje” |
| Spindle Override | Corrección de husillo | Porcentaje de velocidad |
| Tool | Herramienta | Conservar `T1`, `T2`, etc. |
| Tool Change | Cambio de herramienta | Distinguir solicitado/en curso/completado |
| Tool Offset | Compensación de herramienta | Geometría/desgaste según contexto |
| Touch Off | Fijar referencia | En contexto de pieza o herramienta |
| Unhome | Quitar referencia | Evitar “desreferenciar” en botones |
| User | Usuario | Directorio del usuario en archivos |
| Work Offset | Cero de pieza | Usar “sistema de trabajo” si se habla de G54–G59 |

## Elementos que no se traducen

- códigos G y M: `G54`, `G96`, `M3`;
- designadores de eje y coordenada: `X`, `Z`, `U`, `W`;
- unidades: `mm`, `in`, `RPM`, `mm/min`, `mm/rev`;
- nombres de pines/señales HAL;
- claves y secciones INI;
- nombres y extensiones de archivo;
- comandos de terminal, rutas y mensajes que deban coincidir literalmente con
  logs técnicos;
- siglas CNC reconocidas: `MDI`, `DRO`, `CSS`, `G-code`.

## Reglas editoriales críticas

- “Parada de emergencia”, “Pausar” y “Abortar” nunca son sinónimos.
- “Máquina habilitada” y “Husillo encendido” deben ser inequívocos.
- “Referencia máquina” y “cero de pieza” nunca se intercambian.
- En confirmaciones destructivas se nombra el objeto y la acción: “Eliminar el
  archivo…” o “Abortar el programa…”.
- Los valores interpolados, códigos y nombres de archivo deben permanecer
  visibles y sin alteraciones.
- Si una traducción corta pierde precisión, se conserva una etiqueta breve y
  se amplía el tooltip.

## Aprobación

Antes del despliegue final, el operador debe aprobar expresamente al menos:

- Referenciar / quitar referencia;
- cero de pieza / coordenadas máquina;
- correcciones de avance, rápido y husillo;
- abortar / pausar / reanudar;
- anulación de límites;
- solicitud, ejecución y finalización de cambio de herramienta.

