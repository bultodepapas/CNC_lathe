# Archivo de importación

Este directorio conserva archivos recibidos que no deben mezclarse con la
configuración activa hasta establecer su procedencia.

`imported/linuxcnc-1.var` parece una segunda copia de `linuxcnc.var`. La única
diferencia observada inicialmente es el parámetro persistente `5223`, con valor
`150.000000` en la copia archivada y `0.000000` en la activa. No se debe elegir
una de las dos sin confirmar qué sistema de coordenadas estaba vigente en la
máquina al copiarla.

`imported/local-capture-20260829/` conserva la captura plana recibida antes de
entrar por SSH. Fue reemplazada en el árbol operativo por los archivos que la
máquina tenía cargados y ejecutando ese mismo día.
