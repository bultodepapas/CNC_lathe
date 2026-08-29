# HBS86H — manual para familia 86HB250 (transcripción completa)

- PDF original: hbs86h_manual_86hb250_reference.pdf
- Fuente: https://cnc-tehnologi.ru/files/HBS86H.pdf
- Páginas: 6
- Emisor: no identificado en el PDF; copia alojada por CNC Technology.
- Estado: referencia específica y compatible con el kit HLTNC; no es un manual oficial HLTNC.
- Método: extracción del texto nativo con pypdf 6.14.2, modo layout. Los diagramas permanecen normativos en el PDF original.

## Página 1

```text
                HBS86H
2-phase Hybrid Stepper Servo Driver


                       1
```

## Página 2

```text
1. Instruction
1.1 Overview
    HBS86H      is  2 phase    nema   34   series  hybrid   stepper   servo  driver. It   adopts   new
generation 32 bit DSP and vector control technology, which can avoid the stepper motor
losing steps and ensure the accuracy of the motor. The torque reducing is much lower
than open loop stepper motor when it is at higher speed. The high speed performance
and torque are enhanced in a great extent. Meanwhile the current control is based on the
load, that can reduce the motor temperature rising effectively, then can extend the using
life of the motor. The build-in place in position and alarm output signal can help the
upper monitor to monitor and          control. The function of position ultra difference alarm
can ensure the machine work safely. The closed loop system is an ideal improvement
and a good replacement of open loop system, Besides that, it also have some function
of AC servo motors, but price is just half of AC servo.
1.2 Features
1.2.1 Stepper motor closed loop system, never lose step.
1.2.2 Improve motor output torque and working speed.
1.2.3 Automatic current adjustment based on load, lower temperature rising.
1.2.4 Suitable for all mechanical load conditions (include low rigidity belt pulley and
wheel), no need to adjust gain parameter.
1.2.5   Motor    work   smoothly and      low vibration,    high   dynamic    performance      at
acceleration and deceleration.
1.2.6 No vibration from high speed to zero speed
1.2.7 Drive nema 34 series 4N.m, 8N.m, 12N.m closed loop stepper motor.
1.2.8 Pulses response frequency can reach 200KHZ
1.2.9 16 kinds microsteps choice, highest 51200microsteps/rev.
1.2.10 Voltage range: AC18~70V or DC24V~100V
1.2.11 Over-current, over-voltage and position ultra difference protection function.
1.3 Applications
Closed loop stepper system can be applied to all kinds small automatic equipment and
Instruments, such as engraving machine, special industrial sewing machine, stripping
machine,      marking       machine,      Dispensing      machine,      cutting     machine,      laser
phototypesetting, graph plotter, NC machine, automatic, assembly equipment and so
on.

2. Electrical, mechanical, environment Parameter

2.1 Electrical Parameter

Voltage range                      AC18~70V or DC24~100V
Peak current                       Peak 8.0A（current change according to load）


                                                   2
```

## Página 3

```text
Logic input current              7~20mA
frequency                        0~200KHz
Suitable motor                   86HB250-156, 86HB250-118, 86HSE8N-BC38
Encoder lines                    1000
Insulation resistance            >=500MΩ
2.2 Environment Parameter

Cooling method             Natural or radiator
Operating                  Operating Occasions        try to avoid dust, oil, corrosion gas
environment                Operating temprature       0~50℃
                           Operating humidit          40~90%RH
                           virbration                 5.9m/s²Max
Storage temperature        -20℃~65℃
Weight                     About 560g


                                                3
```

## Página 4

```text
3. Driver connector, indicator and wiring diagram

3.1 motor and power supply input port

Port NO.
1                    A+                    A phase winding +
2                    A-                    A phase winding -
3                    B+                    B phase winding +
4                    B-                    B phase winding -
5                    AC1                   Input voltage
6                    AC2

3.2. Encoder input port

Port NO.
1                    EB+                   Encoder B phase input+
2                    EB-                   Encoder B phase input-
3                    EA+                   Encoder A phase input+
4                    EA-                   Encoder A phase input-
5                    VCC                   Encoder voltage（+5V）
6                    EGND                  Encoder Grand（0V）
（The encoder wires misconnected will lead to the damage of driver or encoder.）
3.3.      Signal controller port

Port NO.
1              PUL+             Pulse input +                  If the signal control voltage is
                                                               +5V, then the signal control
2              PUL-             Pulse input -                  input port do not need to
                                                               connect an extra resistance. If
3              DIR+             Direction input +              the signal control voltage is
                                                               +12V, then the signal control
4              DIR-             Direction input -              input port need to connect to a
                                                               1K resistance. If the signal
5              ENA+             Enable input +                 control voltage is +12V, then
                                                               the signal control input port
6              ENA-             Enable input -                 need to connect to a 2K
                                                               resistance.
7              PEND+            Position signal output+        OC output, closed indicate
                                                               finish the position, open circuit
8              PEND-            Position signal output-        indicate position is not finished.
9              ALM+             Alarm signal output+           OC output, there is alarm signal
10             ALM-             Alarm signal output-           when closed, no alarm signal
                                                               when open circuit.


                                                  4
```

## Página 5

```text
3.4.       Switch setting
SW5：Rotate direction setting.on=CW，off=CCW.
SW1、SW2、SW3、SW4：Microstep setting
  Micorstep/rev               SW1                   SW2                   SW3                    SW4

 Default（400）                  on                    on                     on                    on

        800                    off                   on                     on                    on

        1600                   on                    off                    on                    on

        3200                   off                   off                    on                    on

        6400                   on                    on                     off                   on

       12800                   off                   on                     off                   on

       25600                   on                    off                    off                   on

       51200                   off                   off                    off                   on

        1000                   on                    on                     on                    off

        2000                   off                   on                     on                    off

        4000                   on                    off                    on                    off

        5000                   off                   off                    on                    off

        8000                   on                    on                     off                   off

       10000                   off                   on                     off                   off

       20000                   on                    off                    off                   off

       40000                   off                   off                    off                   off


                                                      5
```

## Página 6

```text
3.5.     Status indication
PWR：power indicator light : When power is on, the green light is on.
ALM：Alarm indicator light: If the red light is flicker one time within 3 seconds, that
means over current or interphase short circuit; If the red light is flicker twice within 3
seconds, that means over voltage; if the red light is flicker three times within 3 seconds,
that means position ultra difference or the encoder            connector     is disconnected.
3.6.     Wire diagram


3.7.     Wires for Encoder
Standard wire length for encoder is 3 meters. ( Wire length can be customized.)


                                                    6
```
