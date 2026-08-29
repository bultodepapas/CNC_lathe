# Leadshine HBS86H — datasheet (transcripción completa)

- PDF original: hbs86h_datasheet_leadshine.pdf
- Fuente: https://leadshineusa.com/UploadFile/Down/HBS86Hd.pdf
- Páginas: 7
- Método: extracción del texto nativo con pypdf 6.14.2, modo layout.
- Alcance: se conserva todo el texto recuperable, separado por página. Los diagramas y fotografías permanecen normativos en el PDF original.

## Página 1

```text
                                                                                                                                                                                                                                                                                           Hybrid Servo Drive HBS86 Datasheet
HBS86H                              2-phase Hybrid Servo Drive

20-70VAC or 30-90VDC, 8.2A Peak

No Tuning, Nulls loss of Synchronization

n    Closed-loop, eliminates loss of synchronization
n    Broader operating range                  – higher torque and higher speed
n    Reduced motor heating and more efficient
n     Smooth motion and super-low motor noise
n    Do not need a high torque margin
n    No Tuning and always stable
n     Fast response, no delay and almost no settle time
n    High torque at starting and low speed, high stiffness at standstill
n     Lower cost

Descriptions

The HBS series offers an alternative for applications requiring high performance and high reliability when the servo was the only choice,
while it remains cost-effective. The system includes a 2-phase stepper motor combined with a fully digital, high performance drive and
an internal encoder which is used to close the position, velocity and current loops in real time, just like servo systems. It combines the
best of servo and stepper motor technologies, and delivers unique capabilities and enhancements over both, while at a fraction of the cost
of a servo system.

Applications

The HBS series offers an alternative for applications requiring high performance and high reliability when the servo was the only choice,
while it remains cost-effective. Its great feature of fast response and no hunting make it ideal for applications such as bonding and vision
systems in which rapid motions with a short distance are required and hunting would be a problem. And it is ideal for applications where
the equipment uses a belt-drive mechanism or otherwise has low rigidity and you don't want it to vibrate when stopping                                                                                                                                                           .


Leadshine Motion Technology
3/F, Block 2, Nanyou Tianan Industrial Park, Nanshan District Shenzhen, China                                   Page 1 of 7
Tel: 86-755-26434369 Fax: 86-755-26402718 Website:                                                                                        http://www.leadshine.com
```

## Página 2

```text
                                                                                                                                                                                                     Hybrid Servo Drive HBS86 Datasheet
Specifications

Electrical Specifications

    Parameter                                                                                                                                                                                                Min                                                                                                 Typical                                                                                                          Max                                                                                                    Unit
    Input Voltage                                                                                                                                                                                                30                                                                                                         60                                                                                                      100                                                                                                 VDC
                                                                                                                                                                                                                 20                                                                                                             -                                                                                                      70                                                                                               VAC
    Output Current                                                                                                                                                                                                  0                                                                                                           -                                                                                       8.2(Peak)                                                                                                              A
    Pulse Input Frequency                                                                                                                                                                                           0                                                                                                           -                                                                                                   200                                                                                                   kHz
    Logic Signal Current                                                                                                                                                                                            7                                                                                                       10                                                                                                         16                                                                                                  mA
    Isolation Resistance                                                                                                                                                                                      500                                                                                                               -                                                                                                          -                                                                                              MΩ

Operating Environment

      Cooling                                                                                                                                                                                                                                                                                                Natural Cooling or Forced cooling
                                                                                                                                                                                  Environment                                                                                                                                                                                     Avoid dust, oil fog and corrosive gases
                                                                                                                                                                                  Storage Temperature                                                                                                                                                                             -20℃ － 65℃ (-4℉ － 149℉)
      Operating Environment                                                                                                                                                       Ambient Temperature                                                                                                                                                                             0℃ － 50℃ (32℉ － 122℉)
                                                                                                                                                                                  Humidity                                                                                                                                                                                        40%RH  － 90%RH
                                                                                                                                                                                  Operating Temperature (Heat Sink)                                                                                                                                                               70℃ (158 ℉) Max
      Storage Temperature                                                                                                                                                                                                                                                                                      -20℃ － 65℃ (-4℉ － 149)℉
      Weight                                                                                                                                                                                                                                                                                                                                         580 g (9.88 oz)

Mechanical Specifications


Leadshine Motion Technology
3/F, Block 2, Nanyou Tianan Industrial Park, Nanshan District Shenzhen, China                                   Page 2 of 7
Tel: 86-755-26434369 Fax: 86-755-26402718 Website:                                                                                        http://www.leadshine.com
```

## Página 3

```text
                                                                                                                                                                                                                                                                     Hybrid Servo Drive HBS86 Datasheet
Protection Indications

The green indicator turns on when power-up. When drive protection is activated, the red LED blinks periodicity to indicate the error type


                                            Priority                                                                                     Time(s) of Blink                                                                                                                                                                                                                                 Sequence wave of RED LED                                                                                                                                                                                                                                                                                                                              Description


                                                                                                                                                                                                                                                                                                                                                                                                                                           5S
                                                                                                                                                                                                                                                                            0.2S
                                                          1st                                                                                                                     1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Over-current protection


                                                                                                                                                                                                                                                                                                                                                                                                                                                             5S

                                                                                                                                                                                                                                                                                            0.3S              0.2S
                                                       2nd                                                                                                                        2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                Over-voltage protection


                                                                                                                                                                                                                                                                                                                                                                                                                                           5S
                                                                                                                                                                                                                                                                                            0.3S              0.2S
                                                        3rd                                                                                                                       7                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             Position Following Error


Connectors and Pin Assignment

The HBS86 has four connectors, connector for control signals connections, connector for stator signal connections, connector for encoder
feedback and connector for power and motor connections.

                                                                                                                                                                                                                                                                                 Control Signal Connector                        – Screw Terminal

     Pin                                                    Name                                                           I/O                                                                                                                                                                                                                                                                                                                                        Description

                                                                                                                                                                          Pulse signal                                                             : In single pulse (pulse/direction) mode, this input represents pulse signal, each rising or falling
            1                                              PUL+                                                                    I                                      edge active (software configurable, see hybrid servo software operational manual for more detail); In double
                                                                                                                                                                          pulse mode (software configurable), this input represents clockwise (CW) pulse, active both at high level and
                                                                                                                                                                          low level. 4-5V when PUL-HIGH, 0-0.5V when PUL-LOW. For reliable response, pulse width should be
            2                                                PUL-                                                                  I                                      longer than 10         μs. Series connect resistors for current-limiting when +12V or +24V used. The same as DIR
                                                                                                                                                                          and ENA signal.

                                                                                                                                                                          Direction Signal                                                                                   : In single-pulse mode, this signal has low/high voltage levels, representing two directions of
            3                                               DIR+                                                                   I                                      motor rotation. In double-pulse mode (software configurable), this signal is counter-clock (CCW) pulse,
                                                                                                                                                                          active both at high level and low level. For reliable motion response, DIR signal should be ahead of PUL
                                                                                                                                                                          signal by 5       μs at least. 4-5V when DIR-HIGH, 0-0.5V when DIR-LOW. Please note that rotation direction is
            4                                                 DIR-                                                                 I                                      also related to motor-driver wiring match. Exchanging the connection of two wires for a coil to the driver will
                                                                                                                                                                          reverse motion direction. The direction signal                                     ’s polarity is software configurable.

            5                                             ENA+                                                                     I                                      Enable signal                                                                    : This signal is used for enabling/disabling the driver. In default, high level (NPN control signal)
                                                                                                                                                                          for enabling the driver and low level for disabling the driver. Usually left                                                                                                               UNCONNECTED (ENABLED)                                             .
                                                                                                                                                                          Please note that PNP and Differential control signals are on the contrary, namely Low level for enabling. The
            6                                               ENA-                                                                   I                                      active level of ENA signal is software configurable.


Leadshine Motion Technology
3/F, Block 2, Nanyou Tianan Industrial Park, Nanshan District Shenzhen, China                                   Page 3 of 7
Tel: 86-755-26434369 Fax: 86-755-26402718 Website:                                                                                        http://www.leadshine.com
```

## Página 4

```text
                                                                                                                                                                                                                                               Hybrid Servo Drive HBS86 Datasheet

                                                                                                                                                                                                                                                     Stator Signal Connector               – Screw Terminal

     Pin                                              Name                                                          I/O                                                                                                                                                                                                                                                                                                Description

           1                                        Pend+                                                                O                               In-position Signal                                                                                  : OC output signal, active when the difference between the actual position and the
                                                                                                                                                         command position is zero. This port can sink or source 20mA current at 24V. The resistance between Pend+
           2                                          Pend-                                                              O                               and Pend- is active at high impedance.


                                                                                                                                                         Alarm Signal                                                            : OC output signal, active when one of the following protection is activated: over-voltage, over
           3                                       ALM+                                                                  O                               current and position following error. This port can sink or source 20mA current at 24V. In default, the

                                                                                                                                                         resistance between ALM+ and ALM- is low impedance in normal operation and become high when HBS86
           5                                        ALM-                                                                 O                               goes into error. The active level of alarm signal is software configurable. See Hybrid servo software
                                                                                                                                                         operational manual for more detail.


                                                                                                                                                                                                                                          Encoder Feedback Connector                           – Screw Terminal
            Pin                                      Name                                                                  I/O                                                                                                                                                                                                                                                                                                   Description
              1                                         EB+                                                                        I                                                    Encoder channel B+ input
              2                                           EB-                                                                      I                                                    Encoder channel B- input
              3                                         EA+                                                                        I                                                    Encoder channel A+ input
              4                                           EA-                                                                      I                                                    Encoder channel A- input
              5                                        VCC                                                                      O                                                       +5V @ 100 mA max.
              6                                   EGND                                                                GND                                                               Signal ground


                                                                                                                                                                                                                                             Power and Motor Connector                       – Screw Terminal
         Pin                                         Name                                                                  I/O                                                                                                                                                                                                                                                                                                   Description
               1                                             A+                                                                 O                                                       Motor Phase A+
               2                                              A-                                                                O                                                       Motor Phase A-
               3                                             B+                                                                 O                                                       Motor Phase B+
               4                                               B-                                                               O                                                       Motor Phase B-
               5                                      +Vdc                                                                         I                                                    Power Supply Input (Positive)
                                                                                                                                                                                        20-63VAC or 30-90VDC recommended, leaving rooms for voltage fluctuation and back-EMF.
               6                                       GND                                                            GND                                                               Power Ground (Negative)


Leadshine Motion Technology
3/F, Block 2, Nanyou Tianan Industrial Park, Nanshan District Shenzhen, China                                   Page 4 of 7
Tel: 86-755-26434369 Fax: 86-755-26402718 Website:                                                                                        http://www.leadshine.com
```

## Página 5

```text
                                                                                                                                                                                                                           Hybrid Servo Drive HBS86 Datasheet
RS232 Communication Port

It is used to configure the close-loop current, open-loop current, position following error limit and etc. See hybrid servo drive software
operational manual for more information.

                                                                                                                                                                                                                                                                   RS232 Communication Port
       Pin                                       Name                                                                I/O                                                                                                                                                                 Description
             1                                         NC                                                                 -                                     Not connected.
             2                                       +5V                                                                O                                       +5V power only for STU (Simple Tuning Unit).
             3                                       TxD                                                                O                                       RS232 transmit.
             4                                     GND                                                         GND                                              Ground.
             5                                      RxD                                                                   I                                     RS232 receive.
             6                                         NC                                                                 -                                     Not connected.

DIP Switch Settings

Microstep Resolution (SW1-SW4)

                                                                                         Steps/Revolution                                                                                                                                                                                                                 SW1                                                                                                  SW2                                                                                                   SW3                                                                                           SW4
                                            Software Configured (Default 200)                                                                                                                                                                                                                                                   on                                                                                                    on                                                                                                   on                                                                                            on

                                                                                                                              800                                                                                                                                                                                               off                                                                                                   on                                                                                                   on                                                                                            on

                                                                                                                           1600                                                                                                                                                                                                 on                                                                                                   off                                                                                                   on                                                                                            on

                                                                                                                           3200                                                                                                                                                                                                 off                                                                                                  off                                                                                                   on                                                                                            on

                                                                                                                           6400                                                                                                                                                                                                 on                                                                                                    on                                                                                                   off                                                                                           on

                                                                                                                        12800                                                                                                                                                                                                   off                                                                                                   on                                                                                                   off                                                                                           on

                                                                                                                        25600                                                                                                                                                                                                   on                                                                                                   off                                                                                                   off                                                                                           on

                                                                                                                        51200                                                                                                                                                                                                   off                                                                                                  off                                                                                                   off                                                                                           on

                                                                                                                           1000                                                                                                                                                                                                 on                                                                                                    on                                                                                                   on                                                                                           off

                                                                                                                           2000                                                                                                                                                                                                 off                                                                                                   on                                                                                                   on                                                                                           off

                                                                                                                           4000                                                                                                                                                                                                 on                                                                                                   off                                                                                                   on                                                                                           off

                                                                                                                           5000                                                                                                                                                                                                 off                                                                                                  off                                                                                                   on                                                                                           off

                                                                                                                           8000                                                                                                                                                                                                 on                                                                                                    on                                                                                                   off                                                                                          off

                                                                                                                        10000                                                                                                                                                                                                   off                                                                                                   on                                                                                                   off                                                                                          off

                                                                                                                        20000                                                                                                                                                                                                   on                                                                                                   off                                                                                                   off                                                                                          off

                                                                                                                        40000                                                                                                                                                                                                   off                                                                                                  off                                                                                                   off                                                                                          off

Motor Direction (SW5)

                                                                                                                                                                                                                                                                ON                                                                                                                                                                                                                                                                     OFF
                                                 SW5                                                                                                                                                      Motor direction is positive.                                                                                                                                                                                                                                             Motor direction is negative.

Note     : The actual motor direction is also related to command signal.
Leadshine Motion Technology
3/F, Block 2, Nanyou Tianan Industrial Park, Nanshan District Shenzhen, China                                   Page 5 of 7
Tel: 86-755-26434369 Fax: 86-755-26402718 Website:                                                                                        http://www.leadshine.com
```

## Página 6

```text
                                                                                                                                                                                                                                                                                                              Hybrid Servo Drive HBS86 Datasheet

Motor Selection (SW6)

                                                                                                                                                                                                                                                                                                                                                                                               ON                                                                                                                                                                                                                                                                                                                                                                                                        OFF
                                                                          SW6                                                                                                                                                                                                                                                                  86HS80-EC-1000                                                                                                                                                                                                                                                                                                                                                                                                86HS40-EC-1000

Current Control

The motor current will be adjusted automatically regarding to the load or the stator-rotor relationship. However, the user can also
configure the current in the tuning software. The configurable parameters include close-loop current, holding current, encoder resolution,
micro step and etc. There are also PID parameters for the motor but they have been tuned according to Leadshine matching motor so the
user does not need to tune them.

Matching Motor Specification

HBS86 can work with the following Leadshine three phase hybrid stepper motors with encoder as follows:

                                                                                                                                                                                                                                                                                                                                                                                                 86HS40-EC-1000                                                                                                                                                                                                                                                                                                                                                                    86HS80-EC-1000
                 Step Angle (Degree)                                                                                                                                                                                                                                                                                                                                                                                                                    1.8                                                                                                                                                                                                                                                                                                                                                                             1.8
                 Holding Torque (N.m)                                                                                                                                                                                                                                                                                                                                                                                                                   4.0                                                                                                                                                                                                                                                                                                                                                                             8.0
                 Phase Current (A)                                                                                                                                                                                                                                                                                                                                                                                                                      5.5                                                                                                                                                                                                                                                                                                                                                                             6.0
                 Phase Resistance (Ohm)                                                                                                                                                                                                                                                                                                                                                                                                             0.46                                                                                                                                                                                                                                                                                                                                                                           0.44
                 Phase Inductance (mH)                                                                                                                                                                                                                                                                                                                                                                                                                         4                                                                                                                                                                                                                                                                                                                                                                   3.73
                 Inertia (g.cm                           2)                                                                                                                                                                                                                                                                                                                                                                                      1500                                                                                                                                                                                                                                                                                                                                                                            2580
                 Weight (Kg)                                                                                                                                                                                                                                                                                                                                                                                                                            1.5                                                                                                                                                                                                                                                                                                                                                                             3.8
                 Encoder (lines / Rev.)                                                                                                                                                                                                                                                                                                                                                                                                          1000                                                                                                                                                                                                                                                                                                                                                                            1000


                 Wiring Diagram


86HS40-EC-1000 Mechanical Specification


Leadshine Motion Technology
3/F, Block 2, Nanyou Tianan Industrial Park, Nanshan District Shenzhen, China                                   Page 6 of 7
Tel: 86-755-26434369 Fax: 86-755-26402718 Website:                                                                                        http://www.leadshine.com
```

## Página 7

```text
                                                                                                                                                                                                    Hybrid Servo Drive HBS86 Datasheet

86HS80-EC-1000 Mechanical Specification


Encoder Extension Cable Pin Out

Pin                                  Color                                            Name                                                                                 Description                                                                                                             Pin                                    Color                                              Name                                                                                Description
    1                                    Red                                            VCC                                         +5V power input                                                                                                                                                    4                                 Green                                                      B-                                     Encoder Channel B-
    2                               White                                              GND                                          +5V GND                                                                                                                                                            5                                  Black                                                    A+                                      Encoder Channel A+
    3                              Yellow                                                   B+                                      Encoder Channel B+                                                                                                                                                 6                                    Blue                                                    A-                                     Encoder Channel A-

Typical Connections


                                                                                                                                                                             R=0 if VCC=5V;
                                                                                                                                                                             R=1K(Power>0.125W) if VCC=12V;
                                                                                       Controller                                                                            R=2K(Power>0.125W) if VCC=24V;                                                                                                                                                                                                        HBS86H Drive
                                                                                                                                                                             R must be connected to control signal terminal.
                                                                                               VCC                                                                                                                                                                                                                                                            PUL+                                         270O

                                                                                                                                                                                                                                R                                                                                                                              PUL-

                                                                                                PUL                                                                                                                                                                                                                                                            DIR+                                        270O

                                                                                                                                                                                                                                R                                                                                                                             DIR-

                                                                                               DIR                                                                                                                                                                                                                                                           ENA+                                          270O

                                                                                                                                                                                                                                R                                                                                                                              ENA-

                                                                                  ENABLE

                                                                                    ALARM                                                                                                                                                                                                                                                                    ALM+

                                                                                                                                                                                                                                                                                                                                                             ALM-


                                                                                                                                                                                                                                                                                                                                                               EB+
                                                                                                                                                                                                                                                                                                                                                               EB-
                                                                                                                                                                                                                                                                                                                                                               EA+
                                                                                                                                                                                                        86HS40-EC                                                   Encoder                                                                                     EA-
                                                                                                                                                                                                                                                                                                                                                              VCC
                                                                                                                                                                                                                                                                                                                                                           EGND
                                                                                                                                                                                                                                                                                                                                                                 A+
                                                                                                                                                                                                                                                                                                                                                                 A-
                                                                                                                                                                                                                                                                                                                                                                 B+
                                                                                                                                                                                                                                                                                                                                                                   B-

                                                                                                                                                                                                                                                                                                                                                           +Vdc
                                                                                                                                                                                                                20 ~ 63VAC or 30 ~ 90VDC                                                                                                                       GND


Leadshine Motion Technology
3/F, Block 2, Nanyou Tianan Industrial Park, Nanshan District Shenzhen, China                                   Page 7 of 7
Tel: 86-755-26434369 Fax: 86-755-26402718 Website:                                                                                        http://www.leadshine.com
```
