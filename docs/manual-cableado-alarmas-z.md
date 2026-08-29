# Cableado de alarmas Z1 y Z2

## Antes de trabajar

- Desenergizar, bloquear y verificar ausencia de tensión.
- Usar solamente el `VFIELD +24 VDC` de la Mesa. **Nunca usar los 60 V** de
  alimentación de los drivers.
- Confirmar en la placa la marca `TB6` antes de contar pines.

## Cuatro conductores nuevos

| Desde | Hasta |
|---|---|
| Mesa `VFIELD +24 VDC` | Driver **Z1** `ALM+` |
| Driver **Z1** `ALM-` | Mesa **TB6 pin 10 — INPUT9** |
| Mesa `VFIELD +24 VDC` | Driver **Z2** `ALM+` |
| Driver **Z2** `ALM-` | Mesa **TB6 pin 11 — INPUT10** |

```text
VFIELD +24 V ─── Z1 ALM+   Z1 ALM- ─── TB6-10 / INPUT9
VFIELD +24 V ─── Z2 ALM+   Z2 ALM- ─── TB6-11 / INPUT10
```

No conectar nada a `PEND+`, `PEND-`, `ENA+` ni `ENA-` en esta etapa. No hace
falta unir `ALM-` a GND: la entrada Mesa cierra internamente el circuito hacia
`FIELD GND`.

La entrada de la Mesa ya tiene una resistencia interna nominal de 20 kΩ. No se
añade resistencia externa para esta conexión. Usar pares separados, rotulados
`ALM Z1` y `ALM Z2`, alejados de los cables del motor.

## Comprobación obligatoria

Con los motores imposibilitados para moverse:

1. En estado normal, `INPUT9` e `INPUT10` deben aparecer activos.
2. Abrir temporalmente cada circuito `ALM`, uno por vez: su entrada debe pasar a
   inactiva. Esto simula alarma o cable roto; no provocar un atasco real.
3. No operar el torno hasta instalar y probar el cambio HAL que convierte
   cualquiera de esas caídas en fallo simultáneo de Z1 y Z2.

Si alguna entrada funciona al revés, detener la puesta en marcha y revisar la
polaridad/configuración de `ALM` del driver; no ocultarlo invirtiendo HAL.

> El cableado por sí solo no detiene los ejes: LinuxCNC todavía debe configurarse.
> El corte común adicional mediante `ENA` queda pendiente hasta identificar el
> cableado existente y verificar la lógica exacta de esas entradas.

## Referencias

- [Manual Mesa 7I76E: TB6 y entradas de campo](https://www.mesanet.com/pdf/parallel/7i76eman.pdf)
- [Manual HBS86H: terminales y conexión de ALM](https://www.manualslib.com/manual/1576073/Leadshine-Hbs86h.html)
